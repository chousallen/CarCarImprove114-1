#!/usr/bin/env python3
"""
測試模式 - 只開啟記分板GUI，不需要藍牙連線
"""
import logging
import time
import threading
from gui_scoreboard import ScoreboardGUI

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
log = logging.getLogger(__name__)

class MockMazeCar:
    """
    模擬的迷宮車類別，用於測試GUI介面
    """
    def __init__(self, start_node: int = 1, game_duration: int = 600):
        # 只初始化記分板，不需要藍牙連線
        self.scoreboard = ScoreboardGUI(
            start_position=start_node, 
            game_duration=game_duration
        )
        
        # 測試用的假UID列表
        self.test_uids = [
            "TEST0031", "TEST0025", "TEST0044", "TEST0046", 
            "TEST0045", "TEST0047", "TEST0009", "TEST0003"
        ]
        self.current_test_index = 0
        
        log.info("測試模式啟動 - 只有GUI記分板")
        log.info("按空白鍵模擬找到RFID標籤")
        
    def simulate_find_uid(self):
        """模擬找到RFID標籤"""
        if self.current_test_index < len(self.test_uids):
            uid = self.test_uids[self.current_test_index]
            score, time_left = self.scoreboard.add_UID(uid)
            log.info(f"模擬找到UID: {uid}, 得分: {score}, 剩餘時間: {time_left:.1f}s")
            self.current_test_index += 1
            return True
        return False
    
    def setup_keyboard_handler(self):
        """設置鍵盤事件處理"""
        def on_key_press(event):
            if event.keysym == 'space':
                self.simulate_find_uid()
            elif event.keysym == 'q':
                self.scoreboard.quit()
        
        self.scoreboard.bind('<KeyPress>', on_key_press)
        self.scoreboard.focus_set()  # 確保視窗可以接收鍵盤事件
        
    def run_test_mode(self):
        """執行測試模式"""
        log.info("=== 測試模式說明 ===")
        log.info("• 按 [空白鍵] 模擬找到RFID標籤")
        log.info("• 按 [Q] 退出程式")
        log.info("• 記分板會自動計時和計分")
        log.info("==================")
        
        # 設置鍵盤處理
        self.setup_keyboard_handler()
        
        # 可選：自動測試模式
        if input("是否要自動測試模式？(y/N): ").lower() == 'y':
            self.start_auto_test()
        
        # 啟動GUI主迴圈
        try:
            self.scoreboard.mainloop()
        except KeyboardInterrupt:
            log.info("程式被使用者中斷")
        finally:
            final_score = self.scoreboard.get_current_score()
            log.info(f"最終分數: {final_score}")
    
    def start_auto_test(self):
        """啟動自動測試 - 每5秒自動找到一個UID"""
        def auto_test():
            while True:
                time.sleep(5)  # 每5秒
                if not self.simulate_find_uid():
                    break  # 所有測試UID都用完了
        
        # 在背景執行緒中執行自動測試
        auto_thread = threading.Thread(target=auto_test, daemon=True)
        auto_thread.start()
        log.info("自動測試模式啟動 - 每5秒自動找到一個RFID")

def main():
    """主函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='迷宮記分板測試程式')
    parser.add_argument('--node', type=int, default=1,
                      help='起始節點 (預設: 1)')
    parser.add_argument('--time', type=int, default=600,
                      help='遊戲時間秒數 (預設: 600)')
    
    args = parser.parse_args()
    
    # 建立測試用的迷宮車
    test_car = MockMazeCar(
        start_node=args.node,
        game_duration=args.time
    )
    
    # 執行測試模式
    test_car.run_test_mode()

if __name__ == "__main__":
    main()
