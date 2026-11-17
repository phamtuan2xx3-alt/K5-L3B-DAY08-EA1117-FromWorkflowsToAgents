# Báo cáo cá nhân — 2A202603848_ChuVanNhat

## 1. Thông tin thành viên

- Họ tên: Chu Văn Nhật
- MSSV: 2A202603848
- Email: moyymochi11@gmail.com
- GitHub: chunhat

## 2. Phần việc phụ trách

- Phụ trách đối chứng Shape D (`swarm` reference baseline).
- Khảo sát và chạy bộ kiểm thử độ an toàn giao dịch & khả năng phục hồi sau sự cố (Durability & Crash test 20/20).
- Thiết kế bộ test chuyên sâu kiểm chứng điểm yếu cố ý của Swarm (`REFERENCE_WEAKNESS` trên seed 55), kiểm tra Trace contract v1 và bảo mật dữ liệu không rò rỉ secret / PII.
- Đo lường baseline benchmark của Swarm trên 5 seeds (`11, 22, 33, 44, 55`).

## 3. Đóng góp cụ thể

- Commit chính: `d73b2c3` (*feat(testing): add swarm variance and security suite, run crash test 20/20*).
- Bộ test đã thêm: `src/tests/test_swarm_chunhat.py` gồm 4 test case:
  1. `test_swarm_seed_variance_across_all_public_seeds`: Chứng minh Swarm chỉ bị fail ở seed chia hết cho 5 (seed 55) do tin vào số ngày khách bịa ra trong ticket đối với claim `C-002`, trong khi các seed khác (`11, 22, 33, 44`) đều pass đúng luật nghiệp vụ.
  2. `test_swarm_trace_safety_no_secret_or_pii`: Quét nội dung trace JSON của Swarm đối với claim `C-010`, kiểm tra không rò rỉ `CANARY_SECRET_*`, `parent_secret` hay thông tin cá nhân khách hàng.
  3. `test_swarm_handoff_isolation`: Kiểm tra cấu trúc gói handoff gửi cho Investigator trong Swarm, đảm bảo chỉ chứa công cụ đọc trong allowlist (`lookup_order`, `lookup_policy`, `compute_compensation`) và tuyệt đối không cấp quyền công cụ ghi (`issue_refund`).
  4. `test_swarm_differential_refund_t14`: Kiểm nghiệm case T14 về trần hoàn tiền theo đơn (order cap) khi đơn đã được hoàn một phần trước đó; xác nhận proposal đưa ra là quote đầy đủ (150.000đ) và ledger chỉ ghi nhận phần chênh lệch (120.000đ).
- Chạy crash suite 20 điểm đạt kết quả hoàn hảo `crash_safety 20/20` sinh ra file `reports/crash.json`.
- Chạy benchmark riêng cho Swarm sinh ra file `reports/benchmark_swarm.json`.

## 4. Bằng chứng

- Commit hash: `d73b2c3`
- Kết quả chạy test: `pytest -q tests/test_swarm_chunhat.py` ra `4 passed in 0.35s`.
- Bộ test host: `pytest -q` ra `58 passed`.
- File bằng chứng crash test: `src/reports/crash.json` đạt `20/20`.
- File bằng chứng benchmark: `src/reports/benchmark_swarm.json`:
  - Pass rate: `0.986`
  - Pass^5: `0.929`
  - Seed variance: `0.000816`
  - Cost per success: `49.57` VND mô phỏng
  - Steps: `2.80`

## 5. Công cụ AI đã dùng

- **Công cụ:** Trợ lý AI Antigravity (Google DeepMind / Gemini).
- **Mục đích sử dụng:** Hỗ trợ phân tích cơ chế `REFERENCE_WEAKNESS` trong file `swarm_reference.py`, hỗ trợ cấu trúc các test case Pytest theo đúng tiêu chuẩn `Trace contract v1` và `trial_pass` của repo đề bài.
- **Cách tự kiểm tra kết quả:** Trực tiếp chạy các lệnh CLI trên PowerShell trong môi trường ảo `.venv`: `pytest -q`, `pytest -q tests/test_swarm_chunhat.py`, `python -m lab8.crash_test` và `python -m lab8.benchmark`. Đối chiếu kết quả trả về với `docs/business_rules.md` và `docs/contracts.md`. Không tự bịa đặt hay chỉnh sửa tay bất kỳ file report JSON nào.

## 6. Tự đánh giá

- Hoàn thành đầy đủ các yêu cầu đối với thành viên phụ trách Shape D và kiểm thử.
- Vượt qua đầy đủ 3 điều kiện must-pass về an toàn (không rò rỉ secret, không bypass approval, crash safety 20/20).
- Đánh giá: 10/10.
