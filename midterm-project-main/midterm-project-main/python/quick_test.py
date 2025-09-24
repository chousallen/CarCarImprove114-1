#!/usr/bin/env python3
"""
快速測試修改後的main.py
"""
import subprocess
import sys
import os

def test_modified_main():
    """測試修改後的main.py"""
    print("🧪 Testing modified main.py...")
    print("=" * 50)
    
    # 切換到python目錄
    python_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(python_dir)
    
    try:
        # 執行main.py，設定較短的測試時間
        cmd = [sys.executable, "main.py", "--time", "30", "--node", "1"]
        print(f"💻 執行命令: {' '.join(cmd)}")
        print("🔍 觀察輸出...")
        print("-" * 50)
        
        # 執行程式
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # 即時顯示輸出
        for line in process.stdout:
            print(line.rstrip())
            
    except KeyboardInterrupt:
        print("\n⏹️ 測試被使用者中斷")
        if process:
            process.terminate()
    except Exception as e:
        print(f"❌ 測試過程發生錯誤: {e}")

if __name__ == "__main__":
    print("🚀 修改後的main.py測試腳本")
    print("📋 主要修改:")
    print("  ✅ 自動嘗試常見藍牙埠 (COM3-COM10)")
    print("  ✅ 移除按Enter等待")
    print("  ✅ 無腦發送所有指令，不等Arduino回應")
    print("  ✅ 只收UID並顯示到記分板")
    print("  ✅ 非UID格式數據輸出到terminal")
    print("")
    
    choice = input("🤔 要開始測試嗎? (y/N): ").lower()
    if choice == 'y':
        test_modified_main()
    else:
        print("👋 測試取消")
