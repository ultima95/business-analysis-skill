# Đơn nghỉ phép — Yêu cầu

## Bối cảnh

- Vấn đề: ứng dụng chưa có chức năng đăng ký nghỉ phép. Đầu vào lượt 1: "nhân viên gửi yêu cầu, quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại".
- Đầu vào lượt 2: "nghỉ phép được tính theo ngày làm việc, tối đa 12 ngày một năm; quản lý trực tiếp duyệt, nhân sự chỉ cần xem báo cáo".
- Nguồn đầu vào: hai lượt trao đổi trực tiếp với chủ sản phẩm ngày 2026-11-18, không kèm tài liệu hay ticket.
- Trạng thái: bản nháp để duyệt.

## Tác nhân và bên liên quan

| Tác nhân | Làm / quyết / được thông báo | Ghi chú | Cơ sở |
|---|---|---|---|
| Nhân viên | Tạo đơn nghỉ phép; xem số ngày phép còn lại và trạng thái đơn của mình | Chỉ tạo đơn cho chính mình | Đầu vào lượt 1: "nhân viên gửi yêu cầu"; chi tiết theo A-11 |
| Quản lý trực tiếp | Duyệt hoặc từ chối đơn của nhân viên mình | Người duy nhất có quyền quyết định đơn | Đầu vào lượt 1 "quản lý duyệt" và lượt 2 "quản lý trực tiếp duyệt" |
| Bộ phận hành chính nhân sự | Xem báo cáo nghỉ phép; không duyệt và không sửa đơn | Quyền chỉ đọc | Đầu vào lượt 2: "nhân sự chỉ cần xem báo cáo" |
| Bộ phận hành chính nhân sự | Công bố lịch ngày lễ | Việc nằm ngoài hệ thống | A-03 |

## Phạm vi

Trong phạm vi:

- Gửi đơn nghỉ phép cho một khoảng ngày liên tục, kèm lý do, tính theo ngày làm việc.
- Kiểm tra hạn mức 12 ngày làm việc mỗi năm của nhân viên.
- Quản lý trực tiếp duyệt hoặc từ chối đơn đang chờ.
- Trừ số ngày của đơn khỏi số ngày phép còn lại khi đơn được duyệt.
- Xem số ngày phép còn lại và trạng thái các đơn của một nhân viên.
- Xem báo cáo nghỉ phép cho bộ phận hành chính nhân sự.

Ngoài phạm vi:

- Hủy đơn đã duyệt và hoàn lại ngày phép (xem Q-03).
- Nghỉ nửa ngày, nghỉ theo giờ và mọi đơn vị nhỏ hơn một ngày (xem A-04).
- Nhiều loại nghỉ: nghỉ ốm, nghỉ thai sản, nghỉ không lương (xem A-05).
- Nghỉ hồi tố: gửi đơn cho ngày nghỉ đã qua.
- Nhiều cấp duyệt, duyệt thay, ủy quyền duyệt.
- Nhân sự sửa đơn, sửa số dư phép, hay tự nhập số ngày phép cho nhân viên trong hệ thống này.
- Chuyển phép tồn sang năm sau, thanh toán phép chưa nghỉ, cấu hình hạn mức khác 12 ngày.

## Quy tắc nghiệp vụ

