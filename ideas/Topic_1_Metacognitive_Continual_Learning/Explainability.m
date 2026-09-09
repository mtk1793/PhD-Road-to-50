%% Explainability - SHAP Values & Attention Visualization
classdef Explainability < handle
    methods (Static)
        function shap_results = compute_shap_values(W1, b1, W2, b2, X, feature_names)
            n_samples = min(100, size(X, 1));
            X_sample = X(1:n_samples, :);
            n_features = size(X, 2);
            
            h_base = max(0, mean(X, 1) * W1 + b1);
            base_value = h_base * W2 + b2;
            
            shap_values = zeros(n_samples, n_features);
            
            for f = 1:n_features
                X_present = X_sample;
                X_absent = X_sample;
                X_absent(:, f) = mean(X(:, f));
                
                y_present = Explainability.forward_pass(W1, b1, W2, b2, X_present);
                y_absent = Explainability.forward_pass(W1, b1, W2, b2, X_absent);
                
                shap_values(:, f) = y_present - y_absent;
            end
            
            shap_results.values = shap_values;
            shap_results.base_value = base_value;
            shap_results.feature_names = feature_names;
            shap_results.importance = mean(abs(shap_values), 1);
        end
        
        function attention_results = compute_attention(W1, b1, W2, b2, X, timestamps)
            n_samples = min(100, size(X, 1));
            X_sample = X(1:n_samples, :);
            
            z1 = X_sample * W1 + b1;
            h1 = max(0, z1);
            
            attention_weights = abs(W1) ./ (sum(abs(W1), 1) + 1e-10);
            attention_weights = mean(attention_weights, 2);
            attention_weights = attention_weights / sum(attention_weights);
            
            if nargin >= 5 && ~isempty(timestamps)
                time_idx = 1:n_samples;
                if isdatetime(timestamps)
                    hour_vals = hour(timestamps(1:n_samples)) + minute(timestamps(1:n_samples))/60;
                    temporal_attention = abs(sin(2*pi*hour_vals/24));
                    temporal_attention = temporal_attention / sum(temporal_attention);
                else
                    temporal_attention = ones(n_samples, 1) / n_samples;
                end
            else
                temporal_attention = ones(n_samples, 1) / n_samples;
            end
            
            attention_results.feature_attention = attention_weights;
            attention_results.temporal_attention = temporal_attention;
        end
        
        function plot_shap(shap_results, output_path)
            figure('Position', [100, 100, 800, 400]);
            
            imp = shap_results.importance;
            names = shap_results.feature_names;
            
            [sorted_imp, idx] = sort(imp, 'descend');
            sorted_names = names(idx);
            
            barh(sorted_names, sorted_imp, 'FaceColor', [0.4 0.6 0.8]);
            xlabel('Mean |SHAP Value|');
            title('Feature Importance (SHAP)');
            grid on;
            
            if nargin > 1
                saveas(gcf, output_path);
            end
        end
        
        function plot_drift(shap_results, task_shap_values, output_path)
            figure('Position', [100, 100, 1000, 500]);
            
            n_tasks = length(task_shap_values);
            n_features = length(shap_results.feature_names);
            
            subplot(2, 1, 1);
            heatmap_matrix = zeros(n_tasks, n_features);
            for t = 1:n_tasks
                heatmap_matrix(t, :) = mean(abs(task_shap_values{t}), 1);
            end
            
            imagesc(heatmap_matrix);
            colorbar;
            set(gca, 'XTick', 1:n_features, 'XTickLabel', shap_results.feature_names, ...
                'YTick', 1:n_tasks, 'YTickLabel', strcat('Task ', cellstr(num2str((1:n_tasks)'))), ...
                'XTickLabelRotation', 45);
            title('Feature Importance Drift Across Tasks');
            xlabel('Feature'); ylabel('Task');
            
            subplot(2, 1, 2);
            colors = lines(n_tasks);
            for t = 1:n_tasks
                plot(1:n_features, mean(abs(task_shap_values{t}), 1), '-o', ...
                    'Color', colors(t, :), 'LineWidth', 2, 'DisplayName', sprintf('Task %d', t));
                hold on;
            end
            set(gca, 'XTick', 1:n_features, 'XTickLabel', shap_results.feature_names, 'XTickLabelRotation', 45);
            legend('Location', 'best');
            title('Feature Importance Comparison');
            ylabel('Mean |SHAP|');
            grid on;
            
            if nargin > 2
                saveas(gcf, output_path);
            end
        end
        
        function y_out = forward_pass(W1, b1, W2, b2, X_in)
            h = max(0, X_in * W1 + b1);
            y_out = h * W2 + b2;
        end
    end
end
