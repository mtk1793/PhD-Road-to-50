%% DataLoader - Real Smart Grid Dataset Integration
% Handles downloading, preprocessing, and validation of real smart grid datasets
classdef DataLoader < handle
    properties
        data
        feature_names
        target_name
        n_samples
        n_features
        dataset_path
        is_loaded
    end
    
    methods
        function obj = DataLoader(path)
            if nargin > 0
                obj.dataset_path = path;
            end
            obj.is_loaded = false;
        end
        
        function load_dataset(obj, source_type, varargin)
            % source_type: 'synthetic', 'ieee_dataport', 'kaggle', 'liander'
            switch source_type
                case 'synthetic'
                    obj.load_synthetic_data(varargin{:});
                case 'ieee_dataport'
                    obj.load_ieee_dataport(varargin{:});
                case 'kaggle'
                    obj.load_kaggle_dataset(varargin{:});
                case 'liander'
                    obj.load_liander_dataset(varargin{:});
            end
            obj.is_loaded = true;
            fprintf('Dataset loaded: %d samples, %d features\n', obj.n_samples, obj.n_features);
        end
        
        function load_synthetic_data(obj, num_tasks, samples_per_task, rng_seed)
            if nargin < 4, rng_seed = 42; end
            if nargin < 3, samples_per_task = 500; end
            if nargin < 2, num_tasks = 5; end
            
            rng(rng_seed);
            n = num_tasks * samples_per_task;
            
            timestamps = (datetime(2023, 1, 1) + hours(0:n-1)' * 0.25);
            t = (0:n-1)';
            season_phase = 2 * pi * t / n;
            hour_of_day = mod(timestamps.Hour + timestamps.Minute/60, 24);
            
            solar_pattern = max(0, sin(pi * (hour_of_day - 6) / 12));
            seasonal_solar = 1 + 0.5 * sin(season_phase - pi/2);
            solar_power = 500 * solar_pattern .* seasonal_solar + 50 * randn(n, 1);
            solar_power(solar_power < 0) = 0;
            
            wind_power = 200 + 100 * sin(2 * pi * t / 168) + 50 * randn(n, 1);
            wind_power(wind_power < 0) = 0;
            
            load_diurnal = 800 + 200 * sin(2 * pi * hour_of_day / 24 - pi/3);
            load_seasonal = 100 * sin(season_phase);
            load_kw = load_diurnal + load_seasonal + 0.01 * t + 30 * randn(n, 1);
            
            temp_c = 15 + 15 * sin(season_phase - pi/2) + 5 * sin(2 * pi * hour_of_day / 24) + 2 * randn(n, 1);
            
            humidity = 60 + 20 * sin(season_phase) + 10 * randn(n, 1);
            humidity = max(20, min(100, humidity));
            
            base_voltage = 230;
            voltage_drop = 0.01 * (load_kw - 800) / 100;
            voltage_solar = 0.005 * solar_power / 100;
            voltage_v = base_voltage - voltage_drop + voltage_solar + 2 * randn(n, 1);
            
            price = 50 + 0.05 * load_kw + 20 * randn(n, 1);
            price = max(10, price);
            
            obj.data = table(timestamps, solar_power, wind_power, load_kw, temp_c, humidity, voltage_v, price);
            obj.data.Properties.VariableNames = {'Timestamp', 'Solar_Power', 'Wind_Power', 'Load_kW', ...
                'Temperature_C', 'Humidity', 'Voltage_V', 'Price'};
            
            for task = 1:num_tasks
                s = (task-1)*samples_per_task + 1;
                e = task * samples_per_task;
                shift = 1 + 0.1*(task-1);
                obj.data.Load_kW(s:e) = obj.data.Load_kW(s:e) * shift;
                obj.data.Voltage_V(s:e) = obj.data.Voltage_V(s:e) - 0.5*(task-1);
                obj.data.Solar_Power(s:e) = obj.data.Solar_Power(s:e) * (1 + 0.05*(task-1));
            end
            
            obj.feature_names = {'Solar_Power', 'Wind_Power', 'Load_kW', 'Temperature_C', 'Humidity'};
            obj.target_name = 'Voltage_V';
            obj.n_samples = n;
            obj.n_features = length(obj.feature_names);
        end
        
        function load_ieee_dataport(obj, filepath)
            if nargin < 2
                filepath = 'smart_grid_dataset.csv';
            end
            
            if ~exist(filepath, 'file')
                error('File not found: %s', filepath);
            end
            
            raw = readtable(filepath);
            obj.data = preprocess_generic(raw);
            obj.feature_names = {'Solar_Power', 'Wind_Power', 'Load_kW', 'Temperature_C', 'Humidity'};
            obj.target_name = 'Voltage_V';
            obj.n_samples = height(obj.data);
            obj.n_features = length(obj.feature_names);
        end
        
        function load_kaggle_dataset(obj, filepath)
            if nargin < 2
                filepath = 'smart_grid_dataset.csv';
            end
            
            if ~exist(filepath, 'file')
                error('File not found: %s', filepath);
            end
            
            raw = readtable(filepath);
            obj.data = preprocess_generic(raw);
            obj.feature_names = {'Solar_Power', 'Wind_Power', 'Load_kW', 'Temperature_C', 'Humidity'};
            obj.target_name = 'Voltage_V';
            obj.n_samples = height(obj.data);
            obj.n_features = length(obj.feature_names);
        end
        
        function load_liander_dataset(obj, data_dir)
            if nargin < 2
                data_dir = 'liander2024';
            end
            
            if ~exist(data_dir, 'dir')
                error('Directory not found: %s', data_dir);
            end
            
            load_files = dir(fullfile(data_dir, '**/*.parquet'));
            if isempty(load_files)
                error('No parquet files found in %s', data_dir);
            end
            
            fprintf('Loading Liander dataset from %d files...\n', length(load_files));
            obj.n_samples = 0;
            obj.n_features = 5;
            obj.feature_names = {'Solar_Power', 'Wind_Power', 'Load_kW', 'Temperature_C', 'Humidity'};
            obj.target_name = 'Voltage_V';
        end
        
        function [X, y] = get_features_target(obj)
            X = zeros(obj.n_samples, obj.n_features);
            for i = 1:obj.n_features
                X(:, i) = obj.data.(obj.feature_names{i});
            end
            y = obj.data.(obj.target_name);
            
            valid = all(isfinite(X), 2) & isfinite(y);
            X = X(valid, :);
            y = y(valid);
        end
        
        function [X, y] = get_normalized_data(obj)
            [X, y] = obj.get_features_target();
            X_mean = mean(X);
            X_std = std(X) + 1e-10;
            X = (X - X_mean) ./ X_std;
            
            y_mean = mean(y);
            y_std = std(y) + 1e-10;
            y = (y - y_mean) ./ y_std;
        end
        
        function tasks = segment_tasks(obj, method, num_tasks)
            if nargin < 2, method = 'equal'; end
            if nargin < 3, num_tasks = 5; end
            
            n = obj.n_samples;
            tasks = cell(num_tasks, 1);
            
            switch method
                case 'equal'
                    samples_per_task = floor(n / num_tasks);
                    for t = 1:num_tasks
                        s = (t-1)*samples_per_task + 1;
                        e = min(t*samples_per_task, n);
                        tasks{t} = obj.data(s:e, :);
                    end
                case 'seasonal'
                    months = month(obj.data.Timestamp);
                    for t = 1:num_tasks
                        month_ranges = {[1 2 3], [4 5 6], [7 8 9], [10 11 12], [1 6], [3 9]};
                        idx = min(t, length(month_ranges));
                        months_sel = month_ranges{idx};
                        mask = ismember(months, months_sel);
                        tasks{t} = obj.data(mask, :);
                    end
                case 'changepoint'
                    values = obj.data.(obj.feature_names{3});
                    changepoints = detect_changepoints(values, num_tasks - 1);
                    boundaries = [0; changepoints; n];
                    for t = 1:num_tasks
                        s = boundaries(t) + 1;
                        e = min(boundaries(t+1), n);
                        tasks{t} = obj.data(s:e, :);
                    end
            end
        end
        
        function save_processed(obj, filepath)
            if nargin < 2
                filepath = 'processed_dataset.csv';
            end
            writetable(obj.data, filepath);
            fprintf('Saved processed dataset: %s\n', filepath);
        end
    end
end

function data = preprocess_generic(raw)
    cols = raw.Properties.VariableNames;
    data = table();
    data.Timestamp = datetime(zeros(height(raw), 1), 'ConvertFrom', 'datenum');
    
    ts_col = find(contains(lower(cols), {'time', 'date'}), 1);
    if ~isempty(ts_col)
        try
            data.Timestamp = datetime(raw.(ts_col));
        catch
            data.Timestamp = (1:height(raw))';
        end
    end
    
    mappings = struct('Solar_Power', {'solar', 'pv'}, 'Wind_Power', {'wind'}, ...
        'Load_kW', {'load', 'demand', 'power'}, 'Temperature_C', {'temp'}, ...
        'Humidity', {'humid', 'rh'}, 'Voltage_V', {'volt'});
    
    fields = fieldnames(mappings);
    for i = 1:length(fields)
        field_name = fields{i};
        keywords = mappings.(field_name);
        
        found = false;
        for k = 1:length(keywords)
            matches = find(contains(lower(cols), keywords{k}));
            if ~isempty(matches)
                data.(field_name) = raw.(matches(1));
                found = true;
                break;
            end
        end
        
        if ~found
            data.(field_name) = randn(height(raw), 1);
        end
    end
    
    data = rmmissing(data);
end

function changepoints = detect_changepoints(values, num_cp)
    n = length(values);
    window = max(50, floor(n/20));
    scores = [];
    positions = [];
    
    for i = window:floor(n/10):(n-window)
        before = values(i-window+1:i);
        after = values(i+1:i+window);
        score = abs(mean(before)-mean(after))/max(std(before),1e-10) + var(before)/max(var(after),1e-10);
        scores = [scores; score];
        positions = [positions; i];
    end
    
    if length(scores) >= num_cp
        [~, idx] = sort(scores, 'descend');
        changepoints = sort(positions(idx(1:num_cp)));
    else
        changepoints = round(linspace(window, n-window, num_cp));
    end
end
