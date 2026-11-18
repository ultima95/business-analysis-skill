# Đăng ký nghỉ phép — Yêu cầu

## Bối cảnh

- Vấn đề: Ứng dụng chưa có chức năng đăng ký nghỉ phép. Nay cần: nhân viên gửi yêu cầu, quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại.
- Vì sao bây giờ: yêu cầu không nêu mốc thời gian hay chi phí cụ thể (A-01).
- Nguồn đầu vào: yêu cầu nghiệp vụ do người yêu cầu cung cấp trong phiên làm việc ngày 2026-11-18, gồm hai lượt. Lượt một: nhân viên gửi yêu cầu, quản lý trực tiếp duyệt, hệ thống trừ số ngày phép còn lại. Lượt hai: nghỉ phép tính theo ngày làm việc, tối đa 12 ngày một năm; quản lý trực tiếp duyệt; nhân sự chỉ xem báo cáo.
- Trạng thái mã nguồn: repo chỉ có commit khởi tạo `8948085`, không có mã nguồn. Không có quy tắc nghiệp vụ hiện hữu nào để khôi phục, nên tài liệu này không có mục "Quy tắc khôi phục từ mã nguồn".

## Các vai trò và bên liên quan

| Vai trò | Làm / quyết / được thông báo | Ghi chú | Căn cứ |
|---|---|---|---|
| Nhân viên | Gửi yêu cầu nghỉ, hủy yêu cầu đang chờ, xem yêu cầu và số ngày phép còn lại của mình | Là người khởi tạo yêu cầu; hạn mức 12 ngày một năm | Input: "nhân viên gửi yêu cầu", "tối đa 12 ngày một năm" |
| Quản lý trực tiếp | Duyệt hoặc từ chối yêu cầu của nhân viên thuộc quyền, thu hồi yêu cầu đã duyệt | Người duyệt duy nhất; mỗi nhân viên có một quản lý trực tiếp (A-03) | Input: "quản lý trực tiếp duyệt" |
| Nhân sự | Chỉ xem báo cáo nghỉ phép; không duyệt, không sửa yêu cầu | Không có quyền quyết định trên yêu cầu | Input: "nhân sự chỉ cần xem báo cáo" |

## Phạm vi

Trong phạm vi:

- Nhân viên gửi yêu cầu nghỉ phép và xem trạng thái yêu cầu của mình.
- Nhân viên xem số ngày phép còn lại của mình; hạn mức tối đa 12 ngày làm việc một năm.
- Quản lý trực tiếp duyệt, từ chối, thu hồi yêu cầu của nhân viên thuộc quyền.
- Hệ thống trừ số ngày phép khi yêu cầu được duyệt và hoàn lại khi yêu cầu đã duyệt bị thu hồi.
- Nhật ký thay đổi trạng thái của từng yêu cầu.
- Nhân sự xem báo cáo nghỉ phép trên dữ liệu yêu cầu Đã duyệt.

Ngoài phạm vi:

- Chuyển số ngày phép còn dư sang năm sau (A-08; phạm vi thực tế chờ Q-04).
- Nghỉ nửa ngày và nghỉ theo giờ; đơn vị nghỉ trong phát hành này là ngày làm việc (BR-003; phạm vi thực tế chờ Q-01).
- Quy trình duyệt nhiều cấp: mỗi nhân viên chỉ có một cấp duyệt là quản lý trực tiếp.
- Gửi thông báo qua email hoặc kênh ngoài ứng dụng (A-09).
- Nhập hoặc đồng bộ dữ liệu phép từ hệ thống nhân sự bên ngoài (A-02).
- Nhân sự duyệt, từ chối, thu hồi yêu cầu hoặc sửa số dư phép.
- Hạn mức phép khác 12 ngày theo thâm niên, hợp đồng hay phòng ban (A-10).

## Quy tắc nghiệp vụ

