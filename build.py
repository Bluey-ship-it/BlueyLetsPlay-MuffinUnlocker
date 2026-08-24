#!/usr/bin/env python3
"""
Build script to create standalone executables using PyInstaller
"""

import PyInstaller.__main__
import sys

def build():
    """Build standalone executable"""
    args = [
        'muffin_unlocker.py',
        '--onefile',
        '--windowed',
        '--icon=NONE',
        '--name=muffin_unlocker',
        '--clean',
    ]
    
    if sys.platform == 'win32':
        args.append('--console')  # Show console on Windows
    
    print("Building executable...")
    PyInstaller.__main__.run(args)
    print("✓ Build complete! Executable in ./dist/")

if __name__ == '__main__':
    build()
