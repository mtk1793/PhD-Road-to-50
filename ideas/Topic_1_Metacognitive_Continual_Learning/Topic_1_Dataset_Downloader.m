%% Topic 1: Dataset Downloader for Smart Grid Real-Time Data
% Downloads and prepares the Smart Grid Real-Time Load Monitoring Dataset
% from IEEE DataPort or Kaggle
%
% Author: PhD Research
% Date: May 2026

clear; clc;

fprintf('📥 Smart Grid Dataset Downloader\n');
fprintf('================================\n');

%% ============================================================
% OPTION 1: Download from IEEE DataPort (requires login)
%% ============================================================
fprintf('\nOption 1: IEEE DataPort Dataset\n');
fprintf('URL: https://ieee-dataport.org/documents/smart-grid-real-time-load-monitoring-dataset\n');
fprintf('Size: 12.05 MB\n');
fprintf('Records: 50,000+ at 15-minute intervals\n');
fprintf('Features: Voltage, Current, Power, Solar/Wind, Temperature, Fault Indicators\n\n');

fprintf('To download:\n');
fprintf('1. Visit: https://ieee-dataport.org/documents/smart-grid-real-time-load-monitoring-dataset\n');
fprintf('2. Login to IEEE DataPort\n');
fprintf('3. Download smart_grid_dataset.csv\n');
fprintf('4. Place in: %s\n', pwd);

%% ============================================================
% OPTION 2: Download from Kaggle (requires Kaggle API)
%% ============================================================
fprintf('\n\nOption 2: Kaggle Dataset\n');
fprintf('URL: https://www.kaggle.com/datasets/ziya07/smart-grid-real-time-load-monitoring-dataset\n\n');

fprintf('To download via Kaggle API:\n');
fprintf('1. Install Kaggle CLI: pip install kaggle\n');
fprintf('2. Set up credentials: kaggle datasets download -d ziya07/smart-grid-real-time-load-monitoring-dataset\n');
fprintf('3. Unzip: unzip smart-grid-real-time-load-monitoring-dataset.zip\n');

%% ============================================================
% OPTION 3: Alternative Datasets
%% ============================================================
fprintf('\n\nOption 3: Alternative Real-Time Datasets\n\n');

fprintf('A. Liander2024 Energy Forecasting Benchmark (Hugging Face)\n');
fprintf('   URL: https://huggingface.co/datasets/OpenSTEF/liander2024-energy-forecasting-benchmark\n');
fprintf('   - 2024 data, 55 grid points, 15-min resolution\n');
fprintf('   - Includes weather data, solar/wind profiles\n');
fprintf('   - Download: huggingface-cli download OpenSTEF/liander2024-energy-forecasting-benchmark\n\n');

fprintf('B. Processed Distribution-Level Voltage Dataset (IEEE DataPort)\n');
fprintf('   URL: https://ieee-dataport.org/documents/processed-distribution-level-voltage-dataset-forecasting-and-state-classification\n');
fprintf('   - Real-world voltage measurements from Türkiye\n');
fprintf('   - Hourly data, multiple years\n');
fprintf('   - Perfect for voltage prediction tasks\n\n');

fprintf('C. Germany Quarter-Hourly Electricity Consumption (IEEE DataPort)\n');
fprintf('   URL: https://ieee-dataport.org/documents/germany-quarter-hourly-electricity-consumption-dataset-2015-2026\n');
fprintf('   - 2015-2026, 15-min resolution\n');
fprintf('   - Long-term time series for continual learning\n\n');

%% ============================================================
% AUTOMATED DOWNLOAD (if Kaggle CLI is available)
%% ============================================================
fprintf('\n\nAttempting automated download...\n');

% Check if kaggle CLI is available
[status, ~] = system('kaggle --version');
if status == 0
    fprintf('✅ Kaggle CLI detected. Downloading dataset...\n');
    
    % Download dataset
    cmd = 'kaggle datasets download -d ziya07/smart-grid-real-time-load-monitoring-dataset';
    [status, result] = system(cmd);
    
    if status == 0
        fprintf('✅ Dataset downloaded successfully!\n');
        
        % Unzip
        fprintf('📦 Extracting dataset...\n');
        unzip('smart-grid-real-time-load-monitoring-dataset.zip');
        fprintf('✅ Dataset extracted.\n');
        
        % Verify
        if exist('smart_grid_dataset.csv', 'file')
            fprintf('✅ Verification: smart_grid_dataset.csv found\n');
            data = readtable('smart_grid_dataset.csv');
            fprintf('   Records: %d\n', height(data));
            fprintf('   Columns: %s\n', strjoin(data.Properties.VariableNames, ', '));
        else
            fprintf('❌ Dataset file not found after extraction.\n');
        end
    else
        fprintf('❌ Download failed. Please download manually.\n');
        fprintf('Error: %s\n', result);
    end
else
    fprintf('⚠️  Kaggle CLI not found. Please download manually using one of the options above.\n');
    fprintf('   To install: pip install kaggle\n');
end

%% ============================================================
% DATASET VALIDATION
%% ============================================================
fprintf('\n🔍 Dataset Validation\n');
fprintf('====================\n');

dataset_file = 'smart_grid_dataset.csv';
if exist(dataset_file, 'file')
    data = readtable(dataset_file);
    
    fprintf('✅ Dataset loaded: %d records\n', height(data));
    fprintf('   Columns: %d\n', width(data));
    
    % Check required columns
    required_cols = {'Timestamp', 'Voltage', 'Current', 'Power', 'Solar', 'Wind', 'Temperature'};
    available_cols = data.Properties.VariableNames;
    
    fprintf('\n   Column Mapping:\n');
    for i = 1:length(required_cols)
        % Find similar column
        found = false;
        for col = available_cols
            if contains(lower(col), lower(required_cols{i}(1:4)))
                fprintf('   ✓ %s -> %s\n', required_cols{i}, col);
                found = true;
                break;
            end
        end
        if ~found
            fprintf('   ✗ %s -> Not found\n', required_cols{i});
        end
    end
    
    % Display sample
    fprintf('\n   Sample Data (first 5 rows):\n');
    disp(head(data, 5));
    
    % Basic statistics
    fprintf('\n   Basic Statistics:\n');
    numeric_data = data(:, vartype('numeric'));
    disp(summary(numeric_data));
    
else
    fprintf('❌ Dataset not found: %s\n', dataset_file);
    fprintf('   Please download manually and place in this directory.\n');
end

fprintf('\n✅ Dataset downloader complete!\n');
fprintf('Next step: Run Topic_1_Validation.m to validate the continual learning framework.\n');
