# Đăng ký nghỉ phép — Yêu cầu

## Kiểm soát tài liệu

| Phiên bản | Ngày | Tác giả | Trạng thái |
|---|---|---|---|
| 0.1 | 2026-11-18 | BA, soạn từ brief của người yêu cầu | Draft, chờ trả lời Q-01 đến Q-09 |
| 0.2 | 2026-11-18 | BA, bổ sung trả lời của người yêu cầu | Draft, đã chốt 12 ngày phép một năm, duyệt một cấp, HR chỉ đọc báo cáo |

## Bối cảnh

- Vấn đề: ứng dụng chưa có chức năng xin nghỉ phép; người yêu cầu cần ba việc: nhân viên gửi yêu cầu, quản lý duyệt, hệ thống trừ vào số ngày phép còn lại.
- Vì sao bây giờ: đầu vào không nêu mốc thời gian hay chi phí; ghi ở Q-01.
- Nguồn đầu vào: brief của người yêu cầu trong phiên làm việc ngày 2026-11-18, nguyên văn "nhân viên gửi yêu cầu, quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại".
- Trả lời bổ sung ngày 2026-11-18 của người yêu cầu, nguyên văn "Nghỉ phép được tính theo ngày làm việc, tối đa 12 ngày một năm. Quản lý trực tiếp duyệt, nhân sự chỉ cần xem báo cáo." Trả lời này chốt Q-02, Q-04, Q-05 và Q-07 của bản 0.1, bốn câu hỏi đó đã gỡ khỏi bảng câu hỏi.
- Hiện trạng mã nguồn: repo chỉ có thư mục `.git`, không có tệp mã nguồn nào tại thời điểm phân tích, nên không quy tắc nghỉ phép nào khôi phục được; ghi ở Q-09.

## Tác nhân và bên liên quan

| Tác nhân | Làm / quyết / được thông báo | Ghi chú | Cơ sở |
|---|---|---|---|
| Nhân viên | gửi yêu cầu, hủy yêu cầu của mình, xem số dư, nhận thông báo kết quả | đầu vào chỉ nêu vai "nhân viên", không nêu quyền cụ thể | Đầu vào |
| Quản lý trực tiếp | duyệt hoặc từ chối yêu cầu của nhân viên thuộc quyền | đầu vào chỉ nêu "quản lý duyệt" | Đầu vào |
| Quản lý cấp trên | duyệt yêu cầu của chính quản lý trực tiếp | không có trong đầu vào | A-01, A-07 |
| HR | chỉ xem báo cáo nghỉ phép toàn công ty; không duyệt, không sửa số dư | trả lời 2026-11-18 nêu "nhân sự chỉ cần xem báo cáo" | Trả lời 2026-11-18, A-12 |
| Nhân viên cùng công ty không liên quan | không tham gia, không được xem yêu cầu của người khác | không có trong đầu vào | A-12 |

## Phạm vi

Trong phạm vi:

- Nhân viên tạo, xem và hủy yêu cầu nghỉ phép của chính mình.
- Quản lý trực tiếp duyệt hoặc từ chối yêu cầu kèm lý do từ chối.
- Hệ thống tính số ngày bị trừ, trừ số dư khi duyệt, hoàn số dư khi hủy.
- Nhân viên xem số dư phép còn lại.
- HR xem báo cáo nghỉ phép toàn công ty.
- Thông báo trong ứng dụng khi yêu cầu đổi trạng thái.

Ngoài phạm vi:

- Chấm công, tính lương và các khoản chi trả liên quan đến ngày nghỉ.
- Nghỉ nửa ngày hoặc nghỉ theo giờ; chờ Q-03.
- Các loại nghỉ khác ngoài nghỉ phép năm (nghỉ ốm, nghỉ thai sản, nghỉ không lương).
- Số dư phép do hệ thống cấp theo quy tắc 12 ngày một năm; không đồng bộ với hệ thống nhân sự bên ngoài và HR không nhập tay.
- Duyệt nhiều cấp: mỗi yêu cầu chỉ qua một cấp duyệt là quản lý trực tiếp.