- **BR-001**: Nhân viên chỉ gửi được yêu cầu nghỉ khi số ngày phép còn lại lớn hơn hoặc bằng số ngày xin nghỉ. (A-04)
- **BR-002**: Số ngày phép chỉ bị trừ khi quản lý trực tiếp duyệt yêu cầu; yêu cầu ở trạng thái Chờ duyệt, Từ chối hoặc Đã hủy không làm thay đổi số dư.
- **BR-003**: Số ngày nghỉ của một yêu cầu bằng số ngày làm việc trong khoảng từ ngày bắt đầu đến ngày kết thúc; Thứ Bảy, Chủ nhật và ngày lễ không được tính. Nguồn: input "nghỉ phép được tính theo ngày làm việc"; định nghĩa ngày làm việc theo A-05.
- **BR-004**: Thu hồi một yêu cầu Đã duyệt hoàn lại đúng số ngày đã trừ, đúng một lần cho mỗi yêu cầu. (A-07)
- **BR-005**: Số ngày phép còn lại không được âm; mọi hành động làm số dư âm bị hệ thống từ chối. (A-04)
- **BR-006**: Mỗi lần yêu cầu đổi trạng thái, hệ thống ghi một bản ghi nhật ký gồm người thực hiện, thời điểm, trạng thái trước và trạng thái sau. (A-07)
- **BR-007**: Một nhân viên không có hai yêu cầu ở trạng thái Chờ duyệt hoặc Đã duyệt trùng ngày nghỉ. (A-07)
- **BR-008**: Quản lý chỉ duyệt, từ chối hoặc thu hồi được yêu cầu của nhân viên thuộc quyền quản lý trực tiếp. Nguồn: input "quản lý trực tiếp duyệt".
- **BR-009**: Mỗi nhân viên có hạn mức tối đa 12 ngày làm việc phép mỗi năm dương lịch; số ngày còn dư không chuyển sang năm sau. Nguồn: input "tối đa 12 ngày một năm".
- **BR-010**: Quyết định duyệt phụ thuộc đồng thời ba điều kiện: yêu cầu đang Chờ duyệt, người duyệt là quản lý trực tiếp, số dư đủ; thiếu bất kỳ điều kiện nào thì hệ thống không duyệt.
- **BR-011**: Nhân sự chỉ được xem báo cáo nghỉ phép; không được duyệt, từ chối, thu hồi yêu cầu hay điều chỉnh số ngày phép. Nguồn: input "nhân sự chỉ cần xem báo cáo".
- **BR-012**: Báo cáo nghỉ phép chỉ tính các yêu cầu Đã duyệt; yêu cầu Chờ duyệt, Từ chối và Đã hủy không được tính là ngày nghỉ đã dùng. (A-11)

Bảng quyết định cho BR-010:

| Điều kiện / hành động | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| Yêu cầu đang Chờ duyệt | Y | Y | N | Y |
| Người duyệt là quản lý trực tiếp | Y | Y | Y | N |
| Số dư đủ cho số ngày xin nghỉ | Y | N | Y | Y |
| Kết quả | Duyệt, trừ phép | Không duyệt, báo số dư không đủ | Không duyệt, báo sai trạng thái | Không duyệt, báo không có quyền |

## Yêu cầu chức năng