- **BR-001**: Một đơn nghỉ phép do chính nhân viên nghỉ tạo; không ai tạo đơn thay người khác. Cơ sở: A-11.
- **BR-002**: Chỉ quản lý trực tiếp của nhân viên gửi đơn được duyệt hoặc từ chối đơn đó. Cơ sở: đầu vào lượt 2 "quản lý trực tiếp duyệt"; mỗi nhân viên có đúng một quản lý trực tiếp theo A-02.
- **BR-003**: Số ngày phép còn lại chỉ giảm khi đơn được duyệt; đơn đang Chờ duyệt hoặc Bị từ chối không làm thay đổi số dư. Cơ sở: A-01.
- **BR-004**: Không ghi nhận việc duyệt một đơn có số ngày nghỉ lớn hơn số ngày phép còn lại tại thời điểm duyệt. Cơ sở: A-01; cách xử lý ngoại lệ theo Q-02.
- **BR-005**: Mỗi đơn ở đúng một trạng thái tại một thời điểm, thuộc ba trạng thái Chờ duyệt, Đã duyệt, Bị từ chối; đơn không quay lại trạng thái trước đó. Cơ sở: A-12.
- **BR-006**: Số ngày nghỉ của một đơn tính theo ngày làm việc trong khoảng ngày của đơn, không tính ngày nghỉ hằng tuần và ngày lễ. Cơ sở: đầu vào lượt 2 "tính theo ngày làm việc".
- **BR-007**: Không ghi nhận đơn có khoảng ngày trùng với một đơn khác của cùng nhân viên đang Chờ duyệt hoặc Đã duyệt. Cơ sở: A-13.
- **BR-008**: Đơn đang Chờ duyệt không sửa và không xóa được; nhân viên muốn thay đổi thì chờ quyết định của quản lý rồi gửi đơn mới. Cơ sở: A-14.
- **BR-009**: Hạn mức phép của một nhân viên là 12 ngày làm việc trong một năm dương lịch; tổng số ngày của các đơn Đã duyệt trong năm cộng với số ngày của đơn mới không được vượt 12 ngày. Cơ sở: đầu vào lượt 2 "tối đa 12 ngày một năm"; cách đặt lại hạn mức theo A-15.
- **BR-010**: Bộ phận hành chính nhân sự chỉ được đọc báo cáo nghỉ phép; không được duyệt, từ chối, sửa hay xóa đơn. Cơ sở: đầu vào lượt 2 "nhân sự chỉ cần xem báo cáo".

## Yêu cầu chức năng

