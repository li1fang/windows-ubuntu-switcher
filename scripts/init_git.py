#!/usr/bin/env python3
"""
Git repository initialization script for Windows/Ubuntu Switcher
"""

import os
import sys
import subprocess
import getpass
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_installed():
    """Check if git is installed"""
    success, stdout, stderr = run_command("git --version")
    if not success:
        print("❌ Git is not installed or not in PATH")
        print("Please install Git from: https://git-scm.com/")
        return False
    
    print(f"✅ Git version: {stdout.strip()}")
    return True

def init_git_repo():
    """Initialize git repository"""
    if os.path.exists(".git"):
        print("✅ Git repository already exists")
        return True
    
    success, stdout, stderr = run_command("git init")
    if not success:
        print(f"❌ Failed to initialize git repository: {stderr}")
        return False
    
    print("✅ Git repository initialized")
    return True

def configure_git_user():
    """Configure git user information"""
    print("\n🔧 Configuring Git user information...")
    
    # Check if running in interactive mode
    if not sys.stdin.isatty():
        print("⚠️  Running in non-interactive mode, using default values")
        print("To configure Git user manually, run: git config --global user.name 'Your Name'")
        print("To configure Git email manually, run: git config --global user.email 'your.email@example.com'")
        return True
    
    # Get user input
    name = input("Enter your name: ").strip()
    if not name:
        print("❌ Name is required")
        return False
    
    email = input("Enter your email: ").strip()
    if not email:
        print("❌ Email is required")
        return False
    
    # Configure git
    success, stdout, stderr = run_command(f'git config user.name "{name}"')
    if not success:
        print(f"❌ Failed to set user name: {stderr}")
        return False
    
    success, stdout, stderr = run_command(f'git config user.email "{email}"')
    if not success:
        print(f"❌ Failed to set user email: {stderr}")
        return False
    
    print("✅ Git user configured")
    return True

def add_remote_origin():
    """Add remote origin"""
    print("\n🌐 Configuring remote origin...")
    
    # Check if running in interactive mode
    if not sys.stdin.isatty():
        print("⚠️  Running in non-interactive mode, skipping remote origin")
        print("To add remote origin manually, run: git remote add origin <your-repo-url>")
        return True
    
    repo_url = input("Enter GitHub repository URL (e.g., https://github.com/username/repo.git): ").strip()
    if not repo_url:
        print("⚠️  Skipping remote origin configuration")
        return True
    
    success, stdout, stderr = run_command(f'git remote add origin "{repo_url}"')
    if not success:
        print(f"❌ Failed to add remote origin: {stderr}")
        return False
    
    print("✅ Remote origin added")
    return True

def create_initial_commit():
    """Create initial commit"""
    print("\n📝 Creating initial commit...")
    
    # Add all files
    success, stdout, stderr = run_command("git add .")
    if not success:
        print(f"❌ Failed to add files: {stderr}")
        return False
    
    # Create commit
    success, stdout, stderr = run_command('git commit -m "Initial commit: Windows/Ubuntu Switcher project"')
    if not success:
        print(f"❌ Failed to create commit: {stderr}")
        return False
    
    print("✅ Initial commit created")
    return True

def create_main_branch():
    """Create and switch to main branch"""
    print("\n🌿 Setting up main branch...")
    
    # Check current branch
    success, stdout, stderr = run_command("git branch --show-current")
    if success and stdout.strip() == "main":
        print("✅ Already on main branch")
        return True
    
    # Create and switch to main branch
    success, stdout, stderr = run_command("git checkout -b main")
    if not success:
        print(f"❌ Failed to create main branch: {stderr}")
        return False
    
    print("✅ Created and switched to main branch")
    return True

def main():
    """Main function"""
    print("🚀 Windows/Ubuntu Switcher Git Repository Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_git_installed():
        print("\n❌ Git initialization failed: Git not found")
        return False
    
    # Initialize repository
    if not init_git_repo():
        print("\n❌ Git initialization failed: Could not initialize repository")
        return False
    
    # Configure user
    if not configure_git_user():
        print("\n❌ Git initialization failed: Could not configure user")
        return False
    
    # Add remote origin
    if not add_remote_origin():
        print("\n❌ Git initialization failed: Could not add remote origin")
        return False
    
    # Create main branch
    if not create_main_branch():
        print("\n❌ Git initialization failed: Could not create main branch")
        return False
    
    # Create initial commit
    if not create_initial_commit():
        print("\n❌ Git initialization failed: Could not create initial commit")
        return False
    
    print("\n🎉 Git repository setup completed successfully!")
    print("\nNext steps:")
    print("1. Push to GitHub: git push -u origin main")
    print("2. Create issues for known bugs and features")
    print("3. Invite collaborators to contribute")
    print("4. Start development workflow")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
