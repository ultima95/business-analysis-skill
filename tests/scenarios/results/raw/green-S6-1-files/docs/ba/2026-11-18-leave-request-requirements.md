# Đăng ký nghỉ phép — Yêu cầu

## Bối cảnh

- Vấn đề: ứng dụng chưa có chức năng đăng ký nghỉ phép. Yêu cầu đầu vào nêu ba việc: nhân viên gửi yêu cầu, quản lý duyệt, hệ thống trừ vào số ngày phép còn lại.
- Vì sao bây giờ: yêu cầu đầu vào không nêu mốc thời gian hay sự kiện thúc ép (xem A-11).
- Nguồn đầu vào: tin nhắn yêu cầu của chủ sản phẩm, 2026-11-18; bổ sung cùng ngày: nghỉ phép tính theo ngày làm việc, tối đa 12 ngày một năm, quản lý trực tiếp duyệt, nhân sự chỉ xem báo cáo. Repo hiện chưa có mã nguồn (chỉ có `.git`), nên không có quy tắc nào được phục hồi từ code.

## Các vai và bên liên quan

| Vai | Kích hoạt / làm / quyết / được thông báo | Ghi chú |
|---|---|---|
| Nhân viên | Gửi yêu cầu nghỉ phép; xem số ngày phép còn lại của mình; nhận kết quả duyệt | Chỉ thao tác trên dữ liệu của chính mình (NFR-005) |
| Quản lý trực tiếp | Duyệt hoặc từ chối yêu cầu của nhân viên mình | Quyết định cuối cùng cho một yêu cầu (BR-002) |
| Nhân sự (HR) | Chỉ xem báo cáo nghỉ phép và nhật ký kiểm toán; không duyệt, không sửa yêu cầu hay số dư | Theo bổ sung 2026-11-18; ghi tại A-01 |
| Chủ sản phẩm | Chốt các câu hỏi mở về chính sách | Chủ sở hữu Q-02…Q-05 |

## Phạm vi

Trong phạm vi:

- Nhân viên gửi, xem, huỷ yêu cầu nghỉ phép của mình.
- Nhân viên xem số ngày phép năm còn lại trong năm hiện tại.
- Quản lý trực tiếp xem danh sách chờ duyệt và duyệt hoặc từ chối kèm lý do.
- Hệ thống trừ số ngày phép khi duyệt, hoàn lại khi huỷ, giới hạn 12 ngày một năm, và ghi nhật ký kiểm toán cho mọi thay đổi trạng thái và số dư.
- Nhân sự xem báo cáo nghỉ phép theo nhân viên và theo tháng.
- Thông báo kết quả duyệt cho nhân viên.

Ngoài phạm vi:

- Chấm công, tính lương, tính ngày công thực tế.
- Loại nghỉ khác ngoài phép năm (nghỉ ốm, nghỉ không lương, nghỉ thai sản) và các loại nghỉ cần hồ sơ đính kèm.
- Cộng dồn phép năm chưa dùng sang năm sau (xem A-14).
- Cấu hình quỹ phép theo từng nhân viên; lần phát hành này dùng mức cố định 12 ngày một năm.
- Gửi yêu cầu thay cho người khác.
- Tích hợp phần mềm nhân sự bên thứ ba.

## Quy tắc nghiệp vụ

- **BR-001**: Một yêu cầu nghỉ phép gồm bốn trường bắt buộc — nhân viên gửi, loại phép, ngày bắt đầu, ngày kết thúc — cùng trạng thái; thiếu bất kỳ trường bắt buộc nào thì yêu cầu không được lưu.
- **BR-002**: Chỉ quản lý trực tiếp của nhân viên gửi yêu cầu mới được duyệt hoặc từ chối yêu cầu đó; không vai nào khác quyết định được thay.
- **BR-003**: Hệ thống trừ số ngày phép còn lại đúng bằng số ngày nghỉ ghi trên yêu cầu, đúng một lần, tại thời điểm yêu cầu chuyển sang trạng thái Đã duyệt.
- **BR-004**: Yêu cầu ở trạng thái Đã từ chối hoặc Đã huỷ không làm thay đổi số ngày phép còn lại.
- **BR-005**: Mỗi nhân viên chỉ có một quỹ phép năm, và số dư phép năm còn lại là nguồn duy nhất để kiểm tra và trừ khi duyệt.
- **BR-006**: Số ngày phép còn lại của một nhân viên không được nhỏ hơn 0.
- **BR-007**: Huỷ một yêu cầu đã duyệt chỉ được phép trước ngày bắt đầu nghỉ và hoàn lại đúng số ngày đã trừ; huỷ lần thứ hai không làm thay đổi số dư.
- **BR-008**: Quỹ phép năm của một nhân viên là 12 ngày cho mỗi năm dương lịch; tổng số ngày của các yêu cầu phép năm đã duyệt trong một năm dương lịch không vượt 12 ngày.
- **BR-009**: Số ngày trừ tính theo ngày làm việc; ngày nghỉ tuần và ngày lễ nằm trong khoảng nghỉ không bị trừ.

