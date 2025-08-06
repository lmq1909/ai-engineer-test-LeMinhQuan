import re
from pprint import pprint

def process_and_analyze_ocr_output(raw_text: str) -> list[dict]:
    """
    Đọc chuỗi OCR thô, trích xuất, làm sạch, phân loại và phân tích các giao dịch.

    Args:
        raw_text: Một chuỗi văn bản duy nhất chứa nhiều bản ghi giao dịch.

    Returns:
        Một danh sách các dictionary, mỗi dictionary đại diện cho một giao dịch hợp lệ
        đã được xử lý và làm giàu thông tin.
    """

    # 1. Tách các khối giao dịch riêng lẻ
    # Các giao dịch được phân tách bằng "---"
    transaction_blocks = raw_text.strip().split('---')

    processed_transactions = []

    # Định nghĩa các biểu thức chính quy (Regex) để trích xuất thông tin
    # linh hoạt với các key và dấu phân cách khác nhau.
    patterns = {
        'id': re.compile(r'(?:Transaction ID|ID)\s*[:|]?\s*([T\d]+)'),
        'date': re.compile(r'Date\s*[:|]?\s*(\d{4}-\d{2}-\d{2})'),
        'amount': re.compile(r'Amount\s*[:|]?\s*(-?[\d,O\.]+)'),
        'description': re.compile(r'(?:Description|Desc)\s*[:|]?\s*(.*?)(?=\s*\|?\s*(?:ID|Date|Amount)|$)')
    }

    for block in transaction_blocks:
        if not block.strip():
            continue

        # Thay thế các dấu phân cách để dễ dàng parse hơn
        # và nối các dòng lại thành một dòng duy nhất
        single_line_block = ' '.join(block.strip().splitlines())

        # 2. Trích xuất thông tin thô từ mỗi khối
        extracted_data = {}
        for key, pattern in patterns.items():
            match = pattern.search(single_line_block)
            if match:
                extracted_data[key] = match.group(1).strip().strip(',')
            else:
                extracted_data[key] = None

        # Bỏ qua nếu thiếu thông tin cốt lõi (ID hoặc Amount)
        if not extracted_data.get('amount') or not extracted_data.get('id'):
            continue
            
        # 3. Làm sạch và chuẩn hóa dữ liệu
        # Chuẩn hóa Amount: loại bỏ ký tự lạ và chuyển đổi sang số nguyên
        try:
            # Thay thế ký tự 'O' thành '0' và loại bỏ dấu phẩy/chấm
            cleaned_amount_str = extracted_data['amount'].replace('O', '0').replace(',', '').replace('.', '')
            amount = int(cleaned_amount_str)
        except (ValueError, TypeError):
            # Nếu không thể chuyển đổi, bỏ qua giao dịch này
            continue
            
        # Lọc bỏ các giao dịch không hợp lệ (amount âm)
        if amount < 0:
            continue
            
        description = extracted_data.get('description', '')
        if not description:
            description = ""

        # 4. Phân loại giao dịch
        category = "Khác"
        desc_lower = description.lower()
        if any(keyword in desc_lower for keyword in ["máy bay", "taxi", "grab"]):
            category = "Đi lại"
        elif any(keyword in desc_lower for keyword in ["ăn trưa", "cà phê", "tiếp khách"]):
            category = "Tiếp khách & Ăn uống"
        elif any(keyword in desc_lower for keyword in ["quảng cáo", "ads", "facebook"]):
            category = "Marketing"

        # 5. Gắn cờ giao dịch đáng ngờ
        is_suspicious = False
        if amount > 3_000_000 or "tiền mặt" in desc_lower:
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
    """

    final_transactions = process_and_analyze_ocr_output(raw_ocr_text)

    print("Kết quả các giao dịch đã được xử lý:")
    pprint(final_transactions)
    
    # [
    #  {'id': 'T001', 'date': '2025-07-31', 'amount': 1500000, 'description': 'Thanh toán tiền quảng cáo Facebook Ads', 'category': 'Marketing', 'is_suspicious': False},
    #  {'id': 'T002', 'date': '2025-07-30', 'amount': 3250000, 'description': 'Vé máy bay đi công tác Hà Nội', 'category': 'Đi lại', 'is_suspicious': True},
    #  {'id': 'T005', 'date': '2025-07-31', 'amount': 250000, 'description': 'Tiền taxi ra sân bay', 'category': 'Đi lại', 'is_suspicious': False},
    #  {'id': 'T006', 'date': '2025-07-31', 'amount': 5000000, 'description': 'Rút tiền mặt khẩn cấp', 'category': 'Khác', 'is_suspicious': True}
    # ]