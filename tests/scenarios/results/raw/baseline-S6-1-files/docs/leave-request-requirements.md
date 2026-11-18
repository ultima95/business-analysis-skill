# Yêu cầu chức năng: Đăng ký nghỉ phép

- Trạng thái: Đã chốt quyết định nghiệp vụ, sẵn sàng triển khai
- Phạm vi: Backend + API (UI chỉ mô tả ở mức luồng)
- Ngôn ngữ tài liệu: Tiếng Việt
- Phiên bản: v2

## 0. Quyết định nghiệp vụ đã chốt

| # | Quyết định | Hệ quả kỹ thuật |
|---|---|---|
| D1 | Nghỉ phép tính theo **ngày làm việc**, bỏ cuối tuần và ngày lễ | Hàm tính ngày phải đọc lịch lễ; không cho đơn 0 ngày |
| D2 | Tối đa **12 ngày/năm** cho phép năm | Cap cứng 12 ở cả cấp phát lẫn số dư khả dụng |
| D3 | **Quản lý trực tiếp** duyệt, **một cấp duy nhất** | Không duyệt cấp 2, không uỷ quyền, không fallback HR |
| D4 | **HR chỉ xem báo cáo**, không thao tác nghiệp vụ | HR là vai trò chỉ đọc: không duyệt, không sửa, không điều chỉnh số dư |
| D5 | Cấp đủ 12 ngày đầu kỳ, **không mang sang năm sau** | Không có carry-over; hết kỳ phần dư về 0 |
| D6 | Không cho số dư âm | Mọi yêu cầu vượt số dư bị chặn ở 409 |

Tài liệu này là nguồn sự thật duy nhất khi triển khai. Nếu có mâu thuẫn nội bộ, D1–D6 thắng.

## 1. Mục tiêu

Cho phép nhân viên tự gửi yêu cầu nghỉ phép, quản lý trực tiếp duyệt hoặc từ chối, và hệ thống
tự động trừ số ngày phép còn lại (tối đa 12 ngày/năm) khi yêu cầu được duyệt.

Tiêu chí thành công:

1. Nhân viên gửi được yêu cầu nghỉ và thấy trạng thái xử lý.
2. Quản lý trực tiếp duyệt/từ chối được, có ghi nhận người duyệt và thời điểm duyệt.
3. Số dư phép luôn khớp: không âm, không bị trừ hai lần, không bị trừ khi bị từ chối.
4. Không năm nào vượt quá 12 ngày phép năm đã dùng.
5. Mọi thay đổi số dư truy vết được (ai, khi nào, do yêu cầu nào).
6. HR xem được báo cáo nghỉ phép mà không có quyền sửa dữ liệu.

## 2. Thuật ngữ

| Thuật ngữ | Nghĩa |
|---|---|
| Nhân viên (employee) | Người gửi yêu cầu nghỉ |
| Quản lý (manager) | Quản lý trực tiếp của nhân viên; người duyệt duy nhất |
| Loại phép (leave type) | Phép năm, nghỉ ốm, nghỉ không lương |
| Số dư (balance) | Số ngày phép còn lại của một nhân viên theo một loại phép trong một kỳ |
| Kỳ phép (leave year) | 01/01–31/12 (cố định ở v1) |
| Ngày làm việc | Ngày không phải cuối tuần (T7, CN) và không phải ngày lễ trong lịch công ty |
| Cap | Giới hạn 12 ngày/năm áp cho phép năm |
| Hold | Số ngày đã bị giữ chỗ cho yêu cầu đang chờ duyệt |

## 3. Vai trò và quyền

| Vai trò | Quyền |
|---|---|
| Employee | Tạo, xem, sửa, huỷ yêu cầu của chính mình; xem số dư của mình |
| Manager | Xem và duyệt/từ chối yêu cầu của nhân viên trực thuộc; xem số dư của họ |
| HR | **Chỉ đọc**: xem báo cáo toàn công ty, xem chi tiết đơn, xuất dữ liệu. Không duyệt, không sửa, không điều chỉnh số dư |
| Admin | Cấu hình loại phép, lịch lễ, chính sách; quản lý tài khoản và quan hệ quản lý–nhân viên |
| System | Trừ/hoàn số dư, gửi thông báo, ghi audit log |

Quy tắc phân quyền:

