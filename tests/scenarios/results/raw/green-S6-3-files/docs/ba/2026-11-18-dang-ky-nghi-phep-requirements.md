# Đăng ký nghỉ phép — Yêu cầu

## Bối cảnh

- Vấn đề: nhân viên chưa có nơi gửi yêu cầu nghỉ phép; việc xin nghỉ và trừ ngày phép đang làm ngoài hệ thống nên không có bản ghi thống nhất.
- Vì sao bây giờ: yêu cầu được nêu trong phiên làm việc ngày 2026-11-18, trước khi bắt đầu viết mã cho tính năng này.
- Nguồn đầu vào: mô tả trực tiếp của người yêu cầu — "nhân viên gửi yêu cầu, quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại".
- Đã chốt trong phiên 2026-11-18: nghỉ phép tính theo ngày làm việc; tối đa 12 ngày một năm; quản lý trực tiếp duyệt; nhân sự (HR) chỉ xem báo cáo. Các điểm này thành quy tắc nghiệp vụ BR-001, BR-005, BR-011, BR-012.
- Repo chưa có mã nguồn nghiệp vụ nên không có quy tắc nào được phục hồi từ mã.

## Actor và bên liên quan

| Actor | Làm / quyết / được thông báo | Ghi chú | Cơ sở |
|---|---|---|---|
| Nhân viên | Gửi đơn, hủy đơn của mình, xem số dư và lịch sử đơn của mình | Là người khởi tạo duy nhất của một đơn | Input: "nhân viên gửi yêu cầu" |
| Quản lý trực tiếp | Duyệt hoặc từ chối đơn của nhân viên trong nhóm mình | Không duyệt đơn của chính mình; đây là cấp duyệt duy nhất | Input: "quản lý duyệt", "Quản lý trực tiếp duyệt" |
| HR | Chỉ xem báo cáo nghỉ phép | Không tạo, duyệt, sửa, hủy đơn và không điều chỉnh số dư | Input: "nhân sự chỉ cần xem báo cáo" |
| Hệ thống | Trừ/hoàn ngày phép, chặn đơn vượt số dư, ghi nhật ký trạng thái | Là bên thực thi quy tắc số dư | Input: "hệ thống trừ vào số ngày phép còn lại" |

## Phạm vi

Trong phạm vi:
- Gửi, xem, hủy đơn nghỉ phép năm của một nhân viên.
- Duyệt và từ chối đơn ở một cấp quản lý trực tiếp.
- Trừ số dư khi đơn được duyệt, hoàn số dư khi đơn đã duyệt bị hủy.
- Nhân viên xem số dư và lịch sử đơn của mình; quản lý xem hàng đợi đơn của nhóm.
- HR xem báo cáo nghỉ phép theo nhân viên và theo khoảng thời gian.

Ngoài phạm vi:
- Điều chỉnh số dư phép bởi HR hoặc quản lý (A-15).
- Tính lương, tính bảo hiểm, đồng bộ hệ thống chấm công (A-04).
- Nghỉ ốm, nghỉ thai sản, nghỉ không lương (A-07).
- Duyệt nhiều cấp, quy trình nghỉ việc, tạm hoãn hợp đồng.
- Chọn công nghệ, kiến trúc, cơ sở dữ liệu hay thiết kế màn hình — thuộc bước brainstorming.

## Quy tắc nghiệp vụ

