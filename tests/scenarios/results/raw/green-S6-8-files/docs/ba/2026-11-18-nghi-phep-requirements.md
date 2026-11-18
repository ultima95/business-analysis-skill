# Đăng ký nghỉ phép — Yêu cầu

## Bối cảnh

- Vấn đề: Nhân viên chưa có nơi gửi yêu cầu nghỉ phép trong ứng dụng; việc xin nghỉ và theo dõi số ngày phép còn lại đang nằm ngoài hệ thống.
- Vì sao bây giờ: Yêu cầu tính năng đăng ký nghỉ phép đã được đưa vào phạm vi phát triển ứng dụng.
- Nguồn đầu vào: Mô tả của người yêu cầu — "nhân viên gửi yêu cầu, quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại"; làm rõ ngày 2026-11-18 — "Nghỉ phép được tính theo ngày làm việc, tối đa 12 ngày một năm. Quản lý trực tiếp duyệt, nhân sự chỉ cần xem báo cáo."
- Trạng thái mã nguồn: Repo tại thời điểm phân tích chỉ có lịch sử git, không có mã nguồn. Không có quy tắc nào được khôi phục từ code; mọi điểm chưa có trong đầu vào đều nằm ở bảng Giả định hoặc Câu hỏi mở.

## Tác nhân và bên liên quan

| Tác nhân | Làm / quyết / được thông báo | Ghi chú | Cơ sở |
|---|---|---|---|
| Nhân viên | Gửi đơn nghỉ phép, xem số dư và trạng thái đơn của mình, huỷ đơn | Người khởi tạo duy nhất của đơn | Đầu vào: "nhân viên gửi yêu cầu" |
| Quản lý trực tiếp | Duyệt hoặc từ chối đơn của nhân viên thuộc quyền mình | Người quyết định duy nhất của đơn | Đầu vào: "quản lý duyệt", "Quản lý trực tiếp duyệt" |
| Bộ phận nhân sự (HR) | Chỉ xem báo cáo đơn và số dư để đối soát; không duyệt, không từ chối, không huỷ đơn | Quyền chỉ đọc | Đầu vào: "nhân sự chỉ cần xem báo cáo" |
| Hệ thống | Tính số ngày làm việc, giữ số dư, trừ số dư khi duyệt, chặn vượt 12 ngày/năm, ghi nhật ký | Bên thực thi quy tắc trừ ngày phép | Đầu vào: "hệ thống trừ vào số ngày phép còn lại" |

## Phạm vi

Trong phạm vi:
- Gửi, xem, huỷ đơn nghỉ phép của chính nhân viên.
- Duyệt hoặc từ chối đơn bởi quản lý trực tiếp.
- Giữ và cập nhật số dư ngày phép theo ngày làm việc, giới hạn 12 ngày một năm cho mỗi nhân viên.
- Báo cáo chỉ đọc cho HR về đơn và số dư.
- Nhật ký thay đổi trạng thái đơn.

Ngoài phạm vi:
- Tính lương, tính bảo hiểm, chấm công theo giờ.
- Quy trình tuyển dụng, đánh giá nhân viên.
- Thay đổi cấu trúc tổ chức hoặc quản lý tài khoản người dùng (giả định đã có sẵn — A-13).

## Quy tắc nghiệp vụ

- **BR-001**: Số dư ngày phép chỉ bị trừ khi đơn nghỉ phép chuyển sang trạng thái Đã duyệt; ở trạng thái Chờ duyệt và Từ chối số dư không đổi.
- **BR-002**: Một đơn chỉ được duyệt khi cả hai điều kiện đúng: số ngày làm việc của đơn nhỏ hơn hoặc bằng số dư còn lại tại thời điểm duyệt, và tổng số ngày làm việc của các đơn Đã duyệt trong năm cộng với đơn này không vượt quá 12 ngày.
- **BR-003**: Đơn nghỉ phép có đúng bốn trạng thái — Chờ duyệt, Đã duyệt, Từ chối, Đã huỷ; chỉ đơn ở trạng thái Chờ duyệt mới được duyệt hoặc từ chối, chỉ đơn ở trạng thái Đã duyệt mới được huỷ.
- **BR-004**: Người duyệt một đơn là quản lý trực tiếp của nhân viên gửi đơn; quản lý không phải quản lý trực tiếp không thấy và không duyệt được đơn đó.
- **BR-005**: Số ngày nghỉ của một đơn được tính bằng số ngày làm việc trong khoảng từ ngày bắt đầu đến ngày kết thúc; thứ Bảy, Chủ nhật và ngày lễ không bị trừ.
- **BR-006**: Hai đơn của cùng một nhân viên không được có khoảng ngày chồng lấn, kể cả khi một trong hai đơn đang Chờ duyệt.
- **BR-007**: Khi đơn Đã duyệt được huỷ, số ngày đã trừ được cộng hoàn lại đúng bằng số ngày của đơn đó; mỗi đơn chỉ hoàn một lần.
- **BR-008**: Mỗi lần đơn đổi trạng thái, hệ thống ghi một bản ghi nhật ký gồm người thao tác, thời điểm, trạng thái trước và trạng thái sau.
- **BR-009**: Mỗi nhân viên có tối đa 12 ngày nghỉ phép trong một năm; đơn làm tổng số ngày Đã duyệt trong năm vượt 12 ngày không được duyệt.
- **BR-010**: Nhân sự chỉ có quyền đọc báo cáo đơn nghỉ phép và số dư; mọi yêu cầu duyệt, từ chối hoặc huỷ đơn từ tài khoản nhân sự bị hệ thống từ chối.

