# Phần 3: Tư duy về AI/VLMs

## 1. Thiết kế Prompt chi tiết cho VLM

Dưới đây là một prompt chi tiết được thiết kế để trích xuất thông tin từ email khiếu nại của khách hàng một cách chính xác và có cấu trúc.

---

### **Prompt Gửi đến VLM**

**[ROLE]**
Bạn là một trợ lý ảo chuyên nghiệp, chuyên phân tích và trích xuất thông tin từ các email khiếu nại của khách hàng trong lĩnh vực tài chính. Hãy hành động một cách cẩn thận, chính xác và chỉ dựa vào thông tin được cung cấp.

**[OBJECTIVE]**
Mục tiêu của bạn là đọc kỹ email của khách hàng dưới đây, trích xuất các thông tin quan trọng theo yêu cầu, và định dạng toàn bộ kết quả đầu ra dưới dạng một đối tượng JSON duy nhất.

**[CONTEXT]**
Email sau đây là một khiếu nại từ khách hàng về một giao dịch mà họ cho là không chính xác.

**[KEY STEPS]**
1.  **Đọc và Phân tích:** Đọc toàn bộ nội dung email để hiểu rõ vấn đề của khách hàng.
2.  **Trích xuất Thông tin:** Tìm và trích xuất các trường dữ liệu sau:
    *   `customer_name`: Tên của khách hàng.
    *   `company_name`: Tên công ty của khách hàng (nếu có).
    *   `transaction_id`: Mã giao dịch bị khiếu nại.
    *   `transaction_date`: Ngày giao dịch.
    *   `transaction_amount`: Số tiền của giao dịch (chỉ lấy số).
    *   `reason_for_complaint`: Lý do khách hàng khiếu nại (ví dụ: "không nhận ra giao dịch", "sai số tiền", "giao dịch trùng lặp").
3.  **Tóm tắt Vấn đề:** Viết một câu tóm tắt ngắn gọn (dưới 25 từ) về vấn đề cốt lõi của khách hàng.
4.  **Xử lý Dữ liệu Thiếu:** Nếu bất kỳ thông tin nào không có trong email, hãy sử dụng giá trị `null` cho trường đó. **Tuyệt đối không được tự suy diễn hoặc bịa đặt thông tin.**
5.  **Định dạng Đầu ra:** Trả về kết quả dưới dạng một đối tượng JSON hợp lệ.

**[EXAMPLE]**
*   **Input Email:** "Chào đội ngũ Bizzi, Tôi là Trần Thị B. Tôi xem sao kê và thấy giao dịch T123 ngày 2025-08-01 có số tiền 500,000đ bị trừ 2 lần. Vui lòng kiểm tra. Cảm ơn."
*   **Expected JSON Output:**
    ```
    {
      "customer_name": "Trần Thị B",
      "company_name": null,
      "transaction_id": "T123",
      "transaction_date": "2025-08-01",
      "transaction_amount": 500000,
      "reason_for_complaint": "Giao dịch bị tính phí hai lần",
      "summary": "Khách hàng khiếu nại về việc giao dịch T123 bị tính phí trùng lặp."
    }
    ```

**[INPUT EMAIL]**
{{customer_email_content}}


**[OUTPUT TEMPLATE]**
Hãy trả lời bằng một đối tượng JSON duy nhất theo cấu trúc sau:  
{  
    "customer_name": "...",  
    "company_name": "...",  
    "transaction_id": "...",  
    "transaction_date": "...",  
    "transaction_amount": ...,  
    "reason_for_complaint": "...",  
    "summary": "..."  
}  


---

## 2. Phân tích rủi ro & giải pháp

### Rủi ro 1: VLM "Ảo giác" (Hallucination) hoặc Trích xuất sai thông tin

*   **Mô tả:** VLM có thể bịa đặt thông tin không có trong email (ví dụ: tự tạo một mã giao dịch) hoặc trích xuất sai các chi tiết quan trọng (ví dụ: nhầm lẫn số tiền). Điều này cực kỳ nguy hiểm vì nó dẫn đến việc giải quyết sai vấn đề của khách hàng.
*   **Giải pháp:**
    *   **Cải thiện Prompt:** Thêm các chỉ dẫn cực kỳ nghiêm ngặt như: *"Tuyệt đối không được tự suy diễn hoặc bịa đặt thông tin. Nếu không tìm thấy, hãy dùng giá trị `null`."*. Sử dụng ví dụ (one-shot/few-shot learning) trong prompt cũng giúp "neo" VLM vào đúng định dạng và hành vi mong muốn.
    *   **Cải thiện Quy trình:** Xây dựng một quy trình "Human-in-the-loop". Với các khiếu nại có giá trị cao hoặc khi VLM trả về một điểm tin cậy (confidence score) thấp, hệ thống sẽ tự động tạo một task để nhân viên hỗ trợ xác thực lại thông tin trước khi xử lý.

