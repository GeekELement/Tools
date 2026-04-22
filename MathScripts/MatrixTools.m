clc; clear; close all;

% ================= 用户输入区域 =================
% 在这里直接输入你的纯数字方阵
A = [6,  4,   4;
     0,    0,   -1;
     -6,   -5,  -4];
% ===============================================

[n, m] = size(A);

% 检查是否为方阵
if n ~= m
    error('错误：矩阵必须是方阵才能进行此分析。');
end

disp('================ 矩阵分析结果 ================');
disp('输入矩阵 A:');
disp(A);

% --- 1. 计算行列式 ---
detA = det(A);
fprintf('1. 矩阵的行列式:\n');
fprintf('   det(A) = %.4f\n', detA);

% --- 2. 计算特征值 ---
eigenvalues = eig(A);
fprintf('\n2. 矩阵的特征值:\n');
for i = 1:length(eigenvalues)
    % 判断是否为实数，如果是复数则显示复数格式
    if isreal(eigenvalues(i))
        fprintf('   λ%d = %.4f\n', i, real(eigenvalues(i)));
    else
        fprintf('   λ%d = %.4f + %.4fi\n', i, real(eigenvalues(i)), imag(eigenvalues(i)));
    end
end

% --- 3. 计算伴随矩阵 ---
% 伴随矩阵 = 代数余子式矩阵的转置
adjA = zeros(n);
for i = 1:n
    for j = 1:n
        % 构造余子式矩阵 (删除第i行第j列)
        rows = [1:i-1, i+1:n];
        cols = [1:j-1, j+1:n];
        
        % 处理边界情况（当i或j为1或n时，索引向量可能为空，MATLAB会自动处理，但需确保逻辑正确）
        if isempty(rows) || isempty(cols)
             subM = []; 
        else
             subM = A(rows, cols);
        end
        
        % 计算代数余子式，注意伴随矩阵需要转置，所以赋值给 adjA(j,i)
        adjA(j,i) = (-1)^(i+j) * det(subM);
    end
end

fprintf('\n3. 矩阵的伴随矩阵:\n');
disp(adjA);

% --- 4. 计算逆矩阵 ---
fprintf('4. 矩阵的逆:\n');
% 判断行列式是否为0 (使用极小值作为阈值以应对浮点数误差)
if abs(detA) < 1e-10
    disp('   逆矩阵不存在 (矩阵是奇异矩阵，行列式为 0)。');
else
    invA = inv(A);
    disp(invA);
end

disp('================ 分析结束 ================');