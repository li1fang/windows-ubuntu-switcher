#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
调试用托盘应用
简单实现系统托盘功能
"""

import os
import sys
import pystray
from PIL import Image, ImageDraw

def create_default_icon():
    """创建默认图标"""
    img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([(4, 4), (60, 60)], fill='#0078D7')  # Windows蓝色
    draw.ellipse([(16, 16), (48, 48)], fill='#FF8C00')  # Ubuntu橙色
    return img

def on_exit(icon, _):
    """退出应用"""
    print("退出应用")
    icon.stop()

def show_dialog(_):
    """显示对话框"""
    print("显示对话框")
    
    # 导入必要的GUI模块
    import tkinter as tk
    from tkinter import messagebox
    
    # 创建根窗口
    root = tk.Tk()
    root.withdraw()
    
    # 显示消息框
    messagebox.showinfo("WOWSwitch", "托盘应用工作正常！")
    
    # 销毁根窗口
    root.destroy()

def main():
    """主函数"""
    print("启动简易托盘应用...")
    
    # 获取图标路径
    icon_path = os.environ.get('ICON_PATH', None)
    
    # 尝试加载图标
    if icon_path and os.path.exists(icon_path):
        try:
            print(f"尝试加载图标: {icon_path}")
            image = Image.open(icon_path)
            print(f"成功加载图标，尺寸: {image.size}")
        except Exception as e:
            print(f"加载图标失败: {str(e)}")
            print("使用默认图标")
            image = create_default_icon()
    else:
        print("未找到图标路径或图标不存在，使用默认图标")
        image = create_default_icon()
    
    # 设置托盘图标菜单
    menu = pystray.Menu(
        pystray.MenuItem("测试", show_dialog),
        pystray.MenuItem("退出", on_exit)
    )
    
    # 创建托盘图标
    icon = pystray.Icon("WOWSwitch", image, "WOWSwitch调试", menu)
    
    # 设置单击图标的行为
    icon.on_activate = show_dialog
    
    # 显示托盘图标
    print("托盘图标已创建，现在应该在系统托盘区域可见")
    print("可以通过右键单击图标并选择\"退出\"来关闭程序")
    
    # 启动托盘图标
    icon.run()
    
    print("托盘应用已退出")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 