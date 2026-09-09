%% Baselines - Complete Continual Learning Baseline Implementations
% Implements: Naive Fine-tuning, ER-only, EWC-only, PackNet, Progressive NN, EWC-IXER (ours)
classdef Baselines < handle
    properties (Constant)
        methods_list = {'naive', 'er_only', 'ewc_only', 'packnet', 'progressive_nn', 'ewc_ixer'};
    end
    
    methods (Static)
        function results = run_all_baselines(tasks, config)
            % Run all baseline methods on the same task sequence
            n_methods = 6;
            n_tasks = length(tasks);
            
            results = struct();
            
            for m = 1:n_methods
                method_name = Baselines.methods_list{m};
                fprintf('\n[%s] Training on %d tasks...\n', upper(method_name), n_tasks);
                
                switch method_name
                    case 'naive'
                        results.naive = Baselines.naive_fine_tuning(tasks, config);
                    case 'er_only'
                        results.er_only = Baselines.er_only(tasks, config);
                    case 'ewc_only'
                        results.ewc_only = Baselines.ewc_only(tasks, config);
                    case 'packnet'
                        results.packnet = Baselines.packnet(tasks, config);
                    case 'progressive_nn'
                        results.progressive_nn = Baselines.progressive_nn(tasks, config);
                    case 'ewc_ixer'
                        results.ewc_ixer = Baselines.ewc_ixer(tasks, config);
                end
            end
            
            fprintf('\nAll baselines complete.\n');
        end
        
        function result = naive_fine_tuning(tasks, config)
            % Naive Fine-tuning: Sequential training without any regularization
            result.name = 'Naive Fine-Tuning';
            result.n_tasks = length(tasks);
            result.per_task_rmse = zeros(length(tasks), length(tasks));
            result.loss_curves = cell(length(tasks), 1);
            
            W1 = randn(config.input_dim, config.hidden_dim) * 0.1;
            b1 = zeros(1, config.hidden_dim);
            W2 = randn(config.hidden_dim, 1) * 0.1;
            b2 = 0;
            
            for t = 1:length(tasks)
                [X, y] = prepare_task_data(tasks{t}, config);
                [W1, b1, W2, b2, losses] = train_basic(W1, b1, W2, b2, X, y, config);
                result.loss_curves{t} = losses;
                
                for eval_t = 1:length(tasks)
                    [X_eval, y_eval] = prepare_task_data(tasks{eval_t}, config);
                    y_pred = forward_pass(W1, b1, W2, b2, X_eval);
                    result.per_task_rmse(eval_t, t) = sqrt(mean((y_eval - y_pred).^2));
                end
            end
            
            result.avg_accuracy = mean(diag(result.per_task_rmse));
            result.backward_transfer = compute_bwt(result.per_task_rmse);
        end
        
        function result = er_only(tasks, config)
            % Experience Replay Only: Buffer-based rehearsal without EWC
            result.name = 'Experience Replay Only';
            result.n_tasks = length(tasks);
            result.per_task_rmse = zeros(length(tasks), length(tasks));
            result.loss_curves = cell(length(tasks), 1);
            result.buffer_sizes = zeros(length(tasks), 1);
            
            W1 = randn(config.input_dim, config.hidden_dim) * 0.1;
            b1 = zeros(1, config.hidden_dim);
            W2 = randn(config.hidden_dim, 1) * 0.1;
            b2 = 0;
            replay_buffer = struct('X', {}, 'y', {});
            
            for t = 1:length(tasks)
                [X, y] = prepare_task_data(tasks{t}, config);
                [W1, b1, W2, b2, losses] = train_with_replay(W1, b1, W2, b2, X, y, replay_buffer, config);
                result.loss_curves{t} = losses;
                
                replay_buffer = add_to_buffer(replay_buffer, X, y, config.replay_size);
                result.buffer_sizes(t) = length(replay_buffer);
                
                for eval_t = 1:length(tasks)
                    [X_eval, y_eval] = prepare_task_data(tasks{eval_t}, config);
                    y_pred = forward_pass(W1, b1, W2, b2, X_eval);
                    result.per_task_rmse(eval_t, t) = sqrt(mean((y_eval - y_pred).^2));
                end
            end
            
            result.avg_accuracy = mean(diag(result.per_task_rmse));
            result.backward_transfer = compute_bwt(result.per_task_rmse);
        end
        
        function result = ewc_only(tasks, config)
            % EWC Only: Elastic Weight Consolidation without replay
            result.name = 'EWC Only';
            result.n_tasks = length(tasks);
            result.per_task_rmse = zeros(length(tasks), length(tasks));
            result.loss_curves = cell(length(tasks), 1);
            result.fisher_norms = zeros(length(tasks), 1);
            
            W1 = randn(config.input_dim, config.hidden_dim) * 0.1;
            b1 = zeros(1, config.hidden_dim);
            W2 = randn(config.hidden_dim, 1) * 0.1;
            b2 = 0;
            
            fisher_matrices = {};
            optimal_weights = {};
            
            for t = 1:length(tasks)
                [X, y] = prepare_task_data(tasks{t}, config);
                [W1, b1, W2, b2, losses] = train_with_ewc(W1, b1, W2, b2, X, y, ...
                    fisher_matrices, optimal_weights, config);
                result.loss_curves{t} = losses;
                
                fisher = compute_fisher(W1, b1, W2, b2, X, y);
                fisher_matrices{t} = fisher;
                optimal_weights{t} = struct('W1', W1, 'b1', b1, 'W2', W2, 'b2', b2);
                result.fisher_norms(t) = sum(fisher.W1(:).^2) + sum(fisher.W2(:).^2);
                
                for eval_t = 1:length(tasks)
                    [X_eval, y_eval] = prepare_task_data(tasks{eval_t}, config);
                    y_pred = forward_pass(W1, b1, W2, b2, X_eval);
                    result.per_task_rmse(eval_t, t) = sqrt(mean((y_eval - y_pred).^2));
                end
            end
            
            result.avg_accuracy = mean(diag(result.per_task_rmse));
            result.backward_transfer = compute_bwt(result.per_task_rmse);
        end
        
        function result = packnet(tasks, config)
            % PackNet: Weight pruning and task-specific allocation
            result.name = 'PackNet';
            result.n_tasks = length(tasks);
            result.per_task_rmse = zeros(length(tasks), length(tasks));
            result.loss_curves = cell(length(tasks), 1);
            result.pruning_ratios = zeros(length(tasks), 1);
            
            W1 = randn(config.input_dim, config.hidden_dim) * 0.1;
            b1 = zeros(1, config.hidden_dim);
            W2 = randn(config.hidden_dim, 1) * 0.1;
            b2 = 0;
            
            masks = struct('W1', ones(size(W1)), 'b1', ones(size(b1)), ...
                'W2', ones(size(W2)), 'b2', 1);
            
            prune_fraction = 0.3;
            
            for t = 1:length(tasks)
                [X, y] = prepare_task_data(tasks{t}, config);
                
                for epoch = 1:config.epochs_per_task
                    [W1, b1, W2, b2] = train_epoch_masked(W1, b1, W2, b2, masks, X, y, config);
                end
                
                W1 = W1 .* masks.W1;
                b1 = b1 .* masks.b1;
                W2 = W2 .* masks.W2;
                b2 = b2 .* masks.b2;
                
                if t < length(tasks)
                    [masks, pruned_ratio] = prune_weights(W1, b1, W2, b2, masks, prune_fraction);
                    result.pruning_ratios(t) = pruned_ratio;
                end
                
                for eval_t = 1:length(tasks)
                    [X_eval, y_eval] = prepare_task_data(tasks{eval_t}, config);
                    y_pred = forward_pass(W1, b1, W2, b2, X_eval);
                    result.per_task_rmse(eval_t, t) = sqrt(mean((y_eval - y_pred).^2));
                end
            end
            
            result.avg_accuracy = mean(diag(result.per_task_rmse));
            result.backward_transfer = compute_bwt(result.per_task_rmse);
        end
        
        function result = progressive_nn(tasks, config)
            % Progressive Neural Networks: Task-specific columns with lateral connections
            result.name = 'Progressive NN';
            result.n_tasks = length(tasks);
            result.per_task_rmse = zeros(length(tasks), length(tasks));
            result.loss_curves = cell(length(tasks), 1);
            result.total_parameters = zeros(length(tasks), 1);
            
            n_tasks = length(tasks);
            
            task_W1 = cell(n_tasks, 1);
            task_b1 = cell(n_tasks, 1);
            task_W2 = cell(n_tasks, 1);
            task_b2 = cell(n_tasks, 1);
            task_lateral = cell(n_tasks, 1);
            
            for t = 1:n_tasks
                task_W1{t} = randn(config.input_dim, config.hidden_dim) * 0.1;
                task_b1{t} = zeros(1, config.hidden_dim);
                task_W2{t} = randn(config.hidden_dim, 1) * 0.1;
                task_b2{t} = 0;
                
                if t > 1
                    task_lateral{t} = randn(config.hidden_dim*(t-1), config.hidden_dim) * 0.01;
                end
                
                [X, y] = prepare_task_data(tasks{t}, config);
                
                for epoch = 1:config.epochs_per_task
                    W1_cur = task_W1{t};
                    b1_cur = task_b1{t};
                    
                    if t > 1
                        for prev = 1:t-1
                            [X_prev, y_prev] = prepare_task_data(tasks{prev}, config);
                            h_prev = max(0, X_prev * task_W1{prev} + task_b1{prev});
                        end
                    end
                    
                    h = max(0, X * W1_cur + b1_cur);
                    y_pred = h * task_W2{t} + task_b2{t};
                    
                    residuals = y - y_pred;
                    dL_dy = -2/size(X,1) * residuals;
                    
                    dW2 = h' * dL_dy;
                    db2 = sum(dL_dy);
                    
                    dh = dL_dy * task_W2{t}';
                    dW1 = X' * (dh .* double(X*W1_cur+b1_cur > 0));
                    db1 = sum(dh .* double(X*W1_cur+b1_cur > 0), 1);
                    
                    grad_norm = sqrt(sum(dW1(:).^2)+sum(dW2(:).^2));
                    if grad_norm > 10
                        scale = 10/grad_norm;
                        dW1 = dW1*scale; dW2 = dW2*scale;
                        db1 = db1*scale; db2 = db2*scale;
                    end
                    
                    lr = config.learning_rate / (1 + 0.05*epoch);
                    task_W1{t} = task_W1{t} - lr*dW1;
                    task_b1{t} = task_b1{t} - lr*db1;
                    task_W2{t} = task_W2{t} - lr*dW2;
                    task_b2{t} = task_b2{t} - lr*db2;
                end
                
                result.total_parameters(t) = sum(arrayfun(@(x) numel(x), task_W1(1:t))) + ...
                    sum(arrayfun(@(x) numel(x), task_W2(1:t)));
                
                for eval_t = 1:length(tasks)
                    [X_eval, y_eval] = prepare_task_data(tasks{eval_t}, config);
                    
                    if eval_t <= t
                        h = max(0, X_eval * task_W1{eval_t} + task_b1{eval_t});
                        y_pred = h * task_W2{eval_t} + task_b2{eval_t};
                    else
                        h = max(0, X_eval * task_W1{t} + task_b1{t});
                        y_pred = h * task_W2{t} + task_b2{t};
                    end
                    
                    result.per_task_rmse(eval_t, t) = sqrt(mean((y_eval - y_pred).^2));
                end
            end
            
            result.avg_accuracy = mean(diag(result.per_task_rmse));
            result.backward_transfer = compute_bwt(result.per_task_rmse);
        end
        
        function result = ewc_ixer(tasks, config)
            % EWC-IXER (Ours): Full method with EWC + Experience Replay + Metacognitive
            result.name = 'EWC-IXER (Ours)';
            result.n_tasks = length(tasks);
            result.per_task_rmse = zeros(length(tasks), length(tasks));
            result.loss_curves = cell(length(tasks), 1);
            result.coverage = zeros(length(tasks), 1);
            result.metacognitive_signals = zeros(length(tasks), 1);
            result.adaptation_triggered = false(length(tasks), 1);
            
            W1 = randn(config.input_dim, config.hidden_dim) * 0.1;
            b1 = zeros(1, config.hidden_dim);
            W2 = randn(config.hidden_dim, 1) * 0.1;
            b2 = 0;
            
            fisher_matrices = {};
            optimal_weights = {};
            replay_buffer = struct('X', {}, 'y', {});
            
            for t = 1:length(tasks)
                [X, y] = prepare_task_data(tasks{t}, config);
                
                [W1, b1, W2, b2, losses, eta] = Baselines.train_ewc_ixer_full(...
                    W1, b1, W2, b2, X, y, fisher_matrices, optimal_weights, replay_buffer, config);
                result.loss_curves{t} = losses;
                result.metacognitive_signals(t) = eta;
                result.adaptation_triggered(t) = eta > config.meta_threshold;
                
                replay_buffer = add_to_buffer(replay_buffer, X, y, config.replay_size);
                
                fisher = compute_fisher(W1, b1, W2, b2, X, y);
                fisher_matrices{t} = fisher;
                optimal_weights{t} = struct('W1', W1, 'b1', b1, 'W2', W2, 'b2', b2);
                
                [~, ~, ~, cov] = conformal_prediction(W1, b1, W2, b2, X, y, config.conformal_alpha);
                result.coverage(t) = mean(cov);
                
                for eval_t = 1:length(tasks)
                    [X_eval, y_eval] = prepare_task_data(tasks{eval_t}, config);
                    y_pred = forward_pass(W1, b1, W2, b2, X_eval);
                    result.per_task_rmse(eval_t, t) = sqrt(mean((y_eval - y_pred).^2));
                end
            end
            
            result.avg_accuracy = mean(diag(result.per_task_rmse));
            result.backward_transfer = compute_bwt(result.per_task_rmse);
            result.avg_coverage = mean(result.coverage);
            result.n_adaptations = sum(result.adaptation_triggered);
        end
        
        function [W1, b1, W2, b2, losses, eta] = train_ewc_ixer_full(W1, b1, W2, b2, X, y, ...
                fisher_matrices, optimal_weights, replay_buffer, config)
            losses = zeros(config.epochs_per_task, 1);
            n = size(X, 1);
            
            for epoch = 1:config.epochs_per_task
                z1 = X*W1 + b1;
                h1 = max(0, z1);
                y_pred = h1*W2 + b2;
                
                residuals = y - y_pred;
                task_loss = mean(residuals.^2);
                
                ewc_loss = 0;
                for t = 1:length(fisher_matrices)
                    if ~isempty(fisher_matrices{t})
                        f = fisher_matrices{t};
                        o = optimal_weights{t};
                        ewc_loss = ewc_loss + sum(f.W1(:).*(W1(:)-o.W1(:)).^2) + sum(f.W2(:).*(W2(:)-o.W2(:)).^2);
                    end
                end
                ewc_loss = config.lambda_ewc * ewc_loss;
                
                replay_loss = 0;
                if ~isempty(replay_buffer)
                    X_r = cat(1, replay_buffer.X);
                    y_r = cat(1, replay_buffer.y);
                    h_r = max(0, X_r*W1 + b1);
                    y_pred_r = h_r*W2 + b2;
                    replay_loss = mean((y_r - y_pred_r).^2);
                end
                
                total_loss = task_loss + ewc_loss + 0.5*replay_loss;
                losses(epoch) = total_loss;
                
                dL_dy = -2/n * residuals;
                dW2 = h1' * dL_dy;
                db2 = sum(dL_dy);
                dh = dL_dy * W2';
                relu_grad = double(z1 > 0);
                dW1 = X' * (dh .* relu_grad);
                db1 = sum(dh .* relu_grad, 1);
                
                for t = 1:length(fisher_matrices)
                    if ~isempty(fisher_matrices{t})
                        f = fisher_matrices{t};
                        o = optimal_weights{t};
                        dW1 = dW1 + 2*config.lambda_ewc*f.W1.*(W1-o.W1);
                        dW2 = dW2 + 2*config.lambda_ewc*f.W2.*(W2-o.W2);
                    end
                end
                
                grad_norm = sqrt(sum(dW1(:).^2)+sum(dW2(:).^2));
                if grad_norm > 10
                    scale = 10/grad_norm;
                    dW1 = dW1*scale; dW2 = dW2*scale;
                    db1 = db1*scale; db2 = db2*scale;
                end
                
                lr = config.learning_rate / (1 + 0.05*epoch);
                W1 = W1 - lr*dW1;
                b1 = b1 - lr*db1;
                W2 = W2 - lr*dW2;
                b2 = b2 - lr*db2;
            end
            
            [~, ~, ~, coverage] = conformal_prediction(W1, b1, W2, b2, X, y, config.conformal_alpha);
            eta = abs(mean(coverage) - (1-config.conformal_alpha)) / (1-config.conformal_alpha);
        end
    end
