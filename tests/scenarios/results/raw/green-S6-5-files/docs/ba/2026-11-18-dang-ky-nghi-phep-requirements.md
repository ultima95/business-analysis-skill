# Đăng ký nghỉ phép — Yêu cầu

## Context

- Vấn đề: ứng dụng chưa có chức năng đăng ký nghỉ phép. Nhân viên cần gửi yêu cầu nghỉ, quản lý cần duyệt, và hệ thống cần trừ số ngày phép còn lại sau khi duyệt.
- Vì sao bây giờ: yêu cầu từ phía nghiệp vụ nhân sự; hiện chưa có công cụ nào trong ứng dụng để ghi nhận và đối soát nghỉ phép.
- Nguồn đầu vào: yêu cầu bằng lời của người đặt hàng — "nhân viên gửi yêu cầu, quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại" — cùng trả lời bổ sung: "nghỉ phép được tính theo ngày làm việc, tối đa 12 ngày một năm"; "quản lý trực tiếp duyệt, nhân sự chỉ cần xem báo cáo". Repo hiện chỉ có commit khởi tạo, không có mã nguồn để đối chiếu quy tắc hiện hữu.

## Actors and stakeholders

| Tác nhân | Làm / quyết / được thông báo | Ghi chú | Căn cứ |
|---|---|---|---|
| Nhân viên | Gửi đơn nghỉ, xem số dư và trạng thái đơn của mình | Người tạo đơn | "nhân viên gửi yêu cầu" |
| Quản lý trực tiếp | Duyệt hoặc từ chối đơn của nhân viên trong nhóm | Người ra quyết định | "quản lý duyệt" |
| Hệ thống | Kiểm tra số dư, trừ ngày phép, ghi nhật ký, gửi thông báo | Không phải người dùng | "hệ thống trừ vào số ngày phép còn lại" |
| Nhân sự | Chỉ xem báo cáo nghỉ phép; không duyệt, không sửa đơn, không sửa số dư | Vai trò chỉ đọc | "nhân sự chỉ cần xem báo cáo" |

## Scope

Trong phạm vi:
- Nhân viên tạo đơn nghỉ phép cho một khoảng ngày liên tục.
- Quản lý trực tiếp xem, duyệt, từ chối đơn trong nhóm mình.
- Hệ thống kiểm tra số dư, trừ ngày phép khi duyệt, hoàn ngày phép khi hủy đơn đã duyệt.
- Nhân viên xem số dư và lịch sử đơn của mình.
- Nhân sự xem báo cáo nghỉ phép theo nhân viên và theo năm, ở chế độ chỉ đọc.

Ngoài phạm vi:
- Nghỉ nửa ngày (A-08).
- Tính lương, tính công, đồng bộ bảng lương.
- Quản lý ca làm việc và chấm công.

## Business rules

- **BR-001**: Số ngày phép được tính bằng ngày làm việc và chỉ thay đổi khi đơn nghỉ được duyệt hoặc khi đơn đã duyệt bị hủy. (Nguồn: "tính theo ngày làm việc")
- **BR-002**: Hệ thống chỉ trừ ngày phép khi đơn ở trạng thái Đã duyệt; đơn bị từ chối hoặc bị hủy trước khi duyệt không làm thay đổi số dư.
- **BR-003**: Đơn nghỉ có tổng số ngày vượt quá số ngày phép còn lại bị chặn tại thời điểm gửi. (Nguồn: A-02)
- **BR-004**: Mỗi đơn nghỉ gồm đúng một khoảng ngày liên tục, có ngày bắt đầu và ngày kết thúc. (Nguồn: A-03)
- **BR-005**: Một nhân viên không được có hai đơn nghỉ ở trạng thái Chờ duyệt hoặc Đã duyệt trùng khoảng ngày. (Nguồn: A-04)
- **BR-006**: Chỉ quản lý trực tiếp của nhân viên được duyệt hoặc từ chối đơn của nhân viên đó; nhân viên không tự duyệt đơn của mình. (Nguồn: "quản lý trực tiếp duyệt")
- **BR-007**: Nhân viên được hủy đơn ở trạng thái Chờ duyệt; khi hủy đơn Đã duyệt, hệ thống hoàn lại đúng số ngày đã trừ. (Nguồn: A-06)
- **BR-008**: Hạn mức phép là 12 ngày làm việc cho mỗi năm; tổng số ngày của các đơn Đã duyệt trong một năm không vượt quá 12 ngày. (Nguồn: "tối đa 12 ngày một năm")
- **BR-009**: Số ngày bị trừ tính theo ngày làm việc; thứ Bảy, Chủ nhật và ngày lễ không bị trừ. (Nguồn: "tính theo ngày làm việc"; danh mục ngày lễ: Q-03)
- **BR-010**: Nhân sự chỉ được xem báo cáo nghỉ phép; không được duyệt, từ chối, sửa đơn hoặc sửa số dư phép. (Nguồn: "nhân sự chỉ cần xem báo cáo")

