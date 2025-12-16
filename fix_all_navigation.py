#!/usr/bin/env python3
"""
Comprehensive navigation fix for all HTML pages.
1. Removes "News" from homepage mobile sidebar
2. Extracts correct navigation from homepage
3. Applies to all other pages with proper relative paths
"""

import os
import re
from pathlib import Path

def get_relative_path_depth(file_path):
    """Calculate relative path depth from root"""
    parts = Path(file_path).parts
    # Remove filename, count directory depth
    depth = len(parts) - 1
    return depth

def adjust_paths(nav_html, depth):
    """Adjust relative paths in navigation based on depth"""
    if depth == 0:
        # Root level - paths are already correct (./)
        return nav_html
    
    # Build prefix for relative paths
    prefix = '../' * depth
    
    # Replace paths
    nav_html = re.sub(r'href="\./', f'href="{prefix}', nav_html)
    nav_html = re.sub(r'src="\./img/', f'src="{prefix}img/', nav_html)
    nav_html = re.sub(r'srcset="img/', f'srcset="{prefix}img/', nav_html)
    nav_html = re.sub(r'src="img/', f'src="{prefix}img/', nav_html)
    
    return nav_html

def extract_navigation_blocks(homepage_content):
    """Extract mobile sidebar and desktop navigation from homepage"""
    # Extract mobile sidebar (between <!-- sidebar --> and <!-- sidebar END -->)
    sidebar_start = homepage_content.find('<!-- sidebar -->')
    sidebar_end = homepage_content.find('<!-- sidebar END -->')
    if sidebar_start == -1 or sidebar_end == -1:
        raise ValueError("Could not find sidebar markers in homepage")
    
    mobile_sidebar = homepage_content[sidebar_start:sidebar_end + len('<!-- sidebar END -->')]
    
    # Remove News from mobile sidebar
    # Find and remove the News link
    news_pattern = r'<p class="eldar-project-link mb-0 tc-4062"><img[^>]*alt="news"[^>]*> <a[^>]*href="\./news/"[^>]*>News</a></p>'
    mobile_sidebar = re.sub(news_pattern, '', mobile_sidebar)
    
    # Extract desktop navigation (between <!-- bloc-2 --> with eldar-sidebar and <!-- bloc-2 END -->)
    # Find the desktop sidebar bloc
    desktop_start = homepage_content.find('<!-- bloc-2 -->', homepage_content.find('eldar-sidebar') - 200)
    if desktop_start == -1:
        desktop_start = homepage_content.find('<div class="bloc d-lg-flex d-none l-bloc eldar-sidebar"')
    
    desktop_end = homepage_content.find('<!-- bloc-2 END -->', desktop_start)
    if desktop_end == -1:
        raise ValueError("Could not find desktop navigation end marker")
    
    desktop_nav = homepage_content[desktop_start:desktop_end + len('<!-- bloc-2 END -->')]
    
    return mobile_sidebar, desktop_nav

def fix_page_navigation(file_path, mobile_sidebar_template, desktop_nav_template):
    """Fix navigation in a single page"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    depth = get_relative_path_depth(file_path)
    
    # Adjust paths in templates
    mobile_sidebar = adjust_paths(mobile_sidebar_template, depth)
    desktop_nav = adjust_paths(desktop_nav_template, depth)
    
    # Replace mobile sidebar
    old_sidebar_start = content.find('<!-- sidebar -->')
    old_sidebar_end = content.find('<!-- sidebar END -->')
    if old_sidebar_start != -1 and old_sidebar_end != -1:
        old_sidebar_end += len('<!-- sidebar END -->')
        content = content[:old_sidebar_start] + mobile_sidebar + content[old_sidebar_end:]
    
    # Replace desktop navigation
    # Find desktop sidebar bloc
    desktop_start = content.find('<!-- bloc-2 -->', content.find('eldar-sidebar') - 200 if 'eldar-sidebar' in content else 0)
    if desktop_start == -1:
        desktop_start = content.find('<div class="bloc d-lg-flex d-none l-bloc eldar-sidebar"')
    
    if desktop_start != -1:
        desktop_end = content.find('<!-- bloc-2 END -->', desktop_start)
        if desktop_end != -1:
            desktop_end += len('<!-- bloc-2 END -->')
            content = content[:desktop_start] + desktop_nav + content[desktop_end:]
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    # Read homepage
    homepage_path = 'index.html'
    with open(homepage_path, 'r', encoding='utf-8') as f:
        homepage_content = f.read()
    
    # Extract navigation blocks
    mobile_sidebar_template, desktop_nav_template = extract_navigation_blocks(homepage_content)
    
    # Update homepage (remove News)
    with open(homepage_path, 'w', encoding='utf-8') as f:
        # Replace sidebar in homepage content
        sidebar_start = homepage_content.find('<!-- sidebar -->')
        sidebar_end = homepage_content.find('<!-- sidebar END -->')
        if sidebar_start != -1 and sidebar_end != -1:
            sidebar_end += len('<!-- sidebar END -->')
            homepage_content = homepage_content[:sidebar_start] + mobile_sidebar_template + homepage_content[sidebar_end:]
        f.write(homepage_content)
    
    print(f"✓ Fixed homepage (removed News)")
    
    # Find all HTML files except homepage
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        if 'node_modules' in root or '.git' in root or '__pycache__' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                full_path = os.path.join(root, file)
                # Normalize path
                full_path = os.path.normpath(full_path)
                # Skip homepage
                if full_path == 'index.html' or full_path == './index.html':
                    continue
                html_files.append(full_path)
    
    print(f"Found {len(html_files)} HTML files to fix")
    
    # Fix each page
    fixed_count = 0
    for file_path in sorted(html_files):
        try:
            if os.path.exists(file_path):
                fix_page_navigation(file_path, mobile_sidebar_template, desktop_nav_template)
                fixed_count += 1
                if fixed_count % 10 == 0:
                    print(f"✓ Fixed {fixed_count} pages...")
            else:
                print(f"✗ File not found: {file_path}")
        except Exception as e:
            print(f"✗ Error fixing {file_path}: {e}")
    
    print(f"\n✓ Fixed navigation on {fixed_count} pages")

if __name__ == '__main__':
    main()