end

function [X, y] = prepare_task_data(task_data, config)
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

function [W1, b1, W2, b2, losses] = train_basic(W1, b1, W2, b2, X, y, config)
    losses = zeros(config.epochs_per_task, 1);
    n = size(X, 1);
    
    for epoch = 1:config.epochs_per_task
        z1 = X*W1 + b1;
        h1 = max(0, z1);
        y_pred = h1*W2 + b2;
        residuals = y - y_pred;
        
        losses(epoch) = mean(residuals.^2);
        
        dL_dy = -2/n * residuals;
        dW2 = h1' * dL_dy;
        db2 = sum(dL_dy);
        dh = dL_dy * W2';
        relu_grad = double(z1 > 0);
        dW1 = X' * (dh .* relu_grad);
        db1 = sum(dh .* relu_grad, 1);
        
        grad_norm = sqrt(sum(dW1(:).^2)+sum(dW2(:).^2));
        if grad_norm > 10
            scale = 10/grad_norm;
            dW1 = dW1*scale; dW2 = dW2*scale;
            db1 = db1*scale; db2 = db2*scale;
        end
        
        lr = config.learning_rate / (1 + 0.05*epoch);
        W1 = W1 - lr*dW1;
        b1 = b1 - lr*db1;
        W2 = W2 - lr*dW2;
        b2 = b2 - lr*db2;
    end
