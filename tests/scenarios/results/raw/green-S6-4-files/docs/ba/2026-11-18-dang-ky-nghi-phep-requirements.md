# Đăng ký nghỉ phép — Yêu cầu

## Bối cảnh

- Vấn đề: Nhân viên chưa có cách gửi yêu cầu nghỉ phép trong ứng dụng; việc xin nghỉ và trừ ngày phép còn lại chưa được ghi nhận ở một nơi.
- Vì sao bây giờ: Yêu cầu tính năng mới cho ứng dụng hiện có; cần chốt yêu cầu trước khi lập kế hoạch kỹ thuật.
- Nguồn đầu vào:
  - Tin nhắn yêu cầu của chủ sản phẩm, nguyên văn: "nhân viên gửi yêu cầu, quản lý duyệt, và hệ thống trừ vào số ngày phép còn lại".
  - Trả lời bổ sung của chủ sản phẩm, nguyên văn: "Nghỉ phép được tính theo ngày làm việc, tối đa 12 ngày một năm. Quản lý trực tiếp duyệt, nhân sự chỉ cần xem báo cáo."
- Trạng thái mã nguồn: Repo hiện chỉ có thư mục `.git`, không có mã nguồn, nên không có quy tắc nghiệp vụ nào được phục hồi từ code.

## Các vai trò và bên liên quan

| Vai trò | Làm gì / quyết định / được thông báo | Ghi chú | Cơ sở |
|---|---|---|---|
| Nhân viên | Tạo và gửi đơn nghỉ phép; xem số ngày phép còn lại; xem trạng thái đơn; hủy đơn đang chờ | Người khởi tạo đơn | Nguyên văn "nhân viên gửi yêu cầu"; quyền hủy theo A-03 |
| Quản lý trực tiếp | Duyệt hoặc từ chối đơn của nhân viên mình; là cấp duyệt duy nhất | Một cấp duyệt | Nguyên văn "quản lý duyệt", "Quản lý trực tiếp duyệt"; A-04 |
| Quản lý khác | Không duyệt được đơn của nhân viên ngoài nhóm mình | Ràng buộc quyền | BR-001 |
| Nhân sự (HR) | Chỉ đọc đơn, báo cáo ngày phép và nhật ký; không duyệt, không sửa, không xóa | Vai trò chỉ đọc | Nguyên văn "nhân sự chỉ cần xem báo cáo"; BR-015 |

## Phạm vi

Trong phạm vi:
- Nhân viên tạo, gửi và hủy đơn nghỉ phép.
- Quản lý trực tiếp xem, duyệt, từ chối đơn của nhân viên mình.
- Hệ thống trừ số ngày phép còn lại khi đơn được duyệt và hiển thị số ngày còn lại theo mức tối đa 12 ngày làm việc một năm.
- Nhân sự xem báo cáo ngày phép đã duyệt và nhật ký thay đổi trạng thái.

Ngoài phạm vi:
- Chấm công, tính lương, nghỉ thai sản và các loại nghỉ theo chế độ bảo hiểm.
- Duyệt nhiều cấp và duyệt thay khi quản lý vắng (chờ Q-06).
- Chức năng gán quỹ phép riêng cho từng nhân viên: mức phép là 12 ngày làm việc mỗi năm theo BR-013, không có bước nhập tay.
- Nghỉ nửa ngày hoặc nghỉ theo giờ (xem A-06).
- Tích hợp với hệ thống nhân sự bên ngoài (xem Q-10, Q-02).

## Quy tắc nghiệp vụ