- **FR-001**: As a nhân viên, I want gửi yêu cầu nghỉ phép gồm ngày bắt đầu, ngày kết thúc và lý do, so that xin nghỉ đúng quy trình. Fulfils [BR-001, BR-003, BR-005, BR-007]. Priority: Must.
- **FR-001.AC1**: Given nhân viên còn 12 ngày phép, When nhân viên gửi yêu cầu nghỉ 3 ngày làm việc, Then yêu cầu được ghi nhận ở trạng thái Chờ duyệt và số ngày phép còn lại vẫn là 12 ngày.
- **FR-001.AC2**: Given nhân viên còn 2 ngày phép, When nhân viên gửi yêu cầu nghỉ 3 ngày làm việc, Then hệ thống không ghi nhận yêu cầu, hiển thị thông báo số ngày phép còn lại không đủ và số dư giữ nguyên 2 ngày.
- **FR-001.AC3**: Given ngày kết thúc của yêu cầu trước ngày bắt đầu, When nhân viên gửi, Then hệ thống không ghi nhận yêu cầu và hiển thị thông báo khoảng ngày nghỉ không hợp lệ.
- **FR-001.AC4**: Given nhân viên đã có yêu cầu Chờ duyệt hoặc Đã duyệt trùng ít nhất một ngày với khoảng xin nghỉ mới, When nhân viên gửi, Then hệ thống không ghi nhận yêu cầu và hiển thị ngày bị trùng.
- **FR-001.AC5**: Given khoảng xin nghỉ chỉ gồm Thứ Bảy và Chủ nhật, When nhân viên gửi, Then hệ thống không ghi nhận yêu cầu vì số ngày nghỉ tính được bằng 0.
- **FR-001.AC6**: Given yêu cầu nghỉ 4 ngày làm việc trải từ Thứ Sáu sang Thứ Ba và hai ngày cuối tuần ở giữa, When nhân viên gửi, Then số ngày nghỉ của yêu cầu được tính là 4 ngày.
- **FR-001.AC7**: Given nhân viên đã dùng 10 ngày phép trong năm, When nhân viên gửi yêu cầu nghỉ 3 ngày làm việc, Then hệ thống không ghi nhận yêu cầu vì vượt hạn mức 12 ngày một năm.
- **FR-002**: As a nhân viên, I want xem danh sách yêu cầu nghỉ của mình kèm trạng thái, so that biết yêu cầu đang ở bước nào. Fulfils [BR-002]. Priority: Must.
- **FR-002.AC1**: Given nhân viên có 3 yêu cầu ở ba trạng thái Chờ duyệt, Đã duyệt, Từ chối, When nhân viên mở danh sách, Then hiển thị đủ 3 yêu cầu với đúng trạng thái của từng yêu cầu.
- **FR-002.AC2**: Given tài khoản của nhân viên A, When nhân viên A mở danh sách yêu cầu, Then danh sách không chứa yêu cầu của nhân viên B.
- **FR-003**: As a nhân viên, I want hủy yêu cầu đang Chờ duyệt, so that thu hồi yêu cầu gửi nhầm. Fulfils [BR-002]. Priority: Must.
- **FR-003.AC1**: Given yêu cầu của nhân viên ở trạng thái Chờ duyệt, When nhân viên hủy yêu cầu, Then trạng thái chuyển thành Đã hủy và số ngày phép còn lại không thay đổi.
- **FR-003.AC2**: Given yêu cầu đã ở trạng thái Đã duyệt, When nhân viên hủy yêu cầu, Then hệ thống giữ nguyên trạng thái và hiển thị thông báo cần quản lý trực tiếp thu hồi.
- **FR-004**: As a quản lý trực tiếp, I want xem danh sách yêu cầu Chờ duyệt của nhân viên thuộc quyền, so that xử lý theo thứ tự gửi. Fulfils [BR-008]. Priority: Must.
- **FR-004.AC1**: Given 4 yêu cầu Chờ duyệt từ 4 nhân viên thuộc quyền, When quản lý trực tiếp mở danh sách, Then hiển thị đủ 4 yêu cầu, sắp xếp theo thời điểm gửi tăng dần.
- **FR-004.AC2**: Given yêu cầu của một nhân viên không thuộc quyền quản lý trực tiếp, When quản lý trực tiếp mở danh sách, Then yêu cầu đó không xuất hiện trong danh sách.
- **FR-005**: As a quản lý trực tiếp, I want duyệt yêu cầu nghỉ phép, so that nhân viên được nghỉ và số ngày phép được trừ. Fulfils [BR-002, BR-005, BR-008, BR-009, BR-010]. Priority: Must.
- **FR-005.AC1**: Given yêu cầu 3 ngày ở trạng thái Chờ duyệt và nhân viên còn 12 ngày phép, When quản lý trực tiếp duyệt, Then trạng thái chuyển thành Đã duyệt và số ngày phép còn lại là 9 ngày.
- **FR-005.AC2**: Given số dư của nhân viên đã giảm còn 1 ngày sau khi yêu cầu được gửi, When quản lý trực tiếp duyệt yêu cầu 3 ngày, Then hệ thống không duyệt, yêu cầu giữ trạng thái Chờ duyệt, số dư giữ 1 ngày và hiển thị thông báo số ngày phép không đủ.
- **FR-005.AC3**: Given yêu cầu đã ở trạng thái Đã duyệt, When quản lý trực tiếp duyệt lại, Then hệ thống không tạo bút toán trừ thứ hai và trạng thái giữ nguyên Đã duyệt.
- **FR-006**: As a quản lý trực tiếp, I want từ chối yêu cầu kèm lý do, so that nhân viên biết căn cứ từ chối. Fulfils [BR-002]. Priority: Must.
- **FR-006.AC1**: Given yêu cầu đang Chờ duyệt, When quản lý trực tiếp từ chối và đã nhập lý do, Then trạng thái chuyển thành Từ chối, lý do được lưu cùng yêu cầu và số dư không thay đổi.
- **FR-006.AC2**: Given yêu cầu đang Chờ duyệt, When quản lý trực tiếp từ chối mà không nhập lý do, Then hệ thống không ghi nhận thao tác và yêu cầu giữ trạng thái Chờ duyệt.
- **FR-007**: As a nhân viên, I want xem số ngày phép còn lại của mình, so that chủ động lên kế hoạch nghỉ. Fulfils [BR-002, BR-003, BR-005, BR-009]. Priority: Must.
- **FR-007.AC1**: Given hạn mức 12 ngày phép và 3 ngày đã được duyệt, When nhân viên xem số dư, Then hệ thống hiển thị 9 ngày phép còn lại.
- **FR-007.AC2**: Given hạn mức 12 ngày và 3 ngày đang Chờ duyệt, When nhân viên xem số dư, Then hệ thống hiển thị 12 ngày phép còn lại.
- **FR-007.AC3**: Given hạn mức 12 ngày và 12 ngày đã được duyệt, When nhân viên xem số dư, Then hệ thống hiển thị 0 ngày phép còn lại.
- **FR-008**: The system shall ghi nhật ký cho mỗi lần yêu cầu đổi trạng thái. Fulfils [BR-006]. Priority: Must.
- **FR-008.AC1**: Given yêu cầu vừa được quản lý trực tiếp duyệt, When mở nhật ký của yêu cầu, Then nhật ký có bản ghi gồm người thực hiện, thời điểm, trạng thái trước là Chờ duyệt và trạng thái sau là Đã duyệt.
- **FR-008.AC2**: Given một bản ghi nhật ký đã tồn tại, When người dùng thử sửa hoặc xóa bản ghi, Then hệ thống không cho phép thay đổi và bản ghi giữ nguyên nội dung.
- **FR-009**: The system shall hoàn lại số ngày phép đã trừ khi yêu cầu Đã duyệt bị thu hồi. Fulfils [BR-004]. Priority: Must.
- **FR-009.AC1**: Given yêu cầu 3 ngày đang Đã duyệt và số dư 9 ngày, When yêu cầu bị thu hồi, Then số dư trở lại 12 ngày và trạng thái yêu cầu là Đã hủy.
- **FR-009.AC2**: Given yêu cầu đã bị thu hồi một lần, When quản lý trực tiếp thu hồi lại cùng yêu cầu đó, Then hệ thống không cộng thêm ngày và số dư giữ 12 ngày.
- **FR-010**: As a quản lý trực tiếp, I want thu hồi yêu cầu đã duyệt, so that sửa được quyết định duyệt sai. Fulfils [BR-004, BR-008]. Priority: Should.
- **FR-010.AC1**: Given yêu cầu Đã duyệt của nhân viên thuộc quyền, When quản lý trực tiếp thu hồi và đã nhập lý do, Then trạng thái chuyển thành Đã hủy và số ngày phép được hoàn lại.
- **FR-010.AC2**: Given yêu cầu Đã duyệt của nhân viên không thuộc quyền quản lý trực tiếp, When quản lý trực tiếp thu hồi, Then hệ thống không ghi nhận thao tác và trạng thái giữ nguyên Đã duyệt.
- **FR-011**: As a nhân sự, I want xem báo cáo nghỉ phép theo nhân viên và theo kỳ, so that theo dõi tình hình nghỉ phép mà không can thiệp vào quy trình duyệt. Fulfils [BR-011, BR-012]. Priority: Must.
- **FR-011.AC1**: Given 20 yêu cầu Đã duyệt của 5 nhân viên trong tháng 10, When nhân sự mở báo cáo tháng 10, Then báo cáo hiển thị tổng 20 yêu cầu, tổng số ngày nghỉ đã duyệt và số ngày nghỉ của từng nhân viên.
- **FR-011.AC2**: Given 3 yêu cầu đang Chờ duyệt và 2 yêu cầu Từ chối trong kỳ báo cáo, When nhân sự mở báo cáo, Then tổng số ngày nghỉ đã dùng không bao gồm 5 yêu cầu đó.
- **FR-011.AC3**: Given tài khoản nhân sự đang mở báo cáo, When nhân sự thử duyệt, từ chối hoặc thu hồi một yêu cầu, Then hệ thống từ chối thao tác và yêu cầu giữ nguyên trạng thái.
- **FR-012**: As a nhân sự, I want xuất báo cáo nghỉ phép ra tệp, so that chia sẻ số liệu với bộ phận khác. Fulfils [BR-011, BR-012]. Priority: Should.
- **FR-012.AC1**: Given báo cáo nghỉ phép của tháng 10 đang hiển thị, When nhân sự chọn xuất tệp, Then tệp tải về chứa đủ số dòng bằng số yêu cầu Đã duyệt trong báo cáo.
- **FR-012.AC2**: Given kỳ báo cáo không có yêu cầu Đã duyệt nào, When nhân sự chọn xuất tệp, Then tệp tải về có dòng tiêu đề và 0 dòng dữ liệu.