end

function [W1, b1, W2, b2, losses] = train_with_replay(W1, b1, W2, b2, X, y, replay_buffer, config)
    losses = zeros(config.epochs_per_task, 1);
    n = size(X, 1);
    
    for epoch = 1:config.epochs_per_task
        z1 = X*W1 + b1;
        h1 = max(0, z1);
        y_pred = h1*W2 + b2;
        residuals = y - y_pred;
        task_loss = mean(residuals.^2);
        
        replay_loss = 0;
        if ~isempty(replay_buffer)
            X_r = cat(1, replay_buffer.X);
            y_r = cat(1, replay_buffer.y);
            h_r = max(0, X_r*W1 + b1);
            y_pred_r = h_r*W2 + b2;
            replay_loss = mean((y_r - y_pred_r).^2);
        end
        
        total_loss = task_loss + 0.5*replay_loss;
        losses(epoch) = total_loss;
        
        dL_dy = -2/n * residuals;
        dW2 = h1' * dL_dy;
        db2 = sum(dL_dy);
        dh = dL_dy * W2';
        relu_grad = double(z1 > 0);
        dW1 = X' * (dh .* relu_grad);
        db1 = sum(dh .* relu_grad, 1);
        
        grad_norm = sqrt(sum(dW1(:).^2)+sum(dW2(:).^2));
        if grad_norm > 10
            scale = 10/grad_norm;
            dW1 = dW1*scale; dW2 = dW2*scale;
            db1 = db1*scale; db2 = db2*scale;
        end
        
        lr = config.learning_rate / (1 + 0.05*epoch);
        W1 = W1 - lr*dW1;
        b1 = b1 - lr*db1;
        W2 = W2 - lr*dW2;
        b2 = b2 - lr*db2;
    end
