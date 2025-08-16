#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
图标创建工具
用于将PNG转换为ICO格式，并创建不同尺寸的图标
"""

import os
import sys
from PIL import Image

def create_ico_from_png(png_path, ico_path, sizes=None):
    """
    从PNG创建ICO文件
    
    参数:
    - png_path: PNG图像的路径
    - ico_path: 要保存的ICO文件的路径
    - sizes: 一个包含多个尺寸的列表，如 [(16,16), (32,32), (48,48), (64,64)]
    """
    if sizes is None:
        sizes = [(16,16), (24,24), (32,32), (48,48), (64,64), (128,128), (256,256)]
    
    try:
        # 打开源图像
        img = Image.open(png_path)
        
        # 转换为RGBA模式（如果不是）
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 创建不同尺寸的图像
        icons = []
        for size in sizes:
            # 创建副本并调整大小
            resized_img = img.copy()
            resized_img.thumbnail(size, Image.LANCZOS)
            icons.append(resized_img)
        
        # 保存为ICO文件
        icons[0].save(ico_path, format='ICO', sizes=[(i.width, i.height) for i in icons], 
                      append_images=icons[1:])
        
        print(f"成功创建ICO文件: {ico_path}")
        return True
    except Exception as e:
        print(f"创建ICO文件失败: {str(e)}")
        return False

def main():
    """主函数，用于处理命令行参数"""
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 查找当前目录和上级目录中的logos文件夹
    logos_dir = os.path.join(os.path.dirname(script_dir), "logos")
    
    if not os.path.exists(logos_dir):
        # 如果上级目录不存在logos，检查当前目录下的assets
        logos_dir = os.path.join(script_dir, "assets")
        if not os.path.exists(logos_dir):
            os.makedirs(logos_dir)
            print(f"创建了assets目录: {logos_dir}")
    
    # 检查源PNG文件
    source_png = os.path.join(logos_dir, "samlllogo500x500.png")
    if not os.path.exists(source_png):
        # 尝试在当前目录下查找
        alt_source = os.path.join(script_dir, "samlllogo500x500.png")
        if os.path.exists(alt_source):
            source_png = alt_source
        else:
            print(f"错误: 找不到源PNG文件: {source_png}")
            return False
    
    # 创建不同大小的图标
    success = True
    
    # 创建48x48的图标
    icon_48 = os.path.join(logos_dir, "samlllogo48x48.ico")
    if not os.path.exists(icon_48):
        success &= create_ico_from_png(source_png, icon_48, [(48, 48)])
    
    # 创建系统托盘图标 (16x16 主要尺寸)
    tray_icon = os.path.join(logos_dir, "tray_icon.ico")
    if not os.path.exists(tray_icon):
        success &= create_ico_from_png(source_png, tray_icon, [(16, 16), (24, 24), (32, 32)])
    
    # 创建大图标 (32x32 主要尺寸)
    big_icon = os.path.join(logos_dir, "biglogo48x48.ico")
    if not os.path.exists(big_icon):
        success &= create_ico_from_png(source_png, big_icon, [(32, 32), (48, 48), (64, 64)])
    
    if success:
        print("所有图标创建成功")
        return True
    else:
        print("部分图标创建失败")
        return False

if __name__ == "__main__":
    main() 