- Nhân viên không được duyệt yêu cầu của chính mình, kể cả khi họ là manager.
- Manager chỉ duyệt được yêu cầu của nhân viên có `manager_id` trỏ tới mình (đúng một cấp).
- HR gọi bất kỳ endpoint ghi nào → `403 FORBIDDEN_ROLE`. Có test riêng cho ràng buộc này.
- Nhân viên chưa được gán quản lý trực tiếp không thể submit → `409 NO_MANAGER_ASSIGNED`,
  hướng dẫn liên hệ admin. Không có đường vòng HR duyệt.

## 4. Phạm vi

### Trong phạm vi

- Tạo/sửa/huỷ yêu cầu nghỉ phép.
- Luồng duyệt một cấp bởi quản lý trực tiếp.
- Cap 12 ngày/năm cho phép năm.
- Giữ chỗ số dư khi chờ duyệt, trừ thật khi duyệt, hoàn khi từ chối/huỷ.
- Xem số dư và lịch sử biến động số dư.
- Báo cáo chỉ đọc cho HR.
- Thông báo in-app cho các sự kiện chính.
- Audit log cho mọi thao tác làm thay đổi trạng thái hoặc số dư.

### Ngoài phạm vi

- Duyệt nhiều cấp, duyệt song song, uỷ quyền duyệt, fallback HR duyệt.
- Duyệt một phần (nghỉ 5 ngày, duyệt 3 ngày).
- HR điều chỉnh số dư thủ công; mang phép sang năm sau.
- Chấm công, tính lương, tích hợp bảng lương.
- Nghỉ theo giờ lẻ ngoài mốc nửa ngày; đơn nghỉ bù/tăng ca.
- Email/push/SMS; đồng bộ calendar; mobile app riêng.
- Đa công ty/đa pháp nhân.

## 5. Luồng nghiệp vụ

### 5.1 Trạng thái yêu cầu

```
DRAFT ──submit──> PENDING ──approve──> APPROVED
                    │  │
                    │  └──reject──> REJECTED
                    └──cancel────> CANCELLED
APPROVED ──cancel (trước ngày bắt đầu)──> CANCELLED
```

| Trạng thái | Ý nghĩa | Số dư |
|---|---|---|
| DRAFT | Nháp, chỉ chủ sở hữu thấy | Không ảnh hưởng |
| PENDING | Đã gửi, chờ quản lý trực tiếp duyệt | Bị hold |
| APPROVED | Đã duyệt | Bị trừ thật |
| REJECTED | Bị từ chối | Hold được giải phóng |
| CANCELLED | Bị huỷ (trước khi duyệt, hoặc sau khi duyệt nhưng trước ngày bắt đầu) | Hoàn lại tương ứng |

Chuyển trạng thái không hợp lệ trả `409 CONFLICT`, không im lặng bỏ qua. Không trạng thái nào
cho phép HR can thiệp.

### 5.2 Luồng chính

1. Nhân viên chọn loại phép, ngày bắt đầu, ngày kết thúc, (tuỳ chọn) buổi bắt đầu/kết thúc, lý do.
2. Hệ thống tính số ngày nghỉ thực tế (chỉ đếm ngày làm việc, trừ ngày lễ, hỗ trợ nửa ngày).
3. Hệ thống kiểm tra cap 12 ngày/năm (với phép năm) và số dư khả dụng.
4. Nhân viên gửi → `PENDING`, số dư bị hold, thông báo cho quản lý trực tiếp.
5. Quản lý trực tiếp duyệt → `APPROVED`, hold thành trừ thật, thông báo cho nhân viên.
6. Quản lý trực tiếp từ chối (lý do bắt buộc) → `REJECTED`, hold giải phóng, thông báo nhân viên.

### 5.3 Huỷ

- `PENDING` → `CANCELLED`: nhân viên tự huỷ, giải phóng hold.
- `APPROVED` → `CANCELLED`: chỉ khi ngày bắt đầu còn ở tương lai; hoàn đúng số ngày đã trừ.
- `APPROVED` đã bắt đầu hoặc đã qua: không cho huỷ qua API. Không có đường điều chỉnh thủ công ở v1.

## 6. Quy tắc nghiệp vụ

### 6.1 Tính số ngày nghỉ

