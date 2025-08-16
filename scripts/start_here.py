#!/usr/bin/env python3
"""
Main startup script for Windows/Ubuntu Switcher project
This script provides a menu to access all project tools and scripts
"""

import os
import sys
import subprocess
from pathlib import Path

# Force UTF-8 encoding for Windows compatibility
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        print(f"🔧 Executing command: {cmd}")
        if cwd:
            print(f"   Working directory: {cwd}")
        
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, encoding='utf-8')
        
        print(f"   Return code: {result.returncode}")
        if result.stdout.strip():
            print(f"   STDOUT: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"   STDERR: {result.stderr.strip()}")
        
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"   Exception: {e}")
        return False, "", str(e)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    """Show project banner"""
    print("=" * 60)
    print("🚀 Windows/Ubuntu Switcher Project Manager")
    print("=" * 60)
    print("A comprehensive tool for managing your dual-boot switching project")
    print("=" * 60)

def show_menu():
    """Show main menu"""
    print("\n📋 Available Options:")
    print("1. 🚀 Quick Start - Set up development environment")
    print("2. 🔧 Initialize Git Repository")
    print("3. 📝 Update README with project info")
    print("4. 🏷️  Prepare for Release")
    print("5. 🌐 Publish to GitHub")
    print("6. 🧪 Run Tests")
    print("7. 📚 View Documentation")
    print("8. 🔍 Check Project Status")
    print("9. 🆘 Help & Support")
    print("0. 🚪 Exit")
    print("-" * 60)

def run_quick_start():
    """Run quick start script"""
    print("\n🚀 Starting Quick Start...")
    script_path = "scripts/quick_start.py"
    
    print(f"🔍 Looking for script: {os.path.abspath(script_path)}")
    
    if os.path.exists(script_path):
        print(f"✅ Script found, executing...")
        success, stdout, stderr = run_command(f"python {script_path}")
        if not success:
            print(f"❌ Quick start failed!")
            if stderr:
                print(f"Error details: {stderr}")
            if stdout:
                print(f"Output: {stdout}")
        else:
            print(f"✅ Quick start completed successfully!")
            if stdout:
                print(f"Output: {stdout}")
    else:
        print(f"❌ Script not found: {script_path}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Available files in scripts/: {os.listdir('scripts/') if os.path.exists('scripts/') else 'scripts/ directory not found'}")

def run_git_init():
    """Run git initialization script"""
    print("\n🔧 Initializing Git Repository...")
    print("🔍 Debug: Function run_git_init() was called!")
    
    script_path = "scripts/init_git.py"
    
    print(f"🔍 Debug: Looking for script at: {os.path.abspath(script_path)}")
    print(f"🔍 Debug: Current working directory: {os.getcwd()}")
    
    if os.path.exists(script_path):
        print(f"✅ Script found, executing...")
        print(f"🔍 Debug: About to run: python {script_path}")
        
        success, stdout, stderr = run_command(f"python {script_path}")
        
        print(f"🔍 Debug: Command completed, success={success}")
        print(f"🔍 Debug: stdout length: {len(stdout) if stdout else 0}")
        print(f"🔍 Debug: stderr length: {len(stderr) if stderr else 0}")
        
        if not success:
            print(f"❌ Git initialization failed!")
            if stderr:
                print(f"Error details: {stderr}")
        else:
            print(f"✅ Git initialization completed successfully!")
            if stdout:
                print(f"Output: {stdout}")
    else:
        print(f"❌ Script not found: {script_path}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Available files in scripts/: {os.listdir('scripts/') if os.path.exists('scripts/') else 'scripts/ directory not found'}")

def run_readme_update():
    """Run README update script"""
    print("\n📝 Updating README...")
    script_path = "scripts/update_readme.py"
    
    if os.path.exists(script_path):
        success, stdout, stderr = run_command(f"python {script_path}")
        if not success:
            print(f"❌ README update failed: {stderr}")
    else:
        print(f"❌ Script not found: {script_path}")

def run_release_prep():
    """Run release preparation script"""
    print("\n🏷️  Preparing for Release...")
    script_path = "scripts/prepare_release.py"
    
    if os.path.exists(script_path):
        success, stdout, stderr = run_command(f"python {script_path}")
        if not success:
            print(f"❌ Release preparation failed: {stderr}")
    else:
        print(f"❌ Script not found: {script_path}")

def run_github_publish():
    """Run GitHub publishing script"""
    print("\n🌐 Publishing to GitHub...")
    script_path = "scripts/publish_to_github.py"
    
    if os.path.exists(script_path):
        success, stdout, stderr = run_command(f"python {script_path}")
        if not success:
            print(f"❌ GitHub publishing failed: {stderr}")
    else:
        print(f"❌ Script not found: {script_path}")