- **FR-001**: Là nhân viên, tôi muốn gửi đơn nghỉ phép với khoảng ngày và lý do, để quản lý xem xét và quyết định. Đáp ứng [BR-001, BR-006]. Ưu tiên: Must.
- **FR-001.AC1**: Given nhân viên còn 12 ngày phép, When nhân viên gửi đơn nghỉ 3 ngày làm việc, Then đơn được ghi nhận ở trạng thái Chờ duyệt và số ngày phép còn lại vẫn là 12 ngày.
- **FR-001.AC2**: Given nhân viên nhập ngày kết thúc trước ngày bắt đầu, When nhân viên gửi đơn, Then hệ thống từ chối và không ghi nhận đơn nào.
- **FR-001.AC3**: Given khoảng ngày của đơn chứa 2 ngày nghỉ hằng tuần và 1 ngày lễ, When nhân viên gửi đơn nghỉ 7 ngày liên tiếp, Then số ngày nghỉ của đơn được ghi nhận là 4 ngày.
- **FR-001.AC4**: Given một đơn đang Chờ duyệt, When nhân viên cố sửa hoặc xóa đơn đó, Then hệ thống từ chối thao tác và đơn giữ nguyên nội dung. Đáp ứng [BR-008].
- **FR-002**: Là nhân viên, tôi muốn xem số ngày phép còn lại của mình trong năm, để biết mình còn nghỉ được bao nhiêu ngày. Đáp ứng [BR-003, BR-009]. Ưu tiên: Must.
- **FR-002.AC1**: Given nhân viên chưa có đơn nào được duyệt trong năm, When nhân viên xem số ngày phép còn lại, Then hệ thống hiển thị 12 ngày.
- **FR-002.AC2**: Given nhân viên có 1 đơn 3 ngày đang Chờ duyệt, When nhân viên xem số ngày phép còn lại, Then hệ thống hiển thị số dư không đổi so với trước khi gửi đơn.
- **FR-003**: Là quản lý, tôi muốn duyệt hoặc từ chối đơn đang chờ của nhân viên mình, để đơn được xử lý dứt điểm. Đáp ứng [BR-002, BR-005]. Ưu tiên: Must.
- **FR-003.AC1**: Given đơn của nhân viên A đang Chờ duyệt, When quản lý trực tiếp của A duyệt đơn, Then đơn chuyển sang Đã duyệt và số ngày phép còn lại của A giảm đúng số ngày của đơn.
- **FR-003.AC2**: Given một người không phải quản lý trực tiếp của người gửi đơn, When người đó cố duyệt hoặc từ chối đơn, Then hệ thống từ chối thao tác và đơn giữ nguyên trạng thái Chờ duyệt.
- **FR-003.AC3**: Given một đơn đã ở trạng thái Đã duyệt, When quản lý duyệt lại đơn đó, Then trạng thái không đổi và số ngày phép còn lại không bị trừ thêm.
- **FR-004**: Hệ thống phải trừ số ngày nghỉ của đơn khỏi số ngày phép còn lại của nhân viên tại thời điểm đơn được duyệt. Đáp ứng [BR-003]. Ưu tiên: Must.
- **FR-004.AC1**: Given nhân viên còn 12 ngày phép, When quản lý duyệt đơn 3 ngày, Then số ngày phép còn lại là 9 ngày.
- **FR-004.AC2**: Given một đơn đang Chờ duyệt, When quản lý từ chối đơn đó, Then đơn chuyển sang Bị từ chối và số ngày phép còn lại của nhân viên không đổi.
- **FR-005**: Hệ thống phải chặn việc duyệt đơn có số ngày nghỉ lớn hơn số ngày phép còn lại của nhân viên tại thời điểm duyệt. Đáp ứng [BR-004, BR-009]. Ưu tiên: Must.
- **FR-005.AC1**: Given nhân viên còn 2 ngày phép, When quản lý duyệt đơn 3 ngày của nhân viên đó, Then hệ thống từ chối việc duyệt, đơn vẫn ở Chờ duyệt và số dư vẫn là 2 ngày.
- **FR-005.AC2**: Given nhân viên còn 3 ngày phép và có 2 đơn đang Chờ duyệt với số ngày 2 và 2, When quản lý duyệt đơn thứ hai, Then hệ thống từ chối việc duyệt đơn thứ hai và số dư vẫn là 1 ngày sau lần duyệt đơn thứ nhất.
- **FR-006**: Hệ thống phải từ chối ghi nhận đơn có khoảng ngày trùng với đơn khác của cùng nhân viên đang Chờ duyệt hoặc Đã duyệt. Đáp ứng [BR-007, BR-005]. Ưu tiên: Must.
- **FR-006.AC1**: Given nhân viên có đơn Đã duyệt từ 10/12 đến 12/12, When nhân viên gửi đơn từ 11/12 đến 13/12, Then hệ thống từ chối và không ghi nhận đơn mới.
- **FR-006.AC2**: Given nhân viên có đơn Bị từ chối từ 10/12 đến 12/12, When nhân viên gửi đơn từ 11/12 đến 13/12, Then hệ thống ghi nhận đơn mới ở trạng thái Chờ duyệt.
- **FR-007**: Là nhân viên, tôi muốn xem trạng thái các đơn của mình, để biết đơn nào đang chờ xử lý. Đáp ứng [BR-005]. Ưu tiên: Should.
- **FR-007.AC1**: Given nhân viên có 2 đơn, một ở Chờ duyệt và một ở Bị từ chối, When nhân viên xem danh sách đơn của mình, Then mỗi đơn hiển thị đúng trạng thái của nó và không có đơn của nhân viên khác.
- **FR-008**: Là quản lý, tôi muốn xem danh sách đơn đang chờ của nhân viên mình, để xử lý hết đơn tồn. Đáp ứng [BR-002]. Ưu tiên: Should.
- **FR-008.AC1**: Given 3 nhân viên trực tiếp đang có đơn Chờ duyệt, When quản lý xem danh sách đơn chờ, Then danh sách có đúng 3 đơn đó và không có đơn của nhân viên ngoài nhóm trực tiếp.
- **FR-009**: Hệ thống phải ghi nhận lý do khi quản lý từ chối một đơn. Đáp ứng [BR-005]. Ưu tiên: Could.
- **FR-009.AC1**: Given một đơn đang Chờ duyệt, When quản lý từ chối đơn mà không nhập lý do, Then hệ thống không ghi nhận việc từ chối và đơn vẫn ở Chờ duyệt.
- **FR-009.AC2**: Given một đơn đang Chờ duyệt, When quản lý từ chối kèm lý do, Then đơn chuyển sang Bị từ chối và lý do được lưu cùng đơn.
- **FR-010**: Hệ thống phải ghi nhận mỗi lần đổi trạng thái đơn, gồm thời điểm, người thực hiện, trạng thái trước và trạng thái sau. Đáp ứng [BR-005]. Ưu tiên: Should.
- **FR-010.AC1**: Given một đơn đang Chờ duyệt, When quản lý duyệt đơn, Then lịch sử của đơn có một bản ghi với thời điểm duyệt, người duyệt, trạng thái trước là Chờ duyệt và trạng thái sau là Đã duyệt.
- **FR-011**: Là nhân sự, tôi muốn xem báo cáo nghỉ phép theo nhân viên và theo tháng trong năm, gồm số ngày đã nghỉ, số ngày còn lại và số đơn theo từng trạng thái, để theo dõi việc dùng phép của toàn công ty. Đáp ứng [BR-009, BR-010]. Ưu tiên: Must.
- **FR-011.AC1**: Given 5 nhân viên trong năm có tổng 30 ngày nghỉ đã duyệt, When nhân sự xem báo cáo nghỉ phép của năm, Then báo cáo hiển thị đúng 5 nhân viên, tổng 30 ngày đã nghỉ và số ngày còn lại của từng người.
- **FR-011.AC2**: Given nhân sự đang xem báo cáo nghỉ phép, When nhân sự cố sửa hoặc duyệt một đơn trong báo cáo, Then hệ thống không có thao tác ghi nào cho nhân sự và dữ liệu đơn không đổi.
- **FR-012**: Hệ thống phải từ chối ghi nhận đơn có số ngày nghỉ lớn hơn số ngày phép còn lại của nhân viên tại thời điểm gửi, kèm hạn mức 12 ngày làm việc mỗi năm. Đáp ứng [BR-004, BR-009]. Ưu tiên: Must.
- **FR-012.AC1**: Given nhân viên đã nghỉ 10 ngày trong năm, When nhân viên gửi đơn 3 ngày, Then hệ thống từ chối và chỉ ra số ngày còn lại là 2 ngày.
- **FR-012.AC2**: Given nhân viên đã nghỉ 10 ngày trong năm, When nhân viên gửi đơn 2 ngày, Then hệ thống ghi nhận đơn ở trạng thái Chờ duyệt.