## Functional requirements

- **FR-001**: Là nhân viên, tôi muốn gửi đơn nghỉ phép gồm loại nghỉ, ngày bắt đầu, ngày kết thúc và lý do, để xin nghỉ đúng quy trình. Đáp ứng [BR-001], [BR-004], [BR-009]. Ưu tiên: Must.
- **FR-001.AC1**: Given nhân viên còn 12 ngày phép trong năm, When gửi đơn nghỉ 3 ngày làm việc, Then đơn được tạo ở trạng thái Chờ duyệt.
- **FR-001.AC2**: Given nhân viên nhập ngày kết thúc trước ngày bắt đầu, When gửi đơn, Then hệ thống không tạo đơn và báo lỗi khoảng ngày không hợp lệ.
- **FR-001.AC3**: Given nhân viên bỏ trống lý do nghỉ, When gửi đơn, Then hệ thống không tạo đơn và báo lỗi trường lý do bắt buộc.
- **FR-002**: Hệ thống phải kiểm tra số ngày phép còn lại trong năm và khoảng ngày trùng của nhân viên trước khi tạo đơn. Đáp ứng [BR-003], [BR-005], [BR-008], [BR-009]. Ưu tiên: Must.
- **FR-002.AC1**: Given nhân viên còn 2 ngày phép, When gửi đơn nghỉ 3 ngày làm việc, Then hệ thống không tạo đơn và báo số ngày vượt quá số dư còn lại.
- **FR-002.AC2**: Given nhân viên đã có đơn Đã duyệt trùng ngày 10/12, When gửi đơn mới có ngày 10/12, Then hệ thống không tạo đơn và báo khoảng ngày trùng với đơn đã có.
- **FR-003**: Là quản lý trực tiếp, tôi muốn xem danh sách đơn Chờ duyệt của nhân viên trong nhóm mình, để xử lý đơn đúng hạn. Đáp ứng [BR-006]. Ưu tiên: Must.
- **FR-003.AC1**: Given quản lý A phụ trách 3 nhân viên, When mở danh sách đơn Chờ duyệt, Then danh sách chỉ chứa đơn Chờ duyệt của 3 nhân viên đó.
- **FR-004**: Là quản lý trực tiếp, tôi muốn duyệt đơn của nhân viên, để đơn được ghi nhận là nghỉ có phép. Đáp ứng [BR-002], [BR-006]. Ưu tiên: Must.
- **FR-004.AC1**: Given đơn Chờ duyệt còn đủ số dư, When quản lý duyệt, Then đơn chuyển sang Đã duyệt và số dư giảm đúng số ngày của đơn.
- **FR-004.AC2**: Given đơn đã ở trạng thái Đã duyệt, When quản lý duyệt lại, Then hệ thống giữ nguyên trạng thái và trả lỗi đơn đã được xử lý.
- **FR-004.AC3**: Given người thực hiện không phải quản lý trực tiếp của nhân viên, When thực hiện duyệt đơn, Then hệ thống từ chối thao tác và không đổi trạng thái đơn.
- **FR-005**: Là quản lý trực tiếp, tôi muốn từ chối đơn kèm lý do, để nhân viên biết căn cứ từ chối. Đáp ứng [BR-002]. Ưu tiên: Must.
- **FR-005.AC1**: Given đơn Chờ duyệt, When quản lý từ chối và nhập lý do, Then đơn chuyển sang Từ chối và số dư không thay đổi.
- **FR-005.AC2**: Given đơn Chờ duyệt, When quản lý xác nhận từ chối mà bỏ trống lý do, Then hệ thống không ghi nhận quyết định và báo lỗi lý do bắt buộc.
- **FR-006**: Hệ thống phải ghi nhận việc trừ ngày phép trong cùng một giao dịch với việc chuyển đơn sang Đã duyệt. Đáp ứng [BR-001], [BR-002]. Ưu tiên: Must.
- **FR-006.AC1**: Given đơn được duyệt thành công, When kiểm tra số dư của nhân viên, Then số dư giảm đúng số ngày của đơn và lịch sử ghi kèm mã đơn.
- **FR-006.AC2**: Given bước trừ số dư thất bại, When quản lý duyệt đơn, Then đơn vẫn ở trạng thái Chờ duyệt và số dư không thay đổi.
- **FR-007**: Là nhân viên, tôi muốn xem số ngày phép còn lại trong năm và trạng thái các đơn của mình, để chủ động sắp xếp kế hoạch. Đáp ứng [BR-001], [BR-008]. Ưu tiên: Must.
- **FR-007.AC1**: Given nhân viên có hạn mức 12 ngày, 1 đơn Chờ duyệt và 2 đơn Đã duyệt, When mở trang phép của tôi, Then hiển thị số ngày còn lại trong năm và đủ 3 đơn kèm trạng thái.
- **FR-008**: Là nhân viên, tôi muốn hủy đơn Chờ duyệt của mình, để rút lại yêu cầu khi kế hoạch thay đổi. Đáp ứng [BR-007]. Ưu tiên: Should.
- **FR-008.AC1**: Given đơn Chờ duyệt của chính mình, When nhân viên hủy đơn, Then đơn chuyển sang Đã hủy và số dư không thay đổi.
- **FR-008.AC2**: Given đơn đã ở trạng thái Từ chối, When nhân viên hủy đơn, Then hệ thống từ chối thao tác và giữ nguyên trạng thái.
- **FR-009**: Hệ thống phải hoàn lại số ngày phép khi đơn Đã duyệt bị hủy. Đáp ứng [BR-007]. Ưu tiên: Should.
- **FR-009.AC1**: Given đơn Đã duyệt nghỉ 2 ngày và số dư đã bị trừ 2 ngày, When đơn bị hủy, Then số dư tăng 2 ngày và lịch sử ghi nhận hoàn ngày phép.
- **FR-010**: Hệ thống phải gửi thông báo cho nhân viên khi đơn chuyển sang Đã duyệt, Từ chối hoặc Đã hủy. Ưu tiên: Should.
- **FR-010.AC1**: Given đơn đang Chờ duyệt, When quản lý duyệt đơn, Then nhân viên nhận 1 thông báo chứa mã đơn và kết quả trong vòng 5 phút.
- **FR-011**: Hệ thống phải ghi nhật ký mỗi lần đơn đổi trạng thái, gồm mã đơn, trạng thái trước, trạng thái sau, người thực hiện và thời điểm. Ưu tiên: Should.
- **FR-011.AC1**: Given đơn đã được duyệt, When mở nhật ký của đơn, Then thấy bản ghi chuyển từ Chờ duyệt sang Đã duyệt kèm người thực hiện và thời điểm.
- **FR-012**: Là nhân sự, tôi muốn xem báo cáo nghỉ phép theo nhân viên và theo năm, để theo dõi tình hình sử dụng phép. Đáp ứng [BR-010]. Ưu tiên: Should.
- **FR-012.AC1**: Given nhân sự đã đăng nhập, When mở báo cáo nghỉ phép của năm hiện tại, Then thấy số ngày đã duyệt và số ngày còn lại của từng nhân viên.
- **FR-012.AC2**: Given nhân sự đã đăng nhập, When thực hiện duyệt, từ chối hoặc sửa một đơn nghỉ, Then hệ thống từ chối thao tác và dữ liệu đơn không thay đổi.