## Quy tắc nghiệp vụ

- **BR-001**: Nhân viên tạo yêu cầu nghỉ phép; chỉ quản lý trực tiếp của nhân viên đó được duyệt hoặc từ chối yêu cầu. Nguồn: Đầu vào.
- **BR-002**: Số dư phép chỉ bị trừ khi yêu cầu được duyệt; yêu cầu đang chờ duyệt hoặc bị từ chối không làm thay đổi số dư. Cơ sở: A-02.
- **BR-003**: Yêu cầu có số ngày nghỉ lớn hơn số dư tại thời điểm gửi bị hệ thống từ chối tiếp nhận. Cơ sở: A-03.
- **BR-004**: Số ngày nghỉ bị trừ tính theo ngày làm việc trong khoảng ngày của yêu cầu; thứ Bảy, Chủ nhật và ngày lễ không bị trừ. Nguồn: Trả lời 2026-11-18, "tính theo ngày làm việc".
- **BR-005**: Hai yêu cầu của cùng một nhân viên không được có khoảng ngày giao nhau khi yêu cầu trước đang chờ duyệt hoặc đã duyệt. Cơ sở: A-05.
- **BR-006**: Yêu cầu đã duyệt chỉ được hủy bởi nhân viên tạo yêu cầu và chỉ trước ngày bắt đầu nghỉ; số ngày đã trừ được hoàn lại khi hủy. Cơ sở: A-06.
- **BR-007**: Quản lý không được duyệt yêu cầu của chính mình; yêu cầu đó do quản lý cấp trên kế tiếp quyết định. Cơ sở: A-07.
- **BR-008**: Mỗi nhân viên có tối đa 12 ngày phép năm, tính theo ngày làm việc; số dư hiển thị là 12 ngày trừ số ngày của các yêu cầu đã duyệt. Nguồn: Trả lời 2026-11-18, "tối đa 12 ngày một năm".
- **BR-009**: Mỗi lần yêu cầu đổi trạng thái, nhân viên tạo yêu cầu nhận một thông báo trong ứng dụng. Cơ sở: A-09.
- **BR-010**: HR chỉ được đọc báo cáo nghỉ phép; HR không duyệt yêu cầu và không sửa số dư phép của nhân viên. Nguồn: Trả lời 2026-11-18, "nhân sự chỉ cần xem báo cáo".

## Yêu cầu chức năng

