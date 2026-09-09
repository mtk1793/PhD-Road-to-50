%% StatisticalTests - Wilcoxon Signed-Rank Test & Multi-Seed Analysis
classdef StatisticalTests < handle
    methods (Static)
        function results = run_multi_seed_experiment(baseline_func, tasks_list, config, n_seeds)
            if nargin < 4, n_seeds = 10; end
            
            seed_results = cell(n_seeds, 1);
            
            for s = 1:n_seeds
                fprintf('  Seed %d/%d...\n', s, n_seeds);
                cfg = config;
                cfg.rng_seed = s * 100 + 42;
                rng(cfg.rng_seed);
                
                try
                    seed_results{s} = baseline_func(tasks_list, cfg);
                catch ME
                    fprintf('  Error at seed %d: %s\n', s, ME.message);
                    seed_results{s} = [];
                end
            end
            
            valid = ~cellfun(@isempty, seed_results);
            results = struct('all_results', seed_results(valid), 'n_valid', sum(valid));
        end
        
        function [p_value, h, stats] = wilcoxon_signed_rank(sample1, sample2)
            if length(sample1) ~= length(sample2)
                error('Samples must have same length');
            end
            
            d = sample1(:) - sample2(:);
            abs_d = abs(d);
            [~, rank_order] = sort(abs_d);
            ranks = zeros(size(d));
            ranks(rank_order) = 1:length(d);
            
            W_plus = sum(ranks(d > 0));
            W_minus = sum(ranks(d < 0));
            
            W = min(W_plus, W_minus);
            n = sum(d ~= 0);
            
            if n == 0
                p_value = 1;
                h = false;
                stats = struct('W_plus', 0, 'W_minus', 0, 'n', 0);
                return;
            end
            
            if n > 20
                mu_W = n*(n+1)/4;
                sigma_W = sqrt(n*(n+1)*(2*n+1)/24);
                z = (W - mu_W) / max(sigma_W, 1e-10);
                p_value = 2 * normcdf(-abs(z));
            else
                p_value = StatisticalTests.exact_wilcoxon_pvalue(W, n);
            end
            
            h = p_value < 0.05;
            stats = struct('W_plus', W_plus, 'W_minus', W_minus, 'n', n, 'W', W, 'p_value', p_value);
        end
        
        function p_value = exact_wilcoxon_pvalue(W, n)
            max_W = n*(n+1)/2;
            counts = zeros(max_W + 1, 1);
            counts(1) = 1;
            
            for i = 1:n
                new_counts = zeros(max_W + 1, 1);
                for w = 1:max_W
                    if counts(w) > 0
                        new_counts(w) = new_counts(w) + counts(w);
                        if w + i <= max_W
                            new_counts(w+i) = new_counts(w+i) + counts(w);
                        end
                    end
                end
                counts = new_counts;
            end
            
            p_value = 2 * sum(counts(1:W+1)) / 2^n;
            p_value = min(1, p_value);
        end
        
        function results = compare_methods(method_results, method_names)
            n_methods = length(method_results);
            
            results.p_values = zeros(n_methods, n_methods);
            results.h_matrix = false(n_methods, n_methods);
            results.mean_rmse = zeros(n_methods, 1);
            results.std_rmse = zeros(n_methods, 1);
            
            for m = 1:n_methods
                bwt_values = zeros(length(method_results{m}), 1);
                for i = 1:length(method_results{m})
                    if isfield(method_results{m}{i}, 'backward_transfer')
                        bwt_values(i) = method_results{m}{i}.backward_transfer;
                    else
                        bwt_values(i) = 0;
                    end
                end
                results.mean_rmse(m) = mean(bwt_values);
                results.std_rmse(m) = std(bwt_values);
                
                for m2 = m+1:n_methods
                    bwt_values2 = zeros(length(method_results{m2}), 1);
                    for i = 1:length(method_results{m2})
                        if isfield(method_results{m2}{i}, 'backward_transfer')
                            bwt_values2(i) = method_results{m2}{i}.backward_transfer;
                        else
                            bwt_values2(i) = 0;
                        end
                    end
                    
                    min_len = min(length(bwt_values), length(bwt_values2));
                    [p, h, stats] = StatisticalTests.wilcoxon_signed_rank(...
                        bwt_values(1:min_len), bwt_values2(1:min_len));
                    
                    results.p_values(m, m2) = p;
                    results.h_matrix(m, m2) = h;
                end
            end
            
            results.method_names = method_names;
        end
        
        function effect_size = cliffs_delta(sample1, sample2)
            n1 = length(sample1);
            n2 = length(sample2);
            
            count = 0;
            for i = 1:n1
                for j = 1:n2
                    if sample1(i) > sample2(j)
                        count = count + 1;
                    elseif sample1(i) < sample2(j)
                        count = count - 1;
                    end
                end
            end
            
            effect_size = count / (n1 * n2);
        end
        
        function plot_significance(results, output_path)
            figure('Position', [100, 100, 600, 500]);
            
            n = length(results.mean_rmse);
            x = 1:n;
            
            bar(x, results.mean_rmse, 'FaceColor', [0.4 0.6 0.8]);
            hold on;
            errorbar(x, results.mean_rmse, results.std_rmse, 'k.', 'LineWidth', 2);
            
            for i = 1:n
                for j = i+1:n
                    if results.h_matrix(i, j)
                        y_max = max(results.mean_rmse(i), results.mean_rmse(j)) + ...
                            max(results.std_rmse(i), results.std_rmse(j)) + 0.02;
                        line([i, i, j, j], [y_max-0.01, y_max, y_max, y_max-0.01], ...
                            'Color', 'red', 'LineWidth', 1.5);
                        text((i+j)/2, y_max+0.005, sprintf('p=%.3f', results.p_values(i,j)), ...
                            'HorizontalAlignment', 'center', 'FontSize', 8, 'Color', 'red');
                    end
                end
            end
            
            set(gca, 'XTick', x, 'XTickLabel', results.method_names, 'XTickLabelRotation', 45);
            ylabel('Mean Backward Transfer');
            title('Statistical Significance (Wilcoxon Signed-Rank)');
            grid on;
            
            if nargin > 1
                saveas(gcf, output_path);
            end
        end
    end
end