## Yêu cầu chức năng

- **FR-001**: Là nhân viên, tôi muốn gửi đơn nghỉ phép với ngày bắt đầu, ngày kết thúc và lý do, để xin nghỉ qua ứng dụng. Đáp ứng [BR-006]. Ưu tiên: Must.
- **FR-001.AC1**: Given nhân viên còn 12 ngày phép và không có đơn nào trong khoảng đã chọn, When gửi đơn nghỉ từ 01/12 đến 03/12, Then đơn được tạo ở trạng thái Chờ duyệt và số dư vẫn là 12 ngày.
- **FR-001.AC2**: Given nhân viên đã có đơn Chờ duyệt từ 01/12 đến 03/12, When gửi đơn từ 03/12 đến 05/12, Then hệ thống không tạo đơn và báo khoảng ngày chồng lấn với đơn đang chờ.
- **FR-001.AC3**: Given nhân viên nhập ngày kết thúc trước ngày bắt đầu, When gửi đơn, Then hệ thống không tạo đơn và báo ngày kết thúc phải sau hoặc bằng ngày bắt đầu.
- **FR-001.AC4**: Given nhân viên đã có 11 ngày phép Đã duyệt trong năm và còn 1 ngày phép, When gửi đơn 3 ngày làm việc, Then hệ thống không tạo đơn và báo đơn vượt quá 12 ngày phép của năm.
- **FR-002**: Hệ thống phải tính số ngày làm việc của một đơn và từ chối đơn có số ngày làm việc bằng 0. Đáp ứng [BR-005]. Ưu tiên: Must.
- **FR-002.AC1**: Given đơn từ thứ Sáu 05/12 đến thứ Ba 09/12 có thứ Bảy, Chủ nhật ở giữa, When lưu đơn, Then số ngày nghỉ của đơn là 3 ngày làm việc.
- **FR-002.AC2**: Given đơn chỉ gồm thứ Bảy và Chủ nhật, When gửi đơn, Then hệ thống từ chối và báo đơn không có ngày làm việc nào.
- **FR-003**: Là nhân viên, tôi muốn xem số dư ngày phép còn lại trong năm và trạng thái các đơn của mình, để biết mình còn bao nhiêu ngày trong giới hạn 12 ngày. Đáp ứng [BR-002, BR-009]. Ưu tiên: Must.
- **FR-003.AC1**: Given nhân viên đã nghỉ 3 ngày trong năm và có 3 đơn, When mở trang nghỉ phép của mình, Then thấy số dư 9 trên 12 ngày và trạng thái của cả 3 đơn.
- **FR-003.AC2**: Given nhân viên A đã đăng nhập, When mở danh sách đơn, Then chỉ thấy đơn do A gửi và không thấy đơn của nhân viên khác.
- **FR-004**: Là quản lý trực tiếp, tôi muốn thấy danh sách đơn đang Chờ duyệt của nhân viên thuộc quyền mình, để xử lý đơn đúng người. Đáp ứng [BR-003, BR-004]. Ưu tiên: Must.
- **FR-004.AC1**: Given quản lý có 4 nhân viên trực tiếp, When mở hàng đợi duyệt, Then thấy mọi đơn Chờ duyệt của 4 nhân viên đó và không thấy đơn của nhân viên ngoài nhóm.
- **FR-004.AC2**: Given một đơn đã ở trạng thái Đã duyệt hoặc Từ chối, When quản lý mở hàng đợi duyệt, Then đơn đó không xuất hiện trong hàng đợi.
- **FR-005**: Là quản lý trực tiếp, tôi muốn duyệt đơn nghỉ phép, để đơn được ghi nhận và số ngày phép của nhân viên được trừ. Đáp ứng [BR-001, BR-002, BR-003, BR-009]. Ưu tiên: Must.
- **FR-005.AC1**: Given nhân viên còn 12 ngày phép và có đơn 3 ngày làm việc đang Chờ duyệt, When quản lý duyệt đơn, Then đơn chuyển sang Đã duyệt và số dư còn 9 ngày.
- **FR-005.AC2**: Given nhân viên còn 2 ngày phép và có đơn 3 ngày làm việc đang Chờ duyệt, When quản lý duyệt đơn, Then hệ thống không duyệt, đơn giữ trạng thái Chờ duyệt, số dư giữ 2 ngày và quản lý thấy thông báo số dư không đủ.
- **FR-005.AC3**: Given một đơn đã ở trạng thái Đã huỷ hoặc Từ chối, When quản lý duyệt đơn, Then hệ thống từ chối thao tác và trạng thái đơn không đổi.
- **FR-005.AC4**: Given nhân viên đã nghỉ 11 ngày trong năm và có đơn 2 ngày Chờ duyệt, When quản lý duyệt đơn, Then hệ thống từ chối vì tổng số ngày trong năm sẽ vượt 12 ngày, đơn giữ trạng thái Chờ duyệt.
- **FR-006**: Là quản lý trực tiếp, tôi muốn từ chối đơn kèm lý do, để nhân viên biết vì sao đơn không được chấp thuận. Đáp ứng [BR-003]. Ưu tiên: Must.
- **FR-006.AC1**: Given một đơn đang Chờ duyệt, When quản lý từ chối với lý do "trùng lịch giao hàng", Then đơn chuyển sang Từ chối, số dư không đổi và nhân viên đọc được lý do đó.
- **FR-006.AC2**: Given quản lý để trống ô lý do, When bấm từ chối, Then hệ thống không đổi trạng thái đơn và yêu cầu nhập lý do.
- **FR-007**: Hệ thống phải trừ số dư ngày phép đúng một lần cho mỗi đơn được duyệt, kể cả khi yêu cầu duyệt được gửi lặp lại hoặc gửi đồng thời. Đáp ứng [BR-001]. Ưu tiên: Must.
- **FR-007.AC1**: Given đơn 3 ngày vừa được duyệt và số dư đã giảm từ 12 xuống 9, When cùng yêu cầu duyệt đó được gửi lại lần hai, Then số dư vẫn là 9 và đơn vẫn ở trạng thái Đã duyệt.
- **FR-007.AC2**: Given hai yêu cầu duyệt cùng một đơn 3 ngày đến đồng thời, When cả hai được xử lý, Then số dư chỉ giảm 3 ngày và có đúng một bản ghi nhật ký chuyển trạng thái.
- **FR-008**: Là nhân viên, tôi muốn huỷ đơn đã được duyệt trước ngày bắt đầu nghỉ, để lấy lại số ngày phép khi kế hoạch thay đổi. Đáp ứng [BR-003, BR-007]. Ưu tiên: Should.
- **FR-008.AC1**: Given đơn 3 ngày đang Đã duyệt với ngày bắt đầu là ngày mai, When nhân viên huỷ đơn, Then đơn chuyển sang Đã huỷ và số dư tăng thêm 3 ngày.
- **FR-008.AC2**: Given đơn đã bắt đầu (hôm nay bằng hoặc sau ngày bắt đầu), When nhân viên huỷ đơn, Then hệ thống từ chối và đơn vẫn ở trạng thái Đã duyệt.
- **FR-009**: Hệ thống phải ghi nhật ký cho mỗi lần đơn đổi trạng thái và cho phép HR đọc nhật ký đó. Đáp ứng [BR-008]. Ưu tiên: Must.
- **FR-009.AC1**: Given đơn chuyển từ Chờ duyệt sang Đã duyệt, When HR mở nhật ký của đơn, Then thấy một bản ghi có người thao tác, thời điểm, trạng thái trước là Chờ duyệt và trạng thái sau là Đã duyệt.
- **FR-009.AC2**: Given một lần duyệt bị hệ thống từ chối vì số dư không đủ, When HR mở nhật ký của đơn, Then không có bản ghi chuyển trạng thái cho lần thử đó và trạng thái đơn vẫn là Chờ duyệt.
- **FR-010**: Là nhân viên, tôi muốn nhận thông báo khi đơn của mình được duyệt, bị từ chối hoặc bị huỷ, để biết kết quả mà không phải mở lại ứng dụng. Đáp ứng [BR-003]. Ưu tiên: Should.
- **FR-010.AC1**: Given đơn của nhân viên vừa được quản lý duyệt, When thông báo được gửi, Then nội dung thông báo nêu trạng thái mới là Đã duyệt và số dư còn lại của nhân viên.
- **FR-010.AC2**: Given đơn vừa bị từ chối, When thông báo được gửi, Then nội dung thông báo chứa lý do từ chối do quản lý nhập.
- **FR-011**: Là nhân sự, tôi muốn xem báo cáo đơn nghỉ phép và số dư theo nhân viên và theo kỳ, để đối soát mà không cần quyền duyệt. Đáp ứng [BR-009, BR-010]. Ưu tiên: Must.
- **FR-011.AC1**: Given 20 nhân viên có đơn trong tháng 11, When HR mở báo cáo tháng 11, Then thấy tổng số ngày nghỉ Đã duyệt của từng nhân viên và số dư còn lại trên 12 ngày của năm.
- **FR-011.AC2**: Given HR đã đăng nhập và đang xem một đơn Chờ duyệt, When HR bấm duyệt đơn đó, Then hệ thống trả lỗi 403, đơn giữ trạng thái Chờ duyệt và không có bản ghi nhật ký chuyển trạng thái.

