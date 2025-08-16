#!/bin/bash
# test-switcher.sh
#
# Ubuntu/Windows切换器测试脚本
# 用于测试GRUB配置和切换功能

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

# 函数：打印彩色消息
print_msg() {
    local color=$1
    local msg=$2
    echo -e "${color}${msg}${NC}"
}

# 函数：检查是否以root权限运行
check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        print_msg "$RED" "错误：此脚本需要root权限运行"
        echo "请使用sudo运行此脚本："
        echo "sudo ./test-switcher.sh"
        exit 1
    fi
}

# 函数：检查GRUB配置
check_grub_config() {
    print_msg "$BLUE" "检查GRUB配置..."
    
    if [ ! -f "/boot/grub/grub.cfg" ]; then
        print_msg "$RED" "错误：找不到GRUB配置文件"
        return 1
    fi
    
    # 查找所有Windows引导条目
    WINDOWS_ENTRIES=$(grep -i "menuentry " /boot/grub/grub.cfg | grep -i windows)
    
    if [ -z "$WINDOWS_ENTRIES" ]; then
        print_msg "$RED" "错误：在GRUB配置中找不到Windows引导项"
        return 1
    fi
    
    print_msg "$GREEN" "找到以下Windows引导项:"
    echo "$WINDOWS_ENTRIES"
    
    # 获取GRUB默认引导设置
    print_msg "$BLUE" "GRUB默认引导设置:"
    cat /etc/default/grub | grep -i "^GRUB_DEFAULT"
    
    return 0
}

# 函数：测试手动设置GRUB引导
test_grub_reboot() {
    print_msg "$BLUE" "测试grub-reboot命令..."
    
    # 查找第一个Windows引导项
    FIRST_ENTRY=$(grep -i "menuentry " /boot/grub/grub.cfg | grep -i windows | head -n1 | sed -n 's/.*menuentry \+"\([^"]*\)".*/\1/p')
    
    if [ -z "$FIRST_ENTRY" ]; then
        print_msg "$RED" "错误：无法提取Windows引导项名称"
        return 1
    fi
    
    print_msg "$YELLOW" "将使用引导项: '$FIRST_ENTRY'"
    print_msg "$YELLOW" "注意：此操作不会实际重启系统，仅设置下次启动项"
    
    # 询问是否继续
    read -p "是否继续测试grub-reboot? (y/n): " choice
    if [[ "$choice" != "y" && "$choice" != "Y" ]]; then
        print_msg "$BLUE" "已取消测试"
        return 0
    fi
    
    # 测试设置
    if grub-reboot "$FIRST_ENTRY"; then
        print_msg "$GREEN" "成功设置下次启动为: '$FIRST_ENTRY'"
        
        # 显示GRUB环境文件
        if [ -f /boot/grub/grubenv ]; then
            print_msg "$BLUE" "GRUB环境文件内容:"
            cat /boot/grub/grubenv
        fi
    else
        print_msg "$RED" "设置失败，错误代码: $?"
        return 1
    fi
    
    return 0
}

# 函数：检查标志文件
check_flag_file() {
    print_msg "$BLUE" "检查标志文件..."
    
    # 确保挂载点存在
    if [ ! -d "/mnt/windows" ]; then
        mkdir -p /mnt/windows
        print_msg "$YELLOW" "已创建挂载点: /mnt/windows"
    fi
    
    # 检查挂载状态
    if ! mountpoint -q /mnt/windows; then
        print_msg "$YELLOW" "共享分区未挂载，尝试挂载..."
        
        # 查找共享分区
        SHARED_PART=$(blkid | grep -i "LABEL=\"SHARED\"" | cut -d: -f1)
        
        if [ -n "$SHARED_PART" ]; then
            mount "$SHARED_PART" /mnt/windows
            if [ $? -eq 0 ]; then
                print_msg "$GREEN" "已挂载共享分区: $SHARED_PART"
            else
                print_msg "$RED" "无法挂载共享分区"
                return 1
            fi
        else
            print_msg "$RED" "找不到共享分区"
            return 1
        fi
    else
        print_msg "$GREEN" "共享分区已挂载"
    fi
    
    # 检查标志文件
    FLAG_FILE="/mnt/windows/go-ubuntu.flag"
    if [ -f "$FLAG_FILE" ]; then
        print_msg "$GREEN" "发现标志文件: $FLAG_FILE"
        print_msg "$BLUE" "内容: $(cat "$FLAG_FILE")"
        
        # 询问是否删除
        read -p "是否删除标志文件? (y/n): " choice
        if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
            rm -f "$FLAG_FILE"
            if [ $? -eq 0 ]; then
                print_msg "$GREEN" "标志文件已删除"
            else
                print_msg "$RED" "无法删除标志文件"
                return 1
            fi
        fi
    else
        print_msg "$YELLOW" "未找到标志文件"
        
        # 询问是否创建
        read -p "是否创建测试标志文件? (y/n): " choice
        if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
            echo "Test flag created on $(date)" > "$FLAG_FILE"
            if [ $? -eq 0 ]; then
                print_msg "$GREEN" "已创建测试标志文件"
            else
                print_msg "$RED" "无法创建标志文件"
                return 1
            fi
        fi
    fi
    
    return 0
}

# 函数：测试切换器脚本
test_switcher_script() {
    print_msg "$BLUE" "测试切换器脚本..."
    
    # 检查脚本是否存在
    if [ ! -f "/usr/local/bin/ubuntu-windows-switcher.sh" ]; then
        print_msg "$RED" "错误：切换器脚本不存在"
        return 1
    fi
    
    # 询问是否运行
    print_msg "$YELLOW" "注意：如果标志文件存在，此测试将导致系统重启"
    read -p "是否继续测试切换器脚本? (y/n): " choice
    if [[ "$choice" != "y" && "$choice" != "Y" ]]; then
        print_msg "$BLUE" "已取消测试"
        return 0
    fi
    
    # 运行脚本
    print_msg "$BLUE" "运行切换器脚本..."
    /usr/local/bin/ubuntu-windows-switcher.sh
    
    return 0
}

# 主菜单
show_menu() {
    clear
    print_msg "$BLUE" "========================================"
    print_msg "$BLUE" "   Ubuntu/Windows切换器测试工具"
    print_msg "$BLUE" "========================================"
    echo ""
    echo "1. 检查GRUB配置"
    echo "2. 测试GRUB引导设置"
    echo "3. 检查/创建标志文件"
    echo "4. 测试切换器脚本"
    echo "5. 全部测试"
    echo "0. 退出"
    echo ""
    read -p "请选择操作 [0-5]: " choice
    
    case $choice in
        1) check_grub_config ;;
        2) test_grub_reboot ;;
        3) check_flag_file ;;
        4) test_switcher_script ;;
        5)
            check_grub_config
            echo ""
            test_grub_reboot
            echo ""
            check_flag_file
            echo ""
            read -p "是否继续测试切换器脚本? (y/n): " run_script
            if [[ "$run_script" == "y" || "$run_script" == "Y" ]]; then
                test_switcher_script
            fi
            ;;
        0) exit 0 ;;
        *) print_msg "$RED" "无效选择" ;;
    esac
    
    echo ""
    read -p "按回车键返回主菜单..."
    show_menu
}

# 主程序
check_root
show_menu 