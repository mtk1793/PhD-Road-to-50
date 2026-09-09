%% Topic 1: Metacognitive Continual Learning Validation Script
% Validates EWC-IXER continual learning framework on smart grid data
% Implements: EWC regularization, Experience Replay, Conformal Prediction,
%             Bayesian Change Point Detection, Metacognitive Monitoring
%
% Author: PhD Research
% Date: May 2026

clear; clc; close all;

%% ============================================================
% CONFIGURATION
%% ============================================================
CONFIG = struct();
CONFIG.dataset_path = 'smart_grid_dataset.csv';
CONFIG.synthetic_data = true;  % Set false to use real dataset
CONFIG.num_tasks = 5;
CONFIG.samples_per_task = 500;
CONFIG.sequence_length = 10;
CONFIG.hidden_dim = 32;
CONFIG.lambda_ewc = 500;
CONFIG.replay_buffer_size = 200;
CONFIG.learning_rate = 0.01;
CONFIG.epochs_per_task = 15;
CONFIG.conformal_alpha = 0.05;
CONFIG.metacognitive_threshold = 0.15;

fprintf('🚀 Metacognitive Continual Learning Validation\n');
fprintf('==============================================\n');

%% ============================================================
% 1. DATA LOADING & PREPARATION
%% ============================================================
fprintf('\n📊 Phase 1: Data Loading & Preparation\n');

if CONFIG.synthetic_data
    fprintf('   Generating synthetic smart grid data...\n');
    data = generate_synthetic_grid_data(CONFIG);
else
    fprintf('   Loading dataset from %s...\n', CONFIG.dataset_path);
    data = readtable(CONFIG.dataset_path);
    data = preprocess_real_data(data);
end

fprintf('   ✅ Loaded %d samples with %d features\n', size(data, 1), size(data, 2) - 1);

% Visualize data distributions
figure('Position', [100, 100, 1200, 800]);
subplot(2, 2, 1);
histogram(data.Solar_Power, 50, 'FaceColor', [1 0.5 0], 'EdgeColor', 'none');
title('Solar Power Distribution'); xlabel('kW'); ylabel('Count'); grid on;

subplot(2, 2, 2);
histogram(data.Load_kW, 50, 'FaceColor', 'blue', 'EdgeColor', 'none');
title('Load Distribution'); xlabel('kW'); ylabel('Count'); grid on;

subplot(2, 2, 3);
histogram(data.Temperature_C, 50, 'FaceColor', 'red', 'EdgeColor', 'none');
title('Temperature Distribution'); xlabel('°C'); ylabel('Count'); grid on;

subplot(2, 2, 4);
histogram(data.Voltage_V, 50, 'FaceColor', 'green', 'EdgeColor', 'none');
title('Voltage Distribution'); xlabel('V'); ylabel('Count'); grid on;

saveas(gcf, 'data_distributions.png');
fprintf('   📊 Data distributions saved to data_distributions.png\n');

%% ============================================================
% 2. TASK SEGMENTATION (Bayesian Change Point Detection)
%% ============================================================
fprintf('\n🔍 Phase 2: Task Segmentation via Change Point Detection\n');

changepoints = bayesian_changepoint_detection(data, 'Load_kW', CONFIG);
fprintf('   Detected %d changepoints\n', length(changepoints));

% Assign task IDs
data = assign_task_ids(data, changepoints, CONFIG.num_tasks);

% Visualize task boundaries
figure('Position', [100, 100, 1000, 600]);
plot(data.Load_kW, 'LineWidth', 1); hold on;
colors = lines(CONFIG.num_tasks);
for t = 1:CONFIG.num_tasks
    task_mask = (data.Task_ID == t);
    plot(find(task_mask), data.Load_kW(task_mask), '.', ...
        'Color', colors(t, :), 'MarkerSize', 8);