- **FR-001**: Là nhân viên, tôi muốn gửi yêu cầu nghỉ phép gồm khoảng ngày và lý do, để quản lý trực tiếp xem xét. Đáp ứng [BR-001], [BR-003]. Ưu tiên: Must.
- **FR-001.AC1**: Given nhân viên còn 12 ngày phép, When gửi yêu cầu nghỉ 3 ngày làm việc, Then yêu cầu ở trạng thái Chờ duyệt và số dư vẫn là 12 ngày.
- **FR-001.AC2**: Given nhân viên còn 2 ngày phép, When gửi yêu cầu nghỉ 3 ngày làm việc, Then hệ thống không tiếp nhận yêu cầu và hiển thị số dư hiện tại là 2 ngày.
- **FR-001.AC3**: Given người gửi chưa đăng nhập, When gửi yêu cầu nghỉ phép, Then hệ thống từ chối và không tạo bản ghi yêu cầu.
- **FR-002**: Hệ thống phải tính số ngày bị trừ từ khoảng ngày của yêu cầu theo ngày làm việc. Đáp ứng [BR-004]. Ưu tiên: Must.
- **FR-002.AC1**: Given khoảng nghỉ từ thứ Sáu đến thứ Ba và thứ Hai là ngày lễ, When hệ thống tính số ngày, Then số ngày bị trừ là 2.
- **FR-002.AC2**: Given khoảng nghỉ chỉ gồm thứ Bảy và Chủ nhật, When hệ thống tính số ngày, Then số ngày bị trừ là 0.
- **FR-003**: Hệ thống phải từ chối yêu cầu có khoảng ngày giao với yêu cầu đang chờ duyệt hoặc đã duyệt của cùng nhân viên. Đáp ứng [BR-005]. Ưu tiên: Must.
- **FR-003.AC1**: Given nhân viên có yêu cầu đã duyệt từ 10/12 đến 12/12, When gửi yêu cầu nghỉ từ 12/12 đến 14/12, Then hệ thống không tiếp nhận và nêu ngày giao là 12/12.
- **FR-003.AC2**: Given yêu cầu trước đó đã bị từ chối, When gửi yêu cầu trùng khoảng ngày đó, Then hệ thống tiếp nhận yêu cầu mới.
- **FR-004**: Là quản lý trực tiếp, tôi muốn xem danh sách yêu cầu đang chờ tôi quyết định, để xử lý hết yêu cầu tồn. Đáp ứng [BR-001]. Ưu tiên: Must.
- **FR-004.AC1**: Given ba nhân viên thuộc quyền quản lý gửi yêu cầu, When quản lý mở danh sách chờ duyệt, Then danh sách hiển thị đúng ba yêu cầu kèm số ngày và số dư của từng nhân viên.
- **FR-004.AC2**: Given yêu cầu thuộc quản lý khác, When quản lý mở danh sách chờ duyệt, Then yêu cầu đó không xuất hiện trong danh sách.
- **FR-005**: Là quản lý trực tiếp, tôi muốn duyệt yêu cầu nghỉ, để nhân viên biết kết quả và số dư được cập nhật. Đáp ứng [BR-001], [BR-002]. Ưu tiên: Must.
- **FR-005.AC1**: Given yêu cầu Chờ duyệt 3 ngày của nhân viên còn 12 ngày, When quản lý duyệt, Then trạng thái thành Đã duyệt và số dư còn 9 ngày.
- **FR-005.AC2**: Given yêu cầu đã duyệt, When quản lý duyệt lại lần nữa, Then hệ thống giữ nguyên trạng thái Đã duyệt và số dư không đổi.
- **FR-005.AC3**: Given người duyệt không phải quản lý trực tiếp của nhân viên, When người đó duyệt yêu cầu, Then hệ thống từ chối và ghi nhật ký lần thử.
- **FR-006**: Là quản lý trực tiếp, tôi muốn từ chối yêu cầu kèm lý do, để nhân viên hiểu vì sao yêu cầu không được duyệt. Đáp ứng [BR-001]. Ưu tiên: Must.
- **FR-006.AC1**: Given yêu cầu Chờ duyệt, When quản lý từ chối với lý do "trùng lịch dự án", Then trạng thái thành Bị từ chối, lý do được lưu và số dư không đổi.
- **FR-006.AC2**: Given quản lý bấm từ chối mà chưa nhập lý do, When xác nhận, Then hệ thống không ghi nhận quyết định và giữ trạng thái Chờ duyệt.
- **FR-007**: Hệ thống phải trừ số ngày nghỉ khỏi số dư của nhân viên ngay khi yêu cầu được duyệt. Đáp ứng [BR-002]. Ưu tiên: Must.
- **FR-007.AC1**: Given nhân viên còn 12 ngày, When yêu cầu 3 ngày được duyệt, Then số dư là 9 ngày và bản ghi số dư tham chiếu yêu cầu nguồn.
- **FR-007.AC2**: Given hai yêu cầu của cùng nhân viên được duyệt đồng thời và tổng số ngày vượt số dư, When cả hai được xử lý, Then yêu cầu xử lý sau bị từ chối và số dư chỉ giảm theo yêu cầu đã duyệt.
- **FR-008**: Là nhân viên, tôi muốn hủy yêu cầu đã duyệt trước ngày bắt đầu nghỉ, để kế hoạch nghỉ của tôi thay đổi được. Đáp ứng [BR-006]. Ưu tiên: Should.
- **FR-008.AC1**: Given yêu cầu đã duyệt có ngày bắt đầu sau 5 ngày, When nhân viên hủy, Then trạng thái thành Đã hủy và khoảng ngày đó được giải phóng.
- **FR-008.AC2**: Given yêu cầu đã duyệt có ngày bắt đầu là hôm nay, When nhân viên hủy, Then hệ thống không cho hủy và giữ trạng thái Đã duyệt.
- **FR-009**: Hệ thống phải hoàn lại số ngày phép đã trừ khi yêu cầu đã duyệt bị hủy. Đáp ứng [BR-006]. Ưu tiên: Must.
- **FR-009.AC1**: Given số dư là 9 ngày sau khi duyệt yêu cầu 3 ngày, When yêu cầu đó bị hủy, Then số dư là 12 ngày.
- **FR-009.AC2**: Given yêu cầu đã hủy, When nhân viên hủy lại, Then số dư giữ nguyên và hệ thống báo yêu cầu đã hủy.
- **FR-010**: Hệ thống phải chặn quản lý tự duyệt yêu cầu của chính mình và đưa yêu cầu đó vào danh sách chờ duyệt của quản lý cấp trên kế tiếp. Đáp ứng [BR-007]. Ưu tiên: Must.
- **FR-010.AC1**: Given quản lý gửi yêu cầu nghỉ, When quản lý đó mở danh sách chờ duyệt của mình, Then yêu cầu của chính họ không xuất hiện.
- **FR-010.AC2**: Given quản lý gửi yêu cầu nghỉ và có quản lý cấp trên, When yêu cầu được tạo, Then yêu cầu nằm trong danh sách chờ duyệt của quản lý cấp trên.
- **FR-010.AC3**: Given người gửi không có quản lý cấp trên, When người đó gửi yêu cầu, Then hệ thống không tạo yêu cầu và thông báo cần chỉ định người duyệt.
- **FR-011**: Là nhân viên, tôi muốn xem số ngày phép còn lại của mình, để biết còn bao nhiêu ngày trước khi gửi yêu cầu. Đáp ứng [BR-008]. Ưu tiên: Must.
- **FR-011.AC1**: Given nhân viên được cấp 12 ngày và có 3 ngày thuộc yêu cầu đã duyệt, When mở trang số dư, Then hiển thị còn 9 ngày và tổng được cấp 12 ngày.
- **FR-011.AC2**: Given nhân viên gọi dữ liệu số dư của đồng nghiệp, When yêu cầu được xử lý, Then hệ thống từ chối và trả lỗi không có quyền.
- **FR-012**: Hệ thống phải thông báo trong ứng dụng cho nhân viên tạo yêu cầu mỗi khi trạng thái yêu cầu thay đổi. Đáp ứng [BR-009]. Ưu tiên: Should.
- **FR-012.AC1**: Given yêu cầu đang Chờ duyệt, When quản lý duyệt yêu cầu, Then nhân viên nhận thông báo nêu trạng thái mới và số dư còn lại.
- **FR-012.AC2**: Given thông báo đã hiển thị cho nhân viên, When nhân viên mở thông báo, Then thông báo được đánh dấu đã đọc và vẫn còn trong danh sách thông báo.
- **FR-013**: Là nhân sự, tôi muốn xem báo cáo nghỉ phép theo nhân viên và theo tháng, để theo dõi tình hình nghỉ phép toàn công ty. Đáp ứng [BR-010]. Ưu tiên: Must.
- **FR-013.AC1**: Given tháng 11 có 20 yêu cầu đã duyệt, When HR mở báo cáo tháng 11, Then báo cáo liệt kê đủ 20 yêu cầu kèm số ngày và trạng thái của từng yêu cầu.
- **FR-013.AC2**: Given HR đang xem báo cáo, When HR gọi thao tác duyệt yêu cầu hoặc sửa số dư, Then hệ thống từ chối và trả lỗi không có quyền.
- **FR-013.AC3**: Given người dùng không thuộc vai HR, When người đó gọi báo cáo toàn công ty, Then hệ thống từ chối và trả lỗi không có quyền.