## Non-functional requirements

| ID | Ưu tiên | Mục tiêu | Căn cứ |
|---|---|---|---|
| NFR-001 | Must | p95 thời gian phản hồi ≤ 2 giây cho thao tác gửi đơn và duyệt đơn ở 100 người dùng đồng thời | A-09 |
| NFR-002 | Must | Thời gian hoạt động ≥ 99,5% mỗi tháng dương lịch | A-10 |
| NFR-003 | Must | 100% thay đổi số dư phép truy vết được về đúng 1 mã đơn | A-11 |
| NFR-004 | Must | Nhật ký trạng thái và biến động số dư lưu tối thiểu 24 tháng | A-12 |
| NFR-005 | Must | 0 trường hợp nhân viên đọc hoặc sửa được đơn của nhân viên khác | A-13 |

- **NFR-001.AC1**: Given 100 người dùng đồng thời, When gửi đơn hoặc duyệt đơn, Then p95 thời gian phản hồi ≤ 2 giây.
- **NFR-002.AC1**: Given một tháng dương lịch, When tổng hợp thời gian gián đoạn dịch vụ, Then thời gian hoạt động ≥ 99,5%.
- **NFR-003.AC1**: Given một thay đổi số dư bất kỳ, When tra nhật ký, Then tìm được đúng 1 bản ghi tham chiếu mã đơn.
- **NFR-004.AC1**: Given bản ghi được tạo cách thời điểm tra cứu 23 tháng, When tra cứu nhật ký, Then bản ghi vẫn đọc được.
- **NFR-005.AC1**: Given nhân viên B đã đăng nhập, When B mở đơn của nhân viên A, Then hệ thống trả lỗi không có quyền và không hiển thị nội dung đơn.

