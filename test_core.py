import subprocess
import os
import sys

def check_admin_and_users():
    print("🔄 Step 1: Checking Administrator privileges...")
    
    # Absolute method to check for Admin privileges on Windows
    is_admin = False
    try:
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        pass

    if is_admin:
        print("✅ SUCCESS: Terminal has Administrator privileges!\n")
    else:
        print("❌ ERROR: Administrator privileges not found! Please close VS Code and reopen it using 'Run as Administrator'.\n")
        return

    print("🔄 Step 2: Fetching Windows user list via 'net user'...")
    try:
        # Triggering the native Windows 'net user' command
        result = subprocess.run(['net', 'user'], capture_output=True, text=True, check=True)
        
        print("\n✅ SUCCESS! Raw output retrieved from Windows SAM:\n")
        print("=" * 60)
        print(result.stdout)
        print("=" * 60)
        
    except subprocess.CalledProcessError as e:
        print("\n❌ ERROR! An issue occurred while executing the command:")
        print(e.stderr)

if __name__ == "__main__":
    check_admin_and_users()