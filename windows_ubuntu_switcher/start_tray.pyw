#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Windows/Ubuntu切换器启动脚本
使用.pyw扩展名确保不显示控制台窗口
"""

import os
import sys
import subprocess
import traceback

def ensure_dependencies():
    """确保所需的依赖库已安装"""
    required_packages = ['pystray', 'Pillow']
    for package in required_packages:
        try:
            __import__(package.lower())
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)

def main():
    try:
        # 首先安装依赖
        ensure_dependencies()
        
        # 然后导入所需的库
        import logging
        import tkinter as tk
        from tkinter import messagebox
        
        # 设置日志文件
        log_path = os.path.join(os.path.expanduser("~"), "windows_ubuntu_switcher_debug.log")
        logging.basicConfig(
            filename=log_path,
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filemode='a',
            encoding='utf-8'
        )
        logger = logging.getLogger("start_tray")
        
        # 确保当前工作目录是脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # 导入并运行托盘应用
        from tray_app import main as tray_main
        sys.exit(tray_main())
        
    except Exception as e:
        error_msg = f"托盘应用启动失败: {str(e)}"
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("启动失败", 
                f"{error_msg}\n\n"
                f"详细错误已记录到: {log_path}\n\n"
                f"请确保已安装所有必要的库: pip install pystray Pillow")
        except Exception:
            print(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main() 