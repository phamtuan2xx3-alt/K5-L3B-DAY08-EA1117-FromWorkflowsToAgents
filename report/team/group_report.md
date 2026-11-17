# Báo cáo nhóm — Lab 8 LogiX-VN

## 1. Thông tin nhóm

- Tên nhóm: EA1117
- Lớp: L3B
- Thành viên: xem `TEAM.md`
- Commit chốt: 0731dfe

## 2. Mục tiêu và cách tiếp cận

Nhóm triển khai cùng một quy trình hoàn phí claim trên bốn shape, giữ cố định corpus, seed, pricing và evaluator. Phân công gồm workflow, single, orchestrator, swarm/evaluation và integration. Nhóm ưu tiên code kiểm soát tiền, approval, idempotency và bảo mật; model chỉ hỗ trợ đọc/suy luận và soạn kết quả.

## 3. Giải pháp

- **Workflow:** đọc claim/order/policy, tính quote bằng code rồi gọi host ghi refund.
- **Single:** agent ReAct tối đa 8 bước, chỉ gọi read tools; host kiểm tra quote và ghi refund.
- **Orchestrator:** tạo handoff allowlist cho investigator read-only; orchestrator giữ quyền gọi host.
- **Swarm:** shape tham chiếu dùng làm baseline và đối chứng chi phí/variance.

Tất cả shape truyền quote đầy đủ vào `durability.issue_refund`. Trace chỉ ghi event đã sanitize, quote, quyết định và crash; không ghi secret, raw ticket, PII hoặc internal fields.

## 4. Kết quả

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success (VND) | Mean/P95 steps |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 27.86 | 3.79 / 4.00 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 28.64 | 1.00 / 1.00 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 47.28 | 5.36 / 6.00 |
| swarm | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 2.80 / 3.00 |

Số liệu lấy từ `src/reports/benchmark.json`. Crash suite đạt **20/20** trong `src/reports/crash.json`. Workflow được chọn trong ADR vì đạt pass tuyệt đối với chi phí thấp nhất.

## 5. Khó khăn và cách xử lý

Các lỗi chính liên quan đến ticket không đáng tin, approval sai claim, trần refund theo order, retry/crash và trace có nguy cơ lộ secret. Nhóm xử lý bằng cách lấy dữ liệu từ order row, để host kiểm tra policy/approval/idempotency, truyền crash point xuống durability và dùng allowlist cho handoff/trace.

## 6. Tổng hợp đóng góp

Chi tiết nằm trong bảng đóng góp của `TEAM.md` và các báo cáo cá nhân trong `report/team/`.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất và latency là `unavailable`. Benchmark public không thay thế hidden grading. Có thể cải thiện bằng hidden evaluation, thêm test metamorphic và đo latency trên hệ thống thật.

## 8. Tài liệu tham khảo

- `README.md`, `RUBRIC.md`, `CHECKPOINTS.md`
- `docs/business_rules.md`, `docs/contracts.md`, `docs/architecture.md`, `docs/metrics.md`
- `report/team/decision_adr.md`, `report/team/research_card.md`