## Yêu cầu phi chức năng

| ID | Ưu tiên | Mục tiêu | Cơ sở |
|---|---|---|---|
| NFR-001 | Must | p95 thời gian phản hồi ≤ 2 giây cho thao tác gửi đơn và thao tác duyệt đơn | A-08 |
| NFR-002 | Must | Xử lý 200 lượt gửi đơn hoặc duyệt đơn trong một giờ mà p95 vẫn ≤ 2 giây | A-06 |
| NFR-003 | Must | 100% yêu cầu xem hoặc sửa đơn từ người không phải chủ đơn, không phải quản lý trực tiếp và không phải nhân sự với quyền đọc báo cáo bị từ chối | A-07 |
| NFR-004 | Must | Lịch sử đổi trạng thái đơn được lưu tối thiểu 24 tháng kể từ lần đổi trạng thái cuối cùng | A-09 |
| NFR-005 | Must | Chênh lệch giữa số ngày phép còn lại hiển thị và 12 ngày trừ tổng số ngày của các đơn Đã duyệt trong năm là 0 ngày tại mọi lần đối soát | A-10, BR-009 |
| NFR-006 | Should | p95 thời gian hiển thị báo cáo nghỉ phép 12 tháng cho 500 nhân viên ≤ 5 giây | A-16 |

