# 🚀 Windows/Ubuntu Switcher 项目设置指南

## 📋 项目概述

Windows/Ubuntu自动切换器是一个用于Windows和Ubuntu双系统之间一键切换的工具。该项目目前处于Beta开发阶段，主要功能已经实现，但仍在不断完善中。

## 🎯 快速开始

### 方法1：使用项目管理器（推荐）

#### Windows用户
```bash
# 双击运行
start_project_manager.bat

# 或者在命令行中运行
start_project_manager.bat
```

#### Linux/Unix用户
```bash
# 给脚本执行权限
chmod +x start_project_manager.sh

# 运行脚本
./start_project_manager.sh
```

### 方法2：手动运行

```bash
# 直接运行主脚本
python scripts/start_here.py
```

## 🔧 项目设置步骤

### 第一步：环境检查
项目管理器会自动检查：
- Python 3.6+ 是否已安装
- Git 是否已安装
- 项目文件结构是否完整

### 第二步：快速启动
选择 "🚀 Quick Start" 选项：
- 创建虚拟环境
- 安装Python依赖
- 运行基本测试
- 显示项目信息

### 第三步：Git初始化
选择 "🔧 Initialize Git Repository" 选项：
- 初始化Git仓库
- 配置用户信息
- 设置远程仓库
- 创建初始提交

### 第四步：更新README
选择 "📝 Update README with project info" 选项：
- 添加项目徽章
- 更新GitHub链接
- 配置项目信息

### 第五步：发布到GitHub
选择 "🌐 Publish to GitHub" 选项：
- 检查项目状态
- 推送到GitHub
- 显示后续步骤

## 📁 项目结构

```
windows_ubuntu_switcher/
├── 📁 scripts/                    # 项目管理脚本
│   ├── start_here.py             # 主启动脚本
│   ├── quick_start.py            # 快速启动脚本
│   ├── init_git.py               # Git初始化脚本
│   ├── update_readme.py          # README更新脚本
│   ├── prepare_release.py        # 发布准备脚本
│   └── publish_to_github.py      # GitHub发布脚本
├── 📁 docs/                       # 项目文档
│   ├── project_status.md         # 项目状态
│   ├── project_badges.md         # 项目徽章
│   └── release_checklist.md      # 发布检查清单
├── 📁 tests/                      # 测试文件
├── 📁 windows_ubuntu_switcher/   # 主程序包
├── 📄 README.md                   # 项目说明
├── 📄 CONTRIBUTING.md             # 贡献指南
├── 📄 LICENSE                     # 许可证文件
├── 📄 requirements.txt            # Python依赖
├── 📄 setup.py                    # 安装配置
├── 🚀 start_project_manager.bat   # Windows启动脚本
└── 🚀 start_project_manager.sh    # Linux启动脚本
```

## 🛠️ 可用脚本说明

### 主要脚本

| 脚本 | 功能 | 使用场景 |
|------|------|----------|
| `start_here.py` | 项目管理器主界面 | 日常项目管理 |
| `quick_start.py` | 快速环境设置 | 首次使用项目 |
| `init_git.py` | Git仓库初始化 | 设置版本控制 |
| `update_readme.py` | README文件更新 | 配置项目信息 |
| `prepare_release.py` | 发布准备 | 版本发布前 |
| `publish_to_github.py` | GitHub发布 | 推送到GitHub |

### 启动脚本

| 平台 | 脚本 | 说明 |
|------|------|------|
| Windows | `start_project_manager.bat` | 双击运行，自动检测Python |
| Linux/Unix | `start_project_manager.sh` | 需要执行权限，支持Python3 |

## 📚 文档说明

### 核心文档

- **README.md**: 项目概述、安装和使用说明
- **README_zh.md**: 中文版本的项目说明
- **CONTRIBUTING.md**: 如何贡献代码和报告问题
- **LICENSE**: MIT开源许可证

### 详细文档

- **docs/project_status.md**: 当前开发状态和路线图
- **docs/project_badges.md**: 项目徽章配置说明
- **docs/release_checklist.md**: 发布前检查清单
- **install_guide.md**: 详细安装指南
- **plan.md**: 项目开发计划

## 🔍 项目状态检查

使用项目管理器的 "🔍 Check Project Status" 选项可以：

- 检查必需文件是否存在
- 验证Git仓库状态
- 检查Python环境配置
- 显示缺失的文件和配置

## 🚨 常见问题

### Python版本问题
- 确保安装Python 3.6或更高版本
- 检查Python是否在系统PATH中

### Git配置问题
- 确保Git已正确安装
- 配置Git用户名称和邮箱
- 检查网络连接和GitHub访问

### 依赖安装问题
- 使用虚拟环境避免冲突
- 检查pip是否可用
- 尝试使用pip3命令

### 权限问题
- Windows: 以管理员身份运行
- Linux: 检查脚本执行权限
- 确保对项目目录有写入权限

## 🎯 下一步计划

### 短期目标（1-2周）
- [ ] 修复已知bug
- [ ] 完善错误处理
- [ ] 增加基本测试
- [ ] 优化安装脚本

### 中期目标（1个月）
- [ ] 完善测试覆盖
- [ ] 优化用户体验
- [ ] 增加配置选项
- [ ] 完善文档

### 长期目标（2-3个月）
- [ ] 发布v1.0稳定版
- [ ] 支持更多Linux发行版
- [ ] 增加高级功能
- [ ] 社区反馈整合

## 🤝 获取帮助

### 项目内帮助
- 使用项目管理器的 "🆘 Help & Support" 选项
- 查看各个脚本的代码注释
- 阅读文档文件夹中的详细说明

### 外部资源
- GitHub Issues: 报告bug和请求功能
- GitHub Discussions: 讨论项目相关问题
- 项目Wiki: 详细使用说明（如果启用）

## 📞 联系方式

- 项目维护者: [你的名字]
- 邮箱: [你的邮箱]
- GitHub: [你的GitHub用户名]

---

*祝你的Windows/Ubuntu切换器项目开发顺利！🚀*
