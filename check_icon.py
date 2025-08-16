import os
import sys
from PIL import Image
import pystray

def check_icon():
    """检查图标文件是否可用"""
    print("开始检查图标...")
    
    # 检查当前目录
    current_dir = os.getcwd()
    print(f"当前目录: {current_dir}")
    
    # 检查图标路径
    icon_path = os.path.join(os.path.dirname(current_dir), "logos", "samlllogo48x48.ico")
    print(f"图标路径: {icon_path}")
    print(f"图标文件存在: {os.path.exists(icon_path)}")
    
    # 尝试加载图标
    if os.path.exists(icon_path):
        try:
            img = Image.open(icon_path)
            print(f"图标加载成功，尺寸: {img.size}")
            
            # 尝试创建一个测试托盘图标
            print("尝试创建测试托盘图标...")
            
            def on_exit(icon):
                icon.stop()
            
            icon = pystray.Icon("test_icon", img, "测试图标", menu=pystray.Menu(
                pystray.MenuItem("退出", on_exit)
            ))
            
            print("托盘图标创建成功")
            print("在右下角托盘区域应该能看到测试图标，3秒后将自动退出")
            
            # 使用线程运行图标
            import threading
            import time
            
            def run_icon():
                icon.run()
            
            # 启动图标
            icon_thread = threading.Thread(target=run_icon, daemon=True)
            icon_thread.start()
            
            # 等待3秒后退出
            time.sleep(3)
            icon.stop()
            
            return True
        except Exception as e:
            print(f"图标加载失败: {str(e)}")
            return False
    else:
        print("图标文件不存在")
        return False

if __name__ == "__main__":
    sys.exit(0 if check_icon() else 1) 