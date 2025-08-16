#!/bin/bash
# ubuntu-windows-switcher.sh
# 
# Ubuntu/Windows切换器脚本 - 增强版
# 在Ubuntu启动时检查标志文件，如果存在则设置下次启动为Windows并重启

# 配置
FLAG_FILE="/mnt/windows/go-ubuntu.flag"
LOG_FILE="/var/log/ubuntu-windows-switcher.log"
WINDOWS_GRUB_ENTRY="Windows Boot Manager"  # 根据实际GRUB菜单调整
GRUB_CONFIG="/boot/grub/grub.cfg"

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# 检查GRUB配置函数
check_grub_config() {
    log "检查GRUB配置..."
    
    if [ ! -f "$GRUB_CONFIG" ]; then
        log "错误：找不到GRUB配置文件: $GRUB_CONFIG"
        return 1
    fi
    
    # 查找所有Windows引导条目
    WINDOWS_ENTRIES=$(grep -i "menuentry " "$GRUB_CONFIG" | grep -i windows)
    
    if [ -z "$WINDOWS_ENTRIES" ]; then
        log "错误：在GRUB配置中找不到Windows引导项"
        return 1
    fi
    
    log "找到以下Windows引导项:"
    echo "$WINDOWS_ENTRIES" | tee -a "$LOG_FILE"
    
    # 验证当前配置的Windows引导项是否存在
    if ! grep -q "$WINDOWS_GRUB_ENTRY" "$GRUB_CONFIG"; then
        log "警告：配置的Windows引导项'$WINDOWS_GRUB_ENTRY'在GRUB配置中不存在"
        
        # 提取第一个Windows引导项作为新的默认项
        NEW_ENTRY=$(echo "$WINDOWS_ENTRIES" | head -n1 | sed -n 's/.*menuentry \+"\([^"]*\)".*/\1/p')
        if [ -n "$NEW_ENTRY" ]; then
            log "建议使用引导项: '$NEW_ENTRY'"
            WINDOWS_GRUB_ENTRY="$NEW_ENTRY"
        fi
    else
        log "配置的Windows引导项存在于GRUB配置中"
    fi
    
    return 0
}

# 检查脚本是否以root权限运行
if [ "$(id -u)" -ne 0 ]; then
    log "错误：此脚本需要root权限运行"
    exit 1
fi

# 检查并验证GRUB配置
check_grub_config

# 检查挂载点并挂载共享分区（如果未挂载）
if ! mountpoint -q /mnt/windows; then
    # 确保挂载点存在
    mkdir -p /mnt/windows
    
    # 查找共享分区
    SHARED_PART=$(blkid | grep -i "LABEL=\"SHARED\"" | cut -d: -f1)
    
    if [ -n "$SHARED_PART" ]; then
        mount "$SHARED_PART" /mnt/windows
        log "已挂载共享分区: $SHARED_PART"
    else
        log "错误：找不到共享分区"
        exit 1
    fi
fi

# 检查标志文件
if [ -f "$FLAG_FILE" ]; then
    log "检测到标志文件，准备切换到Windows"
    log "标志文件内容: $(cat "$FLAG_FILE")"
    
    # 删除标志文件
    rm -f "$FLAG_FILE"
    if [ $? -ne 0 ]; then
        log "错误：无法删除标志文件"
        exit 1
    fi
    log "标志文件已删除"
    
    # 获取GRUB默认启动项
    current_default=$(grep -i "^GRUB_DEFAULT=" /etc/default/grub | cut -d= -f2 | tr -d '"')
    log "当前GRUB默认启动项: $current_default"
    
    # 设置下次启动为Windows - 多方法尝试
    log "尝试设置下次启动为Windows: '$WINDOWS_GRUB_ENTRY'"
    if grub-reboot "$WINDOWS_GRUB_ENTRY"; then
        log "成功设置下次启动为: '$WINDOWS_GRUB_ENTRY'"
    else
        log "使用默认GRUB条目失败，尝试查找Windows引导项..."
        
        # 查找所有Windows引导条目
        WINDOWS_ENTRIES=$(grep -i "menuentry " "$GRUB_CONFIG" | grep -i windows)
        
        if [ -n "$WINDOWS_ENTRIES" ]; then
            # 提取第一个Windows引导项名称
            FIRST_ENTRY=$(echo "$WINDOWS_ENTRIES" | head -n1 | sed -n 's/.*menuentry \+"\([^"]*\)".*/\1/p')
            log "尝试使用引导项: '$FIRST_ENTRY'"
            
            if grub-reboot "$FIRST_ENTRY"; then
                log "成功设置下次启动为: '$FIRST_ENTRY'"
            else
                # 最后尝试使用菜单索引
                log "使用引导项名称失败，尝试使用菜单索引..."
                MENU_INDEX=$(grep -n -i "windows" "$GRUB_CONFIG" | head -n1 | cut -d: -f1)
                
                if [ -n "$MENU_INDEX" ]; then
                    MENU_INDEX=$((MENU_INDEX - 1))
                    if grub-reboot "$MENU_INDEX"; then
                        log "成功使用菜单索引($MENU_INDEX)设置下次启动"
                    else
                        log "错误：所有设置方法均失败"
                        exit 1
                    fi
                else
                    log "错误：无法找到Windows引导项索引"
                    exit 1
                fi
            fi
        else
            log "错误：在GRUB配置中找不到Windows引导项"
            exit 1
        fi
    fi
    
    # 确认GRUB设置是否生效
    log "确认GRUB设置是否生效..."
    if [ -f /boot/grub/grubenv ]; then
        log "GRUB环境内容:"
        cat /boot/grub/grubenv | tee -a "$LOG_FILE"
    fi
    
    log "已设置下次启动为Windows，系统将在3秒后重启..."
    sleep 3
    reboot
else
    log "未检测到标志文件，正常启动Ubuntu"
fi

exit 0