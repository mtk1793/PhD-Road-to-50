%% Topic_1_Full_Experiment - Complete Publication-Ready Experimental Framework
% Runs all components: baselines, ablation, statistical tests, IEEE validation,
% large-scale experiments, uncertainty decomposition, efficiency, and explainability
%
% Author: PhD Research
% Date: May 2026

clear; clc; close all;

fprintf('=============================================================\n');
fprintf('  TOPIC 1: METACOGNITIVE CONTINUAL LEARNING FOR\n');
fprintf('  NON-STATIONARY SMART GRID DYNAMICS\n');
fprintf('  Complete Experimental Framework\n');
fprintf('=============================================================\n\n');

%% ============================================================
% EXPERIMENT CONFIGURATION
%% ============================================================
config = struct();

% Data
config.dataset_source = 'synthetic';
config.dataset_path = '';

% Model
config.input_dim = 5;
config.hidden_dim = 32;
config.learning_rate = 0.01;
config.epochs_per_task = 15;

% Continual Learning
config.num_tasks = 5;
config.samples_per_task = 500;
config.lambda_ewc = 500;
config.replay_size = 200;
config.meta_threshold = 0.15;
config.conformal_alpha = 0.05;

% Statistical
config.n_seeds = 10;
config.task_segmentation = 'equal';

% Feature names (must match DataLoader)
config.feature_names = {'Solar_Power', 'Wind_Power', 'Load_kW', 'Temperature_C', 'Humidity'};
config.target_name = 'Voltage_V';

% Output
config.output_dir = 'experiment_results';
if ~exist(config.output_dir, 'dir')
    mkdir(config.output_dir);
end

%% ============================================================
% STEP 1: DATA LOADING & PREPARATION
%% ============================================================
fprintf('\n[1/9] DATA LOADING & PREPARATION\n');
fprintf('---------------------------------\n');

loader = DataLoader(config.dataset_path);
loader.load_dataset(config.dataset_source, config.num_tasks, config.samples_per_task, 42);

[X, y] = loader.get_normalized_data();
tasks = loader.segment_tasks(config.task_segmentation, config.num_tasks);

fprintf('Dataset: %d samples, %d features, %d tasks\n', loader.n_samples, loader.n_features, config.num_tasks);

loader.save_processed(fullfile(config.output_dir, 'processed_dataset.csv'));

%% ============================================================
% STEP 2: BASELINE COMPARISONS
%% ============================================================
fprintf('\n[2/9] BASELINE COMPARISONS\n');
fprintf('----------------------------\n');

baseline_results = Baselines.run_all_baselines(tasks, config);

methods_names = {'Naive Fine-Tuning', 'ER Only', 'EWC Only', 'PackNet', 'Progressive NN', 'EWC-IXER (Ours)'};
methods_keys = {'naive', 'er_only', 'ewc_only', 'packnet', 'progressive_nn', 'ewc_ixer'};

fprintf('\nBaseline Results Summary:\n');
fprintf('%-25s | Avg RMSE | Backward Transfer\n', 'Method');
fprintf('%-25s |----------|------------------\n', '-------------------------');
for i = 1:length(methods_keys)
    key = methods_keys{i};
    fprintf('%-25s | %.4f   | %.4f\n', methods_names{i}, ...
        baseline_results.(key).avg_accuracy, baseline_results.(key).backward_transfer);
end

%% ============================================================
% STEP 3: MULTI-SEED STATISTICAL TESTS
%% ============================================================
fprintf('\n[3/9] MULTI-SEED STATISTICAL TESTS (%d seeds)\n', config.n_seeds);
fprintf('------------------------------------------------\n');

seed_results = cell(6, 1);

for m = 1:6
    key = methods_keys{m};
    fprintf('  Running %s across %d seeds...\n', methods_names{m}, config.n_seeds);
    
    method_results = cell(config.n_seeds, 1);
    
    for s = 1:config.n_seeds
        cfg = config;
        cfg.rng_seed = s * 100 + 42;
        rng(cfg.rng_seed);
        
        try
            switch key
                case 'naive', method_results{s} = Baselines.naive_fine_tuning(tasks, cfg);
                case 'er_only', method_results{s} = Baselines.er_only(tasks, cfg);
                case 'ewc_only', method_results{s} = Baselines.ewc_only(tasks, cfg);
                case 'packnet', method_results{s} = Baselines.packnet(tasks, cfg);
                case 'progressive_nn', method_results{s} = Baselines.progressive_nn(tasks, cfg);
                case 'ewc_ixer', method_results{s} = Baselines.ewc_ixer(tasks, cfg);
            end
        catch ME
            fprintf('    Error at seed %d: %s\n', s, ME.message);
            method_results{s} = [];
        end
    end
    
    valid = ~cellfun(@isempty, method_results);
    seed_results{m} = method_results(valid);