- **BR-001**: Số dư phép năm của một nhân viên tối đa là 12 ngày công trong một năm; số dư không bao giờ vượt 12 ngày công và không cộng dồn sang năm sau. (cơ sở: input "tối đa 12 ngày một năm", A-10)
- **BR-002**: Ngày phép chỉ bị trừ khi đơn chuyển sang trạng thái Đã duyệt; đơn ở trạng thái Chờ duyệt, Từ chối hoặc Đã hủy không làm thay đổi số dư.
- **BR-003**: Số dư khả dụng của một nhân viên bằng số dư hiện tại trừ tổng số ngày của các đơn đang Chờ duyệt; một đơn chỉ được tạo khi tổng số ngày yêu cầu không vượt số dư khả dụng. (cơ sở: A-16)
- **BR-004**: Một đơn hợp lệ khi có ngày bắt đầu và ngày kết thúc, ngày bắt đầu không sau ngày kết thúc, và khoảng ngày không chồng lấn với bất kỳ đơn nào khác của cùng nhân viên ở trạng thái Chờ duyệt hoặc Đã duyệt.
- **BR-005**: Chỉ quản lý trực tiếp của nhân viên tại thời điểm quyết định được duyệt hoặc từ chối đơn, ở một cấp duyệt duy nhất; quản lý không được duyệt hoặc từ chối đơn do chính mình tạo. (cơ sở: input "Quản lý trực tiếp duyệt", A-03, A-12)
- **BR-006**: Hủy một đơn Đã duyệt hoàn lại đúng số ngày đã trừ của đơn đó; chỉ được hủy trước ngày bắt đầu nghỉ.
- **BR-007**: Từ chối đơn bắt buộc kèm lý do tối thiểu 10 ký tự; duyệt đơn không bắt buộc kèm lý do.
- **BR-008**: Đơn ở trạng thái Từ chối hoặc Đã hủy là trạng thái cuối, không chuyển sang trạng thái khác.
- **BR-009**: Số dư phép của một nhân viên không bao giờ nhận giá trị âm.
- **BR-010**: Chỉ các chuyển trạng thái sau được phép — Chờ duyệt → Đã duyệt, Chờ duyệt → Từ chối, Chờ duyệt → Đã hủy, Đã duyệt → Đã hủy; mọi chuyển trạng thái khác bị hệ thống từ chối.
- **BR-011**: Nghỉ phép được tính theo ngày làm việc; mỗi đơn có tổng số ngày là số nguyên từ 1 ngày công trở lên, không hỗ trợ nửa ngày hoặc tính theo giờ. (cơ sở: input "tính theo ngày làm việc")
- **BR-012**: HR chỉ được đọc dữ liệu đơn nghỉ phép và số dư để lập báo cáo; mọi thao tác tạo, duyệt, sửa, hủy đơn hoặc điều chỉnh số dư do HR thực hiện đều bị từ chối. (cơ sở: input "nhân sự chỉ cần xem báo cáo")

Bảng quyết định cho BR-010:

| Điều kiện / hành động | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| Trạng thái hiện tại là Chờ duyệt | Y | Y | Y | N | N |
| Trạng thái hiện tại là Đã duyệt | N | N | N | Y | Y |
| Người thao tác là quản lý của chủ đơn | Y | Y | N | Y | N |
| Người thao tác là chủ đơn | N | N | Y | N | N |
| Hành động yêu cầu | Duyệt | Từ chối | Hủy | Hủy | Duyệt |
| Kết quả | Đã duyệt | Từ chối | Đã hủy | Đã hủy | Bị từ chối |

## Yêu cầu chức năng

