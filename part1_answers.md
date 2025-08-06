# Part 1 – Answers

**Câu 1:** Trong Python, cấu trúc dữ liệu nào sau đây là "immutable" (bất biến)?  
**Trả lời:** D (Tuple)

**Câu 2:** Phương thức đặc biệt nào trong một Class của Python được tự động gọi khi một đối tượng mới được tạo ra?  
**Trả lời:** B (__init__)

**Câu 3:** Overfitting trong Machine Learning là hiện tượng gì?  
**Trả lời:** C (Mô hình hoạt động cực kỳ tốt trên tập huấn luyện nhưng rất kém trên tập kiểm thử.)

**Câu 4:** Lệnh `git clone [url]` dùng để làm gì?  
**Trả lời:** D (Tạo một bản sao của một repository từ xa về máy local.)

**Câu 5:** JSON là viết tắt của cụm từ nào và nó thường được sử dụng để làm gì?  
**Trả lời:** JSON viết tắt của *JavaScript Object Notation*; đây là định dạng trao đổi dữ liệu văn bản nhẹ, có cấu trúc khóa–giá trị, thường dùng để truyền dữ liệu giữa máy chủ và ứng dụng web hoặc lưu trữ cấu hình.

**Câu 6:** Mục đích chính của việc sử dụng Docker khi triển khai ứng dụng là gì?  
**Trả lời:** Docker đóng gói ứng dụng cùng toàn bộ môi trường và phụ thuộc trong một container, bảo đảm “chạy ở đây được thì chạy ở kia cũng được”, giúp đơn giản hóa triển khai, mở rộng và quản lý phiên bản.

**Câu 7:** OCR là viết tắt của cụm từ gì? Hãy nêu 2 thách thức lớn nhất khi xử lý tài liệu tài chính như hoá đơn, biên lai.  
**Trả lời:** OCR là *Optical Character Recognition*. Hai thách thức lớn:  
• Độ đa dạng bố cục (dạng bảng chi tiết nhiều cột, văn bản rời rạc, logo làm nhiễu)
• Đa dạng phông chữ giữa các loại chứng từ. (ví dụ chữ ký làm nhiễu, số 1 in nghiêng rất giống với số 7 in thẳng)
• Nhiễu hình ảnh (mờ, bóng, gấp nếp, chụp lệch) làm giảm độ chính xác nhận dạng.

**Câu 8:** Điểm khác biệt cốt lõi giữa OCR truyền thống (dựa trên template) và OCR sử dụng mô hình ngôn ngữ lớn (LLM) là gì? Tại sao OCR dựa trên LLM phù hợp hơn khi xử lý hàng nghìn loại chứng từ?  
**Trả lời:**   
1. Điểm khác biệt cốt lõi là OCR truyền thống chỉ nhận dạng ký tự dựa trên quy tắc và vị trí (template), trong khi OCR kết hợp LLM/VLM hiểu ngữ cảnh của toàn bộ tài liệu để suy luận thông tin.

2. OCR dựa trên LLM/VLM phù hợp hơn để xử lý hàng nghìn loại chứng từ vì:  
• Khả năng mở rộng vượt trội: Nó không đòi hỏi phải xây dựng và bảo trì hàng nghìn template thủ công. Hệ thống có thể xử lý các bố cục hoàn toàn mới ngay lập tức, giúp mở rộng quy mô một cách hiệu quả.  
• Độ chính xác và linh hoạt cao: Nhờ hiểu ngữ cảnh, nó có thể diễn giải chính xác các tài liệu phức tạp, chất lượng thấp, hoặc thậm chí chữ viết tay mà OCR truyền thống thường thất bại. Nó hiểu mối quan hệ giữa các dữ liệu (ví dụ: trong bảng biểu) thay vì chỉ đọc ký tự rời rạc.  
• Trích xuất toàn diện: VLM không chỉ trích xuất văn bản mà còn có thể diễn giải các yếu tố phi văn bản như bảng, biểu đồ, mang lại kết quả đầy đủ và có giá trị hơn.  

