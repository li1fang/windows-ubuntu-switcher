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
    png_path = os.path.join(os.path.dirname(current_dir), "logos", "samlllogo500x500.png")
    print(f"ICO图标路径: {icon_path}")
    print(f"ICO图标文件存在: {os.path.exists(icon_path)}")
    print(f"PNG图标路径: {png_path}")
    print(f"PNG图标文件存在: {os.path.exists(png_path)}")
    
    # 尝试加载图标
    if os.path.exists(icon_path):
        try:
            img = Image.open(icon_path)
            print(f"ICO图标加载成功，尺寸: {img.size}")
            use_path = icon_path
        except Exception as e:
            print(f"ICO图标加载失败: {str(e)}")
            if os.path.exists(png_path):
                try:
                    img = Image.open(png_path)
                    print(f"PNG图标加载成功，尺寸: {img.size}")
                    use_path = png_path
                except Exception as e:
                    print(f"PNG图标加载失败: {str(e)}")
                    return False
            else:
                return False
    elif os.path.exists(png_path):
        try:
            img = Image.open(png_path)
            print(f"PNG图标加载成功，尺寸: {img.size}")
            use_path = png_path
        except Exception as e:
            print(f"PNG图标加载失败: {str(e)}")
            return False
    else:
        print("所有图标文件都不存在")
        return False
        
    # 尝试创建托盘图标
    try:
        # 创建默认图标
        def create_default_icon():
            from PIL import ImageDraw
            img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            draw.ellipse([(4, 4), (60, 60)], fill='#0078D7')  # Windows蓝色
            draw.ellipse([(16, 16), (48, 48)], fill='#FF8C00')  # Ubuntu橙色
            return img
            
        # 如果没有找到任何图标，使用默认图标
        if 'img' not in locals():
            img = create_default_icon()
            print("使用默认图标")
            
        print("尝试创建测试托盘图标...")
        
        def on_exit(icon):
            icon.stop()
        
        icon = pystray.Icon("test_icon", img, "测试图标", menu=pystray.Menu(
            pystray.MenuItem("退出", on_exit)
        ))
        
        print("托盘图标创建成功")
        print("在右下角托盘区域应该能看到测试图标")
        print("请检查是否能看到图标，按Ctrl+C退出")
        
        # 运行图标
        icon.run()
        
        return True
    except Exception as e:
        print(f"创建托盘图标失败: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = check_icon()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("用户中断测试")
        sys.exit(0) 