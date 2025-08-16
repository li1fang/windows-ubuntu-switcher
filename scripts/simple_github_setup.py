#!/usr/bin/env python3
"""
Simple GitHub setup script - 简化版
"""

import os
import subprocess

def run(cmd):
    """运行命令并显示结果"""
    print(f"🔧 {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ 成功: {result.stdout.strip()}")
    else:
        print(f"❌ 失败: {result.stderr.strip()}")
    return result.returncode == 0

def main():
    print("🚀 简化版 GitHub 设置")
    print("=" * 30)
    
    # 1. 检查 Git
    if not run("git --version"):
        print("请先安装 Git: https://git-scm.com/")
        return
    
    # 2. 初始化仓库
    if os.path.exists(".git"):
        print("✅ Git 仓库已存在")
    else:
        run("git init")
    
    # 3. 添加文件
    run("git add .")
    
    # 4. 创建提交
    run('git commit -m "Initial commit"')
    
    # 5. 设置主分支
    run("git branch -M main")
    
    print("\n🎉 基础设置完成！")
    print("\n下一步：")
    print("1. 在 GitHub 上创建新仓库")
    print("2. 运行: git remote add origin <你的仓库URL>")
    print("3. 运行: git push -u origin main")
    
    # 6. 尝试打开 GitHub
    print("\n🌐 是否要打开 GitHub 创建仓库？")
    choice = input("输入 'y' 打开浏览器，其他键跳过: ").strip().lower()
    if choice == 'y':
        run("start https://github.com/new")

if __name__ == "__main__":
    main()
