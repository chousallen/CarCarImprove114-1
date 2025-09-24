#!/usr/bin/env python3
"""
測試UID處理邏輯
"""
import logging
from main import MazeCar

logging.basicConfig(level=logging.INFO)

def test_uid_formats():
    """測試各種UID格式的處理"""
    print("🧪 測試UID處理邏輯")
    print("=" * 50)
    
    # 創建MazeCar實例（使用虛擬模式）
    car = MazeCar(bt_port="VIRTUAL")
    
    # 測試各種UID格式
    test_cases = [
        # HEX格式（Arduino RFID常見格式）
        "0x1234ABCD",
        "0x12AB",
        "0xABCDEF01",
        "1234ABCD",
        "ABCD1234",
        
        # TEST格式（CSV檔案格式）
        "TEST0031",
        "TEST0025",
        "TEST0044",
        
        # 純數字格式
        "12345678",
        "1234",
        
        # 無效格式
        "INVALID",
        "XYZ123",
        "12G",  # 包含非HEX字符
        "",
        "0",
    ]
    
    print("📋 測試用例:")
    for i, test_uid in enumerate(test_cases, 1):
        print(f"  {i:2d}. {test_uid}")
    print()
    
    print("🔍 UID驗證結果:")
    print("-" * 50)
    
    for test_uid in test_cases:
        # 測試格式化
        formatted = car._format_uid(test_uid)
        
        # 測試驗證
        is_valid = car._is_valid_uid(test_uid)
        
        # 結果
        status = "✅ 有效" if is_valid else "❌ 無效"
        print(f"{test_uid:12s} → {formatted:12s} [{status}]")
    
    print()
    print("🎯 重點確認:")
    print("  • HEX格式 (0x1234ABCD) → 應該被接受並格式化為 1234ABCD")
    print("  • TEST格式 (TEST0031) → 應該被接受並保持原樣")
    print("  • 無效格式應該被拒絕並輸出到terminal")
    print()

def test_scoreboard_integration():
    """測試計分板整合"""
    print("🎯 測試計分板整合")
    print("=" * 50)
    
    try:
        # 創建MazeCar實例
        car = MazeCar(bt_port="VIRTUAL")
        
        # 測試fakeUID.csv中的UID
        test_uids = ["TEST0031", "TEST0025", "TEST0044"]
        
        print("📊 測試計分板更新:")
        for uid in test_uids:
            print(f"\n🧪 測試UID: {uid}")
            
            # 格式化UID
            formatted = car._format_uid(uid)
            print(f"   格式化: {formatted}")
            
            # 檢查有效性
            is_valid = car._is_valid_uid(uid)
            print(f"   有效性: {'✅ 有效' if is_valid else '❌ 無效'}")
            
            # 嘗試添加到計分板
            if is_valid:
                score, time_left = car.scoreboard.add_UID(formatted)
                print(f"   計分: +{score} 分")
                print(f"   總分: {car.scoreboard.get_current_score()}")
            
    except Exception as e:
        print(f"❌ 測試過程發生錯誤: {e}")

if __name__ == "__main__":
    print("🚀 UID處理邏輯測試工具")
    print("="*60)
    
    # 測試格式處理
    test_uid_formats()
    
    # 測試計分板整合
    test_scoreboard_integration()
    
    print("✅ 測試完成")