## Yêu cầu phi chức năng

| ID | Ưu tiên | Mục tiêu đo được | Căn cứ |
|---|---|---|---|
| NFR-001 | Must | Thời gian phản hồi p95 ≤ 2 giây cho các thao tác gửi, duyệt, từ chối ở mức 200 người dùng đồng thời | A-06 |
| NFR-002 | Must | Khả dụng ≥ 99,5% mỗi tháng trong khung giờ hành chính 08:00–18:00 | A-06 |
| NFR-003 | Must | 100% yêu cầu truy cập dữ liệu nghỉ phép ngoài phạm vi quyền bị từ chối trên bộ 40 kịch bản phân quyền | A-07 |
| NFR-004 | Must | Nhật ký kiểm toán được lưu 24 tháng, đọc được bởi nhân viên sở hữu yêu cầu và quản lý trực tiếp | A-07 |
| NFR-005 | Must | 100% yêu cầu Đã duyệt có đúng một bút toán trừ phép; đối soát hằng ngày cho kết quả 0 sai lệch | A-04 |
| NFR-006 | Must | Báo cáo nghỉ phép của một năm có 500 nhân viên trả kết quả trong p95 ≤ 5 giây | A-06 |
| NFR-007 | Must | 0 trong 20 thao tác duyệt, từ chối, thu hồi do tài khoản nhân sự thực hiện được hệ thống chấp nhận | Input "nhân sự chỉ cần xem báo cáo" |