## Yêu cầu phi chức năng

| ID | Ưu tiên | Mục tiêu | Cơ sở |
|---|---|---|---|
| NFR-001 | Must | p95 thời gian phản hồi ≤ 2 giây khi 100 người dùng đồng thời | A-10 |
| NFR-002 | Should | thời gian hoạt động ≥ 99,5% mỗi tháng và khôi phục sau sự cố ≤ 4 giờ | A-11 |
| NFR-003 | Must | 100% yêu cầu tới hệ thống phải xác thực; nhân viên chỉ đọc được yêu cầu và số dư của chính mình; vai HR chỉ đọc dữ liệu toàn công ty | A-12, Trả lời 2026-11-18 |
| NFR-004 | Must | lưu yêu cầu nghỉ và nhật ký thay đổi trạng thái 5 năm | A-13 |
| NFR-005 | Should | nhân viên hoàn tất gửi một yêu cầu trong ≤ 5 bước | A-14 |
| NFR-006 | Must | 100% thay đổi trạng thái yêu cầu được ghi nhật ký kèm người thực hiện và thời điểm | A-15 |

- **NFR-001.AC1**: Given 100 người dùng đồng thời, When mở danh sách yêu cầu chờ duyệt, Then p95 thời gian phản hồi ≤ 2 giây.
- **NFR-002.AC1**: Given một tháng vận hành, When tính tổng thời gian hệ thống không phục vụ được, Then tổng thời gian đó ≤ 0,5% số phút của tháng.
- **NFR-003.AC1**: Given người dùng đã đăng nhập, When người đó gọi dữ liệu yêu cầu của nhân viên khác, Then hệ thống trả lỗi không có quyền và ghi nhật ký lần gọi.
- **NFR-003.AC2**: Given yêu cầu gọi không kèm thông tin xác thực, When hệ thống nhận yêu cầu, Then hệ thống trả lỗi xác thực và không trả dữ liệu.
- **NFR-004.AC1**: Given một yêu cầu được tạo 5 năm trước, When HR tra cứu yêu cầu đó, Then bản ghi và nhật ký của nó vẫn còn.
- **NFR-005.AC1**: Given nhân viên đã đăng nhập, When gửi một yêu cầu nghỉ từ đầu đến khi nhận trạng thái Chờ duyệt, Then số bước người dùng phải thực hiện ≤ 5.
- **NFR-006.AC1**: Given yêu cầu đổi từ Chờ duyệt sang Đã duyệt, When HR tra nhật ký của yêu cầu, Then nhật ký có 1 bản ghi nêu người duyệt và thời điểm duyệt.
- **NFR-006.AC2**: Given một yêu cầu đã qua 4 lần đổi trạng thái, When HR tra nhật ký, Then nhật ký có đúng 4 bản ghi theo thứ tự thời gian.