- Chỉ đếm ngày làm việc: bỏ Thứ 7, Chủ nhật và ngày lễ trong lịch công ty.
- Hỗ trợ nửa ngày (0.5): buổi sáng (`AM`) hoặc buổi chiều (`PM`), chỉ ở ngày đầu và/hoặc ngày cuối
  của đơn; không áp dụng cho ngày giữa.
- Đơn vị số dư là ngày, bước nhảy 0.5.
- `end_date >= start_date`; tổng phải > 0.
- Đơn nửa ngày sáng và nửa ngày chiều cùng một ngày là hai đơn chồng lấn (xem LR-05), không được
  gộp thành 1 ngày trong một đơn.
- Khoảng chọn chỉ gồm ngày không làm việc → `422 NO_WORKING_DAYS`.

### 6.2 Cap 12 ngày/năm

- Phép năm (`ANNUAL`) có entitlement tối đa **12 ngày** mỗi kỳ.
- Kiểm tra tại thời điểm submit **và** lúc approve (dữ liệu có thể đổi giữa hai bước):

```
used_in_period(ANNUAL) + held_in_period(ANNUAL) + total_days(request) <= 12
```

- Vi phạm → `409 ANNUAL_LEAVE_CAP_EXCEEDED`.
- `granted_days` của phép năm luôn bị giới hạn ≤ 12; seed/migration không được tạo giá trị lớn hơn.
- Nhân viên vào giữa năm: entitlement = `round_half_up(12 * số_tháng_còn_lại / 12)`, tối thiểu 0.5,
  tối đa 12. Ví dụ vào 01/07 → 6 ngày.
- Nghỉ ốm và nghỉ không lương **không** trừ vào 12 ngày phép năm và không bị cap.

### 6.3 Kiểm tra hợp lệ

| Mã | Điều kiện | Kết quả |
|---|---|---|
| LR-01 | Thiếu loại phép / ngày bắt đầu / ngày kết thúc | 422 `VALIDATION_ERROR` |
| LR-02 | `end_date < start_date` | 422 `INVALID_DATE_RANGE` |
| LR-03 | Tổng ngày nghỉ = 0 sau khi trừ cuối tuần/lễ | 422 `NO_WORKING_DAYS` |
| LR-04 | Số dư khả dụng < tổng ngày xin nghỉ | 409 `INSUFFICIENT_BALANCE` |
| LR-05 | Chồng lấn với đơn `PENDING`/`APPROVED` khác của cùng nhân viên | 409 `OVERLAPPING_REQUEST` |
| LR-06 | `start_date` ở quá khứ | 422 `PAST_DATE_NOT_ALLOWED` |
| LR-07 | Vi phạm báo trước tối thiểu (mặc định 0 ngày) | 422 `NOTICE_PERIOD_VIOLATION` |
| LR-08 | Vượt cap 12 ngày/năm của phép năm | 409 `ANNUAL_LEAVE_CAP_EXCEEDED` |
| LR-09 | Loại phép cần minh chứng (nghỉ ốm > 2 ngày) mà thiếu file | 422 `ATTACHMENT_REQUIRED` |
| LR-10 | Nhân viên chưa có quản lý trực tiếp | 409 `NO_MANAGER_ASSIGNED` |

Ghi chú:

- Chồng lấn xét giao khoảng ngày, không chỉ trùng ngày bắt đầu.
- Đơn `DRAFT`, `REJECTED`, `CANCELLED` không chặn đơn mới.
- Thứ tự kiểm tra cố định: LR-01 → LR-02 → LR-06/LR-07 → LR-03 → LR-05 → LR-10 → LR-08 → LR-04.
  Giữ nguyên thứ tự này để test ổn định và thông báo lỗi nhất quán.

### 6.4 Số dư và giữ chỗ

- Số dư khả dụng = `granted_days − used_days(APPROVED) − held_days(PENDING)`.
  Không có `adjustment` ở v1 vì HR không được chỉnh; `granted_days` do job cấp phép ghi.
- Hold phát sinh khi submit, giải phóng khi reject/cancel, chuyển thành `used` khi approve.
- Mọi thay đổi số dư nằm trong cùng transaction với thay đổi trạng thái yêu cầu.
- Khoá dòng số dư (`SELECT ... FOR UPDATE`) khi kiểm tra và cập nhật; khoá theo thứ tự
  `(employee_id, leave_type_id, period_start)` tăng dần để tránh deadlock.
- Approve/reject/cancel idempotent theo `(request_id, action, Idempotency-Key)`; gọi lại trả kết quả
  cũ, không sinh giao dịch sổ cái mới.