- **NFR-001.AC1**: Given 200 người dùng đồng thời, When 100 thao tác gửi và 100 thao tác duyệt diễn ra trong 1 phút, Then p95 thời gian phản hồi ≤ 2 giây.
- **NFR-002.AC1**: Given một tháng đo trong khung giờ hành chính, When tính tỉ lệ khả dụng, Then tỉ lệ ≥ 99,5%.
- **NFR-003.AC1**: Given bộ 40 kịch bản truy cập chéo giữa nhân viên và quản lý trực tiếp, When chạy bộ kiểm thử phân quyền, Then 40/40 kịch bản bị từ chối truy cập.
- **NFR-004.AC1**: Given một bản ghi nhật ký được tạo cách thời điểm kiểm tra 23 tháng, When quản lý trực tiếp mở nhật ký của yêu cầu, Then bản ghi vẫn đọc được.
- **NFR-005.AC1**: Given 500 yêu cầu Đã duyệt trong một ngày, When chạy đối soát cuối ngày, Then số bút toán trừ bằng 500 và số sai lệch bằng 0.
- **NFR-006.AC1**: Given dữ liệu của 500 nhân viên trong một năm, When nhân sự mở báo cáo năm, Then p95 thời gian trả kết quả ≤ 5 giây.
- **NFR-007.AC1**: Given tài khoản nhân sự, When thực hiện 20 thao tác duyệt, từ chối và thu hồi trên các yêu cầu có thật, Then 0 thao tác được chấp nhận và 20/20 thao tác bị từ chối.

## Trường hợp biên

