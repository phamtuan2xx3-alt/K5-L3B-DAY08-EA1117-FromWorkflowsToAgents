# Báo cáo cá nhân — 2A202603894_NguyenMinhPhuc

## 1. Thông tin thành viên

- Họ tên: Nguyễn Minh Phúc
- MSSV: 2A202603894
- Email: nminhphuc.nmp0512@gmail.com
- GitHub: https://github.com/NgMinPhuc

## 2. Phần việc phụ trách

Shape C `orchestrator` (orchestrator + investigator chỉ đọc), file `src/lab8/shapes/orchestrator.py`, gồm phần CP2 (luồng xử lý claim) và CP3 (handoff, ledger, crash).

## 3. Đóng góp cụ thể

**Commit chính:** `feat/NgMinPhuc` — `feat(orchestrator): implement shape C (CP2, CP3)`

**Luồng xử lý của shape C:**

1. Orchestrator đọc claim qua `get_claim_view` (không `SELECT *`). Claim không tồn tại → `failed`; thiếu `order_id` → `needs_info`, không ghi ledger, không lấy mã đơn từ chữ trong ticket.
2. Dựng handoff bằng `lab8.handoff.make_handoff`: `facts` để rỗng, `allowed_tools` chỉ gồm 4 tool đọc `lookup_order`, `lookup_policy`, `lookup_refund_history`, `compute_compensation`. Không đưa `parent_secret`, header hay claim row vào handoff.
3. Investigator chạy qua `run_readonly_investigators`, không có tool ghi. Đơn không thấy hoặc principal không sở hữu đơn → `escalated`.
4. Quote do code tính (`compute_compensation`) từ dòng order trong DB; số ngày trễ ghi trong ticket bị bỏ qua. Quote = 0 → `denied`, không gọi host.
5. Orchestrator (không phải investigator) gọi `durability.issue_refund` với **quote đầy đủ** và `crash_at`; host tự trừ phần đã hoàn của đơn (T13, T14). `InjectedCrash` được ghi trace rồi ném lại, không bắt.
6. Mọi nhánh return đi qua `common.finish()`, nên `refund_effects`, `committed_audit_count` và trace luôn đúng contract.

**Quyết định kỹ thuật:**

- **Facts trong handoff để rỗng:** investigator tự đọc dữ liệu từ DB qua tool đọc, nên không có gì từ parent context phải chuyển qua ranh giới.
- **Trace chỉ ghi dữ liệu đã qua allowlist:** handoff đã sanitize, các field của `ORDER_FIELDS`, số tiền và lý do quote. Không ghi ticket, claim row hay order row thô.
- **Lỗi bất ngờ trả `failed`:** `error_reason` chỉ chứa tên loại exception để thông điệp lỗi không mang dữ liệu nhạy cảm ra trace; `InjectedCrash` thì vẫn ném lại.

**Test đã thêm hoặc sửa:** `/src/lab8/shapes/orchestrator.py`

## 4. Bằng chứng

- Ma trận student: `python -m pytest -q -m student -o addopts= -k orchestrator` → **62 passed**.
- Cổng host: `python -m pytest -q` → 54 passed, không có test fail.
- Crash rồi resume: `python -m lab8.run --shape orchestrator --claim-id C-012 --seed 11 --db data/crash.sqlite --crash-at after_effect_before_checkpoint` crash đúng điểm; chạy lại trên cùng DB → `resolved`, 1 dòng ledger 35.000, 1 audit `refund_committed`.
- Benchmark thử trên bộ public (14 claim × 5 seed `11,22,33,44,55`), chưa phải số chính thức trong `src/reports/benchmark.json`:

  | Shape | Pass | Pass^5 | Cost/success | Số bước TB |
  | --- | --- | --- | --- | --- |
  | orchestrator | 1.000 | 1.000 | 56.65 | 5.36 |
  | swarm | 0.986 | 0.929 | 49.57 | 2.80 |

- Quét 70 trace `traces/R-orchestrator-*.json`: không có `CANARY_SECRET_`, `parent_secret`, số điện thoại, địa chỉ, tên hàng hay internal note.

## 5. Công cụ AI đã dùng

- **Claude Code:** đọc đề bài và docs, viết `orchestrator.py` theo hướng dẫn trong docstring và [docs/contracts.md](../../docs/contracts.md).
- **Kiểm tra kết quả:**
  - Chạy ma trận student và cổng host.
  - Chạy crash rồi resume, kiểm tra trực tiếp bảng `refund_ledger` và `audit_events`.
  - Quét trace tìm secret và thông tin cá nhân.
  - Dựng thêm các tình huống giống bộ hidden (ticket nói dối, injection, approval mượn của claim khác, đơn đã hoàn, homoglyph, principal sai, crash ở 3 điểm) và đối chiếu với bảng trong [docs/business_rules.md](../../docs/business_rules.md).
- **Phần tự đọc và hiểu:** ranh giới host/shape (vì sao truyền quote đầy đủ, vì sao shape tự từ chối thì không có audit `policy_denied`) và allowlist của handoff.

## 6. Tự đánh giá

- **Đã làm được:** shape C qua toàn bộ test public và không lộ secret trong trace. Crash rồi resume vẫn chỉ ra một refund.
- **Đánh đổi:** orchestrator tốn hơn swarm khoảng 14% chi phí cho mỗi lần thành công và đi gần gấp đôi số bước, đổi lại ổn định trên cả 5 seed.
- **Giới hạn:** số liệu đo bằng MockLLM nên chưa phản ánh độ dao động của model thật. Kết quả trên bộ hidden 40 claim do giảng viên chấm.