## Trường hợp biên

| Tác nhân | Trạng thái đối tượng | Tạo | Đọc | Sửa | Xóa |
|---|---|---|---|---|---|
| Nhân viên | Chưa có yêu cầu | tạo yêu cầu mới sau khi qua kiểm tra số dư ở FR-001 | xem số dư của mình theo FR-011 | không có bản ghi để sửa | không có bản ghi để xóa |
| Nhân viên | Chờ duyệt | tạo yêu cầu thứ hai nếu khoảng ngày không giao theo FR-003 | xem yêu cầu của mình | sửa nội dung trước khi quản lý quyết định | hủy yêu cầu, số dư không đổi vì chưa trừ |
| Nhân viên | Đã duyệt | tạo yêu cầu mới nếu còn số dư | xem yêu cầu của mình | không được sửa, phải hủy theo FR-008 | hủy trước ngày bắt đầu và hoàn số dư theo FR-009 |
| Nhân viên | Bị từ chối | tạo yêu cầu mới cho khoảng ngày khác | xem lý do từ chối | không được sửa | không cho phép xóa bản ghi |
| Quản lý trực tiếp | Chờ duyệt | không được tạo yêu cầu thay nhân viên | xem yêu cầu của nhân viên thuộc quyền | duyệt theo FR-005 hoặc từ chối theo FR-006 | không cho phép xóa bản ghi |
| Quản lý trực tiếp | Đã duyệt | không được tạo yêu cầu thay nhân viên | xem yêu cầu của nhân viên thuộc quyền | không được đổi quyết định, chỉ nhân viên hủy được | không cho phép xóa bản ghi |
| Quản lý trực tiếp | Yêu cầu của chính mình | tạo yêu cầu cho bản thân | xem yêu cầu của mình | không được tự duyệt theo FR-010 | hủy như nhân viên |
| HR | Mọi trạng thái | không cho phép tạo hoặc điều chỉnh, chỉ đọc theo FR-013 | xem báo cáo toàn công ty theo FR-013 | không cho phép sửa số dư hay quyết định duyệt | không cho phép xóa yêu cầu đã duyệt |
| Nhân viên cùng công ty không liên quan | Mọi trạng thái | không cho phép tạo yêu cầu thay người khác | không được xem yêu cầu của người khác theo NFR-003 | không cho phép | không cho phép |

