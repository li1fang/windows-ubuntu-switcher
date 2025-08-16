# Windows/Ubuntu自动切换系统安装指南

本指南将帮助你设置Windows/Ubuntu自动切换系统，使你能够通过简单的GUI应用程序在Windows和Ubuntu之间自动切换。

## 系统要求

- Windows 10/11操作系统
- Ubuntu 20.04或更高版本
- 共享NTFS分区（用于存放标志文件）
- Python 3.6或更高版本（Windows端）

## 一、磁盘分区设置

### Windows端操作

1. 打开磁盘管理工具：
   - 按下`Win + R`，输入`diskmgmt.msc`，点击确定

2. 对第3个分区（当前为ext4，186.26 GB）进行操作：
   - 右键点击该分区，选择"删除卷"（注意：这将删除分区上的所有数据！）
   - 在释放的空间上右键点击，选择"新建简单卷"
   - 按照向导操作，选择NTFS文件系统
   - 分配盘符E:
   - 设置卷标为"SHARED"

3. 对第4块未分配区域（394.02 GB）进行操作：
   - 右键点击未分配区域，选择"新建简单卷"
   - 按照向导操作，选择NTFS文件系统
   - 分配合适的盘符（如F:）
   - 设置卷标为"WSL_STORAGE"

### Ubuntu端操作

1. 创建挂载点目录：
   ```bash
   sudo mkdir -p /mnt/windows
   ```

2. 编辑/etc/fstab文件，添加自动挂载配置：
   ```bash
   sudo nano /etc/fstab
   ```

3. 添加以下行（根据实际情况调整UUID）：
   ```
   # Windows共享分区
   UUID=<分区UUID> /mnt/windows ntfs defaults,auto,rw,users 0 0
   ```

4. 查找分区UUID：
   ```bash
   sudo blkid | grep SHARED
   ```

5. 挂载分区：
   ```bash
   sudo mount -a
   ```

6. 设置适当的权限：
   ```bash
   sudo chmod 777 /mnt/windows
   ```

## 二、Windows端Python GUI应用程序安装

1. 确保已安装Python 3.6或更高版本：
   - 打开命令提示符，输入`python --version`检查
   - 如果未安装，从[Python官网](https://www.python.org/downloads/)下载并安装

2. 复制应用程序文件：
   - 将`windows_ubuntu_switcher`文件夹复制到合适的位置（如`C:\Program Files`或用户目录）

3. 创建桌面快捷方式：
   - 右键点击桌面，选择"新建" -> "快捷方式"
   - 输入以下命令（根据实际路径调整）：
     ```
     pythonw.exe "C:\Path\to\windows_ubuntu_switcher\main.py"
     ```
   - 为快捷方式命名为"Windows/Ubuntu切换器"
   - 右键点击快捷方式，选择"属性"，点击"更改图标"，选择一个合适的图标

4. （可选）设置开机自启动：
   - 按下`Win + R`，输入`shell:startup`，点击确定
   - 将桌面上创建的快捷方式复制到打开的启动文件夹中

## 三、Ubuntu端自动化脚本安装

1. 复制脚本文件到系统目录：
   ```bash
   sudo cp ubuntu-windows-switcher.sh /usr/local/bin/
   sudo chmod +x /usr/local/bin/ubuntu-windows-switcher.sh
   ```

2. 安装systemd服务：
   ```bash
   sudo cp ubuntu-windows-switcher.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable ubuntu-windows-switcher.service
   ```

3. 测试脚本：
   ```bash
   sudo /usr/local/bin/ubuntu-windows-switcher.sh
   ```

4. 确认GRUB配置：
   - 检查Windows在GRUB菜单中的条目名称：
     ```bash
     grep -i "menuentry " /boot/grub/grub.cfg | grep -i windows
     ```
   - 如果需要，编辑脚本中的`WINDOWS_GRUB_ENTRY`变量：
     ```bash
     sudo nano /usr/local/bin/ubuntu-windows-switcher.sh
     ```

## 四、测试系统

1. 在Windows中：
   - 启动"Windows/Ubuntu切换器"应用程序
   - 点击"切换到Ubuntu"按钮
   - 确认对话框中点击"是"
   - 系统应该会重启并进入Ubuntu

2. 在Ubuntu中：
   - 系统应该会自动检测到标志文件
   - 删除标志文件并设置下次启动为Windows
   - 自动重启回到Windows

3. 检查日志文件：
   - Windows: `windows_ubuntu_switcher.log`（在应用程序目录中）
   - Ubuntu: `/var/log/ubuntu-windows-switcher.log`

## 故障排除

### Windows端问题

1. 应用程序无法启动：
   - 检查Python是否正确安装
   - 检查应用程序文件路径是否正确
   - 查看日志文件中的错误信息

2. 无法创建标志文件：
   - 确保E盘已正确挂载
   - 检查写入权限
   - 尝试以管理员身份运行应用程序

### Ubuntu端问题

1. 脚本未自动运行：
   - 检查systemd服务是否已启用：
     ```bash
     sudo systemctl status ubuntu-windows-switcher.service
     ```
   - 查看日志文件中的错误信息

2. 无法切换回Windows：
   - 检查GRUB配置中Windows的条目名称
   - 尝试使用菜单索引而不是名称
   - 确保grub-reboot命令可用：
     ```bash
     which grub-reboot
     ```

3. 共享分区未挂载：
   - 检查/etc/fstab配置
   - 手动挂载分区：
     ```bash
     sudo mount /mnt/windows
     ```
   - 检查分区UUID是否正确

## 安全注意事项

1. 备份重要数据：
   - 在进行分区操作前，确保备份所有重要数据

2. 创建系统恢复点：
   - 在Windows中创建系统恢复点，以便在出现问题时恢复

3. 准备应急启动U盘：
   - 创建一个可启动的Ubuntu Live USB，以便在启动问题时进行修复