- **BR-001**: Chỉ quản lý trực tiếp của người gửi được duyệt hoặc từ chối đơn nghỉ phép của nhân viên đó; mọi vai trò khác bị chặn. (Cơ sở: A-04, câu trả lời "Quản lý trực tiếp duyệt")
- **BR-002**: Chỉ đơn ở trạng thái Chờ duyệt mới nhận được quyết định duyệt hoặc từ chối; đơn đã ở trạng thái Đã duyệt, Đã từ chối hoặc Đã hủy bị chặn và giữ nguyên trạng thái.
- **BR-003**: Khi đơn được duyệt, số ngày phép còn lại của nhân viên giảm đúng bằng số ngày của đơn, và mức giảm được ghi nhận một lần cho mỗi đơn.
- **BR-004**: Đơn bị từ chối hoặc bị hủy không làm thay đổi số ngày phép còn lại. (Cơ sở: A-01)
- **BR-005**: Đơn chỉ được duyệt khi số ngày phép còn lại tại thời điểm duyệt lớn hơn hoặc bằng số ngày của đơn. (Cơ sở: A-02)
- **BR-006**: Số ngày của đơn bằng số ngày làm việc trong khoảng nghỉ, không tính thứ Bảy, Chủ Nhật và ngày lễ trong lịch của công ty. (Cơ sở: câu trả lời "Nghỉ phép được tính theo ngày làm việc")
- **BR-007**: Nhân viên chỉ hủy được đơn ở trạng thái Nháp hoặc Chờ duyệt; đơn Đã duyệt không hủy được qua thao tác của nhân viên. (Cơ sở: A-03)
- **BR-008**: Mỗi nhân viên có tối đa một quản lý trực tiếp trong hồ sơ; nhân viên không có quản lý trực tiếp không gửi được đơn. (Cơ sở: A-04)
- **BR-009**: Hệ thống chặn đơn có khoảng ngày trùng với một đơn khác của cùng nhân viên đang ở trạng thái Nháp, Chờ duyệt hoặc Đã duyệt. (Cơ sở: A-05)
- **BR-010**: Đơn hợp lệ phải có ngày bắt đầu không sau ngày kết thúc và có ít nhất 1 ngày làm việc theo BR-006.
- **BR-011**: Tại thời điểm gửi, hệ thống chặn đơn có số ngày lớn hơn số ngày phép còn lại hiện tại. (Cơ sở: A-02)
- **BR-012**: Mỗi lần từ chối phải kèm lý do từ chối do quản lý nhập. (Cơ sở: A-07)
- **BR-013**: Mỗi nhân viên được tối đa 12 ngày làm việc nghỉ phép trong một năm dương lịch; hệ thống chặn mọi lượt duyệt làm tổng số ngày của các đơn Đã duyệt trong năm vượt quá 12 ngày. (Cơ sở: câu trả lời "tối đa 12 ngày một năm")
- **BR-014**: Mỗi lần đơn đổi trạng thái, hệ thống ghi một bản ghi nhật ký không sửa được, gồm người thực hiện, thời điểm, trạng thái trước và trạng thái sau.
- **BR-015**: Nhân sự chỉ được đọc đơn, báo cáo và nhật ký; nhân sự không được duyệt, từ chối, sửa hoặc xóa đơn và không được thay đổi số ngày phép của nhân viên. (Cơ sở: câu trả lời "nhân sự chỉ cần xem báo cáo")
- **BR-016**: Mỗi đơn chỉ qua đúng một cấp duyệt là quản lý trực tiếp; không có cấp duyệt thứ hai. (Cơ sở: câu trả lời "Quản lý trực tiếp duyệt")

### Bảng quyết định khi xử lý đơn

| Điều kiện / hành động | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| Người xử lý là quản lý trực tiếp (BR-001) | Y | Y | Y | N | Y |
| Đơn đang ở trạng thái Chờ duyệt (BR-002) | Y | Y | Y | N | Y |
| Số ngày phép còn lại lớn hơn hoặc bằng số ngày đơn (BR-005) | Y | Y | N | – | Y |
| Tổng ngày đã duyệt trong năm cộng số ngày đơn không vượt 12 (BR-013) | Y | Y | Y | – | N |
| Quyết định của quản lý | Duyệt | Từ chối | Duyệt | Duyệt | Duyệt |
| Kết quả | Đơn Đã duyệt, trừ số ngày đơn (BR-003) | Đơn Đã từ chối, không trừ (BR-004) | Chặn duyệt, báo lỗi thiếu ngày phép, đơn giữ Chờ duyệt | Chặn, báo đơn không ở trạng thái Chờ duyệt | Chặn duyệt, báo đã đạt mức 12 ngày trong năm, đơn giữ Chờ duyệt |