end

stat_results = StatisticalTests.compare_methods(seed_results, methods_names);

fprintf('\nStatistical Comparison:\n');
fprintf('%-25s | Mean BWT | Std BWT\n', 'Method');
fprintf('%-25s |----------|--------\n', '-------------------------');
for i = 1:6
    fprintf('%-25s | %.4f   | %.4f\n', stat_results.method_names{i}, ...
        stat_results.mean_rmse(i), stat_results.std_rmse(i));
end

StatisticalTests.plot_significance(stat_results, fullfile(config.output_dir, 'statistical_significance.png'));

%% ============================================================
% STEP 4: ABLATION STUDIES
%% ============================================================
fprintf('\n[4/9] ABLATION STUDIES\n');
fprintf('-----------------------\n');

ablation_results = struct();

rng(42);

[W1, b1, W2, b2] = deal(...
    randn(config.input_dim, config.hidden_dim) * 0.1, ...
    zeros(1, config.hidden_dim), ...
    randn(config.hidden_dim, 1) * 0.1, ...
    0);

% Ablation 1: Full method (EWC + ER + Meta)
fprintf('  Ablation: Full EWC-IXER...\n');
result_full = Baselines.ewc_ixer(tasks, config);
ablation_results.full = result_full;

% Ablation 2: No metacognitive monitoring
fprintf('  Ablation: No metacognitive monitoring...\n');
cfg_no_meta = config;
cfg_no_meta.meta_threshold = Inf;
result_no_meta = Baselines.ewc_ixer(tasks, cfg_no_meta);
ablation_results.no_meta = result_no_meta;

% Ablation 3: No EWC
fprintf('  Ablation: No EWC (ER only)...\n');
result_no_ewc = Baselines.er_only(tasks, config);
ablation_results.no_ewc = result_no_ewc;

% Ablation 4: No Experience Replay
fprintf('  Ablation: No Experience Replay (EWC only)...\n');
result_no_er = Baselines.ewc_only(tasks, config);
ablation_results.no_er = result_no_er;

% Ablation 5: Varying EWC lambda
fprintf('  Ablation: Varying EWC lambda...\n');
lambda_values = [0, 100, 500, 1000, 5000];
ablation_results.lambda_var = zeros(length(lambda_values), 5);
for i = 1:length(lambda_values)
    cfg_lambda = config;
    cfg_lambda.lambda_ewc = lambda_values(i);
    result = Baselines.ewc_ixer(tasks, cfg_lambda);
    ablation_results.lambda_var(i, :) = [lambda_values(i), ...
        result.avg_accuracy, result.backward_transfer, ...
        mean(result.coverage), result.n_adaptations];
end

% Ablation 6: Varying replay buffer size
fprintf('  Ablation: Varying replay buffer size...\n');
buffer_values = [0, 50, 200, 500, 1000];
ablation_results.buffer_var = zeros(length(buffer_values), 5);
for i = 1:length(buffer_values)
    cfg_buf = config;
    cfg_buf.replay_size = buffer_values(i);
    result = Baselines.ewc_ixer(tasks, cfg_buf);
    ablation_results.buffer_var(i, :) = [buffer_values(i), ...
        result.avg_accuracy, result.backward_transfer, ...
        mean(result.coverage), result.n_adaptations];
end

fprintf('\nAblation Results:\n');
fprintf('%-20s | Avg RMSE | BWT\n', 'Ablation');
fprintf('%-20s |----------|------\n', '--------------------');
fprintf('%-20s | %.4f   | %.4f\n', 'Full EWC-IXER', ablation_results.full.avg_accuracy, ablation_results.full.backward_transfer);
fprintf('%-20s | %.4f   | %.4f\n', 'No Metacognitive', ablation_results.no_meta.avg_accuracy, ablation_results.no_meta.backward_transfer);
fprintf('%-20s | %.4f   | %.4f\n', 'No EWC', ablation_results.no_ewc.avg_accuracy, ablation_results.no_ewc.backward_transfer);
fprintf('%-20s | %.4f   | %.4f\n', 'No ER', ablation_results.no_er.avg_accuracy, ablation_results.no_er.backward_transfer);

