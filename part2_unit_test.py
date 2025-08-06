# test_solution.py

import json
import logging
import unittest
# Import hàm cần được kiểm thử từ file part2_solution.py
from part2_solution import process_and_analyze_ocr_output

class TestProcessOCRSolution(unittest.TestCase):
    """
    Bộ unit test cho hàm process_and_analyze_ocr_output.
    Mỗi test case sẽ kiểm tra một khía cạnh cụ thể của hàm.
    """

    # ===== Test Case 1: Kịch bản chính (Happy Path) =====
    def test_full_processing_happy_path(self):
        """
        Kiểm tra kịch bản đầy đủ với dữ liệu mẫu.
        Đảm bảo hàm có thể:
        - Trích xuất đúng số lượng giao dịch hợp lệ.
        - Làm sạch, phân loại, và gắn cờ đúng.
        - Lọc bỏ các giao dịch không hợp lệ (amount âm, thiếu amount).
        """
        raw_ocr_text = """
        Transaction ID: T001
        Date: 2025-07-31 | Amount: 1,500,000 VND | Desc: Thanh toán tiền quảng cáo Facebook Ads
        ---
        ID: T002, Date: 2025-07-30, Amount: 3.250.000, Description: Vé máy bay đi công tác Hà Nội
        ---
        ID T004 | Date 2025-07-29 | Amount -500000 | Desc: Mua giấy in và mực in VPP
        ---
        ID: T005, Date: 2025-07-31, Amount: 25O.OOO, Description: Tiền taxi ra sân bay
        ---
        ID: T006, Date: 2025-07-31, Description: Rút tiền mặt khẩn cấp, Amount: 5,000,000
        ---
        ID: T007, Date: 2025-07-28, Desc: Cà phê với team
        """
        expected_output = [
            {'id': 'T001', 'date': '2025-07-31', 'amount': 1500000, 'description': 'Thanh toán tiền quảng cáo Facebook Ads', 'category': 'Marketing', 'is_suspicious': False},
            {'id': 'T002', 'date': '2025-07-30', 'amount': 3250000, 'description': 'Vé máy bay đi công tác Hà Nội', 'category': 'Đi lại', 'is_suspicious': True},
            {'id': 'T005', 'date': '2025-07-31', 'amount': 250000, 'description': 'Tiền taxi ra sân bay', 'category': 'Đi lại', 'is_suspicious': False},
            {'id': 'T006', 'date': '2025-07-31', 'amount': 5000000, 'description': 'Rút tiền mặt khẩn cấp', 'category': 'Khác', 'is_suspicious': True}
        ]
        result = process_and_analyze_ocr_output(raw_ocr_text, config_rules)
        self.assertEqual(result, expected_output)

    # ===== Test Case 2: Đầu vào rỗng =====
    def test_empty_input_string(self):
        """
        Kiểm tra trường hợp ngoại lệ: đầu vào là một chuỗi rỗng.
        Hàm nên trả về một danh sách rỗng một cách an toàn.
        """
        self.assertEqual(process_and_analyze_ocr_output("", config_rules), [])

    # ===== Test Case 3: Không có giao dịch hợp lệ =====
    def test_no_valid_transactions(self):
        """
        Kiểm tra trường hợp đầu vào có nội dung nhưng không chứa giao dịch hợp lệ.
        Ví dụ: tất cả các block đều thiếu trường 'amount'.
        """
        raw_text = "ID: T007, Date: 2025-07-28, Desc: Cà phê với team\n---\nID: T008, Desc: Test"
        self.assertEqual(process_and_analyze_ocr_output(raw_text, config_rules), [])

    # ===== Test Case 4: Lọc Amount lỗi =====
    def test_filtering_of_malformed_amount(self):
        """
        Kiểm tra khả năng lọc bỏ giao dịch có 'amount' không phải là số.
        Hàm cần xử lý lỗi ValueError nhẹ nhàng và bỏ qua giao dịch.
        """
        raw_text = "ID: T009, Amount: Not a number, Desc: Test"
        self.assertEqual(process_and_analyze_ocr_output(raw_text, config_rules), [])

    # ===== Test Case 5: Kiểm tra Bug Fix cho Description =====
    def test_description_parsing_and_cleaning(self):
        """
        Kiểm tra riêng biệt lỗi đã sửa: trích xuất 'description' không bị "tham lam"
        và loại bỏ được dấu phẩy ở cuối.
        """
        raw_text = "ID: T006, Date: 2025-07-31, Description: Rút tiền mặt khẩn cấp, Amount: 5,000,000"
        result = process_and_analyze_ocr_output(raw_text, config_rules)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['description'], 'Rút tiền mặt khẩn cấp')

    # ===== Test Case 6: Kiểm tra logic phân loại "Tiếp khách & Ăn uống" =====
    def test_category_food_and_beverage(self):
        """
        Kiểm tra cụ thể việc phân loại chính xác cho danh mục "Tiếp khách & Ăn uống".
        """
        raw_text = "ID: T010, Amount: 150000, Desc: Cà phê với khách hàng ABC"
        result = process_and_analyze_ocr_output(raw_text, config_rules)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['category'], 'Tiếp khách & Ăn uống')
        
    # ===== Test Case 7: Kiểm tra cờ đáng ngờ chỉ vì số tiền lớn =====
    def test_suspicious_flag_by_high_amount(self):
        """
        Kiểm tra giao dịch được gắn cờ 'is_suspicious' chỉ vì số tiền lớn hơn 3,000,000,
        nhưng không chứa từ khóa nhạy cảm.
        """
        raw_text = "ID: T011, Amount: 3000001, Desc: Mua phần mềm bản quyền"
        result = process_and_analyze_ocr_output(raw_text, config_rules)
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0]['is_suspicious'])
    
    # ===== Test Case 8: Kiểm tra cờ đáng ngờ chỉ vì từ khóa =====
    def test_suspicious_flag_by_keyword(self):
        """
        Kiểm tra giao dịch được gắn cờ 'is_suspicious' chỉ vì mô tả chứa "tiền mặt",
        nhưng số tiền lại nhỏ.
        """
        raw_text = "ID: T012, Amount: 100000, Desc: Phí rút tiền mặt tại ATM"
        result = process_and_analyze_ocr_output(raw_text, config_rules)
        self.assertEqual(len(result), 1)
        self.assertTrue(result[0]['is_suspicious'])

    # ===== Test Case 9: Xử lý giao dịch thiếu trường Description =====
    def test_missing_description_field(self):
        """
        Kiểm tra trường hợp một giao dịch hợp lệ nhưng không có trường 'description'.
        Hàm cần gán giá trị mặc định (chuỗi rỗng) và phân loại là "Khác".
        """
        raw_text = "ID: T013, Date: 2025-08-01, Amount: 500000"
        result = process_and_analyze_ocr_output(raw_text, config_rules)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['description'], '')
        self.assertEqual(result[0]['category'], 'Khác')
        self.assertFalse(result[0]['is_suspicious'])

    # ===== Test Case 10: Độ bền với thứ tự trường dữ liệu thay đổi =====
    def test_robustness_to_field_order(self):
        """
        Kiểm tra xem hàm có trích xuất đúng không khi thứ tự các trường bị đảo lộn.
        Điều này chứng tỏ việc dùng Regex linh hoạt hơn so với split() đơn giản.
        """
        raw_text = "Amount: 750.000, Description: Ăn trưa cùng team, ID: T014, Date: 2025-08-02"
        expected = {
            'id': 'T014', 'date': '2025-08-02', 'amount': 750000, 
            'description': 'Ăn trưa cùng team', 'category': 'Tiếp khách & Ăn uống', 
            'is_suspicious': False
        }
        result = process_and_analyze_ocr_output(raw_text, config_rules)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], expected)

# Chạy các unit test khi file được thực thi trực tiếp
if __name__ == '__main__':
    # Đọc file cấu hình khi chạy chương trình
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config_rules = json.load(f)
    except FileNotFoundError:
        logging.error("Lỗi: Không tìm thấy file 'config.json'. Vui lòng tạo file cấu hình.")
        config_rules = {} # Thoát hoặc dùng config mặc định
    except json.JSONDecodeError:
        logging.error("Lỗi: File 'config.json' có định dạng không hợp lệ.")
        config_rules = {}
        
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