## Yêu cầu chức năng

- **FR-001**: Là nhân viên, tôi muốn tạo và gửi đơn nghỉ phép với ngày bắt đầu, ngày kết thúc và lý do, để quản lý xem xét. Đáp ứng [BR-006], [BR-008], [BR-009], [BR-010], [BR-011], [BR-013]. Ưu tiên: Must.
- **FR-001.AC1**: Given nhân viên chưa dùng ngày phép nào trong năm, When gửi đơn nghỉ từ thứ Hai đến thứ Tư không có ngày lễ, Then đơn có trạng thái Chờ duyệt và số ngày của đơn là 3.
- **FR-001.AC2**: Given ngày kết thúc trước ngày bắt đầu, When nhân viên gửi đơn, Then hệ thống chặn và hiển thị thông báo lỗi khoảng ngày không hợp lệ, đơn không được tạo.
- **FR-001.AC3**: Given nhân viên đã có đơn Chờ duyệt cho ngày 10 đến 12, When gửi đơn mới cho ngày 11, Then hệ thống chặn và hiển thị thông báo trùng khoảng ngày với đơn hiện có.
- **FR-001.AC4**: Given nhân viên chưa được gán quản lý trực tiếp, When gửi đơn, Then hệ thống chặn và hiển thị thông báo chưa có người duyệt.
- **FR-001.AC5**: Given nhân viên còn 2 ngày phép, When gửi đơn nghỉ 3 ngày làm việc, Then hệ thống chặn và hiển thị thông báo số ngày phép còn lại không đủ.
- **FR-001.AC6**: Given khoảng nghỉ gồm thứ Sáu, thứ Bảy, Chủ Nhật và thứ Hai, When nhân viên gửi đơn, Then số ngày của đơn là 2.
- **FR-001.AC7**: Given nhân viên đã có 10 ngày phép được duyệt trong năm nay, When nhân viên gửi đơn 3 ngày làm việc, Then hệ thống chặn và hiển thị thông báo vượt mức 12 ngày trong năm.
- **FR-001.AC8**: Given khoảng nghỉ chỉ gồm thứ Bảy và Chủ Nhật, When nhân viên gửi đơn, Then hệ thống chặn và hiển thị thông báo khoảng nghỉ không có ngày làm việc.
- **FR-002**: Là nhân viên, tôi muốn xem số ngày phép còn lại và trạng thái các đơn của mình, để biết mình còn bao nhiêu ngày trong mức 12 ngày của năm và đơn đang ở bước nào. Đáp ứng [BR-003], [BR-004], [BR-013]. Ưu tiên: Must.
- **FR-002.AC1**: Given nhân viên chưa dùng ngày phép nào trong năm dương lịch hiện tại, When mở trang nghỉ phép, Then hệ thống hiển thị 12 ngày phép còn lại.
- **FR-002.AC2**: Given nhân viên có một đơn 3 ngày đã được duyệt trong năm, When mở trang nghỉ phép, Then hệ thống hiển thị 9 ngày phép còn lại và đơn ở trạng thái Đã duyệt.
- **FR-002.AC3**: Given nhân viên có một đơn 3 ngày bị từ chối trong năm, When mở trang nghỉ phép, Then hệ thống hiển thị 12 ngày phép còn lại và lý do từ chối của đơn đó.
- **FR-002.AC4**: Given hai nhân viên A và B, When A đăng nhập, Then A chỉ thấy số ngày phép và đơn của A, không thấy dữ liệu của B.
- **FR-003**: Là quản lý trực tiếp, tôi muốn xem danh sách đơn Chờ duyệt của nhân viên mình, để xử lý đúng đơn thuộc nhóm mình. Đáp ứng [BR-001]. Ưu tiên: Must.
- **FR-003.AC1**: Given quản lý A có 3 nhân viên và 2 đơn Chờ duyệt, When A mở danh sách đơn chờ duyệt, Then danh sách có đúng 2 đơn kèm tên nhân viên, khoảng ngày và số ngày.
- **FR-003.AC2**: Given nhân viên C thuộc quản lý B, When quản lý A mở danh sách đơn chờ duyệt, Then danh sách của A không chứa đơn của C.
- **FR-004**: Là quản lý trực tiếp, tôi muốn duyệt đơn của nhân viên mình, để đơn được ghi nhận và ngày phép được trừ. Đáp ứng [BR-001], [BR-002], [BR-003], [BR-005], [BR-013], [BR-014], [BR-016]. Ưu tiên: Must.
- **FR-004.AC1**: Given một đơn 3 ngày đang Chờ duyệt và nhân viên còn 9 ngày phép, When quản lý trực tiếp duyệt, Then đơn chuyển Đã duyệt và số ngày phép còn lại là 6.
- **FR-004.AC2**: Given một đơn đã ở trạng thái Đã duyệt, When quản lý duyệt lại, Then hệ thống chặn và số ngày phép còn lại không đổi.
- **FR-004.AC3**: Given đơn 3 ngày đang Chờ duyệt và nhân viên chỉ còn 2 ngày phép, When quản lý duyệt, Then hệ thống chặn, hiển thị thông báo thiếu ngày phép và đơn giữ trạng thái Chờ duyệt.
- **FR-004.AC4**: Given quản lý không phải quản lý trực tiếp của người gửi, When người đó duyệt đơn, Then hệ thống chặn và hiển thị thông báo không có quyền duyệt.
- **FR-004.AC5**: Given quản lý duyệt thành công một đơn, When xem nhật ký của đơn, Then có một bản ghi gồm người duyệt, thời điểm duyệt, trạng thái trước Chờ duyệt và trạng thái sau Đã duyệt.
- **FR-004.AC6**: Given nhân viên đã có 10 ngày phép được duyệt trong năm, When quản lý duyệt một đơn 3 ngày, Then hệ thống chặn, hiển thị thông báo vượt mức 12 ngày trong năm và đơn giữ trạng thái Chờ duyệt.
- **FR-004.AC7**: Given một đơn đang Chờ duyệt, When nhân sự bấm duyệt đơn đó, Then hệ thống chặn và hiển thị thông báo nhân sự không có quyền duyệt.
- **FR-005**: Là quản lý trực tiếp, tôi muốn từ chối đơn kèm lý do, để nhân viên biết vì sao đơn không được duyệt. Đáp ứng [BR-001], [BR-002], [BR-004], [BR-012]. Ưu tiên: Must.
- **FR-005.AC1**: Given một đơn 3 ngày đang Chờ duyệt và nhân viên còn 9 ngày phép, When quản lý từ chối kèm lý do, Then đơn chuyển Đã từ chối, lý do hiển thị cho nhân viên và số ngày phép còn lại là 9.
- **FR-005.AC2**: Given quản lý bỏ trống ô lý do, When bấm từ chối, Then hệ thống chặn và yêu cầu nhập lý do, đơn giữ trạng thái Chờ duyệt.
- **FR-005.AC3**: Given một đơn đã ở trạng thái Đã từ chối, When quản lý từ chối lại, Then hệ thống chặn và trạng thái đơn không đổi.
- **FR-006**: Là nhân viên, tôi muốn hủy đơn chưa được duyệt, để rút yêu cầu khi kế hoạch thay đổi. Đáp ứng [BR-004], [BR-007], [BR-014]. Ưu tiên: Should.
- **FR-006.AC1**: Given một đơn đang Chờ duyệt và nhân viên còn 9 ngày phép, When nhân viên hủy đơn, Then đơn chuyển Đã hủy và số ngày phép còn lại là 9.
- **FR-006.AC2**: Given một đơn đã ở trạng thái Đã duyệt, When nhân viên bấm hủy, Then hệ thống chặn, hiển thị thông báo đơn đã duyệt không hủy được và trạng thái đơn không đổi.
- **FR-007**: Hệ thống phải gửi thông báo cho người nhận liên quan mỗi khi đơn đổi trạng thái. Đáp ứng [BR-014]. Ưu tiên: Should.
- **FR-007.AC1**: Given một nhân viên gửi đơn thành công, When đơn chuyển sang Chờ duyệt, Then quản lý trực tiếp nhận thông báo trong vòng 5 phút.
- **FR-007.AC2**: Given quản lý vừa duyệt hoặc từ chối một đơn, When đơn đổi trạng thái, Then nhân viên gửi đơn nhận thông báo kèm trạng thái mới trong vòng 5 phút.
- **FR-007.AC3**: Given nhân sự đang theo dõi kỳ báo cáo tháng, When một đơn đổi trạng thái, Then nhân sự không nhận thông báo cho sự kiện đó.
- **FR-008**: Hệ thống phải lưu nhật ký mỗi lần đơn đổi trạng thái và cho nhân sự đọc nhật ký đó. Đáp ứng [BR-002], [BR-014], [BR-015]. Ưu tiên: Should.
- **FR-008.AC1**: Given một đơn trải qua các trạng thái Chờ duyệt, Đã duyệt, When nhân sự mở nhật ký của đơn, Then nhật ký có 2 bản ghi theo thứ tự thời gian, mỗi bản ghi có người thực hiện và thời điểm.
- **FR-008.AC2**: Given một bản ghi nhật ký đã được tạo, When bất kỳ người dùng nào tìm cách sửa hoặc xóa bản ghi, Then hệ thống chặn và nội dung bản ghi giữ nguyên.
- **FR-008.AC3**: Given nhân sự đã đăng nhập, When nhân sự tìm cách sửa trạng thái một đơn, Then hệ thống chặn và trạng thái đơn giữ nguyên.
- **FR-009**: Là nhân sự, tôi muốn xem báo cáo ngày phép đã duyệt theo nhân viên và theo kỳ, để đối chiếu số ngày phép đã dùng với mức 12 ngày mỗi năm. Đáp ứng [BR-003], [BR-013], [BR-015]. Ưu tiên: Must.
- **FR-009.AC1**: Given 2 nhân viên có tổng 5 ngày phép đã duyệt trong tháng 10, When nhân sự chọn kỳ tháng 10, Then báo cáo hiển thị tổng 5 ngày đã duyệt và khớp với nhật ký trừ phép.
- **FR-009.AC2**: Given một nhân viên có 12 ngày phép đã duyệt trong năm, When nhân sự xem báo cáo năm, Then dòng của nhân viên đó hiển thị 12 ngày đã dùng và 0 ngày còn lại.
- **FR-009.AC3**: Given nhân sự đã đăng nhập, When nhân sự tìm cách gán hoặc sửa số ngày phép của một nhân viên, Then hệ thống không có thao tác đó và số ngày phép giữ nguyên.