**Câu 9:** Khi đánh giá hệ thống OCR trích xuất thông tin từ hoá đơn, ngoài Character Error Rate (CER) còn metric quan trọng nào? Tại sao?

**Trả lời:**
Ngoài CER, để đánh giá toàn diện một hệ thống OCR cho hóa đơn, cần xem xét các chỉ số đo lường hiệu quả nghiệp vụ thay vì chỉ độ chính xác của văn bản. Dưới đây là các metric quan trọng:

1. Word Error Rate (WER) - Tỷ lệ lỗi từ
*   **Tại sao quan trọng?** WER đo lỗi ở cấp độ từ, gần hơn với cách con người đọc hiểu, hữu ích để đánh giá chất lượng nhận dạng tổng thể của các trường mô tả dài.

2. Precision, Recall, và F1 Score (cấp trường)
Đây là bộ ba chỉ số đánh giá sự cân bằng giữa việc trích xuất đúng và đủ.

*   **Precision (Độ chính xác):**
    *   **Tại sao quan trọng?** Đo lường mức độ tin cậy của các thông tin mà hệ thống trích xuất. Precision cao có nghĩa là: "Nếu hệ thống trả về một kết quả, khả năng cao là kết quả đó đúng".
    *   **Cách tính:**
        $$
        \text{Precision} = \frac{\text{True Positives (TP)}}{\text{True Positives (TP)} + \text{False Positives (FP)}}
        $$

*   **Recall (Độ phủ):**
    *   **Tại sao quan trọng?** Đo lường khả năng hệ thống tìm thấy **tất cả** các trường thông tin cần thiết. Recall cao đảm bảo hệ thống hiếm khi bỏ sót thông tin quan trọng.
    *   **Cách tính:**
        $$
        \text{Recall} = \frac{\text{True Positives (TP)}}{\text{True Positives (TP)} + \text{False Negatives (FN)}}
        $$

*   **F1 Score (Điểm F1):**
    *   **Tại sao quan trọng?** Là thước đo cân bằng giữa Precision và Recall, đặc biệt hữu ích khi việc bỏ sót thông tin và việc trích xuất sai đều quan trọng như nhau.
    *   **Cách tính:**
        $$
        \text{F1 Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
        $$
    *(Trong đó: **TP** là trích xuất đúng, **FP** là trích xuất sai, **FN** là bỏ sót.)*

3. Exact Match Rate (EMR) - Tỷ lệ khớp chính xác cấp trường
*   **Tại sao quan trọng?** Đây là chỉ số cốt lõi, đo lường phần trăm các trường (ví dụ: "Tổng tiền") được trích xuất **khớp chính xác tuyệt đối** với dữ liệu gốc. Một EMR cao đảm bảo dữ liệu đầu ra đáng tin cậy mà không cần chỉnh sửa thủ công.


**Câu 10:** Mô tả 1 bước tiền xử lý và 1 bước hậu xử lý ảnh hoá đơn để tăng độ chính xác OCR.  
**Trả lời:**  
• Tiền xử lý: Loại bỏ các đường kẻ bảng (Table Line Removal) – Nhiều hóa đơn chứa thông tin trong các bảng có đường kẻ ngang và dọc. Việc loại bỏ các đường kẻ này giúp mô hình OCR không bị nhầm lẫn, tránh việc các đường kẻ bị nhận dạng nhầm thành ký tự (như chữ 'l' hoặc số '1') và giúp tập trung hoàn toàn vào nội dung văn bản.  
• Hậu xử lý: Dùng kiểm tra chính tả/kho từ vựng chuyên ngành để sửa ký tự sai (ví dụ “Hóa dơn” → “Hóa đơn”) và chuẩn hoá định dạng tiền tệ.