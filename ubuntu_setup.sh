#!/bin/bash
# Ubuntu/Windows自动切换系统 - Ubuntu端自动部署脚本

echo "Ubuntu/Windows自动切换系统 - Ubuntu端自动部署脚本"
echo "=================================================="
echo

# 检查是否以root权限运行
if [ "$(id -u)" -ne 0 ]; then
    echo "[错误] 此脚本需要root权限运行"
    echo "请使用sudo运行此脚本: sudo ./ubuntu_setup.sh"
    exit 1
fi

# 创建挂载点目录
echo "创建挂载点目录..."
mkdir -p /mnt/windows
if [ $? -ne 0 ]; then
    echo "[错误] 创建挂载点目录失败"
    exit 1
fi
echo "[成功] 挂载点目录已创建: /mnt/windows"

# 查找共享分区
echo "查找共享分区..."
SHARED_PART=$(blkid | grep -i "LABEL=\"SHARED\"" | cut -d: -f1)
if [ -z "$SHARED_PART" ]; then
    echo "[警告] 未找到标签为SHARED的分区"
    echo "请手动输入共享分区的设备路径（例如/dev/sda3）:"
    read SHARED_PART
    if [ -z "$SHARED_PART" ]; then
        echo "[错误] 未提供分区路径"
        exit 1
    fi
fi
echo "[成功] 找到共享分区: $SHARED_PART"

# 获取分区UUID
SHARED_UUID=$(blkid -s UUID -o value $SHARED_PART)
if [ -z "$SHARED_UUID" ]; then
    echo "[错误] 无法获取分区UUID"
    exit 1
fi
echo "[成功] 分区UUID: $SHARED_UUID"

# 配置自动挂载
echo "配置自动挂载..."
if grep -q "/mnt/windows" /etc/fstab; then
    echo "[警告] /etc/fstab中已存在/mnt/windows的挂载配置"
else
    echo "# Windows共享分区" >> /etc/fstab
    echo "UUID=$SHARED_UUID /mnt/windows ntfs defaults,auto,rw,users 0 0" >> /etc/fstab
    echo "[成功] 已添加自动挂载配置到/etc/fstab"
fi

# 挂载分区
echo "挂载共享分区..."
mount -a
if [ $? -ne 0 ]; then
    echo "[警告] 挂载分区失败，请检查/etc/fstab配置"
else
    echo "[成功] 共享分区已挂载"
fi

# 设置权限
echo "设置分区权限..."
chmod 777 /mnt/windows
if [ $? -ne 0 ]; then
    echo "[警告] 设置权限失败"
else
    echo "[成功] 已设置分区权限"
fi

# 复制脚本到系统目录
echo "复制启动脚本到系统目录..."
cp ubuntu-windows-switcher.sh /usr/local/bin/
if [ $? -ne 0 ]; then
    echo "[错误] 复制脚本失败"
    exit 1
fi
chmod +x /usr/local/bin/ubuntu-windows-switcher.sh
echo "[成功] 脚本已复制到/usr/local/bin/"

# 安装systemd服务
echo "安装systemd服务..."
cp ubuntu-windows-switcher.service /etc/systemd/system/
if [ $? -ne 0 ]; then
    echo "[错误] 复制服务文件失败"
    exit 1
fi
systemctl daemon-reload
systemctl enable ubuntu-windows-switcher.service
if [ $? -ne 0 ]; then
    echo "[警告] 启用服务失败"
else
    echo "[成功] 服务已启用"
fi

# 查找Windows启动项
echo "查找GRUB中的Windows启动项..."
WINDOWS_ENTRIES=$(grep -i "menuentry " /boot/grub/grub.cfg | grep -i windows)
if [ -z "$WINDOWS_ENTRIES" ]; then
    echo "[警告] 未找到Windows启动项，请手动检查GRUB配置"
else
    echo "找到以下Windows启动项:"
    echo "$WINDOWS_ENTRIES"
    
    # 提取第一个Windows启动项的名称
    WINDOWS_ENTRY=$(echo "$WINDOWS_ENTRIES" | head -n 1 | sed -n 's/.*menuentry \+"\([^"]*\)".*/\1/p')
    if [ -n "$WINDOWS_ENTRY" ]; then
        echo "将使用启动项: $WINDOWS_ENTRY"
        
        # 更新脚本中的Windows启动项名称
        sed -i "s/WINDOWS_GRUB_ENTRY=\"Windows Boot Manager\"/WINDOWS_GRUB_ENTRY=\"$WINDOWS_ENTRY\"/" /usr/local/bin/ubuntu-windows-switcher.sh
        echo "[成功] 已更新脚本中的Windows启动项名称"
    fi
fi

# 测试grub-reboot命令
echo "测试grub-reboot命令..."
which grub-reboot > /dev/null
if [ $? -ne 0 ]; then
    echo "[警告] 未找到grub-reboot命令，请确保已安装grub2"
else
    echo "[成功] grub-reboot命令可用"
fi

# 创建日志目录
echo "创建日志目录..."
touch /var/log/ubuntu-windows-switcher.log
chmod 666 /var/log/ubuntu-windows-switcher.log
echo "[成功] 日志文件已创建: /var/log/ubuntu-windows-switcher.log"

echo
echo "Ubuntu端部署完成！"
echo "系统将在下次启动时自动检查标志文件并执行相应操作。"
echo
echo "您可以通过以下命令手动测试脚本:"
echo "sudo /usr/local/bin/ubuntu-windows-switcher.sh"
echo
echo "要查看日志，请使用:"
echo "cat /var/log/ubuntu-windows-switcher.log"
echo

# 询问是否立即测试
echo "是否立即测试脚本？(y/n)"
read TEST_NOW
if [ "$TEST_NOW" = "y" ] || [ "$TEST_NOW" = "Y" ]; then
    echo "运行测试..."
    /usr/local/bin/ubuntu-windows-switcher.sh
fi

echo "设置完成！"