# AI Engineer Test - Lê Minh Quân

Repository này chứa bài làm cho bài test đầu vào vị trí Fresher AI Product Engineer tại Bizzi.

## Cấu trúc Repository

*   `part1_answers.md`: Trả lời các câu hỏi kiến thức nền tảng.
*   `part2_solution.py`: Mã nguồn giải pháp cho bài toán Coding Challenge.
*   `part2_unit_test.py`: Unit test cho `part2_solution.py`.
*   `part3_prompt_design.md`: Thiết kế prompt và trả lời các câu hỏi tư duy về LLMs.
*   `README.md`: Giải thích về thiết kế và các quyết định trong Phần 2 (file này).

## Part 2: Coding Challenge - Giải thích Giải pháp

### Về xử lý OCR: Phương pháp trích xuất dữ liệu

Để trích xuất dữ liệu từ chuỗi text thô, tôi đã kết hợp hai phương pháp:

1.  **String Splitting (`.split('---')`)**: Đầu tiên, tôi dùng phương pháp này để tách chuỗi đầu vào thành các khối văn bản riêng lẻ, mỗi khối tương ứng với một giao dịch. Đây là cách tiếp cận đơn giản và hiệu quả vì dấu `---` là một dấu phân cách nhất quán giữa các giao dịch.

2.  **Biểu thức chính quy (Regular Expressions - Regex)**: Sau khi có từng khối giao dịch, tôi sử dụng Regex để trích xuất các trường thông tin (`id`, `date`, `amount`, `description`).

**Lý do chọn Regex:**
Dữ liệu OCR thô rất không đồng nhất:
*   **Tên trường (key) thay đổi**: `ID` vs. `Transaction ID`, `Desc` vs. `Description`.
*   **Dấu phân cách không nhất quán**: `:`, `|`, và `,`.
*   **Thứ tự các trường có thể bị đảo lộn**.

Regex là công cụ mạnh mẽ và linh hoạt nhất để xử lý loại dữ liệu bán cấu trúc (semi-structured) và nhiễu này. Nó cho phép tôi định nghĩa các "khuôn mẫu" có thể khớp với nhiều biến thể khác nhau của key và dấu phân cách, giúp mã nguồn trở nên mạnh mẽ và ít bị lỗi hơn so với việc dùng `.split()` nhiều lần, vốn rất dễ bị hỏng khi cấu trúc thay đổi.

### Về thiết kế: Lựa chọn cấu trúc dữ liệu

Tôi đã chọn cấu trúc `list` of `dict` (`List[Dict]`) để lưu trữ và trả về kết quả cuối cùng.

*   **Dictionary (`dict`)**: Được chọn để đại diện cho một giao dịch duy nhất. Cấu trúc `key-value` của dictionary rất tự nhiên và dễ đọc, giúp truy cập dữ liệu một cách tường minh (ví dụ: `transaction['amount']`) thay vì qua chỉ số (`transaction[2]`), vốn khó hiểu và khó bảo trì.
*   **List (`list`)**: Được dùng để chứa tập hợp các dictionary giao dịch. Đây là cấu trúc phù hợp nhất để lưu một chuỗi các đối tượng và cho phép lặp qua một cách dễ dàng.

**Lựa chọn khác và tại sao không dùng:**
*   **Custom Class (ví dụ: `class Transaction`)**: Đây là một lựa chọn rất tốt, đặc biệt cho các dự án lớn. Nó cung cấp type hinting mạnh mẽ hơn, khả năng đóng gói logic (ví dụ: phương thức `transaction.categorize()`), và dễ bảo trì hơn. Tuy nhiên, đối với một script nhỏ và mục tiêu của bài toán này, việc dùng `dict` là đủ đơn giản, hiệu quả và không đòi hỏi mã nguồn bổ sung.

### Về xử lý Lỗi: Các trường hợp ngoại lệ đã lường trước

Trong quá trình viết code, tôi đã lường trước và xử lý các trường hợp ngoại lệ (edge cases) sau:
*   **Đầu vào rỗng**: Hàm sẽ trả về một danh sách rỗng nếu chuỗi đầu vào không có nội dung.
*   **Giao dịch thiếu trường bắt buộc**: Các giao dịch thiếu `id` hoặc `amount` sẽ được bỏ qua một cách an toàn.
*   **Dữ liệu `amount` bị lỗi**:
    *   **Ký tự lạ**: `replace('O', '0')` để xử lý lỗi OCR phổ biến.
    *   **Kiểu dữ liệu sai**: Sử dụng khối `try-except` để bắt lỗi `ValueError` khi trường `amount` không thể chuyển đổi thành số (ví dụ: "Not a number").
    *   **Số tiền âm**: Lọc bỏ các giao dịch có `amount` là số âm, vì chúng không hợp lệ theo yêu cầu.
*   **Giao dịch thiếu trường không bắt buộc**: Nếu `description` bị thiếu, hàm sẽ tự động gán một chuỗi rỗng để các bước xử lý sau đó không bị lỗi.
*   **Định dạng chuỗi phức tạp**: Sử dụng Regex "non-greedy" `(.*?)` và "lookahead" `(?=...)` để đảm bảo trích xuất đúng `description` ngay cả khi nó nằm ở giữa các trường khác.

Các trường hợp này đều đã được kiểm chứng thông qua các unit test trong file `part2_unit_test.py`.

### Về cải tiến: Các điểm có thể tối ưu hóa

Nếu có nhiều thời gian hơn, tôi sẽ cải thiện giải pháp ở các điểm sau:
1.  **Mở rộng Unit Test**: Bổ sung thêm nhiều unit test hơn nữa để bao phủ các trường hợp ngoại lệ phức tạp hơn, đảm bảo độ tin cậy của hàm ở mức cao nhất.
2.  **Sử dụng Dataclass hoặc Pydantic**: Để tăng cường tính dễ đọc và đảm bảo kiểu dữ liệu, tôi sẽ chuyển đổi cấu trúc `dict` thành một `dataclass` hoặc một mô hình Pydantic. Pydantic đặc biệt mạnh mẽ vì nó tự động thực hiện việc xác thực (validation) dữ liệu.

