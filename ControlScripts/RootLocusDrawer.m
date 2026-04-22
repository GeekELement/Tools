clear; clc; close all;

s = tf('s');
K = 1;  % 这里的K只是一个占位符，rlocus会自动变化它

% 定义开环传递函数 G(s) = K * N(s)/D(s)
G = K / (s * (s^2 + 9 * s + 18));  % 示例，请替换成您的传函

% 绘制根轨迹（K: 0 → +∞）
figure;
rlocus(G);
title('Root Locus of $$ K \cdot G(s) $$', 'Interpreter', 'latex');
xlabel('Real Axis');
ylabel('Imaginary Axis');
grid on;
