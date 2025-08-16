# 发布检查清单

## 🚀 发布前检查

在发布新版本之前，请确保完成以下检查项：

### 📋 代码质量检查

- [ ] 所有测试通过 (`python -m pytest tests/ -v`)
- [ ] 代码风格检查通过 (`flake8 windows_ubuntu_switcher/`)
- [ ] 没有明显的bug或错误
- [ ] 代码注释完整
- [ ] 函数和变量命名规范

### 🔧 功能测试

- [ ] Windows端功能正常
  - [ ] GUI界面显示正常
  - [ ] 系统切换功能正常
  - [ ] 错误处理正常
- [ ] Ubuntu端功能正常
  - [ ] 服务脚本运行正常
  - [ ] 自动切换功能正常
  - [ ] 权限设置正确
- [ ] 安装脚本正常
  - [ ] Windows安装脚本
  - [ ] Ubuntu安装脚本

### 📚 文档检查

- [ ] README.md 更新完整
- [ ] 安装指南清晰
- [ ] 使用说明详细
- [ ] 故障排除指南完整
- [ ] 贡献指南清晰
- [ ] 许可证文件正确

### 🧪 测试覆盖

- [ ] 基本功能测试
- [ ] 错误情况测试
- [ ] 边界条件测试
- [ ] 性能测试（如适用）
- [ ] 兼容性测试

### 📦 打包检查

- [ ] `setup.py` 配置正确
- [ ] `requirements.txt` 依赖完整
- [ ] 版本号更新
- [ ] 包名称正确
- [ ] 作者信息正确

## 🏷️ 版本发布步骤

### 1. 准备发布

```bash
# 运行发布准备脚本
python scripts/prepare_release.py

# 或者手动执行以下步骤：
# 1. 更新版本号
# 2. 创建发布提交
# 3. 创建发布标签
```

### 2. 推送到GitHub

```bash
# 推送代码和标签
git push origin main --tags

# 验证推送成功
git ls-remote --tags origin
```

### 3. 创建GitHub Release

- 访问 GitHub 仓库页面
- 点击 "Releases" 或 "Tags"
- 点击最新标签的 "Create release from tag"
- 使用发布模板填写信息
- 上传构建的包文件（如果有）
- 发布

### 4. 发布后检查

- [ ] GitHub Release 创建成功
- [ ] 下载链接正常
- [ ] 发布说明清晰
- [ ] 标签正确

## 🔍 发布后验证

### 用户安装测试

- [ ] 从源码安装正常
- [ ] 依赖安装正确
- [ ] 基本功能运行正常

### 文档链接检查

- [ ] README 中的链接正常
- [ ] 文档页面可访问
- [ ] 示例代码可运行

### 社区反馈

- [ ] 监控 Issues 反馈
- [ ] 响应 Pull Requests
- [ ] 更新文档（如需要）

## 🚨 紧急修复流程

如果发布后发现严重问题：

### 1. 立即响应

- 在 GitHub Issues 中标记问题
- 在 README 中添加已知问题说明
- 考虑回滚到上一个版本

### 2. 快速修复

- 创建修复分支
- 修复问题
- 增加回归测试
- 创建补丁版本

### 3. 重新发布

- 更新版本号
- 创建新的发布
- 通知用户更新

## 📊 发布统计

记录每次发布的信息：

| 版本 | 发布日期 | 主要功能 | 已知问题 | 状态 |
|------|----------|----------|----------|------|
| v1.0.0 | YYYY-MM-DD | 基本功能完成 | 无 | ✅ 稳定 |
| v0.9.0 | YYYY-MM-DD | Beta测试版 | 5个已知问题 | 🔄 测试中 |

## 🎯 发布目标

### v1.0.0 目标
- [ ] 所有核心功能稳定
- [ ] 测试覆盖率达到80%+
- [ ] 文档完整
- [ ] 用户反馈良好

### v1.1.0 目标
- [ ] 性能优化
- [ ] 新功能添加
- [ ] 用户体验改进
- [ ] 社区反馈整合

## 📞 发布支持

如果在发布过程中遇到问题：

1. 检查 [GitHub Actions](https://github.com/yourusername/windows-ubuntu-switcher/actions) 状态
2. 查看 [Issues](https://github.com/yourusername/windows-ubuntu-switcher/issues) 中的已知问题
3. 在 [Discussions](https://github.com/yourusername/windows-ubuntu-switcher/discussions) 中寻求帮助
4. 联系项目维护者

---

*保持发布质量，为用户提供可靠的软件*
