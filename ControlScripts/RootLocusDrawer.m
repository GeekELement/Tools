clear; clc; close all;

% ================= 用户配置区域 =================
mode_flag = 1;  % 【关键参数】设置为 0 画0度根轨迹，设置为 1 画180度根轨迹

% 定义 s 变量
s = tf('s');

% ================= 定义传递函数 =================
% 你的形式：1 + K * (M(s) / N(s))
% 请在下方定义 M(s) 和 N(s)
% 示例：M(s) = s + 2, N(s) = s * (s+1) * (s+3)
M_s = s + 2; 
N_s = s * (s + 1) * (s + 3); 

% 构建开环传递函数 G(s) = M(s)/N(s)
G = M_s / N_s; 

% ================= 绘图逻辑 =================
figure('Name', 'Root Locus Plot', 'Color', 'w', 'Position', [100, 100, 800, 600]);

if mode_flag == 1
    % --- 情况 1: 180度根轨迹 (常规负反馈) ---
    % 特征方程: 1 + K*G(s) = 0
    % 相角条件: ∠G(s) = ±180°
    rlocus(G);
    title(['180° Root Locus (Negative Feedback): $$1 + K \\frac{M(s)}{N(s)} = 0$$'], 'Interpreter', 'latex', 'FontSize', 14);
    
elseif mode_flag == 0
    % --- 情况 2: 0度根轨迹 (正反馈) ---
    % 特征方程: 1 - K*G(s) = 0  =>  1 + K*(-G(s)) = 0
    % 相角条件: ∠G(s) = 0°
    % 技巧: 对 -G(s) 绘制常规根轨迹，即可得到 G(s) 的0度根轨迹
    rlocus(-G);
    title(['0° Root Locus (Positive Feedback): $$1 - K \\frac{M(s)}{N(s)} = 0$$'], 'Interpreter', 'latex', 'FontSize', 14);
    
else
    error('错误: mode_flag 参数必须是 0 或 1');
end

% ================= 图形美化 =================
grid on;
sgrid; % 显示阻尼比和自然频率网格
xlabel('Real Axis (seconds^{-1})');
ylabel('Imaginary Axis (seconds^{-1})');

% 自动调整坐标轴以显示更多细节
axis auto; 