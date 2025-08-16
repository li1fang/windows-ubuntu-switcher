#!/usr/bin/env python3
"""
Script to update README.md with project badges and information
"""

import os
import sys
import re
from pathlib import Path

def read_file(file_path):
    """Read file content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Failed to read {file_path}: {e}")
        return None

def write_file(file_path, content):
    """Write content to file"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"❌ Failed to write {file_path}: {e}")
        return False

def get_github_username():
    """Get GitHub username from user input"""
    print("🔧 Updating README.md with project information")
    print("=" * 50)
    
    username = input("Enter your GitHub username: ").strip()
    if not username:
        print("❌ GitHub username is required")
        return None
    
    return username

def update_badges(content, username):
    """Update badges in README content"""
    print("🏷️  Updating project badges...")
    
    # Define badge replacements
    badge_replacements = {
        r'yourusername': username,
        r'your\.email@example\.com': f'{username}@github.com'
    }
    
    # Apply replacements
    for old, new in badge_replacements.items():
        content = re.sub(old, new, content)
    
    return content

def update_links(content, username):
    """Update links in README content"""
    print("🔗 Updating project links...")
    
    # Define link replacements
    link_replacements = {
        r'https://github\.com/yourusername/windows-ubuntu-switcher': f'https://github.com/{username}/windows-ubuntu-switcher',
        r'yourusername/windows-ubuntu-switcher': f'{username}/windows-ubuntu-switcher'
    }
    
    # Apply replacements
    for old, new in link_replacements.items():
        content = re.sub(old, new, content)
    
    return content

def add_project_badges(content, username):
    """Add project badges to README"""
    print("✨ Adding project badges...")
    
    # Check if badges already exist
    if "![Python]" in content and "![License]" in content:
        print("✅ Project badges already exist")
        return content
    
    # Define badges to add
    badges = f"""<div align="center">

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-beta-orange.svg)](https://github.com/{username}/windows-ubuntu-switcher)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20ubuntu-lightgrey.svg)](https://github.com/{username}/windows-ubuntu-switcher)

[![GitHub issues](https://img.shields.io/github/issues/{username}/windows-ubuntu-switcher)](https://github.com/{username}/windows-ubuntu-switcher/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/{username}/windows-ubuntu-switcher)](https://github.com/{username}/windows-ubuntu-switcher/pulls)
[![GitHub contributors](https://img.shields.io/github/contributors/{username}/windows-ubuntu-switcher)](https://github.com/{username}/windows-ubuntu-switcher/graphs/contributors)
[![GitHub last commit](https://img.shields.io/github/last-commit/{username}/windows-ubuntu-switcher)](https://github.com/{username}/windows-ubuntu-switcher/commits/main)

[![GitHub Actions](https://img.shields.io/github/actions/workflow/status/{username}/windows-ubuntu-switcher/ci.yml)](https://github.com/{username}/windows-ubuntu-switcher/actions)

[![GitHub stars](https://img.shields.io/github/stars/{username}/windows-ubuntu-switcher)](https://github.com/{username}/windows-ubuntu-switcher/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/{username}/windows-ubuntu-switcher)](https://github.com/{username}/windows-ubuntu-switcher/network)
[![GitHub watchers](https://img.shields.io/github/watchers/{username}/windows-ubuntu-switcher)](https://github.com/{username}/windows-ubuntu-switcher/watchers)

</div>

"""
    
    # Find the title and add badges after it
    title_pattern = r'(<h2 align="center">.*?</h2>)'
    match = re.search(title_pattern, content, re.DOTALL)
    
    if match:
        title = match.group(1)
        content = content.replace(title, title + '\n\n' + badges)
    else:
        # If no title found, add at the beginning
        content = badges + '\n' + content
    
    return content

def update_contributing_section(content, username):
    """Update contributing section with correct links"""
    print("🤝 Updating contributing section...")
    
    # Update contributing links
    contributing_pattern = r'\[CONTRIBUTING\.md\]\(.*?\)'
    new_contributing_link = f'[CONTRIBUTING.md](https://github.com/{username}/windows-ubuntu-switcher/blob/main/CONTRIBUTING.md)'
    
    content = re.sub(contributing_pattern, new_contributing_link, content)
    
    return content

