#!/usr/bin/env python3
"""
Release preparation script for Windows/Ubuntu Switcher
"""

import os
import sys
import subprocess
import re
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_git_status():
    """Check if we're in a git repository and if it's clean"""
    success, stdout, stderr = run_command("git status --porcelain")
    if not success:
        print("❌ Not in a git repository or git not available")
        return False
    
    if stdout.strip():
        print("❌ Working directory is not clean. Please commit or stash changes first.")
        print("Uncommitted changes:")
        print(stdout)
        return False
    
    print("✅ Working directory is clean")
    return True

def check_git_remote():
    """Check if remote origin is configured"""
    success, stdout, stderr = run_command("git remote get-url origin")
    if not success:
        print("❌ No remote origin configured")
        return False
    
    print(f"✅ Remote origin: {stdout.strip()}")
    return True

def update_version(version):
    """Update version in setup.py"""
    setup_file = Path("setup.py")
    if not setup_file.exists():
        print("❌ setup.py not found")
        return False
    
    content = setup_file.read_text(encoding='utf-8')
    new_content = re.sub(r'version="[^"]*"', f'version="{version}"', content)
    
    if new_content != content:
        setup_file.write_text(new_content, encoding='utf-8')
        print(f"✅ Updated version to {version} in setup.py")
        return True
    else:
        print(f"⚠️  Version already set to {version} in setup.py")
        return True

def create_release_commit(version):
    """Create a release commit"""
    success, stdout, stderr = run_command(f'git add .')
    if not success:
        print(f"❌ Failed to add files: {stderr}")
        return False
    
    success, stdout, stderr = run_command(f'git commit -m "Release version {version}"')
    if not success:
        print(f"❌ Failed to create commit: {stderr}")
        return False
    
    print(f"✅ Created release commit for version {version}")
    return True

def create_release_tag(version):
    """Create a release tag"""
    success, stdout, stderr = run_command(f'git tag -a v{version} -m "Release version {version}"')
    if not success:
        print(f"❌ Failed to create tag: {stderr}")
        return False
    
    print(f"✅ Created release tag v{version}")
    return True

def main():
    """Main function"""
    print("🚀 Windows/Ubuntu Switcher Release Preparation")
    print("=" * 50)
    
    # Check prerequisites
    if not check_git_status():
        sys.exit(1)
    
    if not check_git_remote():
        sys.exit(1)
    
    # Get version from user
    version = input("Enter version number (e.g., 1.0.0): ").strip()
    if not version:
        print("❌ Version number is required")
        sys.exit(1)
    
    # Validate version format
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        print("❌ Invalid version format. Use format: X.Y.Z")
        sys.exit(1)
    
    print(f"\n📦 Preparing release version {version}")
    
    # Update version in setup.py
    if not update_version(version):
        sys.exit(1)
    
    # Create release commit
    if not create_release_commit(version):
        sys.exit(1)
    
    # Create release tag
    if not create_release_tag(version):
        sys.exit(1)
    
    print(f"\n🎉 Release preparation completed for version {version}")
    print("\nNext steps:")
    print(f"1. Push the release: git push origin main --tags")
    print(f"2. Create a release on GitHub with tag v{version}")
    print(f"3. Upload any built artifacts to the GitHub release")

if __name__ == "__main__":
    main()