## Yêu cầu chức năng

- **FR-001**: As a nhân viên, I want gửi yêu cầu nghỉ phép gồm loại phép, ngày bắt đầu và ngày kết thúc, so that quản lý trực tiếp nhận được yêu cầu để quyết định. Fulfils [BR-001]. Priority: Must.
- **FR-001.AC1**: Given nhân viên còn 12 ngày phép và nhập yêu cầu nghỉ từ 2026-12-01 đến 2026-12-03, When nhân viên gửi yêu cầu, Then yêu cầu được lưu ở trạng thái Chờ duyệt với số ngày nghỉ là 3.
- **FR-001.AC2**: Given nhân viên nhập ngày kết thúc trước ngày bắt đầu, When nhân viên gửi yêu cầu, Then hệ thống không lưu yêu cầu và hiển thị thông báo "ngày kết thúc phải sau hoặc bằng ngày bắt đầu".
- **FR-001.AC3**: Given nhân viên để trống loại phép, When nhân viên gửi yêu cầu, Then hệ thống không lưu yêu cầu và đánh dấu trường loại phép là bắt buộc.
- **FR-001.AC4**: Given nhân viên xin nghỉ từ thứ Sáu 2026-12-04 đến thứ Ba 2026-12-08, When nhân viên gửi yêu cầu, Then số ngày nghỉ được tính là 3 ngày làm việc.
- **FR-002**: As a nhân viên, I want xem số ngày phép năm còn lại trong năm hiện tại, so that biết còn bao nhiêu ngày trước khi gửi yêu cầu. Fulfils [BR-005], [BR-008]. Priority: Must.
- **FR-002.AC1**: Given năm hiện tại nhân viên chưa có ngày phép năm nào được duyệt, When nhân viên mở màn hình số dư phép, Then hệ thống hiển thị 12 ngày phép năm còn lại.
- **FR-002.AC2**: Given nhân viên đã có 3 ngày phép năm được duyệt trong năm nay, When nhân viên mở màn hình số dư phép, Then hệ thống hiển thị 9 ngày phép năm còn lại.
- **FR-002.AC3**: Given hôm nay là ngày 2027-01-01, When nhân viên mở màn hình số dư phép, Then hệ thống hiển thị 12 ngày của năm 2027 (A-14).
- **FR-003**: As a quản lý trực tiếp, I want xem danh sách yêu cầu đang Chờ duyệt của nhân viên mình, so that quyết định được mà không phải hỏi từng người. Fulfils [BR-002]. Priority: Must.
- **FR-003.AC1**: Given quản lý có 2 nhân viên trực tiếp và 3 yêu cầu đang Chờ duyệt, When quản lý mở danh sách chờ duyệt, Then danh sách hiển thị đúng 3 yêu cầu kèm tên nhân viên, loại phép, ngày bắt đầu, ngày kết thúc, số ngày nghỉ.
- **FR-003.AC2**: Given quản lý A, When quản lý A tìm yêu cầu của một nhân viên thuộc quản lý B, Then hệ thống trả về 0 yêu cầu.
- **FR-004**: As a quản lý trực tiếp, I want duyệt hoặc từ chối yêu cầu kèm lý do khi từ chối, so that nhân viên biết kết quả và số dư phép chỉ thay đổi theo quyết định. Fulfils [BR-002], [BR-006], [BR-008]. Priority: Must.
- **FR-004.AC1**: Given yêu cầu 3 ngày đang Chờ duyệt và nhân viên còn 12 ngày phép, When quản lý duyệt, Then yêu cầu chuyển Đã duyệt và số dư phép còn 9 ngày.
- **FR-004.AC2**: Given yêu cầu 3 ngày và nhân viên còn 2 ngày phép, When quản lý bấm duyệt, Then yêu cầu giữ trạng thái Chờ duyệt, hệ thống hiển thị thông báo thiếu ngày phép và số dư giữ nguyên 2 ngày.
- **FR-004.AC3**: Given yêu cầu đang Chờ duyệt, When quản lý từ chối kèm lý do, Then yêu cầu chuyển Đã từ chối, lý do được lưu cùng yêu cầu và số dư giữ nguyên.
- **FR-004.AC4**: Given yêu cầu đã ở trạng thái Đã duyệt, When quản lý bấm duyệt lần nữa, Then trạng thái không đổi và số dư không giảm thêm ngày nào.
- **FR-004.AC5**: Given quản lý chính là người gửi yêu cầu, When quản lý mở yêu cầu đó, Then hai thao tác duyệt và từ chối bị vô hiệu.
- **FR-004.AC6**: Given nhân viên đã có 10 ngày phép năm được duyệt trong năm nay, When quản lý duyệt yêu cầu 3 ngày, Then yêu cầu giữ trạng thái Chờ duyệt, hệ thống hiển thị thông báo vượt 12 ngày phép năm và số dư giữ nguyên 2 ngày.
- **FR-005**: The system shall trừ số ngày phép đúng một lần cho mỗi yêu cầu được duyệt, kể cả khi lệnh duyệt được gửi lặp hai lần. Fulfils [BR-003], [BR-005], [BR-009]. Priority: Must.
- **FR-005.AC1**: Given yêu cầu 3 ngày vừa được duyệt, When cùng yêu cầu đó được duyệt lại lần thứ hai, Then số dư phép chỉ giảm 3 ngày.
- **FR-005.AC2**: Given một yêu cầu Chờ duyệt 3 ngày, When 30 ngày sau yêu cầu vẫn ở trạng thái Chờ duyệt, Then số dư phép không thay đổi.
- **FR-006**: As a nhân viên, I want nhận thông báo khi yêu cầu được duyệt hoặc bị từ chối, so that biết kết quả mà không phải mở ứng dụng kiểm tra. Priority: Should.
- **FR-006.AC1**: Given yêu cầu của nhân viên vừa được quản lý duyệt, When lệnh duyệt hoàn tất, Then nhân viên nhận thông báo trong vòng 1 phút.
- **FR-006.AC2**: Given yêu cầu bị từ chối kèm lý do, When lệnh từ chối hoàn tất, Then thông báo gửi cho nhân viên có nội dung lý do từ chối.
- **FR-007**: As a nhân viên, I want huỷ yêu cầu đã duyệt trước ngày bắt đầu nghỉ, so that lấy lại số ngày phép khi kế hoạch thay đổi. Fulfils [BR-004], [BR-007]. Priority: Should.
- **FR-007.AC1**: Given yêu cầu 3 ngày đã duyệt và hôm nay là ngày trước ngày bắt đầu nghỉ, When nhân viên huỷ yêu cầu, Then yêu cầu chuyển Đã huỷ và số dư phép tăng lại 3 ngày.
- **FR-007.AC2**: Given yêu cầu đã duyệt có ngày bắt đầu là hôm qua, When nhân viên bấm huỷ, Then hệ thống không cho huỷ và hiển thị thông báo yêu cầu đã bắt đầu.
- **FR-007.AC3**: Given yêu cầu đã ở trạng thái Đã huỷ, When nhân viên bấm huỷ lần nữa, Then số dư phép không thay đổi.
- **FR-008**: As a quản lý trực tiếp, I want xem lịch sử yêu cầu của nhân viên mình trong 12 tháng gần nhất, so that đối chiếu được khi có khiếu nại về số ngày phép. Priority: Could.
- **FR-008.AC1**: Given nhân viên có 5 yêu cầu trong 12 tháng gần nhất và 2 yêu cầu cũ hơn, When quản lý mở lịch sử của nhân viên đó, Then danh sách hiển thị đúng 5 yêu cầu kèm trạng thái và số ngày.
- **FR-009**: As a nhân sự, I want xem báo cáo nghỉ phép theo nhân viên và theo tháng, so that theo dõi tình hình nghỉ mà không phải can thiệp vào từng yêu cầu. Fulfils [BR-002]. Priority: Must.
- **FR-009.AC1**: Given 50 nhân viên có tổng 120 ngày phép năm đã duyệt trong tháng 11, When nhân sự mở báo cáo tháng 11, Then báo cáo hiển thị đủ 50 nhân viên và tổng 120 ngày.
- **FR-009.AC2**: Given có 4 yêu cầu đang Chờ duyệt trong tháng 11, When nhân sự mở báo cáo tháng 11, Then 4 yêu cầu đó được hiển thị riêng và không cộng vào tổng ngày đã duyệt.
- **FR-009.AC3**: Given nhân sự đang mở báo cáo hoặc một yêu cầu, When nhân sự tìm thao tác duyệt, từ chối hoặc sửa số dư, Then hệ thống không cung cấp các thao tác đó.