## Yêu cầu phi chức năng

| ID | Ưu tiên | Mục tiêu | Cơ sở |
|---|---|---|---|
| NFR-001 | Must | p95 thời gian phản hồi ≤ 2 giây cho thao tác gửi đơn và duyệt đơn khi 100 người dùng đồng thời | A-09 |
| NFR-002 | Must | Khả dụng ≥ 99,5% mỗi tháng; thời gian phục hồi ≤ 4 giờ sau sự cố | A-09 |
| NFR-003 | Must | 100% yêu cầu đọc hoặc sửa đơn được kiểm tra quyền: nhân viên chỉ với đơn của mình, quản lý trực tiếp chỉ với nhân viên của mình, HR chỉ đọc báo cáo | Đầu vào: "Quản lý trực tiếp duyệt, nhân sự chỉ cần xem báo cáo" |
| NFR-004 | Must | Bản ghi nhật ký trạng thái được lưu 24 tháng và chỉ HR đọc được | A-10 |
| NFR-005 | Should | Nhân viên hoàn tất gửi đơn trong ≤ 3 bước và ≤ 60 giây, đo trên 20 người dùng thử | A-12 |
| NFR-006 | Should | Thông báo kết quả đơn được gửi trong ≤ 5 phút sau khi trạng thái đổi | A-09 |