- **FR-001**: Là nhân viên, tôi muốn gửi một đơn nghỉ phép gồm ngày bắt đầu, ngày kết thúc và lý do nghỉ, để quản lý xem xét. Đáp ứng [BR-004], [BR-011]. Ưu tiên: Must.
- **FR-001.AC1**: Given nhân viên còn 12 ngày phép và không có đơn nào trong khoảng 2026-12-01 đến 2026-12-03, When nhân viên gửi đơn nghỉ từ 2026-12-01 đến 2026-12-03, Then hệ thống tạo đơn ở trạng thái Chờ duyệt với tổng 3 ngày công và số dư hiện tại vẫn là 12 ngày.
- **FR-001.AC2**: Given nhân viên nhập ngày bắt đầu sau ngày kết thúc, When nhân viên gửi đơn, Then hệ thống không tạo đơn và hiển thị thông báo ngày bắt đầu phải trước hoặc bằng ngày kết thúc.
- **FR-001.AC3**: Given nhân viên đã có đơn Đã duyệt cho ngày 2026-12-02, When nhân viên gửi đơn mới cho khoảng 2026-12-02 đến 2026-12-04, Then hệ thống không tạo đơn và hiển thị thông báo khoảng ngày trùng với đơn đã có.
- **FR-001.AC4**: Given khoảng nghỉ từ thứ Sáu 2026-12-04 đến thứ Hai 2026-12-07, When nhân viên gửi đơn, Then hệ thống ghi tổng 2 ngày công và không tính thứ Bảy và Chủ nhật.
- **FR-002**: Là nhân viên, tôi muốn xem số dư phép còn lại và số ngày đang chờ duyệt, để biết mình còn bao nhiêu ngày được nghỉ. Đáp ứng [BR-001], [BR-003]. Ưu tiên: Must.
- **FR-002.AC1**: Given nhân viên có số dư 12 ngày và một đơn Chờ duyệt 3 ngày, When nhân viên mở trang số dư phép, Then hệ thống hiển thị số dư hiện tại 12 ngày, số ngày đang chờ 3 ngày và số dư khả dụng 9 ngày.
- **FR-002.AC2**: Given nhân viên vào làm ngày 2026-07-01 trong năm có trần 12 ngày, When nhân viên mở trang số dư phép, Then hệ thống hiển thị số dư khởi tạo 6 ngày theo số tháng làm việc trong năm.
- **FR-003**: Hệ thống phải từ chối tạo đơn khi tổng số ngày yêu cầu vượt số dư khả dụng hoặc vượt trần 12 ngày công của năm. Đáp ứng [BR-001], [BR-003], [BR-009]. Ưu tiên: Must.
- **FR-003.AC1**: Given số dư khả dụng là 2 ngày, When nhân viên gửi đơn nghỉ 3 ngày, Then hệ thống không tạo đơn và hiển thị thông báo vượt quá số dư khả dụng 2 ngày.
- **FR-003.AC2**: Given số dư hiện tại 5 ngày và một đơn Chờ duyệt 4 ngày, When nhân viên gửi đơn nghỉ 2 ngày, Then hệ thống không tạo đơn và hiển thị số dư khả dụng còn 1 ngày.
- **FR-003.AC3**: Given nhân viên đã nghỉ 12 ngày công trong năm, When nhân viên gửi đơn nghỉ 1 ngày, Then hệ thống không tạo đơn và hiển thị thông báo đã dùng hết 12 ngày công của năm.
- **FR-004**: Là quản lý trực tiếp, tôi muốn xem danh sách đơn đang Chờ duyệt của nhân viên trong nhóm mình, để xử lý đơn chờ. Đáp ứng [BR-005]. Ưu tiên: Must.
- **FR-004.AC1**: Given quản lý có 2 nhân viên và mỗi người có 1 đơn Chờ duyệt, When quản lý mở hàng đợi duyệt, Then hệ thống liệt kê đúng 2 đơn kèm tên nhân viên, khoảng ngày và tổng số ngày công.
- **FR-004.AC2**: Given một nhân viên không thuộc nhóm của quản lý có đơn Chờ duyệt, When quản lý mở hàng đợi duyệt, Then đơn của nhân viên đó không xuất hiện trong danh sách.
- **FR-005**: Là quản lý trực tiếp, tôi muốn duyệt hoặc từ chối một đơn Chờ duyệt của nhân viên trong nhóm, để chốt việc nghỉ và cập nhật số dư. Đáp ứng [BR-002], [BR-005]. Ưu tiên: Must.
- **FR-005.AC1**: Given đơn 3 ngày công của nhân viên trong nhóm đang Chờ duyệt và số dư hiện tại 12 ngày, When quản lý duyệt đơn, Then đơn chuyển sang Đã duyệt và số dư của nhân viên còn 9 ngày.
- **FR-005.AC2**: Given quản lý tự tạo một đơn 2 ngày, When quản lý mở đơn đó, Then hệ thống không hiển thị hành động duyệt hoặc từ chối cho quản lý.
- **FR-005.AC3**: Given đơn Chờ duyệt của một nhân viên ngoài nhóm, When quản lý gọi hành động duyệt cho đơn đó, Then hệ thống từ chối thao tác và giữ nguyên trạng thái Chờ duyệt.
- **FR-006**: Là quản lý trực tiếp, tôi muốn từ chối một đơn kèm lý do, để nhân viên biết vì sao đơn không được duyệt. Đáp ứng [BR-002], [BR-007]. Ưu tiên: Must.
- **FR-006.AC1**: Given đơn Chờ duyệt của nhân viên trong nhóm, When quản lý từ chối với lý do "Trùng lịch bàn giao dự án", Then đơn chuyển sang Từ chối, lý do được lưu và số dư của nhân viên không đổi.
- **FR-006.AC2**: Given quản lý nhập lý do từ chối dài 5 ký tự, When quản lý xác nhận từ chối, Then hệ thống không đổi trạng thái đơn và yêu cầu lý do tối thiểu 10 ký tự.
- **FR-007**: Là nhân viên, tôi muốn hủy một đơn đang Chờ duyệt của mình, để rút lại yêu cầu không còn cần thiết. Đáp ứng [BR-010]. Ưu tiên: Should.
- **FR-007.AC1**: Given nhân viên có đơn Chờ duyệt 3 ngày, When nhân viên hủy đơn, Then đơn chuyển sang Đã hủy và số dư của nhân viên không đổi.
- **FR-007.AC2**: Given nhân viên có đơn Đã duyệt, When nhân viên gọi hành động hủy từ danh sách đơn Chờ duyệt, Then hệ thống không cho hủy và giữ nguyên trạng thái Đã duyệt.
- **FR-008**: Là nhân viên, tôi muốn hủy một đơn Đã duyệt trước ngày bắt đầu nghỉ, để lấy lại số ngày phép đã bị trừ. Đáp ứng [BR-006]. Ưu tiên: Must.
- **FR-008.AC1**: Given đơn 3 ngày công đã duyệt, số dư 9 ngày và ngày bắt đầu nghỉ là 2026-12-01, When nhân viên hủy đơn vào 2026-11-25, Then đơn chuyển sang Đã hủy và số dư trở lại 12 ngày.
- **FR-008.AC2**: Given đơn đã duyệt có ngày bắt đầu 2026-12-01, When nhân viên gọi hành động hủy vào 2026-12-02, Then hệ thống từ chối hủy và đơn giữ trạng thái Đã duyệt.
- **FR-009**: Hệ thống phải từ chối mọi chuyển trạng thái không nằm trong danh sách được phép của BR-010, kể cả khi hai người thao tác đồng thời trên cùng một đơn. Đáp ứng [BR-008], [BR-010]. Ưu tiên: Must.
- **FR-009.AC1**: Given đơn đã ở trạng thái Từ chối, When quản lý gọi hành động duyệt cho đơn đó, Then hệ thống từ chối thao tác và trạng thái vẫn là Từ chối.
- **FR-009.AC2**: Given quản lý và nhân viên cùng thao tác trên một đơn Chờ duyệt, When yêu cầu duyệt và yêu cầu hủy đến cùng lúc, Then chỉ một yêu cầu được áp dụng và yêu cầu còn lại bị từ chối kèm thông báo trạng thái đơn đã thay đổi.
- **FR-010**: Là nhân viên, tôi muốn xem lịch sử đơn của mình kèm trạng thái, người quyết định và lý do từ chối, để tra cứu các lần nghỉ trước đó. Đáp ứng [BR-007]. Ưu tiên: Should.
- **FR-010.AC1**: Given nhân viên có 1 đơn Từ chối kèm lý do, When nhân viên mở lịch sử đơn, Then hệ thống hiển thị đơn đó với trạng thái Từ chối, tên quản lý quyết định và lý do từ chối đầy đủ.
- **FR-010.AC2**: Given nhân viên chỉ có đơn của chính mình, When nhân viên mở lịch sử đơn, Then hệ thống không hiển thị đơn của bất kỳ nhân viên khác.
- **FR-011**: Hệ thống phải ghi nhật ký mỗi lần đơn đổi trạng thái, gồm đơn, trạng thái trước, trạng thái sau, người thao tác và thời điểm. Đáp ứng [BR-002], [BR-010]. Ưu tiên: Should.
- **FR-011.AC1**: Given một đơn Chờ duyệt, When quản lý duyệt đơn, Then nhật ký có một bản ghi với trạng thái trước Chờ duyệt, trạng thái sau Đã duyệt, mã quản lý và thời điểm thao tác.
- **FR-011.AC2**: Given một thao tác duyệt bị từ chối do sai quyền, When hệ thống xử lý thao tác, Then nhật ký ghi nhận lần thử bị từ chối kèm mã người thao tác.
- **FR-012**: Là HR, tôi muốn xem báo cáo nghỉ phép theo nhân viên và theo khoảng thời gian, để theo dõi tình hình sử dụng phép năm. Đáp ứng [BR-012]. Ưu tiên: Should.
- **FR-012.AC1**: Given 2 nhân viên có đơn nghỉ trong tháng 11 năm 2026, When HR mở báo cáo nghỉ phép của tháng 11 năm 2026, Then báo cáo liệt kê từng nhân viên với số ngày đã duyệt, số ngày đang chờ và số dư còn lại.
- **FR-012.AC2**: Given HR đang xem báo cáo nghỉ phép, When HR gọi thao tác duyệt đơn hoặc điều chỉnh số dư, Then hệ thống từ chối với mã lỗi quyền truy cập và dữ liệu không thay đổi.
- **FR-013**: Hệ thống phải thông báo cho quản lý khi có đơn mới chờ duyệt và cho nhân viên khi đơn được duyệt hoặc bị từ chối. Đáp ứng [BR-002]. Ưu tiên: Could.
- **FR-013.AC1**: Given nhân viên gửi đơn mới, When đơn được tạo ở trạng thái Chờ duyệt, Then quản lý trực tiếp nhận một thông báo chứa tên nhân viên và khoảng ngày nghỉ.
- **FR-013.AC2**: Given quản lý từ chối đơn, When đơn chuyển sang Từ chối, Then nhân viên nhận một thông báo chứa trạng thái Từ chối và lý do từ chối.