## Yêu cầu phi chức năng

| ID | Ưu tiên | Mục tiêu đo được | Cơ sở |
|---|---|---|---|
| NFR-001 | Must | p95 thời gian phản hồi ≤ 2 giây cho thao tác gửi đơn và duyệt đơn khi có 200 người dùng đồng thời | A-10 |
| NFR-002 | Must | 0 lần trừ trùng: sau 1.000 lượt duyệt đồng thời trên 100 đơn, tổng ngày đã trừ bằng đúng tổng ngày của các đơn Đã duyệt | A-11 |
| NFR-003 | Must | 100% yêu cầu đọc hoặc sửa dữ liệu phép của người khác bị từ chối với người không có quyền, gồm cả yêu cầu ghi của nhân sự | A-12 |
| NFR-004 | Should | Độ sẵn sàng ≥ 99,5% trong giờ hành chính, tính theo tháng | A-13 |
| NFR-005 | Should | Nhật ký thay đổi trạng thái được lưu ≥ 24 tháng kể từ ngày tạo | A-14 |
| NFR-006 | Should | Nhân viên hoàn tất việc gửi một đơn trong ≤ 4 bước và ≤ 2 phút | A-15 |

- **NFR-001.AC1**: Given 200 người dùng đồng thời, When 100 người gửi đơn trong cùng 1 phút, Then p95 thời gian phản hồi là ≤ 2 giây.
- **NFR-002.AC1**: Given 2 quản lý bấm duyệt cùng một đơn tại cùng thời điểm, When hệ thống xử lý, Then chỉ 1 lượt duyệt được ghi nhận và tổng ngày trừ cho đơn đó đúng bằng số ngày của đơn.
- **NFR-003.AC1**: Given nhân viên A đã đăng nhập, When A gọi yêu cầu đọc số ngày phép của nhân viên B, Then hệ thống trả về từ chối truy cập và không trả dữ liệu của B.
- **NFR-003.AC2**: Given nhân sự đã đăng nhập, When nhân sự gọi yêu cầu ghi vào một đơn nghỉ phép, Then hệ thống trả về từ chối truy cập và đơn giữ nguyên.
- **NFR-004.AC1**: Given một tháng có 22 ngày làm việc, When tính độ sẵn sàng trong giờ hành chính, Then tỉ lệ thời gian phục vụ được là ≥ 99,5%.
- **NFR-005.AC1**: Given một bản ghi nhật ký được tạo ngày 01/01/2026, When nhân sự tra cứu vào ngày 01/01/2028, Then bản ghi vẫn đọc được.
- **NFR-006.AC1**: Given một nhân viên đã đăng nhập, When nhân viên gửi một đơn nghỉ 3 ngày, Then số bước thao tác là ≤ 4 và thời gian hoàn tất là ≤ 2 phút.

