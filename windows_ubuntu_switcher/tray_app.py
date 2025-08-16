#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Windows/Ubuntu切换器系统托盘应用
提供系统托盘图标和右键菜单功能，独立于GUI应用
"""

import os
import sys
import time
import threading
import logging
import pystray
from PIL import Image, ImageDraw
import ctypes
import tkinter as tk
from tkinter import messagebox
import atexit
import win32event
import win32api
import winerror
import win32con
import subprocess
import tempfile

# 配置日志
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tray_app.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
    ]
)
logger = logging.getLogger('tray_app')

# 全局变量
tray_icon = None
app_running_flag = os.path.join(tempfile.gettempdir(), "wowswitch_tray_running.tmp")

# 确保在程序启动时设置AppID
def setup_app_id():
    """设置应用程序ID，使任务栏图标正确显示"""
    try:
        # 尝试强制设置AppUserModelID
        app_id = "WOWSwitch.TrayApp.1"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        logger.info(f"已设置应用ID: {app_id}")
        return True
    except Exception as e:
        logger.error(f"设置AppID失败: {str(e)}")
        return False

# 使用Windows互斥体实现单例模式
def ensure_single_instance():
    """确保程序只有一个实例运行"""
    try:
        # 创建一个全局唯一互斥体
        mutex_name = 'Global\\WindowsUbuntuSwitcherTrayMutex'
        mutex = win32event.CreateMutex(None, False, mutex_name)
        last_error = win32api.GetLastError()
        
        # 如果互斥体已存在，说明程序已经运行
        if last_error == winerror.ERROR_ALREADY_EXISTS:
            logger.info("托盘应用已经在运行中")
            # 释放互斥体句柄
            if mutex:
                win32api.CloseHandle(mutex)
                
            # 尝试通知现有实例
            notify_existing_instance()
            return False
        
        # 创建运行标志文件
        with open(app_running_flag, 'w') as f:
            f.write(str(os.getpid()))
        
        # 注册退出时清理函数
        atexit.register(cleanup_on_exit, mutex)
        
        logger.info("托盘应用单例检查通过")
        return True
    except Exception as e:
        logger.error(f"单例检查失败: {str(e)}")
        # 失败时允许程序继续运行
        return True

# 退出时清理
def cleanup_on_exit(mutex=None):
    """程序退出时清理资源"""
    try:
        # 删除运行标志文件
        if os.path.exists(app_running_flag):
            os.remove(app_running_flag)
            logger.info("已删除运行标志文件")
            
        # 释放互斥体
        if mutex:
            win32api.CloseHandle(mutex)
            logger.info("已释放互斥体")
    except Exception as e:
        logger.error(f"退出清理失败: {str(e)}")

# 隐藏控制台窗口
def hide_console():
    """隐藏控制台窗口"""
    try:
        # 尝试获取控制台窗口句柄并隐藏
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0
            logger.info("控制台窗口已隐藏")
        else:
            logger.info("未找到控制台窗口")
    except Exception as e:
        logger.error(f"隐藏控制台窗口失败: {str(e)}")

# 发送消息到现有实例
def notify_existing_instance():
    """通知现有实例"""
    try:
        # 尝试向现有实例发送消息
        app_name = os.environ.get('APP_NAME', 'WOWSwitch')
        hwnd = ctypes.windll.user32.FindWindowW(None, app_name)
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, win32con.SW_SHOW)
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            logger.info("已通知现有实例显示窗口")
            return True
        
        logger.warning("未找到现有实例窗口")
        return False
    except Exception as e:
        logger.error(f"通知现有实例失败: {str(e)}")
        return False

# 创建默认图标
def create_default_icon():
    """创建默认图标（当找不到图标文件时使用）"""
    try:
        # 创建默认图标
        img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([(4, 4), (60, 60)], fill='#0078D7')  # Windows蓝色
        draw.ellipse([(16, 16), (48, 48)], fill='#FF8C00')  # Ubuntu橙色
        logger.info("已创建默认图标")
        return img
    except Exception as e:
        logger.error(f"创建默认图标失败: {str(e)}")
        # 创建一个最小的图标
        return Image.new('RGBA', (16, 16), color=(255, 0, 0, 255))

# 获取图标
def get_icon():
    """获取托盘图标"""
    try:
        # 优先使用环境变量中的图标路径
        if 'ICON_PATH' in os.environ and os.environ['ICON_PATH'] and os.path.exists(os.environ['ICON_PATH']):
            icon_path = os.environ['ICON_PATH']
            logger.info(f"使用环境变量指定的图标: {icon_path}")
            return Image.open(icon_path)
        
        # 查找图标文件
        icon_candidates = [
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logos", "samlllogo48x48.ico"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logos", "samlllogo500x500.png"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "samlllogo48x48.ico")
        ]
        
        for icon_path in icon_candidates:
            if os.path.exists(icon_path):
                logger.info(f"使用图标: {icon_path}")
                return Image.open(icon_path)
        
        # 如果找不到图标，创建默认图标
        logger.warning("未找到图标文件，使用默认图标")
        return create_default_icon()
    except Exception as e:
        logger.error(f"获取图标失败: {str(e)}")
        return create_default_icon()

# 打开GUI应用
def open_gui(_=None):
    """打开GUI应用"""
    try:
        logger.info("尝试打开GUI应用")
        # 获取脚本目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gui_path = os.path.join(script_dir, "main.py")
        
        # 检查GUI文件是否存在
        if not os.path.exists(gui_path):
            logger.error(f"GUI应用文件不存在: {gui_path}")
            show_message("错误", "找不到GUI应用文件")
            return
        
        # 启动GUI应用
        subprocess.Popen(["python", gui_path], cwd=script_dir, shell=True)
        logger.info("已启动GUI应用")
    except Exception as e:
        logger.error(f"打开GUI应用失败: {str(e)}")
        show_message("错误", f"启动GUI应用失败: {str(e)}")

# 切换系统
def switch_system(_=None):
    """从托盘菜单直接切换系统"""
    try:
        logger.info("尝试从托盘直接切换系统")
        # 导入必要的模块
        from system_utils import create_flag_file, reboot_system, check_system_status
        
        # 检查系统状态
        status = check_system_status()
        
        # 检查S盘是否可用
        if not status.get('s_drive_accessible', False):
            logger.error("S盘不可访问，无法切换系统")
            show_message("错误", "S盘不可访问，无法切换系统")
            return
        
        # 询问用户确认
        if not show_confirm("确认", f"确定要从 {status.get('system', 'Windows')} 切换到另一个系统吗？"):
            logger.info("用户取消了切换系统")
            return
        
        # 创建标志文件
        if not create_flag_file():
            logger.error("创建标志文件失败")
            show_message("错误", "创建标志文件失败，无法切换系统")
            return
        
        # 显示消息
        show_message("信息", "系统将在几秒后重启...")
        
        # 重启系统
        threading.Thread(target=reboot_system, daemon=True).start()
    except ImportError as e:
        logger.error(f"导入系统工具模块失败: {str(e)}")
        show_message("错误", "无法加载系统切换功能")
    except Exception as e:
        logger.error(f"切换系统失败: {str(e)}")
        show_message("错误", f"切换系统失败: {str(e)}")

# 显示关于对话框
def show_about(_=None):
    """显示关于对话框"""
    try:
        app_name = os.environ.get('APP_NAME', 'WOWSwitch')
        message = f"{app_name} 托盘应用\n版本: 1.0\n\n提供Windows与Ubuntu快速切换功能"
        show_message("关于", message)
    except Exception as e:
        logger.error(f"显示关于对话框失败: {str(e)}")

# 显示消息对话框
def show_message(title, message):
    """显示消息对话框"""
    try:
        # 创建临时根窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏根窗口
        
        # 设置图标（如果存在）
        try:
            if 'ICON_PATH' in os.environ and os.path.exists(os.environ['ICON_PATH']):
                root.iconbitmap(os.environ['ICON_PATH'])
        except:
            pass
        
        # 显示消息框
        messagebox.showinfo(title, message)
        
        # 销毁根窗口
        root.destroy()
    except Exception as e:
        logger.error(f"显示消息框失败: {str(e)}")

# 显示确认对话框
def show_confirm(title, message):
    """显示确认对话框，返回用户选择（True为确认）"""
    try:
        # 创建临时根窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏根窗口
        
        # 设置图标（如果存在）
        try:
            if 'ICON_PATH' in os.environ and os.path.exists(os.environ['ICON_PATH']):
                root.iconbitmap(os.environ['ICON_PATH'])
        except:
            pass
        
        # 显示确认框
        result = messagebox.askyesno(title, message)
        
        # 销毁根窗口
        root.destroy()
        
        return result
    except Exception as e:
        logger.error(f"显示确认框失败: {str(e)}")
        return False

# 退出应用
def exit_app(icon, _=None):
    """退出托盘应用"""
    try:
        logger.info("退出托盘应用")
        icon.stop()  # 停止图标
    except Exception as e:
        logger.error(f"退出应用失败: {str(e)}")
        sys.exit(1)

# 创建托盘图标
def create_tray_icon():
    """创建系统托盘图标"""
    global tray_icon
    
    try:
        logger.info("创建托盘图标")
        
        # 获取图标
        icon_image = get_icon()
        
        # 创建托盘图标菜单
        menu = pystray.Menu(
            pystray.MenuItem("打开界面", open_gui),
            pystray.MenuItem("切换系统", switch_system),
            pystray.MenuItem("退出", exit_app)
        )
        
        # 创建托盘图标
        app_name = os.environ.get('APP_NAME', 'WOWSwitch')
        tray_icon = pystray.Icon(app_name, icon_image, app_name, menu)
        
        # 设置左键单击行为
        tray_icon.on_activate = open_gui
        
        # 启动图标
        logger.info("托盘图标创建成功，开始运行")
        tray_icon.run()
        logger.info("托盘图标已停止运行")
    except Exception as e:
        logger.error(f"创建托盘图标失败: {str(e)}")
        tray_icon = None
        return False
    
    return True

# 主函数
def main():
    """主函数"""
    try:
        logger.info("托盘应用启动")
        
        # 隐藏控制台窗口
        hide_console()
        
        # 设置应用ID
        setup_app_id()
        
        # 确保只有一个实例运行
        if not ensure_single_instance():
            logger.info("程序已在运行中，退出")
            return
        
        # 创建并启动托盘图标
        create_tray_icon()
        
        # 正常退出
        logger.info("托盘应用正常退出")
        return True
    except Exception as e:
        logger.error(f"托盘应用运行失败: {str(e)}")
        return False

# 如果直接运行，执行main函数
if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"托盘应用异常: {str(e)}")
        sys.exit(1) 