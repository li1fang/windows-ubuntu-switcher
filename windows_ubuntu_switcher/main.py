#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Windows/Ubuntu切换器主程序
提供独立的GUI界面功能
"""

import sys
import os
import argparse
import logging
from gui import MainWindow
from system_utils import create_flag_file, reboot_system, check_system_status
from config import SYSTEM_NAME, LOG_DIR, LOG_FILE

# 配置日志
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=os.path.join(LOG_DIR, LOG_FILE),
    filemode='a'
)
logger = logging.getLogger('main')

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='Windows/Ubuntu自动切换器')
    parser.add_argument('--cli', action='store_true', help='使用命令行模式')
    parser.add_argument('--switch', action='store_true', help='直接执行切换操作')
    parser.add_argument('--status', action='store_true', help='显示系统状态')
    return parser.parse_args()

def switch_system():
    """切换系统函数"""
    logger.info("开始执行系统切换...")
    if create_flag_file():
        logger.info("标志文件创建成功，准备重启...")
        return reboot_system()
    else:
        logger.error("标志文件创建失败，无法切换系统")
        return False

def main():
    """主函数"""
    args = parse_arguments()
    
    logger.info(f"Windows/Ubuntu切换器启动，当前系统: {SYSTEM_NAME}")
    logger.info(f"命令行参数: {args}")
    
    # 检查系统状态
    status = check_system_status()
    logger.info(f"系统状态: {status}")
    
    # 命令行模式
    if args.cli:
        if args.status:
            print(f"当前系统: {status['system']}")
            print(f"S盘可访问: {'是' if status['s_drive_accessible'] else '否'}")
            return 0
            
        if args.switch:
            print("执行系统切换...")
            if switch_system():
                print("系统将在几秒后重启...")
                return 0
            else:
                print("系统切换失败，请查看日志获取详细信息")
                return 1
                
        print("请指定操作参数 (--switch 或 --status)")
        return 1
    
    # GUI模式
    try:
        logger.info("启动GUI界面")
        app = MainWindow()
        app.root.mainloop()
        return 0
    except Exception as e:
        logger.error(f"GUI启动失败: {str(e)}")
        print(f"错误: GUI启动失败 - {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())