- **NFR-001.AC1**: Given 100 người dùng đồng thời gửi và duyệt đơn, When đo 1.000 thao tác liên tiếp, Then p95 thời gian phản hồi là ≤ 2 giây.
- **NFR-002.AC1**: Given hệ thống chạy một tháng, When tính tổng thời gian không phục vụ được, Then tổng đó ≤ 0,5% thời gian của tháng và một sự cố được khắc phục trong ≤ 4 giờ.
- **NFR-003.AC1**: Given nhân viên B đã đăng nhập, When B yêu cầu đọc đơn của nhân viên A, Then hệ thống trả lỗi 403 và 0 trường dữ liệu của đơn được trả về.
- **NFR-003.AC2**: Given tài khoản HR đã đăng nhập, When HR yêu cầu duyệt hoặc từ chối một đơn, Then hệ thống trả lỗi 403 và trạng thái đơn không đổi.
- **NFR-004.AC1**: Given một bản ghi nhật ký được tạo 23 tháng trước, When HR tìm bản ghi đó, Then bản ghi vẫn đọc được; bản ghi 25 tháng trước thì không còn trong hệ thống.
- **NFR-005.AC1**: Given 20 người dùng thử chưa từng dùng tính năng, When mỗi người gửi một đơn, Then ≥ 18 người hoàn tất trong ≤ 3 bước và ≤ 60 giây.
- **NFR-006.AC1**: Given một đơn vừa đổi trạng thái, When đo thời điểm thông báo được gửi, Then thời điểm đó ≤ 5 phút sau lần đổi trạng thái.

## Trường hợp biên