### Rủi ro 2: Bỏ qua Ngữ cảnh và Sắc thái Cảm xúc

*   **Mô tả:** VLM có thể trích xuất đúng dữ kiện nhưng hoàn toàn bỏ lỡ sắc thái của email, chẳng hạn như sự khẩn cấp ("giúp tôi gấp") hoặc sự thất vọng của khách hàng. Điều này dẫn đến việc tất cả các khiếu nại được xử lý như nhau, làm giảm chất lượng dịch vụ khách hàng.
*   **Giải pháp:**
    *   **Cải thiện Prompt:** Mở rộng yêu cầu trích xuất, thêm các trường như `urgency_level` và `customer_sentiment`. Ví dụ:
        ```
        {
          ...,
          "urgency_level": "High | Medium | Low",
          "customer_sentiment": "Positive | Neutral | Negative | Angry"
        }
        ```
        Yêu cầu VLM: *"Dựa vào các từ ngữ trong email, hãy đánh giá mức độ khẩn cấp của yêu cầu và cảm xúc chung của khách hàng."*
    *   **Cải thiện Quy trình:** Sử dụng các trường `urgency_level` và `customer_sentiment` để tự động hóa việc phân loại và ưu tiên ticket. Các ticket có độ khẩn cấp "High" hoặc cảm xúc "Angry" sẽ được đẩy lên hàng đầu hoặc chuyển đến một nhóm hỗ trợ cấp cao.

---

## 3. Kết hợp OCR và LLM để "Dọn dẹp" Dữ liệu

Để tự động sửa lỗi từ OCR, ta có thể thiết kế một prompt chuyên biệt cho tác vụ "dọn dẹp" và chuẩn hóa.

**Ý tưởng:** Sử dụng LLM như một tầng trung gian thông minh giữa OCR và hệ thống xử lý chính. LLM sẽ nhận văn bản OCR thô và trả về phiên bản đã được sửa lỗi dựa trên kiến thức ngữ nghĩa về tài chính và ngôn ngữ.

### **Prompt "Dọn dẹp" OCR**

**[ROLE]**
Bạn là một chuyên gia xử lý dữ liệu, có nhiệm vụ sửa các lỗi văn bản được trích xuất từ hệ thống OCR cho các tài liệu tài chính (hóa đơn, biên lai) của Việt Nam.

**[OBJECTIVE]**
Mục tiêu của bạn là đọc đoạn văn bản bị lỗi dưới đây và trả về một phiên bản đã được làm sạch, sửa lỗi chính tả và chuẩn hóa định dạng.

**[KEY STEPS & RULES]**
1.  **Sửa lỗi chính tả:** Sửa các lỗi chính tả phổ biến trong tiếng Việt, đặc biệt là các thuật ngữ tài chính (ví dụ: "Hóa dơn" -> "Hóa đơn", "Tỏng cọng" -> "Tổng cộng").
2.  **Sửa lỗi nhận dạng ký tự:** Thay thế các ký tự bị OCR nhận dạng sai. Các lỗi phổ biến bao gồm:
    *   Chữ 'O' thành số '0'.
    *   Chữ 'l' thành số '1'.
    *   Chữ 'S' thành số '5'.
3.  **Chuẩn hóa số tiền:** Giữ lại các số và loại bỏ các ký tự không cần thiết như dấu chấm/phẩy phân cách hàng nghìn, đơn vị tiền tệ ("VND", "đ").
4.  **Giữ nguyên cấu trúc:** Cố gắng giữ nguyên cấu trúc và các từ khác của câu gốc nếu chúng đã đúng. Chỉ sửa những gì cần thiết.

**[EXAMPLES]**
*   **Input:** "Hóa dơn GTGT - Tỏng tiền: 1,O0O.OOO đ"
*   **Output:** "Hóa đơn GTGT - Tổng tiền: 1000000"