| Vai trò | Trạng thái yêu cầu | Tạo | Đọc | Sửa | Xóa |
|---|---|---|---|---|---|
| Nhân viên | Chưa có yêu cầu | Gửi được khi số dư đủ (FR-001) | Chỉ thấy danh sách rỗng của mình | Không áp dụng | Không áp dụng |
| Nhân viên | Chờ duyệt | Bị chặn khi trùng ngày (BR-007) | Thấy yêu cầu của mình | Không sửa nội dung, chỉ hủy (FR-003) | Hủy chuyển trạng thái Đã hủy |
| Nhân viên | Đã duyệt | Gửi yêu cầu mới nếu số dư còn đủ | Thấy yêu cầu và số dư đã trừ | Không sửa được; cần quản lý trực tiếp thu hồi (FR-003.AC2) | Không xóa được |
| Nhân viên | Từ chối | Gửi lại yêu cầu mới | Thấy lý do từ chối | Không sửa được | Không xóa được |
| Nhân viên | Đã hủy | Gửi lại yêu cầu mới | Thấy yêu cầu ở trạng thái Đã hủy | Không sửa được | Không xóa được |
| Quản lý trực tiếp | Chờ duyệt | Không tạo yêu cầu thay nhân viên | Thấy yêu cầu thuộc quyền (FR-004) | Duyệt hoặc từ chối (FR-005, FR-006) | Không xóa được |
| Quản lý trực tiếp | Đã duyệt | Không áp dụng | Thấy yêu cầu thuộc quyền | Thu hồi kèm lý do (FR-010) | Không xóa được |
| Quản lý trực tiếp | Yêu cầu ngoài quyền | Không áp dụng | Bị từ chối truy cập (NFR-003) | Bị từ chối (FR-010.AC2) | Bị từ chối |
| Nhân sự | Mọi trạng thái | Bị từ chối; nhân sự không tạo yêu cầu thay nhân viên (BR-011) | Xem báo cáo và số liệu tổng hợp (FR-011) | Bị từ chối; nhân sự không sửa số dư hay nội dung yêu cầu (NFR-007) | Bị từ chối |

## Thuật ngữ

| Thuật ngữ | Ý nghĩa |
|---|---|
| Yêu cầu nghỉ phép | Một bản ghi gồm người gửi, ngày bắt đầu, ngày kết thúc, lý do và trạng thái. |
| Chờ duyệt | Trạng thái của yêu cầu đã gửi và đang chờ quản lý trực tiếp quyết định. |
| Đã duyệt | Trạng thái của yêu cầu được quản lý trực tiếp chấp thuận; số ngày nghỉ đã bị trừ khỏi số dư. |
| Từ chối | Trạng thái của yêu cầu bị quản lý trực tiếp không chấp thuận, kèm lý do. |
| Đã hủy | Trạng thái của yêu cầu do nhân viên hủy khi đang chờ duyệt hoặc do quản lý trực tiếp thu hồi sau khi đã duyệt. |
| Số ngày phép còn lại | Hạn mức phép của năm trừ tổng số ngày của các yêu cầu Đã duyệt. |
| Hạn mức phép | 12 ngày làm việc được cấp cho một nhân viên trong một năm dương lịch. |
| Ngày làm việc | Ngày từ Thứ Hai đến Thứ Sáu, không thuộc lịch ngày lễ của công ty. |
| Quản lý trực tiếp | Người duy nhất có quyền quyết định trên yêu cầu của một nhân viên. |
| Nhân sự | Vai trò chỉ đọc: xem và xuất báo cáo nghỉ phép, không có quyền quyết định hay sửa dữ liệu. |
| Báo cáo nghỉ phép | Tập số liệu tổng hợp theo nhân viên và theo kỳ, chỉ tính các yêu cầu Đã duyệt. |

## Giả định