## Yêu cầu phi chức năng

| ID | Priority | Target |
|---|---|---|
| NFR-001 | Must | p95 thời gian phản hồi ≤ 2 giây cho thao tác gửi yêu cầu và thao tác duyệt, đo ở 200 người dùng đồng thời |
| NFR-002 | Must | Chênh lệch giữa số dư phép hiển thị và sổ phép = 0 ngày sau mỗi lần duyệt hoặc huỷ |
| NFR-003 | Must | Thời gian hoạt động 99,5% mỗi tháng, tính trong khung 08:00–18:00 các ngày làm việc |
| NFR-004 | Must | Nhật ký kiểm toán ghi mọi thay đổi trạng thái và số dư, lưu 24 tháng, chỉ vai nhân sự đọc được |
| NFR-005 | Must | Mỗi nhân viên chỉ đọc được yêu cầu và số dư của chính mình; 0 bản ghi của người khác trả về khi truy vấn trực tiếp |
| NFR-006 | Should | Một yêu cầu gửi xong trong ≤ 5 thao tác trên màn hình gửi yêu cầu |

- **NFR-001.AC1**: Given 200 người dùng đồng thời gửi và duyệt yêu cầu liên tục trong 10 phút, When đo thời gian phản hồi, Then p95 thời gian phản hồi ≤ 2 giây.
- **NFR-002.AC1**: Given 100 yêu cầu được duyệt trong một ngày làm việc, When đối soát số dư cuối ngày, Then chênh lệch là 0 ngày ở 100/100 nhân viên.
- **NFR-003.AC1**: Given một tháng có 22 ngày làm việc, When đo tổng thời gian gián đoạn trong khung 08:00–18:00, Then tổng gián đoạn ≤ 66 phút.
- **NFR-004.AC1**: Given một yêu cầu được duyệt rồi bị huỷ, When nhân sự mở nhật ký của yêu cầu đó, Then nhật ký có 2 bản ghi kèm người thực hiện và thời điểm.
- **NFR-005.AC1**: Given nhân viên A đã đăng nhập, When A truy vấn dữ liệu của một yêu cầu thuộc nhân viên B, Then hệ thống trả về 0 bản ghi.
- **NFR-006.AC1**: Given nhân viên đã đăng nhập và có sẵn loại phép, When gửi một yêu cầu nghỉ 2 ngày, Then số thao tác từ mở màn hình đến khi gửi xong ≤ 5.