## Trường hợp biên

| Vai trò | Trạng thái đơn | Tạo | Đọc | Sửa | Xóa |
|---|---|---|---|---|---|
| Nhân viên | Nháp | Tạo đơn mới với ngày và lý do | Chỉ đơn của mình | Sửa ngày, lý do | Hủy nháp (BR-007) |
| Nhân viên | Chờ duyệt | Bị chặn nếu trùng khoảng ngày (BR-009) | Chỉ đơn của mình, thấy trạng thái Chờ duyệt | Không sửa được nội dung đơn đã gửi | Hủy được, phép không đổi (BR-004) |
| Nhân viên | Đã duyệt | Bị chặn nếu trùng khoảng ngày (BR-009) | Thấy số ngày đã trừ | Không sửa được | Bị chặn (BR-007) |
| Nhân viên | Đã từ chối | Tạo đơn mới cho cùng khoảng ngày | Thấy lý do từ chối | Không sửa được | Không xóa được |
| Nhân viên | Đã hủy | Tạo đơn mới cho cùng khoảng ngày | Thấy trạng thái Đã hủy | Không sửa được | Không xóa được |
| Nhân viên | Đã dùng đủ 12 ngày trong năm | Bị chặn (BR-011, BR-013) | Thấy 0 ngày còn lại | Không sửa được | Không xóa được |
| Quản lý trực tiếp | Chờ duyệt | Không tạo đơn thay nhân viên | Thấy đơn của nhân viên mình | Duyệt hoặc từ chối 1 lần (BR-002) | Không xóa được |
| Quản lý trực tiếp | Đã duyệt | – | Thấy đơn và số ngày đã trừ | Bị chặn (BR-002) | Không xóa được |
| Quản lý khác | Chờ duyệt | Không tạo đơn thay nhân viên | Bị chặn (BR-001) | Bị chặn (BR-001) | Không xóa được |
| Nhân sự | Mọi trạng thái | Không tạo đơn | Thấy đơn, báo cáo và nhật ký | Bị chặn (BR-015) | Không xóa được |

## Thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| Đơn nghỉ phép | Bản ghi một yêu cầu nghỉ gồm người gửi, ngày bắt đầu, ngày kết thúc, lý do và trạng thái. |
| Quỹ phép năm | Số ngày phép tối đa một nhân viên được hưởng trong một năm dương lịch, bằng 12 ngày làm việc. |
| Số ngày phép còn lại | Quỹ phép năm trừ tổng số ngày của các đơn đã được duyệt trong cùng năm. |
| Số ngày của đơn | Số ngày làm việc trong khoảng nghỉ, không tính thứ Bảy, Chủ Nhật và ngày lễ. |
| Ngày làm việc | Ngày từ thứ Hai đến thứ Sáu, không nằm trong lịch ngày lễ của công ty. |
| Quản lý trực tiếp | Người duy nhất được gán làm người duyệt cho một nhân viên. |
| Nhân sự (HR) | Vai trò chỉ đọc, xem báo cáo ngày phép và nhật ký, không tham gia duyệt đơn. |
| Nháp | Trạng thái đơn do nhân viên tạo nhưng chưa gửi. |
| Chờ duyệt | Trạng thái đơn đã gửi và đang chờ quản lý trực tiếp xử lý. |
| Đã duyệt | Trạng thái đơn được quản lý trực tiếp chấp thuận và đã trừ ngày phép. |
| Đã từ chối | Trạng thái đơn bị quản lý trực tiếp từ chối kèm lý do. |
| Đã hủy | Trạng thái đơn bị nhân viên hủy trước khi được duyệt. |