def run_tests():
    """Run project tests"""
    print("\n🧪 Running Tests...")
    
    if os.path.exists("tests/"):
        success, stdout, stderr = run_command("python -m pytest tests/ -v")
        if not success:
            print(f"⚠️  Tests failed: {stderr}")
            print("This is expected for a new project. Tests can be added later.")
    else:
        print("❌ Tests directory not found")

def show_documentation():
    """Show available documentation"""
    print("\n📚 Available Documentation:")
    print("-" * 40)
    
    docs_files = [
        ("README.md", "Project overview and installation"),
        ("README_zh.md", "项目概述和安装说明（中文）"),
        ("CONTRIBUTING.md", "How to contribute to the project"),
        ("docs/project_status.md", "Current project status and roadmap"),
        ("docs/project_badges.md", "Project badges and status indicators"),
        ("docs/release_checklist.md", "Release preparation checklist"),
        ("install_guide.md", "Installation guide"),
        ("plan.md", "Project development plan")
    ]
    
    for filename, description in docs_files:
        if os.path.exists(filename):
            print(f"✅ {filename}")
            print(f"   {description}")
        else:
            print(f"❌ {filename} (not found)")
    
    print("\n💡 Tip: Open these files in your text editor to view the content")

def check_project_status():
    """Check project status"""
    print("\n🔍 Project Status Check:")
    print("-" * 40)
    
    # Check required files
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
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    # Check Git status
    if os.path.exists(".git"):
        print("\n🌿 Git Repository:")
        success, stdout, stderr = run_command("git status --porcelain")
        if success and stdout.strip():
            print("⚠️  Working directory has uncommitted changes")
            print(stdout)
        else:
            print("✅ Working directory is clean")
        
        success, stdout, stderr = run_command("git remote get-url origin")
        if success and stdout.strip():
            print(f"✅ Remote origin: {stdout.strip()}")
        else:
            print("⚠️  No remote origin configured")
    else:
        print("\n❌ Not a Git repository")
    
    # Check Python environment
    print(f"\n🐍 Python Environment:")
    print(f"   Version: {sys.version}")
    print(f"   Virtual Environment: {'Yes' if os.path.exists('.venv') else 'No'}")
    
    if missing_files:
        print(f"\n⚠️  Missing {len(missing_files)} required files")
        print("Please run the Quick Start option to set up the project")

def show_help():
    """Show help and support information"""
    print("\n🆘 Help & Support:")
    print("-" * 40)
    print("This project manager helps you set up and manage your")
    print("Windows/Ubuntu Switcher project for GitHub publication.")
    
    print("\n📋 Recommended Workflow:")
    print("1. Start with 'Quick Start' to set up the environment")
    print("2. Use 'Initialize Git Repository' to set up version control")
    print("3. Update README with your project information")
    print("4. Test your project functionality")
    print("5. Prepare and publish to GitHub")
    
    print("\n🔧 Scripts Available:")
    scripts_dir = "scripts/"
    if os.path.exists(scripts_dir):
        for script_file in os.listdir(scripts_dir):
            if script_file.endswith('.py'):
                print(f"   - {script_file}")
    
    print("\n📚 Documentation:")
    print("   - Check the 'docs/' folder for detailed guides")
    print("   - README.md contains project overview")
    print("   - CONTRIBUTING.md explains how to contribute")
    
    print("\n❓ Need More Help?")
    print("   - Check the project documentation")
    print("   - Create an issue on GitHub")
    print("   - Review the code comments")

def main():
    """Main function"""
    while True:
        clear_screen()
        show_banner()
        show_menu()
        
        try:
            choice = input("\n🎯 Enter your choice (0-9): ").strip()
            
            if choice == "0":
                print("\n👋 Goodbye! Good luck with your project!")
                break
            elif choice == "1":
                run_quick_start()
            elif choice == "2":
                run_git_init()
            elif choice == "3":
                run_readme_update()
            elif choice == "4":
                run_release_prep()
            elif choice == "5":
                run_github_publish()
            elif choice == "6":
                run_tests()
            elif choice == "7":
                show_documentation()
            elif choice == "8":
                check_project_status()
            elif choice == "9":
                show_help()
            else:
                print("\n❌ Invalid choice. Please enter a number between 0-9.")
            
            if choice != "0":
                input("\n⏸️  Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Good luck with your project!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("\n⏸️  Press Enter to continue...")

if __name__ == "__main__":
    main()