- Không có đường nào cập nhật trực tiếp `used_days`/`held_days` ngoài service xử lý transaction.

### 6.5 Cấp phép và chuyển kỳ

- Job đầu kỳ phép: phép năm `granted = 12` (hoặc pro-rata ở 6.2); loại khác `granted = 0` và không
  giới hạn, chỉ dùng khi phát sinh.
- Không mang phép sang năm sau: `granted`, `used`, `held` reset theo kỳ mới.
- Đơn `PENDING` vắt qua 31/12 bị `REJECTED` tự động khi job chạy, lý do `PERIOD_ROLLOVER`, hold kỳ
  cũ được giải phóng, nhân viên và quản lý nhận thông báo.
- Job cấp phép idempotent theo `(employee_id, leave_type_id, period_start)`: chạy lại không nhân đôi.
- Job đối soát hằng đêm: tổng sổ cái phải bằng `granted − used − held`; lệch thì alert.

### 6.6 Thông báo

| Sự kiện | Người nhận |
|---|---|
| Yêu cầu được gửi | Quản lý trực tiếp |
| Yêu cầu được duyệt | Nhân viên |
| Yêu cầu bị từ chối | Nhân viên |
| Yêu cầu bị huỷ khi đang PENDING | Quản lý trực tiếp |

Lỗi gửi thông báo không chặn giao dịch nghiệp vụ; retry tối đa 3 lần rồi ghi log.

## 7. Mô hình dữ liệu

### 7.1 `leave_types`

| Trường | Kiểu | Ghi chú |
|---|---|---|
| id | uuid | PK |
| code | string(32) | unique: `ANNUAL`, `SICK`, `UNPAID` |
| name | string(128) | |
| annual_cap_days | decimal(4,1) | `12` cho `ANNUAL`, `null` cho loại khác |
| requires_attachment | bool | |
| attachment_after_days | decimal(4,1) | null = luôn cần nếu `requires_attachment` |
| is_active | bool | |

### 7.2 `leave_balances`

| Trường | Kiểu | Ghi chú |
|---|---|---|
| id | uuid | PK |
| employee_id | uuid | FK |
| leave_type_id | uuid | FK |
| period_start | date | 01/01 |
| period_end | date | 31/12 |
| granted_days | decimal(4,1) | `<= 12` với `ANNUAL` |
| used_days | decimal(4,1) | tổng đơn `APPROVED` |
| held_days | decimal(4,1) | tổng đơn `PENDING` |
| updated_at | timestamp | |

Ràng buộc: unique `(employee_id, leave_type_id, period_start)`; `granted_days`, `used_days`,
`held_days` đều `>= 0`; với `ANNUAL` thêm check `used_days + held_days <= granted_days`.

### 7.3 `leave_requests`

| Trường | Kiểu | Ghi chú |
|---|---|---|
| id | uuid | PK |
| employee_id | uuid | FK, người xin nghỉ |
| manager_id | uuid | FK, người duyệt — chốt tại thời điểm submit |
| leave_type_id | uuid | FK |
| start_date | date | |
| end_date | date | |
| start_half | enum(`FULL`,`AM`,`PM`) | mặc định `FULL` |
| end_half | enum(`FULL`,`AM`,`PM`) | mặc định `FULL` |
| total_days | decimal(4,1) | server tính, bỏ qua giá trị client gửi |
| reason | text | bắt buộc với `UNPAID` |
| status | enum | `DRAFT`,`PENDING`,`APPROVED`,`REJECTED`,`CANCELLED` |
| submitted_at | timestamp | |
| decided_at | timestamp | |
| decided_by | uuid | quản lý đã quyết định |
| rejection_reason | text | bắt buộc khi `REJECTED` |
| cancelled_at | timestamp | |
| created_at / updated_at | timestamp | |

`total_days` tính lại mỗi lần tạo/sửa. `manager_id` lưu cứng để đổi quản lý sau đó không làm đổi
quyền duyệt của đơn đã gửi.

### 7.4 `leave_balance_transactions` (sổ cái, append-only)

