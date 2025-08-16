#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WOWSwitch模块
提供Windows/Ubuntu系统切换图形用户界面
"""

import os
import sys
import tkinter as tk
import logging
import threading
import time
from PIL import Image, ImageTk
from system_utils import create_flag_file, reboot_system, check_system_status

# 配置常量
WINDOW_TITLE = os.environ.get('APP_NAME', 'WOWSwitch')  # 从环境变量获取，默认为WOWSwitch
WINDOW_SIZE = "320x500"  # 调整窗口尺寸为瘦高型(16:10比例)，略微加宽
FONT_FAMILY = "Microsoft YaHei"  # 使用微软雅黑字体

# 配置日志
logger = logging.getLogger('gui')

# 添加优化图标函数
def optimize_image(image_path, target_size=(200, 200)):
    """优化图像，裁剪透明边缘并调整大小"""
    try:
        if not os.path.exists(image_path):
            logger.error(f"图像文件不存在: {image_path}")
            return None
            
        # 打开图像
        img = Image.open(image_path)
        
        # 如果图像有透明通道，裁剪透明边缘
        if img.mode == 'RGBA':
            # 获取图像数据
            data = img.getdata()
            
            # 找到非透明像素的边界
            non_empty_pixels = [(x, y) for y in range(img.height) for x in range(img.width) 
                              if data[y * img.width + x][3] > 0]
            
            if non_empty_pixels:
                # 计算边界
                x_min = min(x for x, y in non_empty_pixels)
                y_min = min(y for x, y in non_empty_pixels)
                x_max = max(x for x, y in non_empty_pixels)
                y_max = max(y for x, y in non_empty_pixels)
                
                # 裁剪图像
                img = img.crop((x_min, y_min, x_max, y_max))
                
                # 居中放置在正方形画布上
                size = max(img.width, img.height)
                new_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
                paste_x = (size - img.width) // 2
                paste_y = (size - img.height) // 2
                new_img.paste(img, (paste_x, paste_y), img)
                img = new_img
        
        # 调整图像大小，保持宽高比
        img.thumbnail(target_size, Image.LANCZOS)
        
        return img
    except Exception as e:
        logger.error(f"优化图像失败: {str(e)}")
        return None

# 确保在程序启动时设置AppID
def setup_app_id():
    """设置应用程序ID，使任务栏图标正确显示"""
    try:
        import ctypes
        # 设置进程AppUserModelID，这是任务栏显示正确图标的关键
        app_id = "WOWSwitch.App.1"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        logger.info(f"已设置应用ID: {app_id}")
        
        # 尝试设置窗口属性增强图标显示
        try:
            import win32gui
            import win32con
            import win32process
            
            # 尝试获取当前进程主窗口句柄
            def callback(hwnd, hwnds):
                if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    if pid == os.getpid():
                        hwnds.append(hwnd)
                return True
            
            hwnds = []
            win32gui.EnumWindows(callback, hwnds)
            
            if hwnds:
                hwnd = hwnds[0]
                # 设置扩展窗口样式，强制显示在任务栏
                style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                                    style | win32con.WS_EX_APPWINDOW)
                logger.info(f"已设置窗口扩展样式: WS_EX_APPWINDOW")
                
                # 刷新窗口
                win32gui.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 
                                   win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | 
                                   win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
            else:
                logger.warning("找不到当前进程的窗口")
        except Exception as e:
            logger.warning(f"设置窗口扩展样式失败: {str(e)}")
        
        return True
    except Exception as e:
        logger.error(f"设置AppID失败: {str(e)}")
        return False

class SimpleMainWindow:
    """简化版主窗口，使用纯tk控件"""
    
    def __init__(self, root=None):
        """初始化主窗口"""
        # 创建或使用传入的窗口
        if root is None:
            # 先设置AppID确保任务栏图标正确
            setup_app_id()
            self.root = tk.Tk()
            self.owns_root = True
        else:
            self.root = root
            self.owns_root = False
        
        # 检查系统状态 - 提前检查，避免界面加载延迟
        try:
            self.status = check_system_status()
        except Exception as e:
            logger.error(f"获取系统状态失败: {str(e)}")
            self.status = {"system": "Windows", "s_drive_accessible": False}
        
        # 基本设置
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)
        self.root.configure(bg="white")
        self.root.attributes("-topmost", True)  # 临时置顶
        
        # 避免因为GC导致的图像消失
        self.images = {}
        
        # 确保关闭事件被捕获
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        try:
            # 设置图标（如果存在）
            self.set_icon()
            
            # 清理旧的部件
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # 创建界面元素
            self.create_widgets()
            
            # 更新界面显示
            self.update_status_display()
            
            # 取消置顶
            self.root.after(1000, lambda: self.root.attributes("-topmost", False))
            
            # 添加保持窗口显示的计时器，但减少频率以避免卡顿
            self.root.after(1000, self._ensure_window_visibility)
        except Exception as e:
            logger.error(f"初始化界面时出错: {str(e)}")
            # 显示错误信息
            tk.Label(self.root, text=f"初始化错误: {str(e)}", fg="red", bg="white", font=(FONT_FAMILY, 10)).pack(padx=20, pady=20)
    
    def _ensure_window_visibility(self):
        """确保窗口可见性，防止闪退"""
        try:
            # 如果窗口存在，检查状态并确保可见
            if self.root.winfo_exists():
                # 如果窗口被最小化，恢复它
                if self.root.state() == 'iconic':
                    self.root.deiconify()
                
                # 每1000毫秒检查一次，减少CPU使用
                self.root.after(1000, self._ensure_window_visibility)
        except Exception as e:
            logger.error(f"确保窗口可见性失败: {str(e)}")
    
    def set_icon(self):
        """设置窗口图标"""
        try:
            # 设置优先级：1. 环境变量 2. logos目录 3. assets目录
            icon_found = False
            
            # 优先使用环境变量指定的图标
            if 'ICON_PATH' in os.environ and os.path.exists(os.environ['ICON_PATH']):
                try:
                    icon_path = os.environ['ICON_PATH']
                    if icon_path.lower().endswith('.ico'):
                        self.root.iconbitmap(icon_path)
                        logger.info(f"已加载环境变量指定的ICO图标: {icon_path}")
                        icon_found = True
                    elif icon_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                        # 处理PNG图像转为图标
                        img = Image.open(icon_path)
                        img = img.resize((32, 32), Image.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        self.root.iconphoto(True, photo)
                        self.images['icon'] = photo  # 保存引用
                        logger.info(f"已加载环境变量指定的PNG图标: {icon_path}")
                        icon_found = True
                except Exception as e:
                    logger.warning(f"加载环境变量指定的图标失败: {str(e)}")
            
            if not icon_found:
                # 尝试在logos文件夹查找图标
                logos_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logos")
                
                # 尝试加载不同格式和名称的图标
                icon_candidates = [
                    os.path.join(logos_path, "samlllogo48x48.ico"),
                    os.path.join(logos_path, "tray_icon.ico"),
                    os.path.join(logos_path, "biglogo48x48.ico"),
                    os.path.join(logos_path, "samlllogo500x500.png"),
                    os.path.join(os.path.dirname(__file__), "assets", "samlllogo48x48.ico"),
                    os.path.join(os.path.dirname(__file__), "assets", "tray_icon.ico"),
                    os.path.join(os.path.dirname(__file__), "assets", "biglogo48x48.ico")
                ]
                
                for icon_path in icon_candidates:
                    if os.path.exists(icon_path):
                        try:
                            if icon_path.lower().endswith('.ico'):
                                self.root.iconbitmap(icon_path)
                                logger.info(f"已加载ICO图标: {icon_path}")
                                icon_found = True
                                break
                            elif icon_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                                # 处理PNG图像
                                img = Image.open(icon_path)
                                img = img.resize((32, 32), Image.LANCZOS)
                                photo = ImageTk.PhotoImage(img)
                                self.root.iconphoto(True, photo)
                                self.images['icon'] = photo
                                logger.info(f"已加载PNG图标: {icon_path}")
                                icon_found = True
                                break
                        except Exception as e:
                            logger.warning(f"加载图标失败: {str(e)}")
            
            if not icon_found:
                logger.warning("未找到任何可用图标")
            
            # 设置窗口属性
            self.root.attributes('-toolwindow', 0)  # 不是工具窗口
            self.root.attributes('-topmost', True)  # 暂时置顶
            
            # 刷新窗口确保图标显示
            self.root.update_idletasks()
            
            # 取消置顶
            self.root.after(1000, lambda: self.root.attributes('-topmost', False))
        except Exception as e:
            logger.error(f"设置图标失败: {str(e)}")
            # 出错时不阻止继续执行
    
    def create_widgets(self):
        """创建界面元素，使用最简单的方式"""
        # 创建主框架
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=15, pady=20)
        
        # 加载Logo图片
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "assets", "biglogo500x500.png")
            
            # 使用优化函数处理图像 - 调整为更小的尺寸
            logo_image = optimize_image(logo_path, target_size=(180, 180))
            
            if logo_image:
                # 转换为Tkinter格式
                tk_logo = ImageTk.PhotoImage(logo_image)
                # 保存引用
                self.images['logo'] = tk_logo
                
                # 创建显示Logo的标签并添加点击事件
                logo_label = tk.Label(main_frame, image=tk_logo, bg="white", cursor="hand2")
                logo_label.pack(pady=(10, 10))
                # 绑定点击事件到切换系统函数
                logo_label.bind("<Button-1>", lambda e: self.switch_system())
                logger.info(f"已加载优化后的Logo图片: {logo_path}")
            else:
                # 如果优化失败，显示文本替代
                logger.error("无法加载Logo图片")
                logo_label = tk.Label(main_frame, text="[图标]", font=(FONT_FAMILY, 40), bg="white", fg="#0078D7")
                logo_label.pack(pady=(10, 10))
                logo_label.bind("<Button-1>", lambda e: self.switch_system())
        except Exception as e:
            logger.error(f"加载Logo图片失败: {str(e)}")
            # 显示文本替代
            logo_label = tk.Label(main_frame, text="[图标]", font=(FONT_FAMILY, 40), bg="white", fg="#0078D7")
            logo_label.pack(pady=(10, 10))
            logo_label.bind("<Button-1>", lambda e: self.switch_system())
        
        # 创建标题（改为提示性文本）
        title = tk.Label(
            main_frame, 
            text="点击上方图标切换系统",
            font=(FONT_FAMILY, 14, "bold"),
            bg="white"
        )
        title.pack(pady=(0, 25))
        
        # 创建状态框架 - 确保可见
        status_frame = tk.LabelFrame(main_frame, text="系统状态", bg="white", font=(FONT_FAMILY, 11, "bold"), bd=1, relief=tk.GROOVE)
        status_frame.pack(fill=tk.X, padx=5, pady=(0, 15))
        
        # 系统状态
        self.system_label = tk.Label(status_frame, text="当前系统: 正在检测...", bg="white", anchor="w", font=(FONT_FAMILY, 10))
        self.system_label.pack(fill=tk.X, padx=10, pady=5)
        
        # S盘状态
        self.sdrive_label = tk.Label(status_frame, text="S盘状态: 正在检测...", bg="white", anchor="w", font=(FONT_FAMILY, 10))
        self.sdrive_label.pack(fill=tk.X, padx=10, pady=5)
        
        # 状态消息
        self.status_msg = tk.Label(main_frame, text="", fg="black", bg="white", font=(FONT_FAMILY, 10))
        self.status_msg.pack(fill=tk.X, pady=15)
        
        # 空的伸缩框架，用于在垂直方向上填充空间
        spacer = tk.Frame(main_frame, bg="white")
        spacer.pack(expand=True, fill=tk.BOTH)
        
        # 版权信息 - 确保宽度足够
        # 使用固定宽度文本框显示完整版权信息
        copyright_text = f"© 2023 {WINDOW_TITLE}"
        copyright_frame = tk.Frame(main_frame, bg="white")
        copyright_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        copyright_label = tk.Label(
            copyright_frame, 
            text=copyright_text,
            fg="gray", 
            bg="white",
            font=(FONT_FAMILY, 8),
            width=len(copyright_text)+10  # 确保足够宽
        )
        copyright_label.pack(side=tk.BOTTOM)
        
        # 强制更新布局
        self.root.update_idletasks()
    
    def update_status_display(self):
        """更新状态显示"""
        try:
            # 更新系统状态
            system_name = self.status.get('system', 'Windows')
            self.system_label.config(text=f"当前系统: {system_name}")
            
            # 更新S盘状态
            s_drive_accessible = self.status.get('s_drive_accessible', False)
            status_text = "可访问" if s_drive_accessible else "不可访问"
            status_color = "green" if s_drive_accessible else "red"
            self.sdrive_label.config(text=f"S盘状态: {status_text}", fg=status_color)
            
            # 更新状态消息
            if not s_drive_accessible:
                self.status_msg.config(text="S盘不可访问，无法切换系统", fg="red")
            else:
                self.status_msg.config(text="系统准备就绪，点击图标可切换系统", fg="green")
        except Exception as e:
            logger.error(f"更新状态显示失败: {str(e)}")
    
    def switch_system(self):
        """执行系统切换"""
        try:
            # 检查S盘是否可访问
            s_drive_accessible = self.status.get('s_drive_accessible', False)
            if not s_drive_accessible:
                self.status_msg.config(text="S盘不可访问，无法切换系统", fg="red")
                return
                
            # 禁用切换功能
            self.status_msg.config(text="正在准备切换系统...", fg="blue")
            self.root.update()
            
            # 创建标志文件
            if create_flag_file():
                self.status_msg.config(text="正在重启系统...", fg="green")
                self.root.update()
                
                # 使用线程执行重启，避免阻塞主线程
                threading.Thread(target=lambda: self.execute_reboot(), daemon=True).start()
            else:
                self.status_msg.config(text="创建标志文件失败", fg="red")
        except Exception as e:
            logger.error(f"切换系统失败: {str(e)}")
            self.status_msg.config(text=f"切换失败: {str(e)}", fg="red")
    
    def execute_reboot(self):
        """执行重启操作"""
        try:
            # 等待一秒让用户看到状态
            time.sleep(1)
            
            # 关闭窗口
            self.root.after(0, self.root.withdraw)
            
            # 执行重启
            reboot_system()
        except Exception as e:
            logger.error(f"重启失败: {str(e)}")
            # 如果失败，恢复界面
            self.root.after(0, self.root.deiconify)
            self.root.after(0, lambda: self.status_msg.config(text=f"重启失败: {str(e)}", fg="red"))
    
    def on_closing(self):
        """窗口关闭事件处理"""
        try:
            logger.info("关闭窗口")
            
            # 清理资源
            self.images.clear()
            
            # 正常退出应用
            if self.owns_root:
                logger.info("完全退出应用")
                self.root.quit()
                self.root.destroy()
            else:
                logger.info("隐藏窗口")
                self.root.withdraw()
            
        except Exception as e:
            logger.error(f"关闭窗口失败: {str(e)}")
            # 尝试强制退出
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass

class MainWindow(SimpleMainWindow):
    """主窗口，增强版本"""
    
    def __init__(self, root=None):
        """初始化主窗口"""
        # 设置应用ID在创建窗口之前
        setup_app_id()
        
        # 创建或使用传入的窗口
        if root is None:
            self.root = tk.Tk()
            self.owns_root = True
        else:
            self.root = root
            self.owns_root = False
        
        # 基本设置
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)
        self.root.configure(bg="white")
        
        # 设置窗口图标
        self.set_icon()
        
        # 窗口显示在前面
        self.root.attributes("-topmost", True)
        
        # 避免因为GC导致的图像消失
        self.images = {}
        
        # 检查系统状态
        try:
            logger.info("检查系统状态...")
            self.status = check_system_status()
            logger.info(f"系统状态: {self.status}")
        except Exception as e:
            logger.error(f"获取系统状态失败: {str(e)}")
            self.status = {"system": "Windows", "s_drive_accessible": False}
        
        # 确保关闭事件被捕获
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 初始化组件
        self.init_components()
        
        # 更新状态显示
        self.update_status_display()
        
        # 取消置顶
        self.root.after(1000, lambda: self.root.attributes("-topmost", False))
    
    def init_components(self):
        """初始化界面组件"""
        # 清理旧的部件
        for widget in self.root.winfo_children():
            widget.destroy()
        
        try:
            # 创建界面元素
            self.create_widgets()
        except Exception as e:
            logger.error(f"创建界面元素失败: {str(e)}")
            # 显示错误信息
            tk.Label(self.root, text=f"初始化错误: {str(e)}", fg="red", bg="white", font=(FONT_FAMILY, 10)).pack(padx=20, pady=20)

# 导出为主类，兼容现有代码
MainWindow = MainWindow

# 用于直接测试
if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建窗口
    app = MainWindow()
    app.root.mainloop()