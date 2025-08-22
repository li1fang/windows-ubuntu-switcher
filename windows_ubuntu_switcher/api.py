#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Windows/Ubuntu切换器API
提供系统切换的编程接口和命令行工具
"""

import os
import sys
import json
import argparse
import logging
from config import LOG_DIR, LOG_FILE
from system_utils import create_flag_file, reboot_system, check_system_status

# 配置日志
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=os.path.join(LOG_DIR, LOG_FILE),
    filemode='a'
)
logger = logging.getLogger('api')

class WindowsUbuntuSwitcherAPI:
    """Windows/Ubuntu切换器API类"""
    
    @staticmethod
    def get_status():
        """
        获取系统状态
        
        Returns:
            dict: 包含系统状态信息的字典
        """
        try:
            status = check_system_status()
            logger.info(f"API - 获取系统状态: {status}")
            return {
                "success": True,
                "status": status
            }
        except Exception as e:
            logger.error(f"API - 获取系统状态失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def switch_to_ubuntu(silent=False):
        """
        切换到Ubuntu系统
        
        Args:
            silent (bool): 是否静默模式，不显示GUI
            
        Returns:
            dict: 操作结果
        """
        try:
            logger.info(f"API - 切换到Ubuntu (静默模式: {silent})")
            
            # 创建标志文件
            if create_flag_file():
                logger.info("API - 标志文件创建成功")
                
                # 如果是静默模式，直接重启
                if silent:
                    reboot_success = reboot_system()
                    if reboot_success:
                        logger.info("API - 系统重启中")
                        return {
                            "success": True,
                            "message": "系统重启中"
                        }
                    else:
                        logger.error("API - 系统重启失败")
                        return {
                            "success": False,
                            "error": "系统重启失败"
                        }
                else:
                    # 非静默模式，返回成功但不重启
                    return {
                        "success": True,
                        "message": "标志文件创建成功，请手动重启系统"
                    }
            else:
                logger.error("API - 标志文件创建失败")
                return {
                    "success": False,
                    "error": "标志文件创建失败"
                }
        except Exception as e:
            logger.error(f"API - 切换到Ubuntu失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Windows/Ubuntu切换器API命令行工具")
    parser.add_argument("--status", action="store_true", help="获取系统状态")
    parser.add_argument("--switch", action="store_true", help="切换到Ubuntu系统")
    parser.add_argument("--silent", action="store_true", help="静默模式，不显示GUI")
    parser.add_argument("--json", action="store_true", help="以JSON格式输出结果")
    return parser.parse_args()

def main():
    """命令行工具主函数"""
    args = parse_args()
    api = WindowsUbuntuSwitcherAPI()
    result = None
    
    # 执行操作
    if args.status:
        result = api.get_status()
    elif args.switch:
        result = api.switch_to_ubuntu(silent=args.silent)
    else:
        result = {
            "success": False,
            "error": "未指定操作，请使用 --status 或 --switch 参数"
        }
    
    # 输出结果
    if args.json:
        # JSON格式输出
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 普通文本输出
        if result["success"]:
            if "status" in result:
                status = result["status"]
                print(f"系统状态:")
                print(f"  当前系统: {status.get('system', '未知')}")
                print(f"  S盘可访问: {'是' if status.get('s_drive_accessible', False) else '否'}")
            else:
                print(f"操作成功: {result.get('message', '')}")
        else:
            print(f"操作失败: {result.get('error', '未知错误')}")
    
    return 0 if result["success"] else 1

if __name__ == "__main__":
    sys.exit(main()) 