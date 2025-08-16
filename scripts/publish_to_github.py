#!/usr/bin/env python3
"""
Main script to publish Windows/Ubuntu Switcher to GitHub
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

def check_prerequisites():
    """Check all prerequisites"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 or higher is required")
        return False
    
    # Check Git
    success, stdout, stderr = run_command("git --version")
    if not success:
        print("❌ Git is not installed or not in PATH")
        return False
    
    # Check if we're in a git repository
    if not os.path.exists(".git"):
        print("❌ Not in a git repository")
        return False
    
    print("✅ Prerequisites check passed")
    return True

def check_project_structure():
    """Check if project structure is correct"""
    print("\n📁 Checking project structure...")
    
    required_files = [
        "README.md",
        "LICENSE",
        "requirements.txt",
        "setup.py",
        "windows_ubuntu_switcher/main.py",
        "CONTRIBUTING.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    print("✅ Project structure check passed")
    return True

def check_git_status():
    """Check git status"""
    print("\n🔍 Checking git status...")
    
    # Check if working directory is clean
    success, stdout, stderr = run_command("git status --porcelain")
    if not success:
        print(f"❌ Failed to check git status: {stderr}")
        return False
    
    if stdout.strip():
        print("⚠️  Working directory is not clean:")
        print(stdout)
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            return False
    else:
        print("✅ Working directory is clean")
    
    return True

def setup_git_user():
    """Setup git user if not configured"""
    print("\n👤 Checking git user configuration...")
    
    success, stdout, stderr = run_command("git config user.name")
    if not success or not stdout.strip():
        print("⚠️  Git user name not configured")
        name = input("Enter your name: ").strip()
        if name:
            run_command(f'git config user.name "{name}"')
    
    success, stdout, stderr = run_command("git config user.email")
    if not success or not stdout.strip():
        print("⚠️  Git user email not configured")
        email = input("Enter your email: ").strip()
        if email:
            run_command(f'git config user.email "{email}"')
    
    print("✅ Git user configuration complete")
    return True

def setup_remote_origin():
    """Setup remote origin"""
    print("\n🌐 Checking remote origin...")
    
    success, stdout, stderr = run_command("git remote get-url origin")
    if not success:
        print("⚠️  No remote origin configured")
        repo_url = input("Enter GitHub repository URL: ").strip()
        if repo_url:
            success, stdout, stderr = run_command(f'git remote add origin "{repo_url}"')
            if not success:
                print(f"❌ Failed to add remote origin: {stderr}")
                return False
        else:
            print("⚠️  Skipping remote origin setup")
            return True
    else:
        print(f"✅ Remote origin: {stdout.strip()}")
    
    return True

def create_initial_commit():
    """Create initial commit if needed"""
    print("\n📝 Checking commit status...")
    
    success, stdout, stderr = run_command("git log --oneline -1")
    if not success or not stdout.strip():
        print("⚠️  No commits found, creating initial commit...")
        
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
    else:
        print(f"✅ Latest commit: {stdout.strip()}")
    
    return True

def create_main_branch():
    """Ensure we're on main branch"""
    print("\n🌿 Checking branch...")
    
    success, stdout, stderr = run_command("git branch --show-current")
    if success:
        current_branch = stdout.strip()
        if current_branch != "main":
            print(f"⚠️  Currently on branch: {current_branch}")
            response = input("Switch to main branch? (y/N): ").strip().lower()
            if response == 'y':
                success, stdout, stderr = run_command("git checkout -b main")
                if not success:
                    print(f"❌ Failed to create main branch: {stderr}")
                    return False
                print("✅ Switched to main branch")
            else:
                print("⚠️  Staying on current branch")
        else:
            print("✅ Already on main branch")
    
    return True

def push_to_github():
    """Push to GitHub"""
    print("\n🚀 Pushing to GitHub...")
    
    # Check if we have a remote origin
    success, stdout, stderr = run_command("git remote get-url origin")
    if not success:
        print("⚠️  No remote origin, skipping push")
        return True
    
    # Push to GitHub
    success, stdout, stderr = run_command("git push -u origin main")
    if not success:
        print(f"❌ Failed to push to GitHub: {stderr}")
        print("You may need to authenticate with GitHub")
        return False
    
    print("✅ Successfully pushed to GitHub")
    return True

def show_next_steps():
    """Show next steps for the user"""
    print("\n🎉 Project setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Visit your GitHub repository")
    print("2. Create Issues for known bugs and features")
    print("3. Invite collaborators to contribute")
    print("4. Start development workflow")
    print("5. Consider creating a GitHub Release")
    
    print("\n🔗 Useful links:")
    print("- GitHub Issues: Create issues for bugs and features")
    print("- GitHub Discussions: Start discussions with the community")
    print("- GitHub Actions: Monitor CI/CD pipeline")
    print("- GitHub Releases: Create releases for stable versions")
    
    print("\n📚 Documentation:")
    print("- README.md: Project overview and installation")
    print("- CONTRIBUTING.md: How to contribute")
    print("- docs/: Detailed documentation")
    print("- scripts/: Utility scripts for development")

def main():
    """Main function"""
    print("🚀 Windows/Ubuntu Switcher GitHub Publisher")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed")
        print("Please install required tools and try again")
        sys.exit(1)
    
    # Check project structure
    if not check_project_structure():
        print("\n❌ Project structure check failed")
        print("Please ensure all required files are present")
        sys.exit(1)
    
    # Check git status
    if not check_git_status():
        print("\n❌ Git status check failed")
        sys.exit(1)
    
    # Setup git user
    if not setup_git_user():
        print("\n❌ Git user setup failed")
        sys.exit(1)
    
    # Setup remote origin
    if not setup_remote_origin():
        print("\n❌ Remote origin setup failed")
        sys.exit(1)
    
    # Create initial commit
    if not create_initial_commit():
        print("\n❌ Initial commit creation failed")
        sys.exit(1)
    
    # Create main branch
    if not create_main_branch():
        print("\n❌ Main branch setup failed")
        sys.exit(1)
    
    # Push to GitHub
    if not push_to_github():
        print("\n⚠️  Push to GitHub failed")
        print("You can manually push later with: git push -u origin main")
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
