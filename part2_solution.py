import re
import json
import logging
from pprint import pprint

# Thiết lập logging cơ bản
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def process_and_analyze_ocr_output(raw_text: str, config: dict) -> list[dict]: # Thêm 'config' vào tham số
    """
    Đọc chuỗi OCR thô, trích xuất, làm sạch, phân loại và phân tích các giao dịch.

    Args:
        raw_text: Một chuỗi văn bản duy nhất chứa nhiều bản ghi giao dịch.
        config: Một dictionary chứa các quy tắc nghiệp vụ (đọc từ file config.json).

    Returns:
        Một danh sách các dictionary, mỗi dictionary đại diện cho một giao dịch hợp lệ
        đã được xử lý và làm giàu thông tin.
    """
    transaction_blocks = raw_text.strip().split('---')
    processed_transactions = []

    patterns = {
        'id': re.compile(r'(?:Transaction ID|ID)\s*[:|]?\s*([T\d]+)'),
        'date': re.compile(r'Date\s*[:|]?\s*(\d{4}-\d{2}-\d{2})'),
        'amount': re.compile(r'Amount\s*[:|]?\s*(-?[\d,O\.]+)'),
        'description': re.compile(r'(?:Description|Desc)\s*[:|]?\s*(.*?)(?=\s*\|?\s*(?:ID|Date|Amount)|$)')
    }

    for i, block in enumerate(transaction_blocks):
        block_content = block.strip()
        if not block_content:
            continue

        single_line_block = ' '.join(block_content.splitlines())
        extracted_data = {}
        for key, pattern in patterns.items():
            match = pattern.search(single_line_block)
            if match:
                extracted_data[key] = match.group(1).strip().strip(',')
            else:
                extracted_data[key] = None

        # Bỏ qua nếu thiếu thông tin cốt lõi (ID hoặc Amount)
        if not extracted_data.get('amount') or not extracted_data.get('id'):
            # Thêm logging thay vì bỏ qua âm thầm
            logging.warning(f"Bỏ qua khối giao dịch #{i+1} do thiếu ID hoặc Amount. Nội dung: '{block_content}'")
            continue
            
        # Làm sạch và chuẩn hóa Amount
        try:
            cleaned_amount_str = extracted_data['amount'].replace('O', '0').replace(',', '').replace('.', '')
            amount = int(cleaned_amount_str)
        except (ValueError, TypeError):
            logging.warning(f"Bỏ qua khối giao dịch #{i+1} do định dạng Amount không hợp lệ. Nội dung: '{block_content}'")
            continue
            
        # Lọc bỏ các giao dịch không hợp lệ (amount âm)
        if amount < 0:
            logging.info(f"Bỏ qua giao dịch ID {extracted_data['id']} do có số tiền âm ({amount}).")
            continue
            
        description = extracted_data.get('description', "")
        if not description:
            description = ""
        
        # Logic phân loại dựa trên file config
        category = "Khác"
        desc_lower = description.lower()
        for cat, keywords in config['categorization_rules'].items():
            if any(keyword in desc_lower for keyword in keywords):
                category = cat
                break

        # Logic gắn cờ đáng ngờ dựa trên file config
        is_suspicious = False
        suspicious_threshold = config['suspicious_amount_threshold']
        suspicious_keywords = config['suspicious_keywords']
        if amount > suspicious_threshold or any(keyword in desc_lower for keyword in suspicious_keywords):
            is_suspicious = True

        # Tạo đối tượng giao dịch đã được làm sạch
        processed_transaction = {
            "id": extracted_data['id'],
            "date": extracted_data['date'],
            "amount": amount,
            "description": description,
            "category": category,
            "is_suspicious": is_suspicious
        }
        processed_transactions.append(processed_transaction)

    return processed_transactions

# Dữ liệu đầu vào mẫu để kiểm thử
if __name__ == "__main__":
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

    if config_rules:
        raw_ocr_text = """
        Transaction ID: T001
        Date: 2025-07-31 | Amount: 1,500,000 VND
        Desc: Thanh toán tiền quảng cáo Facebook Ads
        ---
        ID: T002, Date: 2025-07-30, Amount: 3.250.000
        Description: Vé máy bay đi công tác Hà Nội
        ---
        ID T004 | Date 2025-07-29 | Amount -500000 | Desc: Mua giấy in và mực in VPP
        ---
        ID: T005, Date: 2025-07-31, Amount: 25O.OOO, Description: Tiền taxi ra sân bay
        ---
        ID: T006, Date: 2025-07-31, Description: Rút tiền mặt khẩn cấp, Amount: 5,000,000
        ---
        ID: T007, Date: 2025-07-28, Desc: Cà phê với team
        ---
        Transaction ID: T008, Date: 2025-08-01, Amount: Not a Number
        """

        final_transactions = process_and_analyze_ocr_output(raw_ocr_text, config_rules)

        print("\nKết quả các giao dịch đã được xử lý:")
        pprint(final_transactions)