function EI = Erosivity60(Prc)
    prc = Prc .* 1000;
    flag = 1;
    while(flag >= 1)
        result = movsum(prc, 6, 'Endpoints', 'fill');
        idx = (result > 0);
        idx = (squeeze(idx))';
        idx1 = (strfind([0, idx, 0], [0, 1]));
        idx2 = (strfind([0, idx, 0], [1, 0]) - 1);
        if isempty(idx1) == 1
            EI(flag) = nan;
            flag = 0;
        else
            idx11 = idx1(1);
            idx12 = idx2(1);
            ii = sum(prc(1, 1, idx11 - 3:idx12 + 2), 3) > 12.7 || max(prc(1, 1, idx11 - 3:idx12 + 2)) > 24.5;
            ii = logical(ii);
            if ii == 0
                EI(flag) = nan;
            else
                out = arrayfun(@(x, y) prc((x - 3):(y + 2)), idx11(ii), idx12(ii), 'un', 0);
                out1 = cell(1, size(out, 2));
                out1{1, 1} = squeeze(out{1, 1});
                out2 = cellfun(@(x) (0.29 * (1 - 0.72 * (exp(-0.082 * (x))))), out1, 'UniformOutput', false);
                ev = cellfun(@(p, q) (p .* q), out1, out2, 'UniformOutput', false);
                i30 = cellfun(@(y) (max(y)), out1, 'UniformOutput', false);
                Ei30 = cellfun(@(s, t) (s .* t), ev, i30, 'UniformOutput', false);
                Eievnt = cellfun(@(c) sum(c, 1), Ei30, 'UniformOutput', false);
                Eievnt = [Eievnt{:}];
                EI(flag) = Eievnt;
            end
            prc(1:idx12 + 2) = nan;
            flag = flag + 1;
        end
    end
end