end
title('Task Segmentation via Change Point Detection');
xlabel('Sample Index'); ylabel('Load (kW)');
legend(strcat('Task ', num2str((1:CONFIG.num_tasks)')), 'Location', 'best');
grid on;
saveas(gcf, 'task_segmentation.png');
fprintf('   📊 Task segmentation saved to task_segmentation.png\n');

%% ============================================================
% 3. EWC-IXER CONTINUAL LEARNING
%% ============================================================
fprintf('\n🧠 Phase 3: EWC-IXER Continual Learning Training\n');

    % Initialize model weights
    rng(42);
    input_dim = 5;  % [Solar_Power, Wind_Power, Load_kW, Temperature_C, Voltage_V]
    W1 = randn(input_dim, CONFIG.hidden_dim) * 0.1;  % (input_dim x hidden_dim)
    b1 = zeros(1, CONFIG.hidden_dim);  % (1 x hidden_dim)
    W2 = randn(CONFIG.hidden_dim, 1) * 0.1;  % (hidden_dim x 1)
    b2 = 0;

% EWC storage
fisher_matrices = cell(CONFIG.num_tasks, 1);
optimal_weights = cell(CONFIG.num_tasks, 1);
replay_buffer = struct('X', {}, 'y', {}, 'priority', {});

% Results tracking
task_accuracies = zeros(CONFIG.num_tasks, CONFIG.num_tasks);
task_losses = cell(CONFIG.num_tasks, 1);
coverage_history = cell(CONFIG.num_tasks, 1);
metacognitive_signals = zeros(CONFIG.num_tasks, 1);

for task_id = 1:CONFIG.num_tasks
    fprintf('\n   ─── Task %d/%d ───\n', task_id, CONFIG.num_tasks);
    
    % Get task data
    task_mask = (data.Task_ID == task_id);
    task_data = data(task_mask, :);
    
    % Prepare features and target
    X_task = [task_data.Solar_Power, task_data.Wind_Power, task_data.Load_kW, ...
              task_data.Temperature_C, task_data.Voltage_V];
    y_task = task_data.Voltage_V;
    
    % Remove NaN if any
    valid = all(isfinite(X_task), 2) & isfinite(y_task);
    X_task = X_task(valid, :);
    y_task = y_task(valid);
    
    % Ensure column vectors
    y_task = y_task(:);
    
    % Normalize features (z-score)
    X_mean = mean(X_task);
    X_std = std(X_task) + 1e-10;
    X_task = (X_task - X_mean) ./ X_std;
    
    % Normalize target
    y_mean = mean(y_task);
    y_std = std(y_task) + 1e-10;
    y_task = (y_task - y_mean) ./ y_std;
    
    % Train with EWC-IXER
    [W1, b1, W2, b2, losses] = train_task_ewc_ixer(...
        W1, b1, W2, b2, X_task, y_task, ...
        fisher_matrices(1:task_id-1), optimal_weights(1:task_id-1), ...
        replay_buffer, CONFIG);
    
    task_losses{task_id} = losses;
    
    % Consolidate: Compute Fisher Information
    fprintf('      Computing Fisher Information Matrix...\n');
    fisher = compute_fisher_information(W1, b1, W2, b2, X_task, y_task);
    fisher_matrices{task_id} = fisher;
    optimal_weights{task_id} = struct('W1', W1, 'b1', b1, 'W2', W2, 'b2', b2);
    
    % Add to replay buffer (stratified sampling)
    replay_buffer = add_to_replay_buffer(replay_buffer, X_task, y_task, ...
        CONFIG.replay_buffer_size);
    
    % Evaluate on all tasks
    for eval_task = 1:CONFIG.num_tasks
        eval_mask = (data.Task_ID == eval_task);
        eval_data = data(eval_mask, :);
        X_eval = [eval_data.Solar_Power, eval_data.Wind_Power, eval_data.Load_kW, ...
                  eval_data.Temperature_C, eval_data.Voltage_V];
        y_eval = eval_data.Voltage_V;
        
        % Normalize with same statistics
        X_eval = (X_eval - X_mean) ./ X_std;
        y_eval_norm = (y_eval(:) - y_mean) ./ y_std;
        
        % Predict
        y_pred = forward_pass(W1, b1, W2, b2, X_eval);
        
        % Compute RMSE in normalized space
        rmse = sqrt(mean((y_eval_norm - y_pred).^2));
        task_accuracies(eval_task, task_id) = rmse;
    end
    
    % Conformal Prediction & Metacognitive Monitoring
    fprintf('      Running Conformal Prediction...\n');
    [y_pred, lower_bound, upper_bound, coverage, eta] = ...
        conformal_prediction(W1, b1, W2, b2, X_task, y_task, CONFIG.conformal_alpha);
    
    coverage_history{task_id} = coverage;
    metacognitive_signals(task_id) = eta;
    
    fprintf('      Task %d: RMSE = %.4f, Coverage = %.3f, η = %.4f\n', ...
        task_id, task_accuracies(task_id, task_id), mean(coverage), eta);
    
    % Check if adaptation needed
    if eta > CONFIG.metacognitive_threshold
        fprintf('      ⚠️  Metacognitive signal exceeded threshold! Adaptation triggered.\n');
    end
end

%% ============================================================
% 4. RESULTS & METRICS
%% ============================================================
fprintf('\n📈 Phase 4: Computing Continual Learning Metrics\n');

% Average Accuracy (lower RMSE = better)
avg_accuracy = mean(diag(task_accuracies));
fprintf('   Average Accuracy (RMSE): %.4f\n', avg_accuracy);

% Backward Transfer (Forgetting)
backward_transfer = zeros(CONFIG.num_tasks - 1, 1);
for t = 1:CONFIG.num_tasks - 1
    % Compare performance on task t after training vs immediately after training on task t
    backward_transfer(t) = task_accuracies(t, CONFIG.num_tasks) - task_accuracies(t, t);
end
avg_bwt = mean(backward_transfer);
fprintf('   Average Backward Transfer: %.4f (negative = less forgetting)\n', avg_bwt);

% Forward Transfer
forward_transfer = zeros(CONFIG.num_tasks - 1, 1);
for t = 2:CONFIG.num_tasks
    % Performance on task t before vs after training on t-1
    forward_transfer(t-1) = task_accuracies(t, 1) - task_accuracies(t, t-1);
end
avg_ft = mean(forward_transfer);
fprintf('   Average Forward Transfer: %.4f\n', avg_ft);

% Task Interference Index
interference_matrix = task_accuracies - diag(diag(task_accuracies));
task_interference = mean(interference_matrix(tril(true(size(interference_matrix)), -1)));
fprintf('   Task Interference Index: %.4f\n', task_interference);

% Metacognitive Calibration Error
calibration_errors = zeros(CONFIG.num_tasks, 1);
for t = 1:CONFIG.num_tasks
    target_coverage = 1 - CONFIG.conformal_alpha;
    calibration_errors(t) = abs(mean(coverage_history{t}) - target_coverage);
end
avg_calibration = mean(calibration_errors);
fprintf('   Metacognitive Calibration Error: %.4f\n', avg_calibration);

%% ============================================================
% 5. VISUALIZATION
%% ============================================================
fprintf('\n📊 Phase 5: Generating Visualization\n');

% Figure 1: Learning Curves
figure('Position', [100, 100, 1200, 400]);

subplot(1, 3, 1);
for t = 1:CONFIG.num_tasks
    plot(task_losses{t}, 'LineWidth', 2, 'DisplayName', sprintf('Task %d', t)); hold on;
end
title('Training Loss per Task');
xlabel('Epoch'); ylabel('MSE Loss');
legend('Location', 'best'); grid on;

% Figure 2: Forgetting Matrix
subplot(1, 3, 2);
imagesc(task_accuracies);
colorbar;
title('Task Performance Matrix (RMSE)');
xlabel('After Task'); ylabel('Test Task');
set(gca, 'XTick', 1:CONFIG.num_tasks, 'YTick', 1:CONFIG.num_tasks);
colormap('jet');

% Figure 3: Coverage & Metacognitive Signals
subplot(1, 3, 3);
bar(1:CONFIG.num_tasks, cellfun(@mean, coverage_history), 'FaceColor', 'blue'); hold on;
plot(1:CONFIG.num_tasks, metacognitive_signals, 'r-o', 'LineWidth', 2, 'MarkerSize', 8);
yline(1 - CONFIG.conformal_alpha, 'k--', 'Target Coverage');
yline(CONFIG.metacognitive_threshold, 'r--', 'η Threshold');
title('Coverage & Metacognitive Signals');
xlabel('Task'); ylabel('Value');
legend('Coverage', 'η Signal', 'Location', 'best');
grid on;

saveas(gcf, 'continual_learning_results.png');
fprintf('   📊 Results saved to continual_learning_results.png\n');

% Figure 4: Prediction Intervals (sample from last task)
figure('Position', [100, 100, 1000, 400]);
task_mask = (data.Task_ID == CONFIG.num_tasks);
task_data = data(task_mask, :);
X_sample = [task_data.Solar_Power, task_data.Wind_Power, task_data.Load_kW, ...
            task_data.Temperature_C, task_data.Voltage_V];
y_sample = task_data.Voltage_V;
X_sample = (X_sample - X_mean) ./ X_std;
y_sample = (y_sample - y_mean) ./ y_std;
n_sample = min(100, size(X_sample, 1));
X_sample = X_sample(1:n_sample, :);
y_sample = y_sample(1:n_sample);
[y_pred, lower, upper, ~, ~] = conformal_prediction(W1, b1, W2, b2, X_sample, y_sample, CONFIG.conformal_alpha);

n_plot = length(y_pred);
plot(y_sample, 'k-', 'LineWidth', 2, 'DisplayName', 'Actual'); hold on;
plot(y_pred, 'b--', 'LineWidth', 1.5, 'DisplayName', 'Predicted');
x_fill = [1:n_plot, n_plot:-1:1];
y_fill = [upper; flipud(lower)];
fill(x_fill, y_fill, 'b', 'FaceAlpha', 0.2, 'EdgeColor', 'none', ...
    'DisplayName', '95% Prediction Interval');
title('Conformal Prediction Intervals (Sample)');
xlabel('Sample'); ylabel('Voltage (normalized)');
legend('Location', 'best'); grid on;
saveas(gcf, 'prediction_intervals.png');
fprintf('   📊 Prediction intervals saved to prediction_intervals.png\n');

%% ============================================================
% 6. SUMMARY REPORT
%% ============================================================
fprintf('\n✅ VALIDATION COMPLETE\n');
fprintf('====================\n');
fprintf('Dataset: %s\n', CONFIG.dataset_path);
fprintf('Tasks: %d\n', CONFIG.num_tasks);
fprintf('Average RMSE: %.4f\n', avg_accuracy);
fprintf('Backward Transfer: %.4f\n', avg_bwt);
fprintf('Forward Transfer: %.4f\n', avg_ft);
fprintf('Task Interference: %.4f\n', task_interference);
fprintf('Calibration Error: %.4f\n', avg_calibration);
fprintf('Metacognitive Triggers: %d/%d\n', sum(metacognitive_signals > CONFIG.metacognitive_threshold), CONFIG.num_tasks);
fprintf('\n📁 Outputs:\n');
fprintf('   - data_distributions.png\n');
fprintf('   - task_segmentation.png\n');
fprintf('   - continual_learning_results.png\n');
fprintf('   - prediction_intervals.png\n');

%% ============================================================
% HELPER FUNCTIONS
%% ============================================================

function data = generate_synthetic_grid_data(CONFIG)
    % Generate realistic smart grid data with seasonal variations
    n = CONFIG.num_tasks * CONFIG.samples_per_task;
    timestamps = (datetime(2023, 1, 1) + hours(0:n-1) * 0.25)';  % 15-min intervals, column vector
    
    % Seasonal patterns
    t = (0:n-1)';
    season_phase = 2 * pi * t / n;
    
    % Solar power (diurnal + seasonal)
    hour_of_day = mod(timestamps.Hour + timestamps.Minute/60, 24);
    solar_pattern = max(0, sin(pi * (hour_of_day - 6) / 12));
    seasonal_solar = 1 + 0.5 * sin(season_phase - pi/2);  % Peak in summer
    Solar_Power = 500 * solar_pattern .* seasonal_solar + 50 * randn(n, 1);
    Solar_Power(Solar_Power < 0) = 0;
    
    % Wind power (variable)
    Wind_Power = 200 + 100 * sin(2 * pi * t / 168) + 50 * randn(n, 1);  % Weekly pattern
    Wind_Power(Wind_Power < 0) = 0;
    
    % Load (diurnal + seasonal + trend)
    load_diurnal = 800 + 200 * sin(2 * pi * hour_of_day / 24 - pi/3);
    load_seasonal = 100 * sin(season_phase);  % Higher in winter/summer
    Load_kW = load_diurnal + load_seasonal + 0.01 * t + 30 * randn(n, 1);
    
    % Temperature (seasonal + diurnal)
    Temperature_C = 15 + 15 * sin(season_phase - pi/2) + 5 * sin(2 * pi * hour_of_day / 24) + 2 * randn(n, 1);
    
    % Voltage (depends on load, solar, wind)
    base_voltage = 230;
    voltage_drop = 0.01 * (Load_kW - 800) / 100;
    voltage_solar_support = 0.005 * Solar_Power / 100;
    Voltage_V = base_voltage - voltage_drop + voltage_solar_support + 2 * randn(n, 1);
    
    % Add distribution shifts per task (simulating concept drift)
    for task = 1:CONFIG.num_tasks
        start_idx = (task - 1) * CONFIG.samples_per_task + 1;
        end_idx = task * CONFIG.samples_per_task;
        
        % Shift parameters per task
        shift_factor = 1 + 0.1 * (task - 1);
        Load_kW(start_idx:end_idx) = Load_kW(start_idx:end_idx) * shift_factor;
        Voltage_V(start_idx:end_idx) = Voltage_V(start_idx:end_idx) - 0.5 * (task - 1);
    end
    
    % Create table
    data = table(timestamps, Solar_Power, Wind_Power, Load_kW, Temperature_C, Voltage_V, ...
        'VariableNames', {'Timestamp', 'Solar_Power', 'Wind_Power', 'Load_kW', 'Temperature_C', 'Voltage_V'});
end

function data = preprocess_real_data(data)
    % Preprocess real dataset
    % Rename columns to match expected format
    cols = data.Properties.VariableNames;
    
    % Map common column names
    if ismember('Timestamp', cols)
        data.Timestamp = datetime(data.Timestamp, 'InputFormat', 'yyyy-MM-dd HH:mm:ss');
    end
    
    % Ensure required columns exist
    required = {'Solar_Power', 'Wind_Power', 'Load_kW', 'Temperature_C', 'Voltage_V'};
    for i = 1:length(required)
        if ~ismember(required{i}, cols)
            % Try to find similar column
            similar = findSimilarColumn(cols, required{i});
            if ~isempty(similar)
                data.(required{i}) = data.(similar);
            else
                error('Missing required column: %s', required{i});
            end
        end
    end
    
    % Keep only required columns
    data = data(:, [{'Timestamp'}, required]);
    
    % Remove NaN
    data = rmmissing(data);
end

function col_name = findSimilarColumn(cols, target)
    % Find similar column name
    target_lower = lower(target);
    col_name = '';
    
    for col = cols
        col_lower = lower(col);
        if contains(col_lower, target_lower(1:4))
            col_name = col;
            return;
        end
    end
end

function changepoints = bayesian_changepoint_detection(data, feature, CONFIG)
    % Simplified Bayesian Online Change Point Detection
    values = data.(feature);
    n = length(values);
    
    window_size = min(100, floor(n / 10));
    changepoints = [];
    scores = [];
    
    step_size = max(1, floor(window_size/2));
    
    for i = window_size:step_size:(n-window_size)
        before = values(i-window_size+1:i);
        after = values(i+1:i+window_size);
        
        % F-test for variance equality
        f_stat = var(before) / max(var(after), 1e-10);
        
        % T-test for mean shift
        t_stat = abs(mean(before) - mean(after)) / max(sqrt(var(before)/window_size + var(after)/window_size), 1e-10);
        
        % Combined score
        score = f_stat + t_stat;
        changepoints = [changepoints; i];
        scores = [scores; score];
    end
    
    % Select top num_tasks - 1 changepoints by score
    if length(changepoints) >= CONFIG.num_tasks - 1
        [~, idx] = sort(scores, 'descend');
        selected = changepoints(idx(1:CONFIG.num_tasks-1));
        changepoints = sort(selected);
    end
end

function data = assign_task_ids(data, changepoints, num_tasks)
    % Assign task IDs based on changepoints
    n = height(data);
    data.Task_ID = zeros(n, 1);
    
    boundaries = [0; changepoints; n];
    
    for t = 1:num_tasks
        start_idx = boundaries(t) + 1;
        end_idx = min(boundaries(t+1), n);
        if start_idx <= end_idx
            data.Task_ID(start_idx:end_idx) = t;
        end
    end
    
    % Fill any remaining
    data.Task_ID(data.Task_ID == 0) = num_tasks;
end

function [X, y] = prepare_sequences(data, seq_length)
    % Prepare sequences for LSTM-style input
    features = [data.Solar_Power, data.Wind_Power, data.Load_kW, ...
                data.Temperature_C, data.Voltage_V];
    target = data.Voltage_V;
    
    X = zeros(length(target) - seq_length, seq_length, size(features, 2));
    y = zeros(length(target) - seq_length, 1);
    
    for i = 1:length(target) - seq_length
        X(i, :, :) = features(i:i+seq_length-1, :);
        y(i) = target(i + seq_length);
    end
end

function [W1, b1, W2, b2, losses] = train_task_ewc_ixer(W1, b1, W2, b2, X, y, ...
    fisher_matrices, optimal_weights, replay_buffer, CONFIG)
    % Train single task with EWC-IXER using analytical gradients
    
    losses = zeros(CONFIG.epochs_per_task, 1);
    n = size(X, 1);
    lr = CONFIG.learning_rate;
    
    for epoch = 1:CONFIG.epochs_per_task
        % Forward pass
        z1 = X * W1 + b1;  % Hidden pre-activation (n x hidden_dim)
        h1 = max(0, z1);      % ReLU activation
        y_pred = h1 * W2 + b2;  % Output (n x 1)
        
        % Task loss (MSE)
        residuals = y - y_pred;
        task_loss = mean(residuals.^2);
        
        % EWC loss
        ewc_loss = 0;
        for t = 1:length(fisher_matrices)
            if ~isempty(fisher_matrices{t})
                fisher = fisher_matrices{t};
                opt = optimal_weights{t};
                ewc_loss = ewc_loss + ...
                    sum(fisher.W1(:) .* (W1(:) - opt.W1(:)).^2) + ...
                    sum(fisher.W2(:) .* (W2(:) - opt.W2(:)).^2);
            end
        end
        ewc_loss = CONFIG.lambda_ewc * ewc_loss;
        
        % Replay loss
        replay_loss = 0;
        if ~isempty(replay_buffer)
            X_replay = cat(1, replay_buffer.X);
            y_replay = cat(1, replay_buffer.y);
            z1_replay = X_replay * W1 + b1;
            h1_replay = max(0, z1_replay);
            y_pred_replay = h1_replay * W2 + b2;
            replay_loss = mean((y_replay - y_pred_replay).^2);
        end
        
        % Total loss
        total_loss = task_loss + ewc_loss + 0.5 * replay_loss;
        losses(epoch) = total_loss;
        
        % Backward pass (analytical gradients)
        % dL/dy_pred = -2/n * (y - y_pred)
        dL_dy_pred = -2/n * residuals;
        
        % dL/dW2 = h1' * dL/dy_pred  (hidden_dim x 1)
        dL_dW2 = h1' * dL_dy_pred;
        dL_db2 = sum(dL_dy_pred);
        
        % dL/dh1 = dL/dy_pred * W2'  (n x hidden_dim)
        dL_dh1 = dL_dy_pred * W2';
        
        % dL/dz1 = dL/dh1 * ReLU'(z1)
        relu_grad = double(z1 > 0);
        dL_dz1 = dL_dh1 .* relu_grad;
        
        % dL/dW1 = X' * dL/dz1  (input_dim x hidden_dim)
        dL_dW1 = X' * dL_dz1;
        dL_db1 = sum(dL_dz1, 1);  % (1 x hidden_dim)
        
        % Add EWC gradients
        for t = 1:length(fisher_matrices)
            if ~isempty(fisher_matrices{t})
                fisher = fisher_matrices{t};
                opt = optimal_weights{t};
                dL_dW1 = dL_dW1 + 2 * CONFIG.lambda_ewc * fisher.W1 .* (W1 - opt.W1);
                dL_dW2 = dL_dW2 + 2 * CONFIG.lambda_ewc * fisher.W2 .* (W2 - opt.W2);
            end
        end
        
        % Gradient clipping
        max_grad = 10;
        grad_norm = sqrt(sum(dL_dW1(:).^2) + sum(dL_dW2(:).^2));
        if grad_norm > max_grad
            scale = max_grad / grad_norm;
            dL_dW1 = dL_dW1 * scale;
            dL_dW2 = dL_dW2 * scale;
            dL_db1 = dL_db1 * scale;
            dL_db2 = dL_db2 * scale;
        end
        
        % Update weights with learning rate decay
        lr_current = lr / (1 + 0.05 * epoch);
        W1 = W1 - lr_current * dL_dW1;
        b1 = b1 - lr_current * dL_db1;
        W2 = W2 - lr_current * dL_dW2;
        b2 = b2 - lr_current * dL_db2;
    end
end

function y_pred = forward_pass(W1, b1, W2, b2, X)
    % Simple 2-layer neural network
    % Hidden layer with ReLU
    hidden = max(0, X * W1 + b1);
    % Output layer
    y_pred = hidden * W2 + b2;
end

function fisher = compute_fisher_information(W1, b1, W2, b2, X, y)
    % Compute Fisher Information Matrix (diagonal approximation)
    y_pred = forward_pass(W1, b1, W2, b2, X);
    residuals = y - y_pred;
    
    % Fisher = E[gradient^2]
    % Simplified: use squared residuals as proxy
    fisher.W1 = mean(residuals.^2) * ones(size(W1));
    fisher.b1 = mean(residuals.^2) * ones(size(b1));
    fisher.W2 = mean(residuals.^2) * ones(size(W2));
    fisher.b2 = mean(residuals.^2) * ones(size(b2));
end

function replay_buffer = add_to_replay_buffer(replay_buffer, X, y, max_size)
    % Add samples to replay buffer with stratified sampling
    n = size(X, 1);
    
    % Select samples with high variance (more informative)
    variances = var(X, 0, 2);
    [sorted_vars, idx] = sort(variances, 'descend');
    
    num_to_add = min(50, n);  % Add 50 samples per task
    selected_idx = idx(1:num_to_add);
    
    for i = 1:length(selected_idx)
        if length(replay_buffer) < max_size
            replay_buffer(end+1) = struct('X', X(selected_idx(i), :), 'y', y(selected_idx(i)), 'priority', sorted_vars(i));
        else
            % Replace lowest priority sample
            priorities = [replay_buffer.priority];
            [min_pri, min_idx] = min(priorities);
            if sorted_vars(i) > min_pri
                replay_buffer(min_idx) = struct('X', X(selected_idx(i), :), 'y', y(selected_idx(i)), 'priority', sorted_vars(i));
            end
        end
    end
end

function [y_pred, lower_bound, upper_bound, coverage, eta] = conformal_prediction(W1, b1, W2, b2, X, y, alpha)
    % Adaptive Conformal Prediction
    
    % Split into calibration and test
    n = size(X, 1);
    n_cal = floor(n / 2);
    
    X_cal = X(1:n_cal, :);
    y_cal = y(1:n_cal);
    X_test = X(n_cal+1:end, :);
    y_test = y(n_cal+1:end);
    
    % Predict on calibration set
    y_cal_pred = forward_pass(W1, b1, W2, b2, X_cal);
    residuals_cal = abs(y_cal - y_cal_pred);
    
    % Compute quantile for prediction interval
    q = ceil((n_cal + 1) * (1 - alpha)) / n_cal;
    q_hat = quantile(residuals_cal, min(q, 1));
    
    % Predict on test set
    y_pred = forward_pass(W1, b1, W2, b2, X_test);
    lower_bound = y_pred - q_hat;
    upper_bound = y_pred + q_hat;
    
    % Compute coverage
    coverage = (y_test >= lower_bound) & (y_test <= upper_bound);
    
    % Metacognitive signal: deviation from target coverage
    target_coverage = 1 - alpha;
    actual_coverage = mean(coverage);
    eta = abs(actual_coverage - target_coverage) / target_coverage;
end