## Yêu cầu phi chức năng

| ID | Ưu tiên | Mục tiêu đo được | Cơ sở |
|---|---|---|---|
| NFR-001 | Must | p95 thời gian phản hồi ≤ 2 giây cho thao tác gửi, duyệt và xem số dư khi 100 người dùng đồng thời | A-05 |
| NFR-002 | Should | Hệ thống khả dụng ≥ 99,5% mỗi tháng, thời gian khôi phục ≤ 4 giờ | A-08 |
| NFR-003 | Must | 100% yêu cầu đọc hoặc sửa đơn được kiểm tra quyền theo 3 vai trò Nhân viên, Quản lý trực tiếp, HR trước khi trả dữ liệu | Input "nhân sự chỉ cần xem báo cáo" |
| NFR-004 | Must | Nhật ký thay đổi trạng thái được lưu 24 tháng kể từ lần ghi cuối của đơn | A-06 |
| NFR-005 | Should | Xử lý 500 đơn mới mỗi ngày cho 2.000 nhân viên mà p95 vẫn ≤ 2 giây | A-09 |

- **NFR-001.AC1**: Given 100 người dùng đồng thời gửi và duyệt đơn, When đo 1.000 yêu cầu liên tiếp, Then p95 thời gian phản hồi là ≤ 2 giây.
- **NFR-002.AC1**: Given một tháng có sự cố dịch vụ, When tổng hợp thời gian gián đoạn, Then tổng thời gian gián đoạn trong tháng ≤ 3,6 giờ và thời gian khôi phục mỗi sự cố ≤ 4 giờ.
- **NFR-003.AC1**: Given 3 vai trò Nhân viên, Quản lý trực tiếp và HR, When mỗi vai trò gọi thao tác đọc hoặc sửa đơn ngoài quyền của mình, Then 100% lời gọi bị từ chối với mã lỗi quyền truy cập.
- **NFR-004.AC1**: Given một đơn đã đóng ở trạng thái cuối từ 25 tháng trước, When HR tra nhật ký của đơn đó, Then hệ thống trả về 0 bản ghi nhật ký đã hết hạn lưu.
- **NFR-005.AC1**: Given 500 đơn mới trong một ngày cho 2.000 nhân viên, When đo p95 trong khung giờ cao điểm, Then p95 thời gian phản hồi vẫn là ≤ 2 giây.

