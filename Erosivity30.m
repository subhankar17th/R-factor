% The funcation takes the rainfall intensity (mm/hour) from the sattelite datasets for
% event based rainfall erosviity estimation.

function EI = Erosivity30(Prc)

    % Scale 30-minute intensity to precipitation values
    prc = Prc .* 0.5;
    flag = 1;
    while flag >= 1
        
        % Compute the moving sum of the precipitation values over a window of 12
        result = movsum(prc, 12, 'Endpoints', 'fill');
        
        % Identify indices where the moving sum exceeds 1.27
        idx = (result > 1.27);
        idx = squeeze(idx)';
        
        % Find start and end of sequences where condition is met
        idx1 = strfind([0, idx, 0], [0, 1]);
        idx2 = strfind([0, idx, 0], [1, 0]) - 1;
        if isempty(idx1) == 1
            
            % If no sequences found, assign NaN to EI and exit loop
            EI(flag) = nan;
            flag = 0;
        else
            
            % Otherwise, process the first sequence
            idx11 = idx1(1);
            idx12 = idx2(1);
            
            % Check if the sum or the max in the extended window exceeds thresholds
            ii = sum(prc(1, 1, idx11 - 6 : idx12 + 5), 3) > 12.7 || max(prc(1, 1, idx11 - 6 : idx12 + 5)) > 12.7;
            ii = logical(ii);
            if ii == 0
                
                % If condition not met, assign NaN to EI
                EI(flag) = nan;
            else
                
                % Extract relevant precipitation values
                out = arrayfun(@(x, y) prc((x - 6):(y + 5)), idx11(ii), idx12(ii), 'un', 0);
                out1 = cell(1, size(out, 2));
                out1{1, 1} = squeeze(out{1, 1});
                
                % Calculate the erosivity factors
                out2 = cellfun(@(x) (0.29 * (1 - 0.72 * (exp(-0.082 * (x .* 2))))), out1, 'UniformOutput', false);
                ev = cellfun(@(p, q) (p .* q), out1, out2, 'UniformOutput', false);
                i30 = cellfun(@(y) (max(y .* 2)), out1, 'UniformOutput', false);
                
                % Calculate the event erosivity
                Ei30 = cellfun(@(s, t) (s .* t), ev, i30, 'UniformOutput', false);
                Eievnt = cellfun(@(c) sum(c, 1), Ei30, 'UniformOutput', false);
                Eievnt = [Eievnt{:}];
                
                % Store the event erosivity in EI
                EI(flag) = Eievnt;
            end
            
            % Mark the processed part of the precipitation array as NaN
            prc(1:idx12 + 5) = nan;
            flag = flag + 1;
        end
    end
end