| Tác nhân | Trạng thái đối tượng | Tạo | Đọc | Sửa | Xóa |
|---|---|---|---|---|---|
| Nhân viên | Chờ duyệt | Được tạo đơn mới nếu không chồng lấn và không vượt 12 ngày/năm (FR-001.AC2, FR-001.AC4) | Chỉ đơn của mình | Không sửa được; phải huỷ rồi gửi lại | Huỷ đơn Chờ duyệt, không ảnh hưởng số dư |
| Nhân viên | Đã duyệt | Được tạo đơn mới nếu không chồng lấn và còn số dư | Chỉ đơn của mình | Không sửa được | Huỷ trước ngày bắt đầu thì hoàn số dư (FR-008.AC1); sau đó thì bị từ chối |
| Nhân viên | Từ chối | Được tạo đơn mới | Chỉ đơn của mình | Không | Không xoá được, giữ làm lịch sử |
| Nhân viên | Đã huỷ | Được tạo đơn mới | Chỉ đơn của mình | Không | Không xoá được |
| Quản lý trực tiếp | Chờ duyệt | Không tạo đơn thay nhân viên | Chỉ đơn của nhân viên trực tiếp | Chỉ đổi sang Đã duyệt hoặc Từ chối | Không xoá |
| Quản lý trực tiếp | Đã duyệt | Không | Chỉ đơn của nhân viên trực tiếp | Không | Không xoá |
| HR | Mọi trạng thái | Không tạo đơn | Toàn bộ đơn, số dư và báo cáo | Không sửa trạng thái (BR-010) | Không xoá |

## Thuật ngữ

| Thuật ngữ | Ý nghĩa |
|---|---|
| Đơn nghỉ phép | Bản ghi một yêu cầu nghỉ của một nhân viên, gồm ngày bắt đầu, ngày kết thúc, lý do, số ngày nghỉ và trạng thái. |
| Số dư ngày phép | Số ngày làm việc còn lại mà một nhân viên được nghỉ trong năm, tính từ giới hạn 12 ngày. |
| Quản lý trực tiếp | Người được gán là cấp trên trực tiếp của nhân viên trong cơ cấu tổ chức. |
| Ngày làm việc | Ngày trong tuần không phải thứ Bảy, Chủ nhật hoặc ngày lễ. |
| Chờ duyệt | Trạng thái của đơn đã gửi và đang đợi quản lý trực tiếp quyết định. |
| Đã duyệt | Trạng thái của đơn được chấp thuận; số ngày của đơn đã bị trừ vào số dư. |
| Từ chối | Trạng thái của đơn không được chấp thuận; số dư không đổi. |
| Đã huỷ | Trạng thái của đơn Đã duyệt được nhân viên huỷ trước ngày bắt đầu; số ngày đã trừ được hoàn lại. |
| Nhật ký trạng thái | Chuỗi bản ghi mỗi lần đơn đổi trạng thái, kèm người thao tác và thời điểm. |
| Báo cáo nghỉ phép | Bảng chỉ đọc cho HR, tổng hợp số ngày nghỉ Đã duyệt và số dư còn lại của từng nhân viên theo kỳ. |

## Giả định