## Trường hợp biên

| Actor | Trạng thái đơn | Tạo | Đọc | Sửa | Xóa |
|---|---|---|---|---|---|
| Nhân viên | Chưa có đơn | Tạo đơn nếu không chồng lấn và không vượt số dư khả dụng | Xem số dư và lịch sử rỗng | Không áp dụng | Không áp dụng |
| Nhân viên | Chờ duyệt | Không tạo đơn chồng lấn | Xem đơn của mình | Không sửa nội dung; chỉ hủy (FR-007) | Hủy đơn (FR-007) |
| Nhân viên | Đã duyệt | Không tạo đơn chồng lấn | Xem đơn của mình | Chỉ hủy trước ngày bắt đầu (FR-008) | Hủy đơn, hoàn số dư (FR-008) |
| Nhân viên | Từ chối | Tạo đơn mới cho cùng khoảng ngày | Xem đơn và lý do từ chối | Không cho phép (BR-008) | Không cho phép (BR-008) |
| Quản lý trực tiếp | Chờ duyệt | Không tạo đơn thay nhân viên | Xem đơn của nhóm mình | Duyệt hoặc từ chối (FR-005, FR-006) | Không xóa được; chỉ từ chối kèm lý do |
| Quản lý trực tiếp | Đã duyệt | Không áp dụng | Xem đơn của nhóm mình | Không duyệt lại (BR-010) | Không xóa được; nhân viên tự hủy |
| Quản lý trực tiếp | Đơn của chính mình | Tạo như nhân viên | Xem đơn của mình | Không tự duyệt hoặc tự từ chối (BR-005) | Hủy theo FR-007, FR-008 |
| HR | Mọi trạng thái | Không cho phép (BR-012) | Xem báo cáo tổng hợp mọi nhân viên | Không cho phép (BR-012) | Không cho phép (BR-012) |