| Trường | Kiểu | Ghi chú |
|---|---|---|
| id | uuid | PK |
| balance_id | uuid | FK |
| request_id | uuid | nullable (null khi cấp phép đầu kỳ) |
| type | enum | `GRANT`,`HOLD`,`RELEASE`,`DEDUCT`,`REFUND`,`RESET` |
| days | decimal(4,1) | dấu +/- theo nghĩa của `type` |
| actor_id | uuid | người dùng hoặc `system` |
| note | text | |
| created_at | timestamp | |

Số dư tổng hợp lại được từ sổ cái — dùng cho job đối soát.

### 7.5 `holidays`

| Trường | Kiểu | Ghi chú |
|---|---|---|
| id | uuid | PK |
| date | date | unique |
| name | string | |
| is_working_day | bool | ngày làm bù |

### 7.6 `leave_request_events` (audit)

`id, request_id, from_status, to_status, actor_id, actor_role, payload(jsonb), created_at`

Chỉ insert, không update/delete.

## 8. API

| Method | Path | Role | Mô tả |
|---|---|---|---|
| GET | `/api/leave-types` | mọi role | Loại phép đang hoạt động |
| GET | `/api/me/leave-balances?period=` | employee | Số dư của tôi |
| GET | `/api/me/leave-requests?status=&from=&to=` | employee | Đơn của tôi |
| POST | `/api/me/leave-requests` | employee | Tạo đơn; `submit=true` để gửi ngay |
| PATCH | `/api/leave-requests/{id}` | employee (chủ sở hữu) | Sửa khi `DRAFT`/`PENDING` |
| POST | `/api/leave-requests/{id}/submit` | employee (chủ sở hữu) | Gửi duyệt |
| POST | `/api/leave-requests/{id}/approve` | manager được gán | Duyệt |
| POST | `/api/leave-requests/{id}/reject` | manager được gán | Từ chối, body có `reason` |
| POST | `/api/leave-requests/{id}/cancel` | employee (chủ sở hữu) | Huỷ |
| GET | `/api/leave-requests/inbox` | manager | Đơn `PENDING` của nhân viên mình |
| GET | `/api/leave-requests/{id}` | owner / manager được gán / HR (đọc) | Chi tiết + lịch sử sự kiện |
| GET | `/api/reports/leave-balances?period=&department_id=` | HR | Báo cáo số dư: granted/used/held/remaining |
| GET | `/api/reports/leave-usage?from=&to=&group_by=department\|employee` | HR | Báo cáo sử dụng phép |
| GET | `/api/reports/leave-usage/export.csv` | HR | Xuất CSV cùng bộ lọc |

Chuẩn chung:

- Mọi mutation hỗ trợ `Idempotency-Key`.
- Lỗi: `{ error: { code, message, details } }`.
- Danh sách phân trang `limit`/`cursor`.
- Endpoint `/api/me/*` bỏ qua mọi `employee_id` client gửi; luôn lấy từ token.
- HR gọi endpoint ghi → `403 FORBIDDEN_ROLE`; HR không có route nào khác ngoài báo cáo và xem chi tiết.

## 9. Tiêu chí chấp nhận

1. Nhân viên có 12 ngày phép năm, gửi đơn 3 ngày làm việc, quản lý trực tiếp duyệt → còn 9 ngày;
   sổ cái có `HOLD 3`, `RELEASE 3`, `DEDUCT 3` nhất quán.
2. Nhân viên đã dùng 10 ngày, gửi đơn 3 ngày → `409 ANNUAL_LEAVE_CAP_EXCEEDED` (không phải lỗi
   thiếu số dư, vì cap kiểm tra trước).
3. Nhân viên đã dùng 2 ngày, còn 2 ngày, gửi đơn 3 ngày → bị chặn, không tạo đơn.
4. Quản lý trực tiếp từ chối đơn 3 ngày → số dư trở lại như trước, đơn `REJECTED` kèm lý do,
   sổ cái có `RELEASE`.
5. Hai đơn chờ duyệt giao nhau → đơn thứ hai `409 OVERLAPPING_REQUEST`.
6. Đơn Thứ Sáu → Thứ Hai có 1 ngày lễ → `total_days = 2`.
7. Đơn nửa ngày sáng ngày đầu + nửa ngày chiều ngày cuối trong 3 ngày làm việc → `total_days = 2`.
8. Đơn chỉ rơi vào Thứ Bảy, Chủ Nhật, ngày lễ → `422 NO_WORKING_DAYS`.
9. Gọi `approve` hai lần cùng idempotency key → chỉ một giao dịch `DEDUCT`.
10. Hai request đồng thời tiêu cùng số dư còn lại → đúng một thành công, cái kia
    `INSUFFICIENT_BALANCE`; số dư không âm, không vượt 12.
