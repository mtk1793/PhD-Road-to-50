%% UncertaintyDecomposition - Epistemic vs Aleatoric Uncertainty
% Decomposes total prediction uncertainty into epistemic (model) and aleatoric (data) components
classdef UncertaintyDecomposition < handle
    methods (Static)
        function results = decompose_uncertainty(W1, b1, W2, b2, X_test, y_test, config)
            n = size(X_test, 1);
            
            [y_pred, aleatoric, epistemic, total, coverage] = ...
                UncertaintyDecomposition.mc_dropout_predict(W1, b1, W2, b2, X_test, config);
            
            rmse = sqrt(mean((y_test - y_pred).^2));
            calibration = abs(mean(coverage) - (1 - config.conformal_alpha));
            
            nll = UncertaintyDecomposition.negative_log_likelihood(y_test, y_pred, total);
            
            results.y_pred = y_pred;
            results.aleatoric = aleatoric;
            results.epistemic = epistemic;
            results.total = total;
            results.coverage = coverage;
            results.rmse = rmse;
            results.calibration = calibration;
            results.nll = nll;
            results.epistemic_ratio = mean(epistemic) / mean(total);
        end
        
        function [y_pred, aleatoric, epistemic, total, coverage] = mc_dropout_predict(W1, b1, W2, b2, X, config)
            n_mc = 30;
            n = size(X, 1);
            predictions = zeros(n, n_mc);
            dropout_rate = 0.1;
            
            for m = 1:n_mc
                mask1 = double(rand(size(b1)) > dropout_rate);
                mask2 = double(rand(size(b2)) > dropout_rate);
                
                W1_drop = W1;
                b1_drop = b1 .* mask1;
                
                z1 = X * W1_drop + b1_drop;
                h1 = max(0, z1) .* mask1;
                y_pred = h1 * W2 + b2 * mask2;
                
                predictions(:, m) = y_pred;
            end
            
            y_pred = mean(predictions, 2);
            
            epistemic = var(predictions, 0, 2);
            
            residuals = bsxfun(@minus, predictions, y_pred);
            aleatoric = mean(residuals.^2, 2);
            
            total = epistemic + aleatoric;
            
            std_total = sqrt(total);
            q_hat = prctile(std_total, (1-config.conformal_alpha)*100);
            coverage = (y_pred - 1.96*std_total <= 0) & (y_pred + 1.96*std_total >= 0);
        end
        
        function nll = negative_log_likelihood(y_true, y_pred, variance)
            variance = max(variance, 1e-10);
            nll = 0.5 * mean(log(2*pi*variance) + (y_true - y_pred).^2 ./ variance);
        end
        
        function plot_uncertainty(results, output_path)
            figure('Position', [100, 100, 1200, 400]);
            
            n = min(100, length(results.y_pred));
            idx = 1:n;
            
            subplot(1, 3, 1);
            plot(idx, results.y_pred(idx), 'b-', 'LineWidth', 2); hold on;
            fill([idx, fliplr(idx)], ...
                [results.y_pred(idx)-1.96*sqrt(results.total(idx)); ...
                 fliplr(results.y_pred(idx)+1.96*sqrt(results.total(idx)))], ...
                'b', 'FaceAlpha', 0.2, 'EdgeColor', 'none');
            plot(idx, results.aleatoric(idx), 'r--', 'LineWidth', 1.5);
            legend('Prediction', '95% CI', 'Aleatoric Unc.');
            title('Predictions with Uncertainty');
            grid on;
            
            subplot(1, 3, 2);
            scatter(results.epistemic(1:end), results.aleatoric(1:end), 10, 'filled');
            xlabel('Epistemic Uncertainty');
            ylabel('Aleatoric Uncertainty');
            title('Epistemic vs Aleatoric');
            grid on;
            
            subplot(1, 3, 3);
            pie([mean(results.epistemic), mean(results.aleatoric)]);
            title(sprintf('Uncertainty Ratio\nEpistemic: %.1f%%', results.epistemic_ratio*100));
            
            if nargin > 1
                saveas(gcf, output_path);
            end
        end
    end
end
