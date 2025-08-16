#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置文件
包含Windows/Ubuntu切换器应用程序的配置信息
"""

import platform

# 标志文件路径
FLAG_FILE_PATH = "S:\\go-ubuntu.flag"  # 共享专用盘路径

# 系统名称
SYSTEM_NAME = "Windows"
SYSTEM_VERSION = platform.version()

# GUI配置
WINDOW_TITLE = "Windows/Ubuntu切换器"
WINDOW_SIZE = "450x350"
BUTTON_TEXT = "切换到Ubuntu"
CONFIRM_MESSAGE = "确定要切换到Ubuntu系统吗？\n系统将会重启。"
SUCCESS_MESSAGE = "标志文件已创建，系统将在几秒后重启..."
ERROR_CREATE_FLAG = "创建标志文件失败: {}"
ERROR_REBOOT = "重启系统失败: {}"

# 重启配置
REBOOT_TIMEOUT = 3  # 秒

# 托盘应用配置
TRAY_ICON_TITLE = "Windows/Ubuntu切换器"
TRAY_TOOLTIP_CHECK_INTERVAL = 60  # 秒

# API配置
API_VERSION = "1.0.0"
API_DESCRIPTION = "Windows/Ubuntu切换器API"

# 其他设置
LOG_FILE = "windows_ubuntu_switcher.log"
DEBUG_MODE = False  # 调试模式开关