## Trường hợp biên

| Vai | Trạng thái yêu cầu | Tạo | Đọc | Sửa | Xoá |
|---|---|---|---|---|---|
| Nhân viên | Chờ duyệt | Chỉ tạo cho chính mình; trùng khoảng ngày xử lý theo Q-04 | Chỉ thấy yêu cầu của mình | Sửa được cho đến khi quản lý quyết định (A-07) | Không xoá cứng; huỷ thành Đã huỷ |
| Nhân viên | Đã duyệt | Không áp dụng | Thấy | Không sửa; chỉ huỷ theo BR-007 | Không xoá cứng |
| Nhân viên | Đã từ chối | Không áp dụng | Thấy kèm lý do | Không sửa; muốn xin lại thì gửi yêu cầu mới | Không xoá cứng |
| Quản lý trực tiếp | Chờ duyệt | Không tạo hộ nhân viên | Thấy yêu cầu của nhân viên mình | Không sửa nội dung yêu cầu | Không xoá |
| Quản lý trực tiếp | Đã duyệt | Không áp dụng | Thấy | Không đổi quyết định sang từ chối (Q-05) | Huỷ được, hoàn ngày theo BR-007 |
| Quản lý trực tiếp | Đã từ chối | Không áp dụng | Thấy | Không sửa | Không xoá |
| Nhân sự | Mọi trạng thái | Không tạo hộ, không duyệt hộ | Xem báo cáo tháng và nhật ký kiểm toán | Không sửa yêu cầu hay số dư | Không xoá yêu cầu |
| Hệ thống (đầu năm) | Mọi trạng thái | Cấp 12 ngày phép năm cho mỗi nhân viên vào ngày 01-01 (BR-008, A-14) | Không áp dụng | Không áp dụng | Không áp dụng |