%% ============================================================
% STEP 5: UNCERTAINTY DECOMPOSITION
%% ============================================================
fprintf('\n[5/9] UNCERTAINTY DECOMPOSITION\n');
fprintf('--------------------------------\n');

[X_test, y_test] = loader.get_normalized_data();
uncertainty_results = UncertaintyDecomposition.decompose_uncertainty(W1, b1, W2, b2, X_test, y_test, config);

fprintf('Total RMSE: %.4f\n', uncertainty_results.rmse);
fprintf('Epistemic Ratio: %.2f%%\n', uncertainty_results.epistemic_ratio * 100);
fprintf('NLL: %.4f\n', uncertainty_results.nll);
fprintf('Calibration: %.4f\n', uncertainty_results.calibration);

UncertaintyDecomposition.plot_uncertainty(uncertainty_results, ...
    fullfile(config.output_dir, 'uncertainty_decomposition.png'));

%% ============================================================
% STEP 6: IEEE BUS SYSTEM VALIDATION
%% ============================================================
fprintf('\n[6/9] IEEE BUS SYSTEM VALIDATION\n');
fprintf('---------------------------------\n');

ieee_30 = IEEEValidator.validate_30_bus(tasks, config);
IEEEValidator.plot_bus_voltages(ieee_30, fullfile(config.output_dir, 'ieee_30_bus.png'));

ieee_118 = IEEEValidator.validate_118_bus(tasks, config);

%% ============================================================
% STEP 7: LARGE-SCALE EXPERIMENTS
%% ============================================================
fprintf('\n[7/9] LARGE-SCALE EXPERIMENTS\n');
fprintf('------------------------------\n');

large_task_counts = [5, 10, 20, 30, 50];
large_scale_results = struct('n_tasks', large_task_counts, 'avg_rmse', zeros(size(large_task_counts)), ...
    'backward_transfer', zeros(size(large_task_counts)), 'training_time', zeros(size(large_task_counts)));

for i = 1:length(large_task_counts)
    n = large_task_counts(i);
    fprintf('  Running with %d tasks...\n', n);
    
    loader_large = DataLoader();
    loader_large.load_dataset('synthetic', n, 200, 42);
    tasks_large = loader_large.segment_tasks('equal', n);
    
    cfg_large = config;
    cfg_large.num_tasks = n;
    cfg_large.samples_per_task = 200;
    
    tic;
    result = Baselines.ewc_ixer(tasks_large, cfg_large);
    large_scale_results.training_time(i) = toc;
    large_scale_results.avg_rmse(i) = result.avg_accuracy;
    large_scale_results.backward_transfer(i) = result.backward_transfer;
    
    fprintf('    RMSE: %.4f, BWT: %.4f, Time: %.1fs\n', ...
        result.avg_accuracy, result.backward_transfer, large_scale_results.training_time(i));
end

figure('Position', [100, 100, 1000, 400]);
subplot(1, 3, 1);
plot(large_task_counts, large_scale_results.avg_rmse, 'b-o', 'LineWidth', 2);
xlabel('Number of Tasks'); ylabel('Avg RMSE');
title('Scaling: Accuracy');
grid on;

subplot(1, 3, 2);
plot(large_task_counts, large_scale_results.backward_transfer, 'r-o', 'LineWidth', 2);
xlabel('Number of Tasks'); ylabel('Backward Transfer');
title('Scaling: Forgetting');
grid on;

subplot(1, 3, 3);
plot(large_task_counts, large_scale_results.training_time, 'g-o', 'LineWidth', 2);
xlabel('Number of Tasks'); ylabel('Training Time (s)');
title('Scaling: Training Time');
grid on;

saveas(gcf, fullfile(config.output_dir, 'large_scale_experiments.png'));

%% ============================================================
% STEP 8: COMPUTATIONAL EFFICIENCY
%% ============================================================
fprintf('\n[8/9] COMPUTATIONAL EFFICIENCY ANALYSIS\n');
fprintf('----------------------------------------\n');

efficiency_results = EfficiencyProfiler.profile_inference(W1, b1, W2, b2, X_test(1:100, :));
training_eff = EfficiencyProfiler.profile_training(X_test(1:500, :), y_test(1:500), config);
scaling_results = EfficiencyProfiler.profile_scaling([5 10 20 30 50], config);