end

function [W1, b1, W2, b2, losses] = train_with_ewc(W1, b1, W2, b2, X, y, fisher_matrices, optimal_weights, config)
    losses = zeros(config.epochs_per_task, 1);
    n = size(X, 1);
    
    for epoch = 1:config.epochs_per_task
        z1 = X*W1 + b1;
        h1 = max(0, z1);
        y_pred = h1*W2 + b2;
        residuals = y - y_pred;
        task_loss = mean(residuals.^2);
        
        ewc_loss = 0;
        for t = 1:length(fisher_matrices)
            if ~isempty(fisher_matrices{t})
                f = fisher_matrices{t};
                o = optimal_weights{t};
                ewc_loss = ewc_loss + sum(f.W1(:).*(W1(:)-o.W1(:)).^2) + sum(f.W2(:).*(W2(:)-o.W2(:)).^2);
            end
        end
        ewc_loss = config.lambda_ewc * ewc_loss;
        
        total_loss = task_loss + ewc_loss;
        losses(epoch) = total_loss;
        
        dL_dy = -2/n * residuals;
        dW2 = h1' * dL_dy;
        db2 = sum(dL_dy);
        dh = dL_dy * W2';
        relu_grad = double(z1 > 0);
        dW1 = X' * (dh .* relu_grad);
        db1 = sum(dh .* relu_grad, 1);
        
        for t = 1:length(fisher_matrices)
            if ~isempty(fisher_matrices{t})
                f = fisher_matrices{t};
                o = optimal_weights{t};
                dW1 = dW1 + 2*config.lambda_ewc*f.W1.*(W1-o.W1);
                dW2 = dW2 + 2*config.lambda_ewc*f.W2.*(W2-o.W2);
            end
        end
        
        grad_norm = sqrt(sum(dW1(:).^2)+sum(dW2(:).^2));
        if grad_norm > 10
            scale = 10/grad_norm;
            dW1 = dW1*scale; dW2 = dW2*scale;
            db1 = db1*scale; db2 = db2*scale;
        end
        
        lr = config.learning_rate / (1 + 0.05*epoch);
        W1 = W1 - lr*dW1;
        b1 = b1 - lr*db1;
        W2 = W2 - lr*dW2;
        b2 = b2 - lr*db2;
    end
