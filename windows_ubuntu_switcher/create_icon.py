#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
创建图标文件
生成一个简单的图标文件，用于Windows/Ubuntu切换器应用程序
"""

import os
import sys
import ctypes
from pathlib import Path
from PIL import Image, ImageDraw

def create_icon():
    """创建一个简单的图标文件"""
    # 确保assets目录存在
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # 创建图标
    img = Image.new('RGBA', (32, 32), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((2, 2, 14, 14), fill=(0, 120, 215))
    draw.rectangle((18, 2, 30, 14), fill=(0, 120, 215))
    draw.rectangle((2, 18, 14, 30), fill=(0, 120, 215))
    draw.rectangle((18, 18, 30, 30), fill=(0, 120, 215))
    draw.ellipse((8, 8, 24, 24), outline=(233, 84, 32), width=2)
    
    icon_path = os.path.join(assets_dir, "icon.ico")
    img.save(icon_path)
    return icon_path

def create_shortcut():
    """在桌面创建快捷方式"""
    try:
        # 获取桌面路径(兼容中文用户名)
        desktop = Path(os.path.join(os.environ["USERPROFILE"], "Desktop"))
        
        # 创建快捷方式(使用英文名称避免编码问题)
        shortcut_path = desktop / "Windows_Ubuntu_Switcher.lnk"
        target_path = os.path.join(os.path.dirname(__file__), "main.py")
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        
        # 使用Windows Script Host创建快捷方式
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = sys.executable
        shortcut.Arguments = f'"{target_path}"'
        shortcut.IconLocation = icon_path
        shortcut.WorkingDirectory = os.path.dirname(__file__)
        shortcut.save()
        
        print(f"快捷方式已创建: {shortcut_path}")
        return True
    except Exception as e:
        print(f"创建快捷方式失败: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        icon_path = create_icon()
        if create_shortcut():
            print("桌面快捷方式创建成功！")
    except Exception as e:
        print(f"操作失败: {str(e)}")
        print("请确保已安装依赖库:")
        print("pip install Pillow pywin32")