## Giả định

| ID | Giả định | Cơ sở trong đầu vào, hoặc ảnh hưởng nếu sai |
|---|---|---|
| A-01 | Đơn bị từ chối không làm thay đổi số ngày phép còn lại. | Đầu vào chỉ nêu việc trừ khi đơn được duyệt; nếu sai thì cần thêm bước hoàn phép khi từ chối và BR-004 đổi. |
| A-02 | Hệ thống chặn mọi trường hợp làm số ngày phép còn lại âm hoặc vượt mức 12 ngày trong năm. | Đầu vào nêu "trừ vào số ngày phép còn lại" và "tối đa 12 ngày một năm"; nếu cho phép vượt thì BR-005, BR-011, BR-013 và FR-004.AC3, FR-004.AC6 đổi thành cảnh báo. |
| A-03 | Nhân viên hủy được đơn ở trạng thái Nháp và Chờ duyệt, không hủy được đơn Đã duyệt. | Đầu vào không nêu quyền hủy; nếu cho hủy sau khi duyệt thì cần luồng hoàn phép và AC mới cho FR-006. |
| A-04 | Mỗi nhân viên có tối đa một quản lý trực tiếp trong hồ sơ; không có quản lý trực tiếp thì không gửi được đơn. | Đầu vào nêu "Quản lý trực tiếp duyệt"; nếu một nhân viên có nhiều quản lý thì BR-001, BR-016 và FR-003 đổi. |
| A-05 | Hệ thống chặn đơn trùng khoảng ngày với đơn đang Nháp, Chờ duyệt hoặc Đã duyệt của cùng nhân viên. | Đầu vào không nêu; nếu không chặn thì cần quy tắc ưu tiên khi hai đơn phủ cùng ngày và BR-009 bị bỏ. |
| A-06 | Đơn vị nghỉ nhỏ nhất là 1 ngày làm việc; chưa hỗ trợ nghỉ nửa ngày hoặc nghỉ theo giờ. | Đầu vào nêu "ngày làm việc"; nếu cần nửa ngày hoặc giờ thì thêm trường buổi và công thức trừ theo giờ cho FR-001, FR-002. |
| A-07 | Lý do từ chối là bắt buộc. | Đầu vào không nêu; nếu không bắt buộc thì bỏ FR-005.AC2 và BR-012. |
| A-08 | Thông báo gửi qua email và thông báo trong ứng dụng. | Đầu vào không nêu kênh; nếu chỉ dùng một kênh thì FR-007 giảm một AC. |
| A-09 | Mỗi đơn chỉ được trừ phép một lần, kể cả khi có nhiều lượt duyệt đồng thời. | Suy ra từ BR-003; nếu không bảo đảm thì NFR-002 không đạt. |
| A-10 | p95 ≤ 2 giây ở 200 người dùng đồng thời là mức chấp nhận cho NFR-001. | Đầu vào không nêu số; nếu mức này chưa đạt thì mục tiêu NFR-001 cần chốt lại. |
| A-11 | 0 lần trừ trùng là mức chấp nhận cho NFR-002. | Đầu vào không nêu số; nếu chấp nhận sai lệch thì NFR-002 cần ngưỡng khác. |
| A-12 | 100% yêu cầu không có quyền bị từ chối là mức chấp nhận cho NFR-003. | Đầu vào không nêu số; nếu có ngoại lệ cho nhân sự đọc dữ liệu thì phải ghi rõ phạm vi. |
| A-13 | Độ sẵn sàng ≥ 99,5% trong giờ hành chính theo tháng là mức chấp nhận cho NFR-004. | Đầu vào không nêu số; nếu ứng dụng cần chạy 24/7 thì mục tiêu tính lại. |
| A-14 | Lưu nhật ký ≥ 24 tháng là mức chấp nhận cho NFR-005. | Đầu vào không nêu số; nếu có yêu cầu lưu lâu hơn theo quy định nội bộ thì tăng mục tiêu. |
| A-15 | ≤ 4 bước và ≤ 2 phút để gửi một đơn là mức chấp nhận cho NFR-006. | Đầu vào không nêu số; nếu mức này chưa đạt thì cần chốt lại với chủ sản phẩm. |
| A-16 | Mức 12 ngày áp dụng cho mọi nhân viên, không phân biệt thâm niên hay loại hợp đồng. | Đầu vào nêu "tối đa 12 ngày một năm" không kèm ngoại lệ; nếu có ngoại lệ thì BR-013 cần bảng phân loại. |

