from moviepy.editor import VideoFileClip
import os

# 定义输入和输出文件夹的相对路径
input_folder = './video_input'
output_folder = './video_output'

# 检查输入文件夹是否存在，如果不存在则创建
if not os.path.exists(input_folder):
    print(f"{input_folder} 文件夹不存在。")
    exit()  # 终止程序

# 获取输入文件夹中的视频文件
video_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi', '.mov'))]

# 检查输入文件夹是否为空
if not video_files:
    print(f"{input_folder} 文件夹是空的。")
    exit()  # 终止程序

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历视频文件并进行转换
for video_file in video_files:
    video_path = os.path.join(input_folder, video_file)
    
    # 修改输出文件名，添加 'output' 后缀
    name, ext = os.path.splitext(video_file)  # 分离文件名和扩展名
    output_file_name = f"{name}_output{ext}"  # 创建新的文件名
    output_path = os.path.join(output_folder, output_file_name)
    
    # 进行视频转换并调整大小为640x480
    clip = VideoFileClip(video_path)
    resized_clip = clip.resize(newsize=(640, 480))  # 设置新的分辨率为640x480
    resized_clip.write_videofile(output_path)

# 视频转换完成
print("视频转换完成。")