end

function [W1, b1, W2, b2] = train_epoch_masked(W1, b1, W2, b2, masks, X, y, config)
    n = size(X, 1);
    W1_m = W1 .* masks.W1;
    b1_m = b1 .* masks.b1;
    W2_m = W2 .* masks.W2;
    b2_m = b2 .* masks.b2;
    
    z1 = X * W1_m + b1_m;
    h1 = max(0, z1);
    y_pred = h1 * W2_m + b2_m;
    residuals = y - y_pred;
    
    dL_dy = -2/n * residuals;
    dW2 = h1' * dL_dy;
    db2 = sum(dL_dy);
    dh = dL_dy * W2_m';
    relu_grad = double(z1 > 0);
    dW1 = X' * (dh .* relu_grad);
    db1 = sum(dh .* relu_grad, 1);
    
    grad_norm = sqrt(sum(dW1(:).^2)+sum(dW2(:).^2));
    if grad_norm > 10
        scale = 10/grad_norm;
        dW1 = dW1*scale; dW2 = dW2*scale;
        db1 = db1*scale; db2 = db2*scale;
    end
    
    lr = config.learning_rate / (1 + 0.05*config.epochs_per_task);
    W1 = W1 - lr*dW1.*masks.W1;
    b1 = b1 - lr*db1.*masks.b1;
    W2 = W2 - lr*dW2.*masks.W2;
    b2 = b2 - lr*db2.*masks.b2;
