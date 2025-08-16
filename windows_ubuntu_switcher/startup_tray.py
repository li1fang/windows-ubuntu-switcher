#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
专用托盘应用启动脚本
简化版的托盘启动程序，避免导入过多依赖
"""

import os
import sys
import time
import logging
from PIL import Image

# 配置日志
script_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(script_dir, 'tray_startup.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """主函数"""
    try:
        # 记录启动信息
        logging.info("托盘应用启动脚本开始执行")
        
        # 设置环境变量
        app_name = 'WOWSwitch'
        os.environ['APP_NAME'] = app_name
        
        # 设置图标路径
        icon_path = os.path.join(os.path.dirname(script_dir), 'logos', 'samlllogo48x48.ico')
        if not os.path.exists(icon_path):
            # 尝试备用图标
            icon_path = os.path.join(os.path.dirname(script_dir), 'logos', 'samlllogo500x500.png')
            logging.info(f"使用备用图标: {icon_path}")
        
        os.environ['ICON_PATH'] = icon_path
        logging.info(f"设置图标路径: {icon_path}")
        
        # 检查图标是否存在
        if not os.path.exists(icon_path):
            logging.warning(f"图标文件不存在: {icon_path}")
            try:
                # 尝试创建图标
                from ico_creator import main as create_icons
                create_icons()
                
                # 再次检查图标是否创建成功
                if os.path.exists(icon_path):
                    logging.info("图标创建成功")
                else:
                    logging.error("图标创建失败")
            except Exception as e:
                logging.error(f"创建图标出错: {str(e)}")
        
        # 尝试导入pystray
        try:
            import pystray
            logging.info("成功导入pystray库")
        except ImportError:
            logging.error("pystray库未安装，尝试安装...")
            # 尝试安装pystray
            import subprocess
            subprocess.call([sys.executable, "-m", "pip", "install", "-q", "pystray", "pillow", "pywin32"])
            
            # 再次尝试导入
            try:
                import pystray
                logging.info("pystray库安装成功")
            except ImportError:
                logging.error("pystray库安装失败")
                raise
        
        # 导入托盘应用模块
        try:
            import tray_app
            logging.info("成功导入tray_app模块")
            
            # 启动托盘应用
            logging.info("开始启动托盘应用")
            tray_app.main()
            
            logging.info("托盘应用正常退出")
        except Exception as e:
            logging.error(f"托盘应用启动失败: {str(e)}")
            
            # 尝试启动GUI作为备用方案
            logging.info("尝试启动GUI作为备用方案")
            try:
                from gui import MainWindow
                import tkinter as tk
                
                # 创建主窗口
                root = tk.Tk()
                app = MainWindow(root)
                root.mainloop()
                logging.info("GUI应用正常退出")
            except Exception as gui_error:
                logging.error(f"GUI应用启动失败: {str(gui_error)}")
    
    except Exception as e:
        logging.error(f"托盘启动脚本出错: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 