## Câu hỏi mở

| ID | Câu hỏi | Người trả lời | Chặn |
|---|---|---|---|
| Q-01 | Ngày phép bị trừ ngay khi nhân viên gửi đơn (giữ chỗ) hay chỉ trừ khi quản lý duyệt? Nếu giữ chỗ thì đơn Chờ duyệt chiếm quỹ phép. | Chủ sản phẩm | FR-001, FR-004, FR-005, FR-006 |
| Q-02 | Phép dư của năm trước có chuyển sang năm sau không, và nếu có thì dùng đến ngày nào? | Trưởng phòng nhân sự | FR-002, FR-009 |
| Q-03 | Lịch ngày lễ và ngày làm việc đặc biệt của công ty lấy từ nguồn nào và ai cập nhật? | Trưởng phòng nhân sự | FR-001, FR-004 |
| Q-04 | Đơn nghỉ phép phải gửi trước ngày bắt đầu tối thiểu bao nhiêu ngày làm việc? | Trưởng phòng nhân sự | FR-001 |
| Q-05 | Nghỉ ốm và nghỉ đột xuất có dùng cùng luồng đơn và trừ cùng mức 12 ngày mỗi năm không? | Trưởng phòng nhân sự | FR-001, FR-002 |
| Q-06 | Khi quản lý trực tiếp vắng mặt hoặc đã nghỉ việc thì ai duyệt đơn đang chờ? | Trưởng phòng nhân sự | FR-004, FR-007 |
| Q-07 | Đơn đã duyệt muốn hủy hoặc đổi ngày thì ai được phép làm và số ngày phép hoàn lại theo quy tắc nào? | Trưởng phòng nhân sự và quản lý trực tiếp | FR-006, FR-002 |
| Q-08 | Quản lý có được tự duyệt đơn của chính mình không? | Trưởng phòng nhân sự | FR-004 |
| Q-09 | Thời gian duyệt trung bình hiện nay là bao nhiêu và ai chịu trách nhiệm cho chỉ số này sau khi phát hành tính năng? | Trưởng phòng nhân sự | FR-009 |
| Q-10 | Nhân viên vào giữa năm hoặc làm bán thời gian có được hưởng đủ 12 ngày hay tính theo tỉ lệ thời gian làm việc trong năm? | Trưởng phòng nhân sự | FR-001, FR-002, FR-009 |

## Bước tiếp theo

Brainstorm giải pháp với file này làm ngữ cảnh, sau đó lập kế hoạch triển khai.