end

function [masks, pruned_ratio] = prune_weights(W1, b1, W2, b2, masks, prune_fraction)
    all_weights = [W1(:); W2(:)];
    threshold = prctile(abs(all_weights), prune_fraction*100);
    
    masks.W1 = masks.W1 .* (abs(W1) > threshold);
    masks.W2 = masks.W2 .* (abs(W2) > threshold);
    
    total = numel(W1) + numel(W2);
    remaining = sum(masks.W1(:)) + sum(masks.W2(:));
    pruned_ratio = 1 - remaining/total;
end

function buffer = add_to_buffer(buffer, X, y, max_size)
    n_add = min(20, size(X, 1));
    for i = 1:n_add
        if length(buffer) < max_size
            buffer(end+1) = struct('X', X(i, :), 'y', y(i));
        end
    end
end

function fisher = compute_fisher(W1, b1, W2, b2, X, y)
    y_pred = forward_pass(W1, b1, W2, b2, X);
    residuals = y - y_pred;
    mag = mean(residuals.^2);
    fisher.W1 = mag * ones(size(W1));
    fisher.b1 = mag * ones(size(b1));
    fisher.W2 = mag * ones(size(W2));
    fisher.b2 = mag;
end

function y_pred = forward_pass(W1, b1, W2, b2, X)
    h = max(0, X*W1 + b1);
    y_pred = h*W2 + b2;
end

function [y_pred, lower, upper, coverage] = conformal_prediction(W1, b1, W2, b2, X, y, alpha)
    n = size(X, 1);
    n_cal = floor(n/2);
    X_cal = X(1:n_cal, :);
    y_cal = y(1:n_cal);
    X_test = X(n_cal+1:end, :);
    y_test = y(n_cal+1:end);
    
    y_cal_pred = forward_pass(W1, b1, W2, b2, X_cal);
    residuals = abs(y_cal - y_cal_pred);
    q_hat = prctile(residuals, (1-alpha)*100);
    
    y_pred = forward_pass(W1, b1, W2, b2, X_test);
    lower = y_pred - q_hat;
    upper = y_pred + q_hat;
    coverage = (y_test >= lower) & (y_test <= upper);
end

function bwt = compute_bwt(per_task_rmse)
    n = size(per_task_rmse, 1);
    bwt = 0;
    count = 0;
    for t = 2:n
        for eval_t = 1:t-1
            bwt = bwt + per_task_rmse(eval_t, t) - per_task_rmse(eval_t, eval_t);
            count = count + 1;
        end
    end
    if count > 0
        bwt = bwt / count;
    end
end