| ID | Giả định | Căn cứ trong input, hoặc ảnh hưởng nếu sai |
|---|---|---|
| A-01 | Phát hành này không gắn với mốc thời gian bắt buộc nào. | Input không nêu deadline; nếu sai, phạm vi phải cắt theo mốc và FR-010, FR-012 có thể bị loại khỏi phát hành. |
| A-02 | Số dư phép do hệ thống này tính và lưu, không đồng bộ từ hệ thống nhân sự bên ngoài. | Input chỉ nói "hệ thống trừ vào số ngày phép còn lại"; nếu sai, phát sinh yêu cầu đồng bộ và quy tắc xử lý lệch số dư. |
| A-03 | Mỗi nhân viên có một quản lý trực tiếp duy nhất làm người duyệt; không có duyệt nhiều cấp. | Input "quản lý trực tiếp duyệt" ở số ít; nếu sai, FR-004, FR-005, FR-010, FR-011 và BR-008 phải sửa theo chuỗi duyệt. |
| A-04 | Số dư phép không được âm và được kiểm tra ở cả lúc gửi và lúc duyệt. | Suy ra từ "trừ vào số ngày phép còn lại"; nếu sai, BR-001 và BR-005 phải cho phép số dư âm có kiểm soát. |
| A-05 | Ngày làm việc là Thứ Hai đến Thứ Sáu, trừ các ngày trong lịch nghỉ lễ của công ty. | Input nói "tính theo ngày làm việc" nhưng không định nghĩa; nếu sai, BR-003 phải tính cả ngày cuối tuần hoặc theo ca. |
| A-06 | Tải đỉnh 200 người dùng đồng thời; khả dụng 99,5% trong giờ hành chính. | Không có số trong input; nếu sai, NFR-001, NFR-002 và NFR-006 phải đặt lại mục tiêu. |
| A-07 | Nhật ký kiểm toán lưu 24 tháng; nhân viên đọc nhật ký yêu cầu của mình, quản lý trực tiếp đọc nhật ký yêu cầu thuộc quyền. | Không có trong input; nếu sai, NFR-003, NFR-004 và BR-006, BR-007 phải sửa theo mức lưu và phạm vi đọc khác. |
| A-08 | 12 ngày là hạn mức cố định của mỗi năm và số ngày còn dư không chuyển sang năm sau. | Input "tối đa 12 ngày một năm" xác nhận con số; phần không chuyển năm là giả định — nếu sai, BR-009 và FR-007 phải thêm quy tắc chuyển phép. |
| A-09 | Thông báo cho người dùng chỉ hiển thị trong ứng dụng, không gửi email. | Không có trong input; nếu sai, phát sinh yêu cầu gửi thông báo ngoài ứng dụng và NFR riêng. |
| A-10 | Hạn mức 12 ngày áp dụng như nhau cho mọi nhân viên, không tính theo thâm niên, hợp đồng hay tỉ lệ thời gian làm việc trong năm. | Input nêu một con số chung "tối đa 12 ngày một năm"; nếu sai, BR-009 và FR-007 phải nhận hạn mức riêng theo từng nhân viên. |
| A-11 | Báo cáo nhân sự xem chỉ gồm yêu cầu Đã duyệt, không gồm yêu cầu Chờ duyệt, Từ chối hay Đã hủy. | Input chỉ nói "nhân sự chỉ cần xem báo cáo"; nếu sai, BR-012 và FR-011 phải thêm số liệu theo từng trạng thái. |

## Câu hỏi mở

| ID | Câu hỏi | Người trả lời | Chặn |
|---|---|---|---|
| Q-01 | Nghỉ nửa ngày hoặc nghỉ theo giờ có thuộc phát hành này không? | Chủ sản phẩm | FR-001 |
| Q-02 | Khi quản lý trực tiếp vắng mặt, ai duyệt thay và việc duyệt thay có cần ghi lý do? | Trưởng phòng Nhân sự | FR-005, FR-010 |
| Q-03 | Có giới hạn số nhân viên cùng nghỉ trong một ngày hoặc trong cùng một nhóm không? | Quản lý trực tiếp | FR-005 |
| Q-04 | Số ngày phép còn dư của năm trước có được chuyển sang năm sau không, và tối đa bao nhiêu ngày? | Trưởng phòng Nhân sự | FR-007 |
| Q-05 | Yêu cầu nghỉ phải được gửi trước ngày bắt đầu tối thiểu bao nhiêu ngày làm việc? | Trưởng phòng Nhân sự | FR-001 |
| Q-06 | Lịch ngày lễ của công ty do ai cập nhật và theo nguồn nào? | Trưởng phòng Nhân sự | FR-001, FR-007 |
| Q-07 | Nhân viên vào làm giữa năm nhận đủ 12 ngày phép hay theo tỉ lệ số tháng còn lại? | Trưởng phòng Nhân sự | FR-007 |
| Q-08 | Báo cáo nhân sự cần nhóm theo đơn vị nào (phòng ban, quản lý trực tiếp, toàn công ty) và theo kỳ nào (tháng, quý, năm)? | Trưởng phòng Nhân sự | FR-011 |
| Q-09 | Tệp xuất báo cáo cần định dạng nào để bộ phận nhận dùng được? | Trưởng phòng Nhân sự | FR-012 |
| Q-10 | Ai cấp hạn mức 12 ngày đầu năm và ai điều chỉnh số dư khi cần, khi nhân sự chỉ xem báo cáo và không phải người duyệt? | Trưởng phòng Nhân sự | FR-007 |

## Bước tiếp theo

Brainstorm giải pháp với tài liệu này làm ngữ cảnh, sau đó viết kế hoạch triển khai.
