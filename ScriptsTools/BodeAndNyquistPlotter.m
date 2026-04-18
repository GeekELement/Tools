% 定义 s
s = tf('s');

% ========== 在这里输入你的传递函数 G(s) = ... ==========
% 示例（请删除或注释掉示例，替换为你自己的）：
% G = 20*(0.23*s + 1) / (s * (0.5*s + 1) * (0.05*s + 1));

G = 20*(0.23*s + 1)/(s*(0.5*s + 1)*(0.05*s + 1));  % ←←← 在等号右边填写你的传递函数，例如：20*(0.23*s + 1)/(s*(0.5*s + 1)*(0.05*s + 1))

% ========== 自动计算并输出结果 ==========
[GM, PM, Wcg, Wcp] = margin(G);
GM_dB = 20*log10(GM);

fprintf('相角裕度 PM = %.2f deg\n', PM);
fprintf('幅值裕度 GM = %.4f (%.2f dB)\n', GM, GM_dB);
fprintf('增益穿越频率 wc = %.4f rad/s\n', Wcp);
fprintf('相位穿越频率 wg = %.4f rad/s\n', Wcg);

figure;
margin(G); grid on; % 绘制Bode图
title('Bode Diagram');

figure;
nyquist(G); grid on; % 绘制Nyquist图
title('Nyquist Diagram');