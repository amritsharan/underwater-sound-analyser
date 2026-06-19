#!/usr/bin/env python
"""
Quick Launcher for Desktop Application
Run this to start the Underwater Sound Classifier desktop app
"""

import sys
import subprocess
import os
from pathlib import Path

# Support UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def get_venv_python():
    """Find and return the venv Python executable path"""
    project_dir = Path(__file__).parent
    venv_paths = [
        project_dir / ".venv311" / "Scripts" / "python.exe",
        project_dir / ".venv" / "Scripts" / "python.exe",
    ]
    
    for venv_path in venv_paths:
        if venv_path.exists():
            return str(venv_path)
    
    return None


def check_requirements():
    """Check if all requirements are installed"""
    # Map package names to their import names
    required = {
        'PyQt5': 'PyQt5',
        'librosa': 'librosa',
        'numpy': 'numpy',
        'scipy': 'scipy',
        'sklearn': 'sklearn',
        'matplotlib': 'matplotlib',
        'soundfile': 'soundfile',
        'PyQtChart': 'PyQt5.QtChart'
    }
    missing = []
    
    for package_name, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        print("❌ Missing packages:", ", ".join(missing))
        print("\nInstalling missing packages...")
        venv_python = get_venv_python()
        if venv_python:
            subprocess.check_call([venv_python, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("✅ All packages installed!")
    
    return len(missing) == 0


def main():
    """Main launcher"""
    print("🐋 Underwater Sound Classifier - Desktop App")
    print("=" * 50)
    
    # Check if we're running in venv, if not restart with venv python
    venv_python = get_venv_python()
    if venv_python and sys.executable != venv_python:
        print("🔄 Restarting with venv Python...")
        import subprocess
        result = subprocess.call([venv_python, __file__] + sys.argv[1:])
        sys.exit(result)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Failed to install requirements")
        sys.exit(1)
    
    print("\n✅ Starting desktop application...")
    print("-" * 50)
    
    # Import and run
    try:
        from desktop.app import main as app_main
        app_main()
    except Exception as e:
        print(f"\n❌ Error starting app: {e}")
        print("\nMake sure you're in the project root directory")
        print(f"Current directory: {os.getcwd()}")
        sys.exit(1)


if __name__ == '__main__':
    main()
