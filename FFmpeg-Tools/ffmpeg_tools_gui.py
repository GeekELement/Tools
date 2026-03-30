import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import os
import threading


class FFmpegToolsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("FFmpeg 工具箱")
        self.root.geometry("900x700")
        self.root.minsize(900, 700)
        self.root.configure(bg='#f5f5f5')

        # ==========================================
        # 在这里修改 FFmpeg 路径
        # ==========================================
        self.ffmpeg_path = r"D:\Apps\ffmpeg\bin\ffmpeg.exe"

        # 配色方案
        self.colors = {
            'primary': '#2196F3',
            'secondary': '#757575',
            'success': '#4CAF50',
            'danger': '#f44336',
            'warning': '#FF9800',
            'bg': '#f5f5f5',
            'card': '#ffffff',
            'text': '#212121'
        }

        # 设置样式
        self.setup_styles()

        # 创建主容器
        self.main_container = tk.Frame(root, bg=self.colors['bg'])
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # 创建标题栏
        self.create_header()

        # 创建内容区域
        self.create_content()

        # 创建状态栏
        self.create_statusbar()

        # 检查ffmpeg
        self.check_ffmpeg()

    def setup_styles(self):
        """设置自定义样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # 按钮样式
        self.style.configure('Primary.TButton',
                           font=('微软雅黑', 10, 'bold'),
                           foreground='white',
                           background=self.colors['primary'],
                           padding=(20, 8))
        self.style.map('Primary.TButton',
                      background=[('active', '#1976D2'), ('pressed', '#1565C0')])

        self.style.configure('Secondary.TButton',
                           font=('微软雅黑', 9),
                           foreground=self.colors['text'],
                           background='#e0e0e0',
                           padding=(15, 6))
        self.style.map('Secondary.TButton',
                      background=[('active', '#bdbdbd'), ('pressed', '#9e9e9e')])

        # 标签样式
        self.style.configure('Title.TLabel',
                           font=('微软雅黑', 16, 'bold'),
                           foreground=self.colors['text'],
                           background=self.colors['bg'])

        self.style.configure('Subtitle.TLabel',
                           font=('微软雅黑', 11),
                           foreground=self.colors['secondary'],
                           background=self.colors['bg'])

        self.style.configure('CardTitle.TLabel',
                           font=('微软雅黑', 12, 'bold'),
                           foreground=self.colors['text'])

        # 框架样式
        self.style.configure('Card.TFrame', background=self.colors['card'])
        self.style.configure('Card.TLabelframe', background=self.colors['card'])
        self.style.configure('Card.TLabelframe.Label',
                           font=('微软雅黑', 11, 'bold'),
                           foreground=self.colors['primary'])

        # 输入框样式
        self.style.configure('Custom.TEntry', padding=8)

        # 标签页样式
        self.style.configure('Custom.TNotebook', background=self.colors['bg'])
        self.style.configure('Custom.TNotebook.Tab',
                           font=('微软雅黑', 10),
                           padding=(15, 8))

    def create_header(self):
        """创建标题栏"""
        header = tk.Frame(self.main_container, bg=self.colors['primary'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title = tk.Label(header, text="FFmpeg 工具箱",
                        font=('微软雅黑', 18, 'bold'),
                        fg='white', bg=self.colors['primary'])
        title.pack(side=tk.LEFT, padx=20, pady=10)

        subtitle = tk.Label(header, text="音视频处理工具",
                           font=('微软雅黑', 10),
                           fg='#E3F2FD', bg=self.colors['primary'])
        subtitle.pack(side=tk.LEFT, padx=5, pady=15)

        # 关于按钮
        about_btn = tk.Label(header, text="?",
                            font=('微软雅黑', 12, 'bold'),
                            fg='white', bg=self.colors['primary'],
                            cursor='hand2', width=3)
        about_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        about_btn.bind('<Button-1>', lambda e: self.show_about())

    def create_content(self):
        """创建内容区域"""
        content = tk.Frame(self.main_container, bg=self.colors['bg'])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 左侧功能区
        left_panel = tk.Frame(content, bg=self.colors['bg'])
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建标签页
        self.notebook = ttk.Notebook(left_panel, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 创建各个功能页面
        self.create_video_concat_tab()
        self.create_audio_extract_tab()
        self.create_audio_transcode_tab()
        self.create_av_merge_tab()
        self.create_video_transcode_tab()
        self.create_image_to_video_tab()

        # 右侧日志区
        right_panel = tk.Frame(content, bg=self.colors['bg'], width=350)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(15, 0))
        right_panel.pack_propagate(False)

        self.create_log_panel(right_panel)

    def create_log_panel(self, parent):
        """创建日志面板"""
        # 日志标题
        log_title = tk.Frame(parent, bg=self.colors['card'], height=40)
        log_title.pack(fill=tk.X, pady=(0, 10))
        log_title.pack_propagate(False)

        tk.Label(log_title, text="运行日志",
                font=('微软雅黑', 12, 'bold'),
                fg=self.colors['primary'], bg=self.colors['card']).pack(side=tk.LEFT, padx=15, pady=8)

        # 清空按钮
        clear_btn = tk.Label(log_title, text="清空",
                            font=('微软雅黑', 9),
                            fg=self.colors['secondary'], bg=self.colors['card'],
                            cursor='hand2')
        clear_btn.pack(side=tk.RIGHT, padx=15, pady=10)
        clear_btn.bind('<Button-1>', lambda e: self.clear_log())

        # 日志文本框
        log_frame = tk.Frame(parent, bg=self.colors['card'])
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=('Consolas', 10),
            bg='#fafafa',
            fg=self.colors['text'],
            insertbackground=self.colors['primary'],
            relief=tk.FLAT,
            padx=10,
            pady=10,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 配置日志颜色标签
        self.log_text.tag_config('success', foreground=self.colors['success'])
        self.log_text.tag_config('error', foreground=self.colors['danger'])
        self.log_text.tag_config('warning', foreground=self.colors['warning'])
        self.log_text.tag_config('info', foreground=self.colors['primary'])

    def create_statusbar(self):
        """创建状态栏"""
        statusbar = tk.Frame(self.main_container, bg=self.colors['card'], height=30)
        statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        statusbar.pack_propagate(False)

        self.status_label = tk.Label(statusbar, text="就绪",
                                    font=('微软雅黑', 9),
                                    fg=self.colors['secondary'],
                                    bg=self.colors['card'])
        self.status_label.pack(side=tk.LEFT, padx=15, pady=5)

        # FFmpeg状态指示器
        self.ffmpeg_indicator = tk.Label(statusbar, text="● FFmpeg",
                                        font=('微软雅黑', 9),
                                        fg=self.colors['secondary'],
                                        bg=self.colors['card'])
        self.ffmpeg_indicator.pack(side=tk.RIGHT, padx=15, pady=5)

    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)

    def log(self, message, level='info'):
        """添加日志"""
        self.log_text.insert(tk.END, message + "\n", level)
        self.log_text.see(tk.END)

    def check_ffmpeg(self):
        """检查FFmpeg是否可用"""
        try:
            result = subprocess.run([self.ffmpeg_path, '-version'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                self.log(f"✓ FFmpeg 可用", 'success')
                self.log(f"  {version}", 'info')
                self.ffmpeg_indicator.config(fg=self.colors['success'])
                self.status_label.config(text="FFmpeg 已就绪")
                return True
            else:
                self.log("✗ FFmpeg 返回错误", 'error')
                self.ffmpeg_indicator.config(fg=self.colors['danger'])
                return False
        except FileNotFoundError:
            self.log(f"✗ FFmpeg 未找到: {self.ffmpeg_path}", 'error')
            self.ffmpeg_indicator.config(fg=self.colors['danger'])
            self.status_label.config(text="FFmpeg 未找到")
            return False
        except Exception as e:
            self.log(f"✗ 检查 FFmpeg 时出错: {str(e)}", 'error')
            self.ffmpeg_indicator.config(fg=self.colors['danger'])
            return False

    def show_about(self):
        messagebox.showinfo("关于",
                           "FFmpeg 工具箱 v1.0\n\n"
                           "基于 FFmpeg 的音视频处理工具\n"
                           "支持视频拼接、音频提取、格式转换等功能")

    def run_ffmpeg(self, command, success_msg="操作完成"):
        def execute():
            try:
                self.status_label.config(text="正在处理...")
                ffmpeg_cmd = [self.ffmpeg_path] + command[1:]
                self.log(f"执行: {' '.join(ffmpeg_cmd[:5])}...", 'info')

                process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate()

                if process.returncode == 0:
                    self.log(f"✓ {success_msg}", 'success')
                    self.status_label.config(text="处理完成")
                    messagebox.showinfo("成功", success_msg)
                else:
                    self.log(f"✗ 错误: {stderr[:200]}", 'error')
                    self.status_label.config(text="处理失败")
                    messagebox.showerror("错误", f"操作失败:\n{stderr[:500]}")
            except Exception as e:
                self.log(f"✗ 异常: {str(e)}", 'error')
                self.status_label.config(text="发生异常")
                messagebox.showerror("错误", f"发生异常: {str(e)}")

        thread = threading.Thread(target=execute)
        thread.start()

    # ========== 创建卡片式布局的辅助方法 ==========
    def create_card(self, parent, title):
        """创建卡片容器"""
        card = tk.Frame(parent, bg=self.colors['card'], relief=tk.FLAT,
                       bd=1, highlightbackground='#e0e0e0', highlightthickness=1)

        if title:
            title_frame = tk.Frame(card, bg=self.colors['card'], height=40)
            title_frame.pack(fill=tk.X, padx=15, pady=(10, 0))
            title_frame.pack_propagate(False)

            tk.Label(title_frame, text=title,
                    font=('微软雅黑', 12, 'bold'),
                    fg=self.colors['primary'], bg=self.colors['card']).pack(side=tk.LEFT)

        return card

    def create_file_selector(self, parent, label, button_text="选择文件", command=None):
        """创建文件选择器"""
        frame = tk.Frame(parent, bg=self.colors['card'])
        frame.pack(fill=tk.X, padx=15, pady=8)

        tk.Label(frame, text=label,
                font=('微软雅黑', 10),
                fg=self.colors['text'], bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        entry = tk.Entry(frame, font=('微软雅黑', 10),
                        bg='#fafafa', relief=tk.SOLID, bd=1,
                        highlightbackground='#e0e0e0', highlightthickness=1)
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))

        btn = tk.Button(frame, text=button_text,
                       font=('微软雅黑', 9),
                       bg=self.colors['primary'], fg='white',
                       activebackground='#1976D2', relief=tk.FLAT,
                       cursor='hand2', command=command)
        btn.pack(side=tk.RIGHT)

        return entry

    def create_action_button(self, parent, text, command, color=None):
        """创建操作按钮"""
        color = color or self.colors['primary']
        btn = tk.Button(parent, text=text,
                       font=('微软雅黑', 11, 'bold'),
                       bg=color, fg='white',
                       activebackground='#1976D2' if color == self.colors['primary'] else color,
                       relief=tk.FLAT, cursor='hand2',
                       padx=30, pady=10, command=command)
        return btn

    # ========== 视频拼接 ==========
    def create_video_concat_tab(self):
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text=" 视频拼接 ")

        # 主卡片
        card = self.create_card(tab, "视频列表")
        card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 列表区域
        list_frame = tk.Frame(card, bg=self.colors['card'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # 使用Treeview替代Listbox
        columns = ('序号', '文件名', '路径')
        self.video_tree = ttk.Treeview(list_frame, columns=columns,
                                       show='headings', height=10)
        self.video_tree.heading('序号', text='#')
        self.video_tree.heading('文件名', text='文件名')
        self.video_tree.heading('路径', text='路径')
        self.video_tree.column('序号', width=40, anchor='center')
        self.video_tree.column('文件名', width=200)
        self.video_tree.column('路径', width=300)
        self.video_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                  command=self.video_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.video_tree.config(yscrollcommand=scrollbar.set)

        # 按钮区域
        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Button(btn_frame, text="+ 添加视频",
                 font=('微软雅黑', 9), bg='#E3F2FD', fg=self.colors['primary'],
                 relief=tk.FLAT, cursor='hand2',
                 command=self.add_video_to_list).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="- 移除选中",
                 font=('微软雅黑', 9), bg='#FFEBEE', fg=self.colors['danger'],
                 relief=tk.FLAT, cursor='hand2',
                 command=self.remove_video_from_list).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="↑ 上移",
                 font=('微软雅黑', 9), bg=self.colors['bg'],
                 relief=tk.FLAT, cursor='hand2',
                 command=self.move_video_up).pack(side=tk.LEFT, padx=5)

        tk.Button(btn_frame, text="↓ 下移",
                 font=('微软雅黑', 9), bg=self.colors['bg'],
                 relief=tk.FLAT, cursor='hand2',
                 command=self.move_video_down).pack(side=tk.LEFT, padx=5)

        # 输出设置
        output_frame = tk.Frame(card, bg=self.colors['card'])
        output_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(output_frame, text="输出文件:",
                font=('微软雅黑', 10), bg=self.colors['card']).pack(side=tk.LEFT)

        self.concat_output_entry = tk.Entry(output_frame, font=('微软雅黑', 10),
                                           bg='#fafafa', relief=tk.SOLID, bd=1)
        self.concat_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(output_frame, text="浏览",
                 font=('微软雅黑', 9), bg=self.colors['secondary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_concat_output).pack(side=tk.LEFT)

        # 执行按钮
        action_frame = tk.Frame(card, bg=self.colors['card'])
        action_frame.pack(fill=tk.X, padx=15, pady=15)

        self.create_action_button(action_frame, "▶ 开始拼接",
                                  self.concat_videos).pack(side=tk.RIGHT)

    def add_video_to_list(self):
        files = filedialog.askopenfilenames(
            filetypes=[("视频文件", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv")]
        )
        for i, file in enumerate(files, 1):
            filename = os.path.basename(file)
            self.video_tree.insert('', tk.END, values=(i, filename, file))

    def remove_video_from_list(self):
        selection = self.video_tree.selection()
        if selection:
            self.video_tree.delete(selection[0])
            self.renumber_video_list()

    def move_video_up(self):
        selection = self.video_tree.selection()
        if selection:
            item = selection[0]
            idx = self.video_tree.index(item)
            if idx > 0:
                self.video_tree.move(item, '', idx - 1)
                self.renumber_video_list()

    def move_video_down(self):
        selection = self.video_tree.selection()
        if selection:
            item = selection[0]
            idx = self.video_tree.index(item)
            if idx < len(self.video_tree.get_children()) - 1:
                self.video_tree.move(item, '', idx + 1)
                self.renumber_video_list()

    def renumber_video_list(self):
        """重新编号"""
        for i, item in enumerate(self.video_tree.get_children(), 1):
            values = self.video_tree.item(item, 'values')
            self.video_tree.item(item, values=(i, values[1], values[2]))

    def select_concat_output(self):
        file = filedialog.asksaveasfilename(defaultextension=".mp4",
                                            filetypes=[("MP4", "*.mp4")])
        if file:
            self.concat_output_entry.delete(0, tk.END)
            self.concat_output_entry.insert(0, file)

    def concat_videos(self):
        videos = [self.video_tree.item(item, 'values')[2]
                  for item in self.video_tree.get_children()]
        output = self.concat_output_entry.get()

        if len(videos) < 2:
            messagebox.showwarning("警告", "请至少添加两个视频文件")
            return
        if not output:
            messagebox.showwarning("警告", "请选择输出文件")
            return

        list_file = os.path.join(os.path.dirname(output), "concat_list.txt")
        with open(list_file, "w", encoding="utf-8") as f:
            for video in videos:
                f.write(f"file '{video}'\n")

        command = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", output]
        self.run_ffmpeg(command, "视频拼接完成")

    # ========== 音视频分离 ==========
    def create_audio_extract_tab(self):
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text=" 音频提取 ")

        card = self.create_card(tab, "从视频中提取音频")
        card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 输入文件
        input_frame = tk.Frame(card, bg=self.colors['card'])
        input_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(input_frame, text="输入视频:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.extract_input_entry = tk.Entry(input_frame, font=('微软雅黑', 10),
                                           bg='#fafafa', relief=tk.SOLID, bd=1)
        self.extract_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(input_frame, text="选择视频",
                 font=('微软雅黑', 9), bg=self.colors['primary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_extract_input).pack(side=tk.RIGHT)

        # 设置区域
        settings_frame = tk.Frame(card, bg=self.colors['card'])
        settings_frame.pack(fill=tk.X, padx=15, pady=10)

        # 输出格式
        tk.Label(settings_frame, text="输出格式:",
                font=('微软雅黑', 10), bg=self.colors['card']).pack(side=tk.LEFT)

        self.audio_format = ttk.Combobox(settings_frame,
                                         values=["mp3", "aac", "wav", "flac", "ogg", "m4a"],
                                         width=12, state='readonly')
        self.audio_format.set("mp3")
        self.audio_format.pack(side=tk.LEFT, padx=10)

        # 输出文件
        output_frame = tk.Frame(card, bg=self.colors['card'])
        output_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(output_frame, text="输出文件:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.audio_output_entry = tk.Entry(output_frame, font=('微软雅黑', 10),
                                          bg='#fafafa', relief=tk.SOLID, bd=1)
        self.audio_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(output_frame, text="浏览",
                 font=('微软雅黑', 9), bg=self.colors['secondary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_audio_output).pack(side=tk.RIGHT)

        # 执行按钮
        action_frame = tk.Frame(card, bg=self.colors['card'])
        action_frame.pack(fill=tk.X, padx=15, pady=20)

        self.create_action_button(action_frame, "▶ 提取音频",
                                  self.extract_audio).pack(side=tk.RIGHT)

    def select_extract_input(self):
        file = filedialog.askopenfilename(
            filetypes=[("视频文件", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv")]
        )
        if file:
            self.extract_input_entry.delete(0, tk.END)
            self.extract_input_entry.insert(0, file)
            base = os.path.splitext(file)[0]
            self.audio_output_entry.delete(0, tk.END)
            self.audio_output_entry.insert(0, base + ".mp3")

    def select_audio_output(self):
        file = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3", "*.mp3"), ("AAC", "*.aac"), ("WAV", "*.wav"),
                      ("FLAC", "*.flac"), ("OGG", "*.ogg"), ("M4A", "*.m4a")]
        )
        if file:
            self.audio_output_entry.delete(0, tk.END)
            self.audio_output_entry.insert(0, file)

    def extract_audio(self):
        input_file = self.extract_input_entry.get()
        output_file = self.audio_output_entry.get()
        fmt = self.audio_format.get()

        if not input_file or not output_file:
            messagebox.showwarning("警告", "请选择输入和输出文件")
            return

        command = ["ffmpeg", "-i", input_file, "-vn", "-acodec", fmt, output_file]
        self.run_ffmpeg(command, "音频提取完成")

    # ========== 音频转码 ==========
    def create_audio_transcode_tab(self):
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text=" 音频转码 ")

        card = self.create_card(tab, "转换音频格式")
        card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 输入文件
        input_frame = tk.Frame(card, bg=self.colors['card'])
        input_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(input_frame, text="输入音频:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.transcode_input_entry = tk.Entry(input_frame, font=('微软雅黑', 10),
                                             bg='#fafafa', relief=tk.SOLID, bd=1)
        self.transcode_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(input_frame, text="选择音频",
                 font=('微软雅黑', 9), bg=self.colors['primary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_transcode_input).pack(side=tk.RIGHT)

        # 设置区域
        settings_frame = tk.Frame(card, bg=self.colors['card'])
        settings_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(settings_frame, text="输出格式:",
                font=('微软雅黑', 10), bg=self.colors['card']).pack(side=tk.LEFT)

        self.transcode_format = ttk.Combobox(settings_frame,
                                            values=["mp3", "aac", "wav", "flac", "ogg", "wma"],
                                            width=12, state='readonly')
        self.transcode_format.set("mp3")
        self.transcode_format.pack(side=tk.LEFT, padx=10)

        tk.Label(settings_frame, text="码率:",
                font=('微软雅黑', 10), bg=self.colors['card']).pack(side=tk.LEFT, padx=(30, 0))

        self.bitrate = ttk.Combobox(settings_frame,
                                   values=["128k", "192k", "256k", "320k"],
                                   width=12, state='readonly')
        self.bitrate.set("192k")
        self.bitrate.pack(side=tk.LEFT, padx=10)

        # 输出文件
        output_frame = tk.Frame(card, bg=self.colors['card'])
        output_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(output_frame, text="输出文件:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.transcode_output_entry = tk.Entry(output_frame, font=('微软雅黑', 10),
                                              bg='#fafafa', relief=tk.SOLID, bd=1)
        self.transcode_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(output_frame, text="浏览",
                 font=('微软雅黑', 9), bg=self.colors['secondary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_transcode_output).pack(side=tk.RIGHT)

        # 执行按钮
        action_frame = tk.Frame(card, bg=self.colors['card'])
        action_frame.pack(fill=tk.X, padx=15, pady=20)

        self.create_action_button(action_frame, "▶ 开始转码",
                                  self.transcode_audio).pack(side=tk.RIGHT)

    def select_transcode_input(self):
        file = filedialog.askopenfilename(
            filetypes=[("音频文件", "*.mp3 *.aac *.wav *.flac *.ogg *.wma *.m4a")]
        )
        if file:
            self.transcode_input_entry.delete(0, tk.END)
            self.transcode_input_entry.insert(0, file)

    def select_transcode_output(self):
        file = filedialog.asksaveasfilename(
            filetypes=[("MP3", "*.mp3"), ("AAC", "*.aac"), ("WAV", "*.wav"),
                      ("FLAC", "*.flac"), ("OGG", "*.ogg")]
        )
        if file:
            self.transcode_output_entry.delete(0, tk.END)
            self.transcode_output_entry.insert(0, file)

    def transcode_audio(self):
        input_file = self.transcode_input_entry.get()
        output_file = self.transcode_output_entry.get()
        bitrate = self.bitrate.get()

        if not input_file or not output_file:
            messagebox.showwarning("警告", "请选择输入和输出文件")
            return

        command = ["ffmpeg", "-i", input_file, "-b:a", bitrate, output_file]
        self.run_ffmpeg(command, "音频转码完成")

    # ========== 音视频合成 ==========
    def create_av_merge_tab(self):
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text=" 音视频合成 ")

        card = self.create_card(tab, "合并视频和音频")
        card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 视频输入
        video_frame = tk.Frame(card, bg=self.colors['card'])
        video_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(video_frame, text="视频文件:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.merge_video_entry = tk.Entry(video_frame, font=('微软雅黑', 10),
                                         bg='#fafafa', relief=tk.SOLID, bd=1)
        self.merge_video_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(video_frame, text="选择视频",
                 font=('微软雅黑', 9), bg=self.colors['primary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_merge_video).pack(side=tk.RIGHT)

        # 音频输入
        audio_frame = tk.Frame(card, bg=self.colors['card'])
        audio_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(audio_frame, text="音频文件:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.merge_audio_entry = tk.Entry(audio_frame, font=('微软雅黑', 10),
                                         bg='#fafafa', relief=tk.SOLID, bd=1)
        self.merge_audio_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(audio_frame, text="选择音频",
                 font=('微软雅黑', 9), bg=self.colors['primary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_merge_audio).pack(side=tk.RIGHT)

        # 输出文件
        output_frame = tk.Frame(card, bg=self.colors['card'])
        output_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(output_frame, text="输出文件:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.merge_output_entry = tk.Entry(output_frame, font=('微软雅黑', 10),
                                          bg='#fafafa', relief=tk.SOLID, bd=1)
        self.merge_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(output_frame, text="浏览",
                 font=('微软雅黑', 9), bg=self.colors['secondary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_merge_output).pack(side=tk.RIGHT)

        # 执行按钮
        action_frame = tk.Frame(card, bg=self.colors['card'])
        action_frame.pack(fill=tk.X, padx=15, pady=20)

        self.create_action_button(action_frame, "▶ 开始合成",
                                  self.merge_av).pack(side=tk.RIGHT)

    def select_merge_video(self):
        file = filedialog.askopenfilename(
            filetypes=[("视频文件", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv")]
        )
        if file:
            self.merge_video_entry.delete(0, tk.END)
            self.merge_video_entry.insert(0, file)

    def select_merge_audio(self):
        file = filedialog.askopenfilename(
            filetypes=[("音频文件", "*.mp3 *.aac *.wav *.flac *.ogg *.m4a")]
        )
        if file:
            self.merge_audio_entry.delete(0, tk.END)
            self.merge_audio_entry.insert(0, file)

    def select_merge_output(self):
        file = filedialog.asksaveasfilename(defaultextension=".mp4",
                                            filetypes=[("MP4", "*.mp4")])
        if file:
            self.merge_output_entry.delete(0, tk.END)
            self.merge_output_entry.insert(0, file)

    def merge_av(self):
        video_file = self.merge_video_entry.get()
        audio_file = self.merge_audio_entry.get()
        output_file = self.merge_output_entry.get()

        if not video_file or not audio_file or not output_file:
            messagebox.showwarning("警告", "请填写所有文件路径")
            return

        command = ["ffmpeg", "-i", video_file, "-i", audio_file,
                  "-c:v", "copy", "-c:a", "aac", "-shortest", output_file]
        self.run_ffmpeg(command, "音视频合成完成")

    # ========== 视频转码 ==========
    def create_video_transcode_tab(self):
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text=" 视频转码 ")

        card = self.create_card(tab, "转换视频格式")
        card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 输入文件
        input_frame = tk.Frame(card, bg=self.colors['card'])
        input_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(input_frame, text="输入视频:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.video_transcode_input_entry = tk.Entry(input_frame, font=('微软雅黑', 10),
                                                   bg='#fafafa', relief=tk.SOLID, bd=1)
        self.video_transcode_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(input_frame, text="选择视频",
                 font=('微软雅黑', 9), bg=self.colors['primary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_video_transcode_input).pack(side=tk.RIGHT)

        # 设置区域
        settings_frame = tk.Frame(card, bg=self.colors['card'])
        settings_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(settings_frame, text="输出格式:",
                font=('微软雅黑', 10), bg=self.colors['card']).pack(side=tk.LEFT)

        self.video_format = ttk.Combobox(settings_frame,
                                        values=["mp4", "avi", "mkv", "mov", "wmv", "flv"],
                                        width=12, state='readonly')
        self.video_format.set("mp4")
        self.video_format.pack(side=tk.LEFT, padx=10)

        tk.Label(settings_frame, text="分辨率:",
                font=('微软雅黑', 10), bg=self.colors['card']).pack(side=tk.LEFT, padx=(30, 0))

        self.resolution = ttk.Combobox(settings_frame,
                                      values=["原始", "1920x1080", "1280x720", "854x480", "640x360"],
                                      width=12, state='readonly')
        self.resolution.set("原始")
        self.resolution.pack(side=tk.LEFT, padx=10)

        # 视频码率
        bitrate_frame = tk.Frame(card, bg=self.colors['card'])
        bitrate_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(bitrate_frame, text="视频码率:",
                font=('微软雅黑', 10), bg=self.colors['card']).pack(side=tk.LEFT)

        self.video_bitrate = ttk.Combobox(bitrate_frame,
                                         values=["原始", "8000k", "4000k", "2000k", "1000k", "500k"],
                                         width=12, state='readonly')
        self.video_bitrate.set("原始")
        self.video_bitrate.pack(side=tk.LEFT, padx=10)

        # 输出文件
        output_frame = tk.Frame(card, bg=self.colors['card'])
        output_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(output_frame, text="输出文件:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.video_transcode_output_entry = tk.Entry(output_frame, font=('微软雅黑', 10),
                                                    bg='#fafafa', relief=tk.SOLID, bd=1)
        self.video_transcode_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(output_frame, text="浏览",
                 font=('微软雅黑', 9), bg=self.colors['secondary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_video_transcode_output).pack(side=tk.RIGHT)

        # 执行按钮
        action_frame = tk.Frame(card, bg=self.colors['card'])
        action_frame.pack(fill=tk.X, padx=15, pady=20)

        self.create_action_button(action_frame, "▶ 开始转码",
                                  self.transcode_video).pack(side=tk.RIGHT)

    def select_video_transcode_input(self):
        file = filedialog.askopenfilename(
            filetypes=[("视频文件", "*.mp4 *.avi *.mkv *.mov *.flv *.wmv")]
        )
        if file:
            self.video_transcode_input_entry.delete(0, tk.END)
            self.video_transcode_input_entry.insert(0, file)

    def select_video_transcode_output(self):
        file = filedialog.asksaveasfilename(
            filetypes=[("MP4", "*.mp4"), ("AVI", "*.avi"), ("MKV", "*.mkv"),
                      ("MOV", "*.mov"), ("WMV", "*.wmv")]
        )
        if file:
            self.video_transcode_output_entry.delete(0, tk.END)
            self.video_transcode_output_entry.insert(0, file)

    def transcode_video(self):
        input_file = self.video_transcode_input_entry.get()
        output_file = self.video_transcode_output_entry.get()
        resolution = self.resolution.get()
        bitrate = self.video_bitrate.get()

        if not input_file or not output_file:
            messagebox.showwarning("警告", "请选择输入和输出文件")
            return

        command = ["ffmpeg", "-i", input_file]

        if resolution != "原始":
            command.extend(["-s", resolution])
        if bitrate != "原始":
            command.extend(["-b:v", bitrate])

        command.append(output_file)
        self.run_ffmpeg(command, "视频转码完成")

    # ========== 图片转视频 ==========
    def create_image_to_video_tab(self):
        tab = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(tab, text=" 图片转视频 ")

        card = self.create_card(tab, "将图片序列转换为视频")
        card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 图片文件夹
        folder_frame = tk.Frame(card, bg=self.colors['card'])
        folder_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(folder_frame, text="图片文件夹:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.image_folder_entry = tk.Entry(folder_frame, font=('微软雅黑', 10),
                                          bg='#fafafa', relief=tk.SOLID, bd=1)
        self.image_folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(folder_frame, text="选择文件夹",
                 font=('微软雅黑', 9), bg=self.colors['primary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_image_folder).pack(side=tk.RIGHT)

        # 设置区域
        settings_frame = tk.Frame(card, bg=self.colors['card'])
        settings_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(settings_frame, text="帧率 (fps):",
                font=('微软雅黑', 10), bg=self.colors['card']).pack(side=tk.LEFT)

        self.fps = ttk.Combobox(settings_frame,
                               values=["1", "5", "10", "24", "30", "60"],
                               width=12, state='readonly')
        self.fps.set("1")
        self.fps.pack(side=tk.LEFT, padx=10)

        tk.Label(settings_frame, text="图片格式:",
                font=('微软雅黑', 10), bg=self.colors['card']).pack(side=tk.LEFT, padx=(30, 0))

        self.image_format = ttk.Combobox(settings_frame,
                                        values=["jpg", "jpeg", "png", "bmp"],
                                        width=12, state='readonly')
        self.image_format.set("jpg")
        self.image_format.pack(side=tk.LEFT, padx=10)

        # 输出文件
        output_frame = tk.Frame(card, bg=self.colors['card'])
        output_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(output_frame, text="输出视频:",
                font=('微软雅黑', 10), bg=self.colors['card'],
                width=10, anchor='w').pack(side=tk.LEFT)

        self.image_video_output_entry = tk.Entry(output_frame, font=('微软雅黑', 10),
                                                bg='#fafafa', relief=tk.SOLID, bd=1)
        self.image_video_output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        tk.Button(output_frame, text="浏览",
                 font=('微软雅黑', 9), bg=self.colors['secondary'], fg='white',
                 relief=tk.FLAT, cursor='hand2',
                 command=self.select_image_video_output).pack(side=tk.RIGHT)

        # 提示信息
        tip_frame = tk.Frame(card, bg=self.colors['card'])
        tip_frame.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(tip_frame,
                text="提示: 图片需要按数字顺序命名，如 1.jpg, 2.jpg, 3.jpg...",
                font=('微软雅黑', 9),
                fg=self.colors['secondary'], bg=self.colors['card']).pack(anchor='w')

        # 执行按钮
        action_frame = tk.Frame(card, bg=self.colors['card'])
        action_frame.pack(fill=tk.X, padx=15, pady=20)

        self.create_action_button(action_frame, "▶ 开始生成",
                                  self.image_to_video).pack(side=tk.RIGHT)

    def select_image_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.image_folder_entry.delete(0, tk.END)
            self.image_folder_entry.insert(0, folder)

    def select_image_video_output(self):
        file = filedialog.asksaveasfilename(defaultextension=".mp4",
                                            filetypes=[("MP4", "*.mp4")])
        if file:
            self.image_video_output_entry.delete(0, tk.END)
            self.image_video_output_entry.insert(0, file)

    def image_to_video(self):
        folder = self.image_folder_entry.get()
        output_file = self.image_video_output_entry.get()
        fps = self.fps.get()
        img_fmt = self.image_format.get()

        if not folder or not output_file:
            messagebox.showwarning("警告", "请选择图片文件夹和输出文件")
            return

        import glob
        pattern = os.path.join(folder, f"*.{img_fmt}")
        images = glob.glob(pattern)

        if not images:
            messagebox.showwarning("警告", f"未找到 {img_fmt} 格式的图片")
            return

        input_pattern = os.path.join(folder, f"%d.{img_fmt}")
        command = ["ffmpeg", "-framerate", fps, "-i", input_pattern,
                  "-c:v", "libx264", "-pix_fmt", "yuv420p", output_file]
        self.run_ffmpeg(command, "图片转视频完成")


def main():
    root = tk.Tk()
    app = FFmpegToolsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