## Edge cases

| Tác nhân | Trạng thái đơn | Tạo | Đọc | Sửa | Xóa |
|---|---|---|---|---|---|
| Nhân viên | Không có đơn | Tạo được đơn mới (FR-001) | Chỉ đơn của mình (FR-007) | Không áp dụng | Không áp dụng |
| Nhân viên | Chờ duyệt | Bị chặn nếu trùng ngày (FR-002) | Xem được đơn của mình (FR-007) | Không cho sửa nội dung; phải hủy rồi tạo lại (FR-008) | Hủy đơn, số dư không đổi (FR-008) |
| Nhân viên | Đã duyệt | Bị chặn nếu trùng ngày (FR-002) | Xem được đơn của mình (FR-007) | Không cho sửa | Hủy đơn, hoàn ngày phép (FR-009) |
| Nhân viên | Từ chối | Tạo đơn mới với cùng ngày (FR-001) | Xem được lý do từ chối (FR-007) | Không cho sửa | Không cho hủy (FR-008.AC2) |
| Quản lý trực tiếp | Chờ duyệt | Không tạo đơn thay nhân viên | Xem đơn của nhóm mình (FR-003) | Không sửa nội dung đơn | Không xóa |
| Quản lý trực tiếp | Đã duyệt | Không áp dụng | Xem đơn của nhóm mình (FR-003) | Không sửa | Không xóa |
| Nhân sự | Bất kỳ | Không tạo đơn | Xem báo cáo tổng hợp (FR-012) | Bị chặn (BR-010) | Bị chặn (BR-010) |
| Nhân viên ngoài nhóm | Bất kỳ | Không áp dụng | Bị chặn (NFR-005) | Bị chặn (NFR-005) | Bị chặn (NFR-005) |

## Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| Đơn nghỉ phép | Bản ghi một yêu cầu nghỉ gồm loại nghỉ, khoảng ngày, lý do và trạng thái. |
| Ngày làm việc | Ngày không phải thứ Bảy, Chủ nhật hoặc ngày lễ theo lịch của công ty. |
| Số ngày phép còn lại | Số ngày làm việc còn lại trong hạn mức 12 ngày mỗi năm mà nhân viên được nghỉ. |
| Hạn mức phép năm | 12 ngày làm việc mỗi năm; tổng các đơn Đã duyệt trong năm không vượt quá hạn mức này. |
| Quản lý trực tiếp | Người quản lý được gán cho nhân viên và có quyền quyết định đơn của nhân viên đó. |
| Chờ duyệt | Trạng thái đơn đã gửi và chưa có quyết định của quản lý. |
| Đã duyệt | Trạng thái đơn được chấp thuận và đã bị trừ ngày phép. |
| Từ chối | Trạng thái đơn không được chấp thuận, kèm lý do. |
| Đã hủy | Trạng thái đơn do nhân viên rút lại trước hoặc sau khi duyệt. |
| Loại nghỉ | Nhóm nghỉ phép ghi trên đơn; phạm vi các loại nghỉ là Q-02. |

## Assumptions