*   **Input:** "Thanh toán cho món hàng A, SỐ lượng: l, thành tiển: S0.000"
*   **Output:** "Thanh toán cho món hàng A, Số lượng: 1, thành tiền: 50000"

**[INPUT TEXT]**
{{raw_ocr_text}}


**[OUTPUT]**
Chỉ trả về chuỗi văn bản đã được làm sạch.

---

## 4. Tư duy Sản phẩm: Trích xuất Thông tin "Phi kỹ thuật"

Nếu là Product Owner, ngoài các thông tin kỹ thuật cơ bản cần trích xuất (như mã giao dịch, ngày tháng), tôi sẽ muốn AI không chỉ trích xuất dữ liệu mà còn phải phân loại chúng thành hai nhóm thông tin có giá trị cao sau:

### 1. Thông tin Định danh và Liên hệ (Identification and Contact Information)
*   **Thông tin cần trích xuất:** `customer_name`, `company_name`, `email_address`, `phone_number`.
*   **Tại sao thông tin này lại có giá trị?** Đây là nhóm thông tin vận hành cốt lõi. Việc AI trích xuất chính xác các thông tin này giúp hệ thống **xác định ngay lập tức khách hàng là ai và tạo ticket với đầy đủ dữ liệu để đội ngũ hỗ trợ có thể liên hệ lại ngay**. Điều này trực tiếp làm giảm thời gian xử lý ban đầu, tăng tốc độ phản hồi và nâng cao hiệu quả hoạt động.

### 2. "Loại Vấn đề Gốc" (Root Cause Category)
*   **Thông tin cần trích xuất:** Đây là thông tin "phi kỹ thuật" mang tính chiến lược dài hạn. Thay vì chỉ lấy lý do mà khách hàng nêu ra, AI sẽ phân loại chúng vào các nhóm có ý nghĩa hơn về mặt sản phẩm. Ví dụ:
    *   `Unrecognized_Merchant`: Khách hàng không nhận ra tên cửa hàng/dịch vụ trên sao kê.
    *   `Suspected_Fraud`: Khách hàng tin rằng đây là giao dịch lừa đảo.
    *   `Incorrect_Amount`: Số tiền bị tính sai.
    *   `Duplicate_Charge`: Giao dịch bị tính phí nhiều lần.
    *   `Service_Not_Rendered`: Khách hàng đã trả tiền nhưng không nhận được hàng hóa/dịch vụ.
*   **Tại sao thông tin này lại có giá trị?** Thông tin này là "vàng" vì nó giúp chuyển từ việc **"phản ứng"** với từng khiếu nại sang việc **"chủ động"** cải thiện sản phẩm và quy trình trong dài hạn.
    1.  **Phát hiện Vấn đề Hệ thống:** Nếu có nhiều ticket được phân loại là `Unrecognized_Merchant` đối với cùng một nhà cung cấp (ví dụ: "SQ*GOODFOOD" thay vì "Nhà hàng Good Food"), đội ngũ sản phẩm có thể làm việc với đối tác thanh toán để làm rõ thông tin hiển thị trên sao kê, giúp giảm bớt sự hoang mang cho tất cả người dùng trong tương lai.
    2.  **Cải thiện Trải nghiệm Người dùng (UX):** Một lượng lớn ticket `Duplicate_Charge` có thể chỉ ra một lỗi trong luồng thanh toán của ứng dụng hoặc một vấn đề từ phía cổng thanh toán. Đây là tín hiệu rõ ràng để đội ngũ kỹ thuật điều tra và khắc phục.
    3.  **Xây dựng Tính năng Phòng ngừa:** Nếu `Suspected_Fraud` là một danh mục phổ biến, Product Owner có thể ưu tiên phát triển các tính năng bảo mật cao hơn như cảnh báo giao dịch theo thời gian thực, hoặc một quy trình đơn giản hơn để người dùng có thể tạm khóa thẻ ngay trong ứng dụng.

Tóm lại, việc AI trích xuất cả thông tin **vận hành (liên hệ)** và thông tin **chiến lược (vấn đề gốc)** sẽ biến bộ phận chăm sóc khách hàng từ một trung tâm chi phí thành một nguồn dữ liệu vô giá để cải tiến sản phẩm.