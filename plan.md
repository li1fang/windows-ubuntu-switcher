# Windows/Ubuntu自动切换器修复计划

## 项目概述
Windows/Ubuntu自动切换器是一个用于在双系统环境中实现自动切换的工具。工具由两部分组成：
1. Windows端GUI应用程序（Python实现）
2. Ubuntu端服务脚本（Bash实现）

## 当前问题
1. **GRUB引导问题**：重装Linux后，GRUB自动引导失效，无法正确进入Linux
2. **Linux设置问题**：在Linux上的设置可能存在问题，导致系统无法正确切换
3. **冗余代码**：当前脚本包含冗余代码，降低了维护性
4. **WSL2部署**：尝试使用WSL2修改和部署Linux部分失败，需要清理相关代码

## 修复步骤

### 1. 清理项目和WSL2相关文件
- 清理与WSL2部署相关的文件和配置
- 整理项目结构，移除无关文件

### 2. 优化Windows组件
- 保留S盘作为共享存储中心
- 增强Windows脚本的错误处理，提高S盘访问的稳定性
- 测试GUI界面和切换功能

### 3. 改进Ubuntu脚本
- 简化ubuntu-windows-switcher.sh脚本
- 改进GRUB引导项检测和设置逻辑
- 加强日志记录和错误处理
- 确保脚本有足够权限执行GRUB相关操作

### 4. 修复GRUB引导
- 详细检查GRUB配置文件，确认Windows启动项的准确名称
- 验证grub-reboot命令正确功能
- 检查GRUB默认引导设置
- 确保适当的启动顺序

### 5. 开发API和系统集成
- 创建简单的命令行API
- 为Windows添加任务栏集成
- 为Ubuntu添加系统菜单集成

### 6. 测试和文档
- 全面测试双向切换功能
- 编写完整的安装和使用文档
- 准备GitHub发布

## 实施时间表
1. 清理项目：1天
2. 优化Windows组件：1天
3. 改进Ubuntu脚本：1-2天
4. 修复GRUB引导：2-3天
5. 开发API和系统集成：2-3天
6. 测试和文档：1-2天

总计：8-12天

## 技术细节
### 共享存储策略
- 保留S盘作为共享存储中心
- 标志文件路径：
  - Windows端：`S:\go-ubuntu.flag`
  - Ubuntu端：`/mnt/windows/go-ubuntu.flag`（基于挂载的共享分区）

### GRUB引导检测改进
采用多重方法检测Windows启动项：
1. 首先使用配置的启动项名称
2. 若失败，则搜索所有包含"Windows"的启动项
3. 最后尝试使用菜单索引方法

### GRUB配置检查要点
- 确认`/boot/grub/grub.cfg`中Windows启动项的准确名称
- 验证GRUB默认引导配置
- 测试手动执行`grub-reboot`命令效果
- 检查GRUB超时设置

### 系统集成方案
- Windows：使用系统托盘图标集成
- Ubuntu：创建桌面快捷方式和系统菜单项 