- **NFR-001.AC1**: Given 100 lượt gửi đơn và duyệt đơn đồng thời, When đo thời gian phản hồi của từng lượt, Then p95 thời gian phản hồi ≤ 2 giây.
- **NFR-002.AC1**: Given 200 lượt gửi đơn và duyệt đơn trong một giờ, When hệ thống xử lý hết số lượt đó, Then 0 lượt thất bại do quá tải.
- **NFR-003.AC1**: Given một người không phải chủ đơn, không phải quản lý trực tiếp và không phải nhân sự đọc báo cáo, When người đó yêu cầu xem hoặc sửa đơn, Then 100% yêu cầu bị từ chối.
- **NFR-004.AC1**: Given một đơn có lần đổi trạng thái cách thời điểm kiểm tra 24 tháng, When tra lịch sử của đơn, Then bản ghi của lần đổi đó vẫn còn.
- **NFR-005.AC1**: Given nhân viên có 3 đơn Đã duyệt với tổng 7 ngày trong năm, When đối soát số dư, Then số ngày phép còn lại hiển thị là 5 ngày.
- **NFR-006.AC1**: Given 500 nhân viên có dữ liệu 12 tháng, When nhân sự mở báo cáo nghỉ phép, Then p95 thời gian hiển thị ≤ 5 giây.

## Trường hợp biên

| Tác nhân | Trạng thái đối tượng | Tạo | Đọc | Sửa | Xóa |
|---|---|---|---|---|---|
| Nhân viên | Chưa có đơn nào | Đơn mới ở Chờ duyệt, số dư không đổi | Chỉ thấy số dư và danh sách đơn của mình | Không có đơn để sửa | Không có đơn để xóa |
| Nhân viên | Chờ duyệt | Bị từ chối nếu trùng khoảng ngày với đơn đang hiệu lực hoặc vượt số dư, ngược lại ghi nhận đơn mới | Thấy trạng thái Chờ duyệt | Không cho sửa, đơn giữ nguyên | Không cho xóa, đơn giữ nguyên |
| Nhân viên | Đã duyệt | Chỉ ghi nhận nếu khoảng ngày không trùng đơn đã duyệt và số dư còn đủ | Thấy trạng thái Đã duyệt và số dư đã giảm | Không cho sửa | Không cho xóa, đơn được giữ làm lịch sử theo A-09 |
| Nhân viên | Bị từ chối | Ghi nhận đơn mới nếu khoảng ngày không trùng đơn đang hiệu lực | Thấy trạng thái Bị từ chối và lý do từ chối | Không cho sửa | Không cho xóa, đơn được giữ làm lịch sử theo A-09 |
| Nhân viên | Đã dùng hết 12 ngày trong năm | Bị từ chối vì số dư là 0 ngày | Thấy số dư 0 ngày và các đơn đã duyệt | Không có đơn nào sửa được | Không cho xóa |
| Quản lý trực tiếp | Chờ duyệt | Không tạo đơn thay nhân viên | Thấy đơn của nhân viên mình | Duyệt hoặc từ chối; từ chối cần lý do | Không cho xóa, chỉ đổi trạng thái |
| Quản lý trực tiếp | Đã duyệt | Không tạo đơn thay nhân viên | Thấy đơn và số dư của nhân viên mình | Duyệt lại không làm đổi trạng thái và không trừ thêm ngày | Không cho xóa |
| Quản lý trực tiếp | Bị từ chối | Không tạo đơn thay nhân viên | Thấy đơn và lý do từ chối | Không cho duyệt lại đơn đã từ chối | Không cho xóa |
| Quản lý không trực tiếp | Mọi trạng thái | Không tạo đơn | Không thấy đơn của nhân viên ngoài nhóm trực tiếp | Không duyệt, không từ chối | Không xóa |
| Nhân sự | Mọi trạng thái | Không tạo đơn | Thấy báo cáo tổng hợp của toàn công ty | Không cho sửa | Không cho xóa |

## Thuật ngữ