## Bảng thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| Đơn nghỉ phép | Bản ghi một yêu cầu nghỉ gồm ngày bắt đầu, ngày kết thúc, lý do nghỉ, trạng thái và người quyết định. |
| Số dư phép | Số ngày công phép năm còn lại của một nhân viên trong năm hiện tại, tối đa 12 ngày. |
| Số dư khả dụng | Số dư phép trừ tổng số ngày công của các đơn đang Chờ duyệt. |
| Ngày công | Ngày làm việc theo lịch của công ty, không gồm thứ Bảy, Chủ nhật và ngày lễ. |
| Chờ duyệt | Trạng thái đơn đã gửi, đang chờ quản lý trực tiếp quyết định. |
| Đã duyệt | Trạng thái đơn được quản lý chấp thuận; ngày công của đơn đã bị trừ khỏi số dư. |
| Từ chối | Trạng thái đơn bị quản lý không chấp thuận, bắt buộc kèm lý do; trạng thái cuối. |
| Đã hủy | Trạng thái đơn bị chủ đơn rút lại; trạng thái cuối. |
| Quản lý trực tiếp | Người quản lý được gán cho nhân viên tại thời điểm quyết định đơn; là cấp duyệt duy nhất. |
| HR | Bộ phận nhân sự, chỉ có quyền đọc báo cáo nghỉ phép. |

## Giả định