## Bảng quyết định — duyệt yêu cầu

| Điều kiện / hành động | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| Yêu cầu đang ở trạng thái Chờ duyệt | Y | Y | Y | N | Y |
| Người bấm duyệt là quản lý trực tiếp của người gửi | Y | Y | N | Y | Y |
| Số dư phép ≥ số ngày yêu cầu | Y | N | – | – | Y |
| Tổng ngày phép năm đã duyệt trong năm + số ngày yêu cầu ≤ 12 | Y | Y | – | – | Y |
| Người bấm duyệt khác người gửi | Y | Y | – | Y | N |
| Kết quả | Đã duyệt, trừ ngày | Giữ Chờ duyệt, báo thiếu ngày phép | Từ chối thao tác, báo không có quyền | Từ chối thao tác, báo sai trạng thái | Từ chối thao tác, báo không tự duyệt |

## Thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| Yêu cầu nghỉ phép | Một bản ghi nhân viên xin nghỉ trong khoảng ngày xác định, có trạng thái và kết quả duyệt. |
| Loại phép | Nhóm nghỉ có quỹ ngày riêng; lần phát hành này chỉ dùng loại phép năm. |
| Phép năm | Loại nghỉ có quỹ 12 ngày làm việc cho mỗi năm dương lịch. |
| Số ngày phép còn lại (số dư phép) | Số ngày còn dùng được của một nhân viên trong một loại phép tại thời điểm hiện tại. |
| Quản lý trực tiếp | Người quản lý được gán cho nhân viên trong dữ liệu tổ chức, là người duy nhất quyết định yêu cầu của nhân viên đó. |
| Ngày làm việc | Ngày thuộc lịch làm việc của công ty, không gồm ngày nghỉ tuần và ngày lễ. |
| Chờ duyệt | Yêu cầu đã gửi, chưa có quyết định của quản lý. |
| Đã duyệt | Yêu cầu được quản lý chấp thuận; số ngày đã bị trừ khỏi số dư. |
| Đã từ chối | Yêu cầu bị quản lý từ chối kèm lý do; số dư không đổi. |
| Đã huỷ | Yêu cầu do người gửi hoặc quản lý huỷ; nếu trước đó đã duyệt thì số ngày được hoàn. |

## Giả định