| Thuật ngữ | Ý nghĩa |
|---|---|
| Đơn nghỉ phép | Một yêu cầu nghỉ cho một khoảng ngày liên tục của một nhân viên, kèm lý do. |
| Hạn mức phép năm | 12 ngày làm việc mà một nhân viên được nghỉ trong một năm dương lịch. |
| Số ngày phép còn lại | Hạn mức phép năm trừ tổng số ngày của các đơn đã được duyệt trong năm. |
| Ngày làm việc | Ngày trong khoảng ngày của đơn, không phải ngày nghỉ hằng tuần và không phải ngày lễ. |
| Ngày lễ | Ngày nghỉ do bộ phận hành chính nhân sự công bố, không tính vào số ngày nghỉ của đơn. |
| Quản lý trực tiếp | Người duy nhất có quyền quyết định đơn của một nhân viên. |
| Chờ duyệt | Trạng thái của đơn đã được ghi nhận và đang đợi quản lý trực tiếp quyết định. |
| Đã duyệt | Trạng thái của đơn được quản lý trực tiếp chấp thuận và đã trừ vào số ngày phép còn lại. |
| Bị từ chối | Trạng thái của đơn bị quản lý trực tiếp không chấp thuận, kèm lý do. |
| Báo cáo nghỉ phép | Bảng tổng hợp theo nhân viên và theo tháng trong năm, gồm số ngày đã nghỉ, số ngày còn lại và số đơn theo từng trạng thái. |
| Lượt gửi hoặc duyệt đơn | Một lần nhân viên gửi đơn hoặc một lần quản lý quyết định một đơn. |

## Giả định