11. Nhân viên huỷ đơn `PENDING` → hold giải phóng ngay, quản lý nhận thông báo.
12. Nhân viên huỷ đơn `APPROVED` có ngày bắt đầu tương lai → hoàn đủ số ngày.
13. Nhân viên không phải quản lý của người gửi gọi `approve` → `403`.
14. Quản lý gọi `approve` trên đơn của chính mình → `403`.
15. HR gọi `POST /approve` → `403 FORBIDDEN_ROLE`; HR gọi `PATCH` đơn → `403`; HR gọi
    `GET /api/reports/leave-balances` → `200`.
16. Nhân viên chưa có quản lý trực tiếp submit → `409 NO_MANAGER_ASSIGNED`.
17. Nhân viên vào 01/07 → `granted_days = 6`; gửi đơn 7 ngày bị chặn cap.
18. Chạy job cấp phép hai lần → `granted_days` vẫn 12, không có `GRANT` trùng.
19. Đơn `PENDING` vắt qua 31/12 → `REJECTED` với lý do `PERIOD_ROLLOVER`, hold kỳ cũ giải phóng.
20. Mọi chuyển trạng thái và biến động số dư có mặt trong audit log với actor và thời điểm.
21. Job đối soát: tổng sổ cái bằng `granted − used − held` cho mọi dòng số dư.

## 10. Phi chức năng

- **Múi giờ**: lưu UTC; "hôm nay" và ngày nghỉ tính theo múi giờ công ty (`Asia/Ho_Chi_Minh`).
- **Hiệu năng**: `GET /api/me/leave-balances` p95 < 200ms với 5.000 nhân viên; báo cáo HR p95 < 2s
  với dữ liệu một năm.
- **Toàn vẹn**: không đường nào ghi `used_days`/`held_days` ngoài service xử lý transaction.
- **Bảo mật**: kiểm tra quyền ở service, không chỉ route; lọc dữ liệu theo actor, không tin
  `employee_id` từ client; HR chỉ đọc ở cả route và service.
- **Truy vết**: audit log giữ tối thiểu 2 năm; sổ cái giữ vĩnh viễn.
- **Migration**: seed 3 loại phép (`ANNUAL` cap 12, `SICK`, `UNPAID`), lịch lễ năm hiện tại, cấp số
  dư pro-rata cho nhân viên hiện có trước khi bật tính năng.
- **Quan sát**: metric `leave_balance_reconciliation_drift` phải bằng 0; alert khi khác 0.

## 11. Rủi ro và cách xử lý

| Rủi ro | Xử lý |
|---|---|
| Hai đơn tranh nhau số dư | Khoá dòng balance theo thứ tự cố định + transaction + kiểm tra lại trước commit |
| Duyệt hai lần do retry/double click | Idempotency key + kiểm tra trạng thái hiện tại |
| Lịch lễ đổi sau khi đơn đã duyệt | Không tính lại đơn đã duyệt; chỉ áp dụng cho đơn mới |
| Đổi quản lý khi đơn đang chờ | `manager_id` chốt lúc submit; quản lý mới không duyệt được đơn cũ |
| Không có HR điều chỉnh số dư | Mọi thay đổi đi qua đơn nghỉ + huỷ; sai sót xử lý bằng migration có audit, không bằng API |
| Sai lệch số dư do bug | Job đối soát hằng đêm từ sổ cái + alert drift |
| Nhân viên không có quản lý trực tiếp | Chặn submit với `NO_MANAGER_ASSIGNED`; admin phải gán quản lý trước |

## 12. Thứ tự triển khai

1. Schema, migration, seed loại phép/lịch lễ; backfill số dư pro-rata.
2. Service tính ngày nghỉ thuần (weekend, holiday, nửa ngày) + unit test đầy đủ.
3. Service số dư: hold/deduct/release, cap 12, idempotency + test concurrency.
4. API tạo/sửa/submit/cancel.
5. API approve/reject + phân quyền quản lý trực tiếp + chặn self-approve.
6. Job cấp phép đầu kỳ + xử lý đơn vắt qua năm + job đối soát.
7. Thông báo in-app + audit log.
8. Endpoint báo cáo HR (read-only) + xuất CSV.