| ID | Giả định | Cơ sở trong input, hoặc ảnh hưởng nếu sai |
|---|---|---|
| A-01 | Đơn nghỉ phép có bốn trạng thái Chờ duyệt, Đã duyệt, Từ chối, Đã huỷ | Input chỉ nêu gửi và duyệt; nếu có thêm trạng thái (ví dụ Chờ duyệt cấp 2) thì BR-003 và luồng FR-004 đến FR-008 phải mở rộng |
| A-02 | Số dư bị trừ tại thời điểm duyệt, không phải tại thời điểm gửi đơn | Input: "quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại"; nếu trừ khi gửi thì FR-001 và FR-007 đổi |
| A-04 | Mỗi nhân viên có một số dư ngày phép dùng chung cho mọi đơn nghỉ có hưởng lương trong năm | Input chỉ nêu "tối đa 12 ngày một năm"; nếu tách nhiều loại nghỉ (phép năm, nghỉ ốm, nghỉ không lương) thì cần nhiều số dư và BR-002, BR-009 phải nêu rõ loại |
| A-06 | Hệ thống chặn hai đơn chồng lấn của cùng một nhân viên | Không có trong input; nếu cho phép chồng lấn thì BR-006 và FR-001.AC2 bị bỏ |
| A-07 | Đơn Đã duyệt được huỷ trước ngày bắt đầu và hoàn lại đúng số ngày đã trừ | Không có trong input; nếu không cho huỷ thì FR-008 và BR-007 bị bỏ |
| A-08 | Từ chối đơn bắt buộc phải có lý do | Không có trong input; nếu lý do là tùy chọn thì FR-006.AC2 bị bỏ |
| A-09 | Các mục tiêu số của NFR-001, NFR-002, NFR-006 là giá trị tạm đặt để viết được yêu cầu | Không có trong input; nếu doanh nghiệp đặt mục tiêu khác thì các NFR này đổi ngưỡng |
| A-10 | Nhật ký trạng thái được lưu 24 tháng theo yêu cầu lưu trữ nội bộ | Không có trong input; nếu quy định lưu trữ khác thì NFR-004 đổi |
| A-12 | Mục tiêu của NFR-005 (3 bước, 60 giây) là giá trị tạm đặt | Không có trong input; nếu bỏ đo khả dụng thì NFR-005 bị bỏ |
| A-13 | Ứng dụng đã có đăng nhập, tài khoản nhân viên và quan hệ quản lý trực tiếp | Input nói "ứng dụng của chúng tôi" đã tồn tại; nếu chưa có thì phạm vi phải mở rộng sang quản lý người dùng |
| A-14 | Báo cáo cho HR được lọc theo tháng và theo năm, hiển thị mọi nhân viên có ít nhất một đơn trong kỳ | Input chỉ nêu "nhân sự chỉ cần xem báo cáo"; nếu HR cần lọc theo phòng ban hoặc xuất tệp thì FR-011 mở rộng |
| A-15 | Ngày lễ dùng để xác định ngày làm việc do HR khai báo trong ứng dụng; trước khi HR khai báo, hệ thống chỉ loại trừ thứ Bảy và Chủ nhật | Không có trong input; nếu ngày lễ lấy từ nguồn khác thì FR-002 đổi cách lấy dữ liệu |

## Câu hỏi mở

| ID | Câu hỏi | Người trả lời | Chặn |
|---|---|---|---|
| Q-01 | 12 ngày phép được cấp theo năm dương lịch hay năm làm việc của từng nhân viên, và ngày phép dư cuối năm có được chuyển sang năm sau không? | Trưởng phòng Nhân sự | BR-002, BR-009, FR-003, FR-005 |
| Q-02 | Ngoài phép năm, công ty có loại nghỉ nào khác dùng chung hoặc dùng số dư riêng (nghỉ ốm, nghỉ không lương, nghỉ nửa ngày) không? | Trưởng phòng Nhân sự | A-04, BR-002, BR-009, FR-001 |
| Q-03 | Danh sách ngày lễ dùng để tính ngày làm việc do ai cập nhật mỗi năm và theo lịch của năm nào? | Trưởng phòng Nhân sự | BR-005, FR-002, A-15 |
| Q-04 | Đơn phải được gửi trước ngày nghỉ tối thiểu bao nhiêu ngày, và có ngoại lệ cho trường hợp khẩn cấp không? | Trưởng phòng Nhân sự | FR-001 |
| Q-05 | Khi quản lý trực tiếp vắng mặt, ai được duyệt thay và việc duyệt thay có cần ghi vào nhật ký không? | Trưởng phòng Nhân sự | BR-004, FR-004, FR-005 |
| Q-06 | Nhân viên có được huỷ đơn đã duyệt khi đơn đã bắt đầu (đang nghỉ) không, hay chỉ trước ngày bắt đầu? | Trưởng phòng Nhân sự | BR-003, FR-008 |
| Q-07 | Số dư ngày phép hiện được lưu ở hệ thống nào và hệ thống đó có phải nguồn dữ liệu gốc cho tính năng này không? | Trưởng phòng Nhân sự | FR-003, FR-005, FR-007 |
| Q-08 | Thông báo kết quả đơn được gửi qua kênh nào (email, thông báo trong ứng dụng, ứng dụng chat nội bộ)? | Trưởng phòng Nhân sự | FR-010, NFR-006 |
| Q-09 | Chỉ số thành công của tính năng là gì và mục tiêu số cụ thể (ví dụ thời gian xử lý một đơn trung bình giảm từ bao nhiêu xuống bao nhiêu)? | Trưởng phòng Nhân sự | NFR-001 |

## Bước tiếp theo

Chuyển sang brainstorming giải pháp với file này làm ngữ cảnh; các câu hỏi mở Q-01 đến Q-09 được giải đáp song song với thiết kế chi tiết.
