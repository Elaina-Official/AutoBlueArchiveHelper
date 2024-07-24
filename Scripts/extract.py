import os
import ffmpeg
import cv2
import subprocess

def extract_frames(video_path, output_folder, width=640, height=360):
    """
    使用 ffmpeg 从视频中提取所有帧，按比例缩放到 360p，并保存到指定文件夹。
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_pattern = os.path.join(output_folder, 'frame_%04d.png')

    # 构建 FFmpeg 命令
    ffmpeg_input = ffmpeg.input(video_path)
    ffmpeg_output = (
        ffmpeg
        .output(ffmpeg_input, output_pattern, vf=f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2")
        .global_args('-loglevel', 'error')
        .run()
    )

def get_total_frames(video_path):
    """
    使用 cv2 统计视频总帧数，以跳过处理完成的视频
    """
    video_capture = cv2.VideoCapture(video_path)
    frames = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
    return frames

def main():
    current_file_path = os.path.abspath(__file__) # 当前文件路径
    root_dir = os.path.dirname(os.path.dirname(current_file_path)) # 获取项目根目录
    root_dir.replace("\\", "/").strip() # 替换成标准路径

    video_folder = root_dir + '/Videos' # 获取待处理视频目录
    screenshot_folder = root_dir + '/Frames' # 获取截图文件夹存放目录

    # 确保截图文件夹存在
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)

    # 遍历 Video 文件夹中的所有视频文件
    for video_file in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video_file)

        # 检查是否为文件（排除文件夹）
        if os.path.isfile(video_path):
            # 获取视频文件的名称（不带扩展名）
            video_name = os.path.splitext(video_file)[0]

            # 为该视频创建一个子文件夹
            output_folder = os.path.join(screenshot_folder, video_name)

            # 统计总帧数
            total_frames = get_total_frames(video_path)

            # 如果已经处理完成，则跳过
            if os.path.exists(output_folder) and len(os.listdir(output_folder)) >= total_frames:
                print(f"Video {video_file} already processed, skipping...")
                continue
            
            # 从视频中提取帧
            print(f"Processing video {video_file}...")
            extract_frames(video_path, output_folder)
            print(f"Video {video_file} processing finished...")

if __name__ == '__main__':
    main()
