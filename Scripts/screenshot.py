# 注意：此程序无法捕获由硬件渲染的图像(即使用GPU, 启用图形加速等)
import win32gui
import sys, os, threading, time
import keyboard
from PyQt5.QtGui import QScreen, QGuiApplication
from PyQt5.QtCore import Qt

# 截图判断
screenshot_flag = False 
screenshot_count = 0

# 获取窗口和句柄
def get_all_window_titles():
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    return hwnd_title

# 打印句柄和窗口名
def print_all_window_titles():
    window_titles = get_all_window_titles()
    print("Handle \t Title")
    for hwnd, title in window_titles.items():
        if title != "":
            print(f"{hwnd} \t {title}")

# 根据窗口名获取句柄
def get_hwnd(window_title):
    window_dict = get_all_window_titles()
    window_dict = {v : k for k, v in window_dict.items()}
    hwnd = window_dict[window_title]
    return hwnd

# 获取窗口截图
def get_screenshot(hwnd, save_folder, frame_rate):
    global screenshot_flag, screenshot_count
    # 捕获帧率
    frame_interval = 1.0 / frame_rate
    # 获取所有窗口
    windows = QGuiApplication(sys.argv)
    # 获取主屏幕对象
    screen = QGuiApplication.primaryScreen()

    while (True):
        if screenshot_flag:
            # 根据句柄获取窗口截图
            screenshot = screen.grabWindow(hwnd)
            # 保存截图
            screenshot.save(save_folder + f"/screenshot_{screenshot_count}.jpg")
            screenshot_count += 1
        time.sleep(frame_interval)

# 反转截图状态
def reverse_screenshot_flag():
    global screenshot_flag, screenshot_count
    if screenshot_flag:
        print("停止截图...")
    else:
        print("开始截图...")
    screenshot_flag = not screenshot_flag

if __name__ == '__main__':
    print_all_window_titles()
    # 窗口名
    window_title = "Put your window title here." 
    # 项目根目录
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 替换成标准路径
    root_dir = root_dir.replace("\\", "/").strip()
    # 保存窗口截图的目录
    save_folder = (root_dir + "/Screenshots")
    # 获取窗口句柄 
    hwnd = get_hwnd(window_title)
    # 捕获帧数
    frame_rate = 60

    # 启动截图线程
    screenshot_thread = threading.Thread(target=get_screenshot, args=(hwnd, save_folder, frame_rate))
    screenshot_thread.daemon = True
    screenshot_thread.start()

    # 监听快捷键 Alt+B 切换截图状态
    keyboard.add_hotkey('alt+b', reverse_screenshot_flag)
    # 保持主线程运行, 按下 esc 退出
    keyboard.wait('esc')