| ID | Giả định | Cơ sở trong input, hoặc ảnh hưởng nếu sai |
|---|---|---|
| A-01 | Vai nhân sự chỉ đọc báo cáo và nhật ký kiểm toán, không duyệt và không sửa số dư phép. | Bổ sung 2026-11-18: "nhân sự chỉ cần xem báo cáo". Nếu nhân sự cần sửa số dư thì phải thêm một FR điều chỉnh kèm ghi nhật ký. |
| A-02 | Mỗi nhân viên đã có tài khoản định danh và quan hệ quản lý trực tiếp trong dữ liệu tổ chức hiện có. | Cần cho BR-002. Nếu chưa có thì phải thêm bước gán quản lý trực tiếp trước khi duyệt được. |
| A-03 | Trạng thái yêu cầu gồm bốn giá trị: Chờ duyệt, Đã duyệt, Đã từ chối, Đã huỷ. | Input nêu bước gửi và bước duyệt; hai trạng thái còn lại suy ra từ BR-004 và BR-007. Nếu sai thì đổi bảng trạng thái và các AC tương ứng. |
| A-04 | Trong lần phát hành này chỉ có loại phép năm; trường loại phép nhận một giá trị duy nhất là Phép năm. | Bổ sung 2026-11-18 chốt quỹ 12 ngày một năm. Nếu có thêm loại nghỉ khác thì mỗi loại cần quỹ riêng và FR-002 phải hiển thị nhiều dòng. |
| A-05 | Ứng dụng đã có kênh gửi thông báo cho nhân viên. | Cần cho FR-006. Nếu chưa có thì FR-006 phải kèm hạng mục xây kênh, và ngưỡng 1 phút tại FR-006.AC1 phải xem lại. |
| A-06 | Nhân viên được tự huỷ yêu cầu đã duyệt trước ngày bắt đầu nghỉ. | Input không nêu. Nếu sai thì bỏ FR-007 và BR-007, và số dư chỉ giảm, không bao giờ tăng. |
| A-07 | Nhân viên sửa được yêu cầu đang Chờ duyệt. | Input không nêu. Nếu sai thì bỏ nhánh sửa trong bảng trường hợp biên và thêm AC chặn sửa. |
| A-08 | Ngưỡng số tại NFR-001, NFR-002, NFR-003, NFR-006 là giá trị tạm đặt. | Input không nêu chỉ tiêu phi chức năng. Nếu sai chỉ đổi ngưỡng, không đổi luồng nghiệp vụ. |
| A-09 | Một yêu cầu gồm nhiều ngày liên tục trong một lần gửi, không tách thành một yêu cầu cho mỗi ngày. | Input nói "gửi yêu cầu" ở dạng một lần. Nếu sai thì luồng gửi đổi sang tạo theo từng ngày và FR-001 phải tách nhỏ. |
| A-10 | Quản lý không được tự duyệt yêu cầu của chính mình. | Input không nêu; đây là kiểm soát nội bộ. Nếu sai thì bỏ FR-004.AC5 và cột R5 của bảng quyết định. |
| A-11 | Chưa có mốc thời gian phát hành cố định; thứ tự làm theo MoSCoW trong tài liệu này. | Input không nêu deadline. Nếu có deadline cố định thì cắt các yêu cầu Should và Could trước. |
| A-12 | Đơn vị nhỏ nhất của một yêu cầu là 1 ngày làm việc; không có nghỉ nửa ngày. | Bổ sung chỉ nêu ngày làm việc. Nếu cho nghỉ nửa ngày thì số ngày thành số thập phân và BR-008, FR-001.AC4 phải đổi. |
| A-13 | Một yêu cầu nghỉ không vượt qua ranh giới năm dương lịch; yêu cầu vắt qua ngày 31-12 bị chặn khi gửi. | Quỹ 12 ngày tính theo năm dương lịch (BR-008). Nếu cho phép vắt năm thì phải tách số ngày theo hai năm và thêm AC tương ứng. |
| A-14 | Phép năm không dùng hết không cộng dồn sang năm sau; mỗi năm dương lịch bắt đầu lại từ 12 ngày. | Bổ sung nêu "tối đa 12 ngày một năm". Nếu có cộng dồn thì số dư đầu năm phải cộng thêm phần chuyển sang và BR-008 phải đổi. |
| A-15 | Nhân viên vào làm giữa năm nhận đủ 12 ngày của năm đó, không tính theo tỉ lệ tháng làm việc. | Bổ sung không nêu cách chia theo thời gian làm việc. Nếu tính tỉ lệ thì BR-008 đổi thành công thức theo số tháng làm việc. |

## Câu hỏi mở

| ID | Câu hỏi | Người trả lời | Blocks |
|---|---|---|---|
| Q-02 | Chặn yêu cầu vượt số dư phép ở bước gửi, ở bước duyệt, hay ở cả hai bước? | Chủ sản phẩm | FR-001, FR-004 |
| Q-03 | Thông báo kết quả duyệt đi qua kênh nào: email, thông báo trong ứng dụng, hay cả hai? | Chủ sản phẩm | FR-006 |
| Q-04 | Hai yêu cầu của cùng một nhân viên có khoảng ngày chồng nhau thì xử lý thế nào: chặn yêu cầu thứ hai, hay cho phép và trừ hai lần? | Chủ sản phẩm + nhân sự | FR-001 |
| Q-05 | Quản lý đã duyệt một yêu cầu thì có được đổi quyết định sang từ chối không? | Chủ sản phẩm | FR-004, FR-007 |

## Bước tiếp theo

Brainstorm giải pháp với tài liệu này làm ngữ cảnh, sau đó viết kế hoạch triển khai từ các FR đã chốt. Hai câu hỏi đã chốt ngày 2026-11-18: số ngày tính theo ngày làm việc (BR-009), quỹ phép 12 ngày một năm (BR-008); phần còn lại của quyết định nằm tại A-12…A-15.