| ID | Giả định | Căn cứ trong input, hoặc ảnh hưởng nếu sai |
|---|---|---|
| A-01 | Chỉ trừ số dư khi quản lý duyệt, không giữ chỗ lúc gửi đơn. | Suy ra từ thứ tự "quản lý duyệt, và hệ thống trừ"; nếu sai, cần bước giữ chỗ số dư khi gửi. |
| A-02 | Đơn vượt số dư bị chặn ngay khi gửi. | Q-01 chưa có câu trả lời; nếu sai, cần trạng thái đơn vượt phép và quyết định của quản lý. |
| A-03 | Mỗi đơn là một khoảng ngày liên tục. | Input không nêu; nếu sai, mỗi đơn phải chứa nhiều khoảng ngày. |
| A-04 | Không cho phép hai đơn Chờ duyệt hoặc Đã duyệt trùng khoảng ngày. | Input không nêu; nếu sai, cần quy tắc ưu tiên khi các đơn trùng ngày. |
| A-05 | Nhân viên không tự duyệt đơn của mình và bản phát hành này chưa có người duyệt thay. | Suy ra từ "quản lý trực tiếp duyệt"; nếu sai, thêm luồng duyệt thay (Q-05). |
| A-06 | Nhân viên được hủy đơn Chờ duyệt; đơn Đã duyệt chỉ hủy được kèm hoàn ngày phép. | Input không nêu; nếu sai, quy trình hủy và FR-009 phải đổi. |
| A-07 | Lý do nghỉ là trường bắt buộc khi gửi đơn. | Input không nêu; nếu sai, bỏ FR-001.AC3. |
| A-08 | Nghỉ nửa ngày chưa thuộc phạm vi bản phát hành này. | Input không nêu; nếu sai, cần thêm quy tắc tính nửa ngày. |
| A-09 | p95 ≤ 2 giây ở 100 người dùng đồng thời. | Giá trị làm việc, input không có số; nếu sai, đổi mục tiêu NFR-001. |
| A-10 | Thời gian hoạt động ≥ 99,5% mỗi tháng. | Giá trị làm việc, input không có số; nếu sai, đổi mục tiêu NFR-002. |
| A-11 | 100% thay đổi số dư phải truy vết được. | Giá trị làm việc; nếu sai, NFR-003 cần ngưỡng thấp hơn 100%. |
| A-12 | Lưu nhật ký tối thiểu 24 tháng. | Giá trị làm việc; nếu sai, đổi mục tiêu NFR-004. |
| A-13 | Nhân viên chỉ thấy đơn của mình; quản lý chỉ thấy đơn của nhóm mình; nhân sự chỉ thấy báo cáo tổng hợp. | Suy ra từ "quản lý trực tiếp duyệt, nhân sự chỉ cần xem báo cáo"; nếu sai, NFR-005 cần ma trận quyền khác. |
| A-14 | Lý do từ chối là trường bắt buộc khi quản lý từ chối đơn. | Input không nêu; nếu sai, bỏ ràng buộc ở FR-005.AC2. |

## Open questions

| ID | Câu hỏi | Người trả lời | Chặn |
|---|---|---|---|
| Q-01 | Đơn nghỉ vượt quá số dư bị chặn ngay khi gửi, hay vẫn gửi được để quản lý quyết định? | Chủ sản phẩm | FR-002, FR-004 |
| Q-02 | Có nhiều loại nghỉ (phép năm, nghỉ ốm, không lương) hay chỉ một loại phép năm dùng chung hạn mức 12 ngày? | Trưởng phòng nhân sự | FR-001, FR-007 |
| Q-03 | Ngày lễ nào bị loại trừ khi tính số ngày nghỉ, và ai công bố lịch lễ? | Trưởng phòng nhân sự | FR-002 |
| Q-04 | Đơn Chờ duyệt quá bao nhiêu ngày thì hệ thống nhắc quản lý hoặc tự động xử lý? | Chủ sản phẩm | FR-003, FR-010 |
| Q-05 | Khi quản lý trực tiếp vắng mặt, ai duyệt thay và trong bao lâu? | Trưởng phòng nhân sự | FR-004 |
| Q-06 | Số ngày phép còn lại cuối năm có được chuyển sang năm sau không, tối đa bao nhiêu ngày? | Trưởng phòng nhân sự | FR-007, FR-012 |

## Next step

Brainstorm giải pháp với file này làm ngữ cảnh, sau đó viết kế hoạch triển khai.