| ID | Giả định | Cơ sở trong input, hoặc ảnh hưởng nếu sai |
|---|---|---|
| A-01 | Số dư khởi tạo của nhân viên vào giữa năm bằng số tháng làm việc trong năm nhân 1 ngày công, làm tròn xuống, tối đa 12 ngày. | Input không nêu cách tính cho người vào giữa năm; nếu sai chỉ đổi công thức khởi tạo của BR-001, không đổi danh sách FR. |
| A-02 | Ngày công loại trừ thứ Bảy, Chủ nhật và các ngày lễ do công ty công bố; lịch lễ là dữ liệu cấu hình theo năm. | Input nói "ngày làm việc" nhưng không nêu lịch lễ; nếu sai tổng số ngày công của mọi đơn thay đổi và BR-011, BR-003 phải tính lại. |
| A-03 | Mỗi nhân viên có đúng một quản lý trực tiếp tại một thời điểm. | Input nói "Quản lý trực tiếp duyệt" ở dạng số ít; nếu sai cần quy tắc chọn người duyệt và đổi BR-005. |
| A-04 | Không tích hợp hệ thống chấm công và tính lương trong phạm vi này. | Input chỉ nêu ba bước gửi, duyệt, trừ; nếu sai phạm vi tăng thêm luồng đồng bộ. |
| A-05 | Ngưỡng hiệu năng là p95 ≤ 2 giây với 100 người dùng đồng thời. | Input không nêu; đây là giá trị làm việc, nếu sai chỉ đổi NFR-001. |
| A-06 | Nhật ký thay đổi trạng thái được lưu 24 tháng. | Input không nêu; nếu sai chỉ đổi NFR-004. |
| A-07 | Luồng này chỉ áp dụng cho nghỉ phép năm; nghỉ ốm, thai sản và không lương nằm ngoài phạm vi. | Input chỉ nói "ngày phép"; nếu sai cần thêm loại đơn và đổi BR-001, BR-011, FR-001. |
| A-08 | Hệ thống khả dụng ≥ 99,5% mỗi tháng và thời gian khôi phục ≤ 4 giờ. | Input không nêu; đây là giá trị làm việc, nếu sai chỉ đổi NFR-002. |
| A-09 | Khối lượng đỉnh là 500 đơn mới mỗi ngày cho 2.000 nhân viên. | Input không nêu; nếu sai chỉ đổi NFR-005. |
| A-10 | Số dư không cộng dồn sang năm sau; ngày phép chưa dùng hết của năm trước không được chuyển sang năm sau. | Input chỉ nói "tối đa 12 ngày một năm"; nếu sai cần thêm quy tắc cộng dồn và đổi BR-001, FR-002. |
| A-11 | Chỉ ba vai trò Nhân viên, Quản lý trực tiếp và HR được xem dữ liệu nghỉ phép; không có vai trò quản trị khác. | Input nêu ba vai trò; nếu sai NFR-003 và bảng trường hợp biên phải thêm dòng. |
| A-12 | Khi nhân viên đổi quản lý trực tiếp trong lúc đơn đang Chờ duyệt, quản lý mới tại thời điểm quyết định là người duyệt đơn đó. | Input không nêu; nếu sai BR-005 và FR-004 phải đổi cách xác định người duyệt. |
| A-13 | Không có ngưỡng báo trước tối thiểu: nhân viên được gửi đơn cho ngày bắt đầu là hôm nay, miễn là đơn hợp lệ theo BR-004. | Input không nêu; nếu sai thêm một quy tắc và một AC cho FR-001. |
| A-14 | Không có ngưỡng riêng cho độ dài đơn; độ dài bị giới hạn bởi số dư khả dụng và trần 12 ngày công mỗi năm. | Input không nêu; nếu sai thêm quy tắc cho FR-001 và FR-003. |
| A-15 | Điều chỉnh số dư ngoài luồng này do bộ phận vận hành hệ thống thực hiện trực tiếp trên dữ liệu, không qua giao diện nghỉ phép. | Input nói HR chỉ xem báo cáo; nếu sai cần thêm FR điều chỉnh số dư và đổi BR-012. |
| A-16 | Đơn đang Chờ duyệt giữ chỗ số ngày trong số dư khả dụng ngay từ lúc gửi. | Input không nêu; nếu sai BR-003 và FR-002, FR-003 phải đổi cách tính số dư khả dụng. |

## Bước tiếp theo

Brainstorm giải pháp với tài liệu này làm ngữ cảnh, sau đó viết kế hoạch triển khai.