def update_development_guide_section(content, username):
    """Update development guide section with correct links"""
    print("📚 Updating development guide section...")
    
    # Update development guide links
    dev_guide_pattern = r'\[DEVELOPGUIDE\.md\]\(.*?\)'
    new_dev_guide_link = f'[DEVELOPGUIDE.md](https://github.com/{username}/windows-ubuntu-switcher/blob/main/DEVELOPGUIDE.md)'
    
    content = re.sub(dev_guide_pattern, new_dev_guide_link, content)
    
    return content

def update_community_section(content, username):
    """Update community section with correct links"""
    print("🏘️  Updating community section...")
    
    # Update GitHub Issues link
    issues_pattern = r'\[GitHub Issues\]\(https://github\.com/yourusername/windows-ubuntu-switcher/issues/new/choose\)'
    new_issues_link = f'[GitHub Issues](https://github.com/{username}/windows-ubuntu-switcher/issues/new/choose)'
    
    content = re.sub(issues_pattern, new_issues_link, content)
    
    # Update Discord link (if exists)
    discord_pattern = r'\[Discord server\]\(https://discord\.gg/eHyXHtSE\)'
    if discord_pattern in content:
        print("⚠️  Discord link found - you may want to update this with your own server")
    
    return content

def update_roadmap_section(content, username):
    """Update roadmap section with correct links"""
    print("🗺️  Updating roadmap section...")
    
    # Update roadmap link
    roadmap_pattern = r'\[public roadmap\]\(https://github\.com/orgs/labring/projects/4/views/9\)'
    new_roadmap_link = f'[public roadmap](https://github.com/{username}/windows-ubuntu-switcher/projects)'
    
    content = re.sub(roadmap_pattern, new_roadmap_link, content)
    
    return content

def update_links_section(content, username):
    """Update links section with correct URLs"""
    print("🔗 Updating links section...")
    
    # Update GitHub repository links
    links_pattern = r'https://github\.com/labring/.*?'
    new_links = [
        f'[Sealos Action](https://github.com/{username}/windows-ubuntu-switcher-action)',
        f'[Cluster Image](https://github.com/{username}/windows-ubuntu-switcher-cluster-image)',
        f'[Rootfs Image](https://github.com/{username}/windows-ubuntu-switcher-runtime)',
        '[Buildah](https://github.com/containers/buildah) The functionalities of Buildah are extensively utilized in Windows/Ubuntu Switcher to ensure that system switching is compatible with OCI standard.'
    ]
    
    # Find and replace the links section
    links_section_pattern = r'(## Links\n\n)(.*?)(\n\n<!-- ## License -->)'
    match = re.search(links_section_pattern, content, re.DOTALL)
    
    if match:
        prefix = match.group(1)
        suffix = match.group(3)
        new_links_content = '\n'.join(new_links)
        new_section = prefix + new_links_content + suffix
        content = re.sub(links_section_pattern, new_section, content)
    
    return content

def main():
    """Main function"""
    # Get GitHub username
    username = get_github_username()
    if not username:
        sys.exit(1)
    
    # Read README.md
    readme_path = "README.md"
    content = read_file(readme_path)
    if not content:
        sys.exit(1)
    
    print(f"📖 Reading {readme_path}...")
    
    # Update content
    content = update_badges(content, username)
    content = update_links(content, username)
    content = add_project_badges(content, username)
    content = update_contributing_section(content, username)
    content = update_development_guide_section(content, username)
    content = update_community_section(content, username)
    content = update_roadmap_section(content, username)
    content = update_links_section(content, username)
    
    # Write updated content back to file
    if write_file(readme_path, content):
        print(f"\n✅ Successfully updated {readme_path}")
        print(f"📝 Updated with GitHub username: {username}")
        print("\n🔍 Please review the changes and make any additional edits as needed")
    else:
        print(f"\n❌ Failed to update {readme_path}")
        sys.exit(1)

if __name__ == "__main__":
    main()