## Thuật ngữ

| Thuật ngữ | Ý nghĩa |
|---|---|
| Yêu cầu nghỉ phép | Một bản ghi gồm nhân viên tạo, khoảng ngày nghỉ, lý do, trạng thái và quyết định của quản lý. |
| Trạng thái yêu cầu | Một trong các giá trị Chờ duyệt, Đã duyệt, Bị từ chối, Đã hủy. |
| Số dư phép | Số ngày phép năm còn lại của một nhân viên trong năm hiện tại, tính bằng ngày làm việc và tối đa 12 ngày. |
| Ngày phép năm | 12 ngày làm việc mỗi năm mà mỗi nhân viên được nghỉ có hưởng lương. |
| Ngày làm việc | Ngày từ thứ Hai đến thứ Sáu, trừ ngày lễ. |
| Ngày lễ | Ngày trong danh mục ngày lễ do HR duy trì; danh mục và phạm vi quốc gia chờ Q-08. |
| Quản lý trực tiếp | Người quản lý được gán cho nhân viên và là người quyết định yêu cầu của nhân viên đó. |
| Quản lý cấp trên | Quản lý của quản lý trực tiếp, là người quyết định yêu cầu của chính quản lý trực tiếp. |
| HR | Bộ phận nhân sự; trong phạm vi này chỉ đọc báo cáo nghỉ phép. |

## Giả định

