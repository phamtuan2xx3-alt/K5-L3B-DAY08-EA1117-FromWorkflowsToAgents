# Báo cáo cá nhân — 2A202603758_PhamMinhDuc

## 1. Thông tin thành viên

- Họ tên: Phạm Minh Đức
- MSSV: 2A202603758
- Email: minhpham141098@gmail.com
- GitHub: ducpham13

## 2. Phần việc phụ trách

Shape A `workflow` — `src/lab8/shapes/workflow.py`

## 3. Đóng góp cụ thể

- Commit `2910db0`: implement toàn bộ Shape A workflow theo 7 bước trong docstring
  - Bước 1: `get_claim_view` — đọc claim qua allowlist
  - Bước 2: thiếu `order_id` → `needs_info`, không ghi ledger
  - Bước 3: `lookup_order` với principal scope; không tìm thấy → `escalated`, trace không lộ PII
  - Bước 4–5: `compute_compensation` từ order row (không đọc số tiền từ ticket); quote = 0 → `denied`
  - Bước 6: gọi `durability.issue_refund` với full quote và `crash_at`; không bắt `InjectedCrash`
  - Bước 7: thành công → `resolved`; dùng `finish()` để tự lấy `refund_effects` và `committed_audit_count`

## 4. Bằng chứng

- Commit hash: `2910db0` trên nhánh `2A202603758_PhamMinhDuc`
- File: `src/lab8/shapes/workflow.py`

## 5. Công cụ AI đã dùng

Dùng Claude Code (claude-sonnet-4-6) để đọc các file tham chiếu (`swarm_reference.py`, `common.py`, `tools.py`, `durability.py`, `contracts.md`, `business_rules.md`) và sinh code workflow. Tự kiểm tra bằng cách đọc lại từng bước của code so với docstring và business rules, đảm bảo:
- Không lộ PII trong trace (chỉ log field đã qua allowlist)
- Truyền full quote vào host, không tự trừ phần đã hoàn
- Không bắt `InjectedCrash` để crash suite hoạt động đúng
- Dùng `finish()` thay vì tự điền `refund_effects`

## 6. Tự đánh giá

Đã hoàn thành Shape A workflow với logic đúng theo business rules. Các must-pass đã được xem xét kỹ: approval do host kiểm (không tự quyết), không lộ secret/PII trong trace, crash không tạo thêm refund vì `InjectedCrash` không bị bắt. Chưa chạy được test suite do môi trường thiếu dependency (`pyyaml`), cần setup venv đầy đủ để xác nhận xanh.