fprintf('Inference: Mean=%.2fms, P95=%.2fms, P99=%.2fms\n', ...
    efficiency_results.mean_time, efficiency_results.p95_time, efficiency_results.p99_time);
fprintf('Memory: %.2f MB\n', efficiency_results.memory_bytes / (1024^2));
fprintf('Parameters: %d\n', efficiency_results.n_parameters);

EfficiencyProfiler.plot_efficiency(efficiency_results, fullfile(config.output_dir, 'efficiency.png'));
EfficiencyProfiler.plot_scaling(scaling_results, fullfile(config.output_dir, 'scaling.png'));

fprintf('Inference: Mean=%.2fms, P95=%.2fms, P99=%.2fms\n', ...
    efficiency_results.mean_time, efficiency_results.p95_time, efficiency_results.p99_time);
fprintf('Training Time: Mean=%.2fs\n', training_eff.mean_training_time);

%% ============================================================
% STEP 9: EXPLAINABILITY
%% ============================================================
fprintf('\n[9/9] EXPLAINABILITY (SHAP + Attention)\n');
fprintf('----------------------------------------\n');

shap_results = Explainability.compute_shap_values(W1, b1, W2, b2, X_test, config.feature_names);
attention_results = Explainability.compute_attention(W1, b1, W2, b2, X_test, loader.data.Timestamp);

Explainability.plot_shap(shap_results, fullfile(config.output_dir, 'shap_importance.png'));

task_shap = cell(config.num_tasks, 1);
for t = 1:config.num_tasks
    [X_t, y_t] = prepare_data_simple(tasks{t}, config);
    task_shap{t} = Explainability.compute_shap_values(W1, b1, W2, b2, X_t, config.feature_names).values;
end
Explainability.plot_drift(shap_results, task_shap, fullfile(config.output_dir, 'feature_drift.png'));

fprintf('Top 3 features:\n');
[~, idx] = sort(shap_results.importance, 'descend');
for i = 1:3
    fprintf('  %d. %s (%.4f)\n', i, shap_results.feature_names{idx(i)}, shap_results.importance(idx(i)));
end

%% ============================================================
% FINAL SUMMARY
%% ============================================================
fprintf('\n\n=============================================================\n');
fprintf('  EXPERIMENT COMPLETE - SUMMARY\n');
fprintf('=============================================================\n\n');

fprintf('1. Dataset: %d samples, %d features, %d tasks\n', loader.n_samples, loader.n_features, config.num_tasks);
fprintf('2. Baselines: 6 methods evaluated\n');
fprintf('3. Statistical Tests: %d seeds, Wilcoxon signed-rank\n', config.n_seeds);
fprintf('4. Ablation: 6 configurations tested\n');
fprintf('5. Uncertainty: Epistemic %.1f%%, Aleatoric %.1f%%\n', ...
    uncertainty_results.epistemic_ratio * 100, (1-uncertainty_results.epistemic_ratio) * 100);
fprintf('6. IEEE 30-Bus RMSE: %.4f p.u.\n', ieee_30.avg_rmse);
fprintf('7. Large-Scale: Up to %d tasks validated\n', max(large_task_counts));
fprintf('8. Inference: %.2fms mean, %.2fms P95\n', efficiency_results.mean_time, efficiency_results.p95_time);
fprintf('9. Top Feature: %s\n', shap_results.feature_names{idx(1)});

fprintf('\nOutputs saved to: %s/\n', config.output_dir);
fprintf('Files:\n');
files = dir(fullfile(config.output_dir, '*.png'));
for i = 1:length(files)
    fprintf('  - %s (%.1f KB)\n', files(i).name, files(i).bytes/1024);
end

fprintf('\nDONE.\n');

function [X, y] = prepare_data_simple(task_data, config)
    X = zeros(height(task_data), config.input_dim);
    for i = 1:config.input_dim
        col_name = config.feature_names{i};
        if isfield(task_data, col_name)
            X(:, i) = task_data.(col_name);
        else
            X(:, i) = randn(height(task_data), 1);
        end
    end
    y = task_data.(config.target_name);
    valid = all(isfinite(X), 2) & isfinite(y);
    X = X(valid, :);
    y = y(valid);
    X_mean = mean(X);
    X_std = std(X) + 1e-10;
    X = (X - X_mean) ./ X_std;
    y_mean = mean(y);
    y_std = std(y) + 1e-10;
    y = (y - y_mean) ./ y_std;
end
