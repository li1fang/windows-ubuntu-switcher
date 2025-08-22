#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
系统操作工具函数
包含创建标志文件、重启系统等功能
"""

import os
import subprocess
import logging
import time
from tkinter import messagebox
from config import FLAG_FILE_PATH, ERROR_CREATE_FLAG, ERROR_REBOOT, REBOOT_TIMEOUT, LOG_DIR, LOG_FILE

# 配置日志
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(LOG_DIR, LOG_FILE),
    filemode='a'
)
logger = logging.getLogger('system_utils')

def create_flag_file():
    """
    创建标志文件
    
    Returns:
        bool: 操作是否成功
    """
    try:
        # 检查S盘是否存在
        s_drive_path = "S:\\"
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            if os.path.exists(s_drive_path):
                logger.info(f"成功访问S盘")
                break
            else:
                retry_count += 1
                error_msg = f"尝试访问S盘 ({retry_count}/{max_retries})"
                logger.warning(error_msg)
                time.sleep(1)  # 等待1秒再重试
        
        if not os.path.exists(s_drive_path):
            error_msg = "无法访问S盘，请确保该共享驱动器已正确挂载"
            logger.error(error_msg)
            messagebox.showerror("错误", error_msg)
            return False
            
        # 确保目录存在
        flag_dir = os.path.dirname(FLAG_FILE_PATH)
        if not os.path.exists(flag_dir):
            try:
                os.makedirs(flag_dir, exist_ok=True)
                logger.info(f"已创建目录: {flag_dir}")
            except Exception as e:
                error_msg = f"无法创建目录{flag_dir}: {str(e)}"
                logger.error(error_msg)
                messagebox.showerror("错误", error_msg)
                return False
                
        # 检查目录是否可写
        test_file = os.path.join(flag_dir, "test_write.tmp")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            logger.info(f"目录{flag_dir}可写")
        except Exception as e:
            error_msg = f"目录{flag_dir}不可写: {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("错误", error_msg)
            return False
            
        # 创建标志文件
        try:
            # 尝试删除已存在的标志文件
            if os.path.exists(FLAG_FILE_PATH):
                os.remove(FLAG_FILE_PATH)
                logger.info(f"已删除已存在的标志文件")
                
            with open(FLAG_FILE_PATH, 'w') as f:
                flag_content = f"Switch to Ubuntu - Created at {time.strftime('%Y-%m-%d %H:%M:%S')}"
                f.write(flag_content)
            logger.info(f"标志文件已创建: {FLAG_FILE_PATH}")
            logger.info(f"标志文件内容: {flag_content}")
            return True
        except Exception as e:
            error_msg = f"创建标志文件失败: {str(e)}"
            logger.error(error_msg)
            messagebox.showerror("错误", error_msg)
            return False
            
    except Exception as e:
        error_msg = f"系统错误: {str(e)}"
        logger.error(error_msg)
        messagebox.showerror("错误", error_msg)
        return False

def reboot_system():
    """
    重启系统
    
    Returns:
        bool: 操作是否成功
    """
    try:
        # 确保标志文件已创建
        if not os.path.exists(FLAG_FILE_PATH):
            error_msg = "错误: 标志文件未创建，无法重启"
            logger.error(error_msg)
            messagebox.showerror("错误", error_msg)
            return False
            
        # 直接使用Windows的shutdown命令立即重启系统
        logger.info("正在执行系统重启")
        # /t 0表示立即重启，不等待
        subprocess.run(["shutdown", "/r", "/t", "0"])
        return True
    except Exception as e:
        error_msg = ERROR_REBOOT.format(str(e))
        logger.error(error_msg)
        messagebox.showerror("错误", error_msg)
        return False

def check_system_status():
    """
    检查当前系统状态
    
    Returns:
        str: 系统状态信息
    """
    # 检查是否能访问S盘
    s_drive_accessible = os.path.exists("S:\\")
    
    # 获取操作系统信息
    import platform
    system_info = platform.system()
    version_info = platform.version()
    
    status = {
        "system": f"{system_info} {version_info}",
        "s_drive_accessible": s_drive_accessible,
    }
    
    logger.info(f"系统状态: {status}")
    return status