| ID | Giả định | Cơ sở trong input, hoặc ảnh hưởng nếu sai |
|---|---|---|
| A-01 | Các vai tham gia gồm nhân viên, quản lý trực tiếp, quản lý cấp trên và HR. | Trả lời 2026-11-18 xác nhận ba vai nhân viên, quản lý trực tiếp, HR; quản lý cấp trên là giả định thêm cho trường hợp quản lý tự xin nghỉ (A-07), nếu bỏ thì FR-010 mất đối tượng duyệt. |
| A-02 | Số dư chỉ bị trừ tại thời điểm duyệt. | Đầu vào chỉ nói "trừ vào số ngày phép còn lại", không nêu thời điểm; nếu trừ lúc gửi thì FR-006 và FR-007 phải đổi. |
| A-03 | Không tiếp nhận yêu cầu vượt số dư tại thời điểm gửi. | Đầu vào không nêu; nếu cho phép số dư âm thì BR-003 và FR-001.AC2 bị bỏ. |
| A-05 | Không cho phép hai yêu cầu giao khoảng ngày. | Đầu vào không nêu; nếu cho phép thì FR-003 bị bỏ và FR-007 cần thêm bước kiểm tra số dư khi duyệt. |
| A-06 | Yêu cầu đã duyệt hủy được trước ngày bắt đầu nghỉ và được hoàn số dư. | Đầu vào không nêu; nếu không cho hủy thì FR-008 và FR-009 bị bỏ. |
| A-07 | Quản lý không tự duyệt; yêu cầu của quản lý do cấp trên kế tiếp duyệt. | Trả lời 2026-11-18 chốt duyệt một cấp là quản lý trực tiếp, không nói trường hợp quản lý tự xin nghỉ; nếu cho tự duyệt thì BR-007 và FR-010 bị bỏ. |
| A-09 | Thông báo cho nhân viên là thông báo trong ứng dụng. | Đầu vào không nêu; nếu cần email hoặc tin nhắn ngoài ứng dụng thì FR-012 tăng thêm kênh gửi. |
| A-10 | p95 thời gian phản hồi ≤ 2 giây với 100 người dùng đồng thời. | Đầu vào không nêu số; nếu số người dùng thực tế lớn hơn thì NFR-001 phải đặt lại. |
| A-11 | Thời gian hoạt động ≥ 99,5% mỗi tháng và khôi phục ≤ 4 giờ. | Đầu vào không nêu số; nếu nghiệp vụ cần cao hơn thì NFR-002 phải đặt lại. |
| A-12 | Mọi yêu cầu phải xác thực; nhân viên chỉ đọc dữ liệu của chính mình, HR đọc báo cáo toàn công ty. | Trả lời 2026-11-18 nêu "nhân sự chỉ cần xem báo cáo"; nếu HR không được xem chi tiết từng yêu cầu thì phạm vi báo cáo của FR-013 phải thu hẹp còn số liệu tổng hợp. |
| A-13 | Lưu yêu cầu và nhật ký 5 năm. | Đầu vào không nêu số; con số này chờ Q-06 xác nhận theo quy định lưu trữ. |
| A-14 | Nhân viên gửi xong một yêu cầu trong ≤ 5 bước. | Đầu vào không nêu số; nếu số bước lớn hơn thì NFR-005 phải đặt lại. |
| A-15 | Ghi nhật ký mọi thay đổi trạng thái kèm người thực hiện và thời điểm. | Đầu vào không nêu; nếu không cần nhật ký thì NFR-006 và NFR-004 bị bỏ. |

## Câu hỏi mở

| ID | Câu hỏi | Người trả lời | Chặn |
|---|---|---|---|
| Q-01 | Mốc thời gian hoặc sự kiện nào khiến chức năng này phải ra mắt, và chi phí hiện tại của việc xin nghỉ ngoài ứng dụng là gì? | Chủ sản phẩm | tất cả FR |
| Q-03 | Phiên bản này có hỗ trợ nghỉ nửa ngày hoặc nghỉ theo giờ không? | Chủ sản phẩm | FR-002 |
| Q-06 | Quy định lưu trữ của công ty yêu cầu giữ yêu cầu nghỉ và nhật ký trong bao nhiêu năm? | HR | NFR-004 |
| Q-08 | Danh mục ngày lễ theo quốc gia hoặc khu vực nào, và ai chịu trách nhiệm cập nhật danh mục đó? | HR | FR-002 |
| Q-09 | Hệ thống hiện tại đang lưu số dư phép ở đâu, và repo này có phải nơi duy nhất chứa mã nguồn của ứng dụng không? | Chủ sản phẩm | tất cả FR |
| Q-10 | Nhân viên vào làm hoặc rời công ty giữa năm được tính số ngày phép theo tháng làm việc hay cấp đủ 12 ngày? | HR | FR-011 |
| Q-11 | Số dư phép có đặt lại vào ngày 1 tháng 1 dương lịch hay theo năm tài chính của công ty? | HR | FR-011, FR-007 |
| Q-12 | Báo cáo nghỉ phép cần nhóm theo phòng ban, theo tháng hay theo trạng thái, và HR được xem chi tiết từng yêu cầu hay chỉ số liệu tổng hợp? | Trưởng phòng nhân sự | FR-013 |

## Bước tiếp theo

Chuyển sang brainstorming với tệp này làm ngữ cảnh, sau đó viết kế hoạch triển khai.