| ID | Giả định | Cơ sở trong input, hoặc ảnh hưởng nếu sai |
|---|---|---|
| A-01 | Số ngày phép chỉ bị trừ khi đơn được duyệt; đơn đang chờ không giữ chỗ ngày phép, nhưng vẫn bị kiểm tra số dư tại thời điểm gửi. | Đầu vào nói "hệ thống trừ vào số ngày phép còn lại" mà không nêu thời điểm; nếu sai thì thêm bước giữ chỗ khi gửi đơn và hoàn ngày khi từ chối. |
| A-02 | "Quản lý trực tiếp" là quan hệ có sẵn trong dữ liệu nhân sự và mỗi nhân viên có đúng một quản lý trực tiếp. | Đầu vào lượt 2 nêu "quản lý trực tiếp duyệt" nhưng không nói quan hệ này có sẵn; nếu sai thì cần quy tắc chọn người duyệt. |
| A-03 | Hệ thống nhận lịch ngày lễ từ bộ phận hành chính nhân sự; không có lịch này thì mọi ngày trong khoảng ngày của đơn chỉ loại trừ ngày nghỉ hằng tuần. | Đầu vào lượt 2 nói "tính theo ngày làm việc" mà không định nghĩa ngày lễ; nếu sai thì BR-006 và FR-001.AC3 phải viết lại. |
| A-04 | Đơn vị nghỉ là ngày nguyên; không có nửa ngày và không có nghỉ theo giờ. | Không nêu trong đầu vào; nếu sai thì BR-006 và các AC dùng 0,5 ngày phải viết lại. |
| A-05 | Chỉ có một loại nghỉ là phép năm, không tách nghỉ ốm, thai sản hay không lương. | Không nêu trong đầu vào; nếu sai thì thêm loại nghỉ và quy tắc trừ riêng cho từng loại. |
| A-06 | Khối lượng đỉnh là 200 lượt gửi đơn hoặc duyệt đơn trong một giờ. | Số ước lượng của người viết yêu cầu; nếu sai thì mục tiêu của NFR-002 thay đổi. |
| A-07 | Chỉ chủ đơn, quản lý trực tiếp và nhân sự với quyền đọc báo cáo được xem một đơn. | Không nêu trong đầu vào; nếu sai thì phạm vi truy cập của NFR-003 phải thay đổi. |
| A-08 | p95 thời gian phản hồi mục tiêu là 2 giây cho thao tác gửi đơn và duyệt đơn. | Không nêu trong đầu vào; nếu sai thì mục tiêu của NFR-001 thay đổi. |
| A-09 | Lịch sử đổi trạng thái đơn được lưu tối thiểu 24 tháng. | Không nêu trong đầu vào; nếu sai thì mục tiêu của NFR-004 và thời hạn giữ đơn bị từ chối thay đổi. |
| A-10 | Số ngày phép còn lại luôn bằng 12 ngày trừ tổng số ngày của các đơn Đã duyệt trong năm. | Suy ra từ đầu vào lượt 1 và lượt 2; nếu sai thì cần thêm nguồn điều chỉnh số dư ngoài đơn nghỉ phép. |
| A-11 | Nhân viên chỉ tạo đơn cho chính mình, không tạo đơn hộ người khác. | Đầu vào nói "nhân viên gửi yêu cầu"; nếu sai thì thêm quyền tạo đơn hộ và quy tắc xác nhận của người nghỉ. |
| A-12 | Một đơn chỉ có ba trạng thái Chờ duyệt, Đã duyệt, Bị từ chối và không chuyển ngược. | Suy ra từ luồng "gửi yêu cầu, quản lý duyệt" trong đầu vào; nếu sai thì cần thêm trạng thái và luật chuyển trạng thái. |
| A-13 | Đơn trùng khoảng ngày với đơn đang Chờ duyệt hoặc Đã duyệt của cùng nhân viên bị từ chối ghi nhận. | Không nêu trong đầu vào; nếu sai thì cho phép nhiều đơn chồng lấn và bỏ BR-007. |
| A-14 | Đơn đang Chờ duyệt không sửa và không xóa được. | Không nêu trong đầu vào; nếu sai thì thêm luồng sửa và xóa đơn đang chờ. |
| A-15 | Hạn mức 12 ngày được đặt lại vào ngày 01/01 hằng năm, không cộng dồn ngày chưa nghỉ sang năm sau. | Đầu vào lượt 2 chỉ nêu "tối đa 12 ngày một năm"; nếu sai thì BR-009 và NFR-005 phải tính thêm phần cộng dồn. |
| A-16 | Báo cáo nghỉ phép cho 500 nhân viên và 12 tháng có p95 thời gian hiển thị 5 giây. | Số ước lượng của người viết yêu cầu; nếu sai thì mục tiêu của NFR-006 thay đổi. |
| A-17 | Báo cáo nghỉ phép của nhân sự bao gồm toàn bộ nhân viên trong công ty và không giới hạn theo bộ phận. | Đầu vào lượt 2 nói "nhân sự chỉ cần xem báo cáo" mà không nêu phạm vi; nếu sai thì FR-011 phải thêm bộ lọc theo bộ phận. |

## Phụ thuộc

- Lịch ngày lễ phải có trước khi tính số ngày nghỉ của đơn; lịch do bộ phận hành chính nhân sự công bố, hệ thống không tự sinh (A-03).
- Quan hệ quản lý trực tiếp phải có trong dữ liệu nhân sự hiện có trước khi phân quyền duyệt (A-02).
- Hạn mức 12 ngày là giá trị cố định của bản phát hành này; thay đổi hạn mức cần yêu cầu riêng (A-15).

## Câu hỏi mở

| ID | Câu hỏi | Người trả lời | Chặn |
|---|---|---|---|
| Q-01 | Nhân viên vào làm giữa năm hoặc nghỉ việc giữa năm thì hạn mức 12 ngày được tính theo tỉ lệ tháng làm việc hay giữ nguyên 12 ngày? | Bộ phận hành chính nhân sự | FR-002, FR-012 |
| Q-02 | Khi số ngày phép còn lại không đủ, quản lý có được duyệt ngoại lệ để số dư âm không? | Chủ sản phẩm | FR-005 |
| Q-03 | Bản phát hành này có cần hủy đơn đã duyệt và hoàn lại ngày phép không? | Chủ sản phẩm | FR-004 |

## Bước tiếp theo

Chuyển sang brainstorming với tài liệu này làm ngữ cảnh, sau đó writing-plans trước khi viết mã.
