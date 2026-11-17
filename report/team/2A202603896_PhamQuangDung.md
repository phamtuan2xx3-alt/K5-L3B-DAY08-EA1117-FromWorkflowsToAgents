# Báo cáo cá nhân — 2A202603896_PhamQuangDung

## 1. Thông tin thành viên

- Họ tên: Phạm Quang Dũng
- MSSV: 2A202603896
- Email: phamquangdung188@gmail.com
- GitHub: https://github.com/quanggpham

## 2. Phần việc phụ trách

Shape C `orchestrator` (`src/lab8/shapes/orchestrator.py`): orchestrator đọc claim, dựng handoff theo allowlist, giao cho investigator chỉ có tool đọc, rồi tự gọi `durability.issue_refund`. Kèm theo là bộ test ranh giới bảo mật của shape C (`src/tests/test_orchestrator_boundary.py`).

## 3. Đóng góp cụ thể

Commit chính (nhánh `phamquangdung`):

- `1dc1e83` `feat(shapes): implement orchestrator with read-only investigator`
- `d7b428e` `test(shapes): cover orchestrator handoff and trace boundary`

Test đã thêm: `src/tests/test_orchestrator_boundary.py`, 32 test, gắn marker `student`:

- `test_trace_has_no_secret_pii_or_ticket`: với mọi claim public, trace và `RunResult` không chứa `CANARY_SECRET_`, `parent_secret`, header, nội dung ticket, hay phone, địa chỉ, internal note, tên hàng của bất kỳ đơn nào.
- `test_handoff_is_allowlisted_and_read_only`: mỗi lần chạy có đúng một handoff; key nằm trong `ALLOWED_FIELDS`, tool nằm trong `READONLY_TOOLS`, `facts` rỗng.
- `test_ticket_delay_never_overrides_order_row`: C-002 (ticket ghi trễ 5 ngày, order row ghi 2 ngày) ra `denied` ở cả 5 seed, kể cả seed 55 là seed swarm trả nhầm.

Quyết định kỹ thuật:

1. **Ranh giới code / model.** Số tiền do `compute_compensation` tính; investigator chỉ đọc. Chỉ orchestrator (code) gọi `issue_refund`. MockLLM được gọi đúng một lần với `purpose="draft"` để soạn câu trả lời; prompt chỉ có `claim_id` và số đề xuất, không có ticket.
2. **Handoff với `facts={}`.** Investigator tự đọc order qua `lookup_order`, và tool này đã kiểm principal sở hữu đơn. Vì vậy orchestrator không cần chuyển dữ kiện nào. Ticket, `principal_id`, `parent_secret` và `raw_headers` không bao giờ vào handoff. Dùng allowlist trong code (`make_handoff`) chứ không dùng tóm tắt bằng LLM, vì tóm tắt không phải là redaction.
3. **Không tin chữ trong ticket.** `order_id` chỉ lấy từ cột của claim; số ngày trễ chỉ lấy từ order row. Shape C không có đoạn `REFERENCE_WEAKNESS` như swarm.
4. **Truyền quote đầy đủ vào `issue_refund`.** Host tự trừ phần đơn đã được hoàn (T13, T14). Nếu shape tự trừ trước, host sẽ trừ lần hai. `proposal_amount` luôn là quote đầy đủ.
5. **Crash.** `crash_at` được truyền thẳng vào `issue_refund`. Khi gặp `InjectedCrash`, shape ghi trace rồi raise lại, không nuốt lỗi; khi chạy lại, idempotency key `refund:{claim_id}` giữ đúng một refund (T12).
6. **Trace cố ý không ghi:** claim row, ticket, `principal_id`, `parent_secret`, `raw_headers`, và các cột phone/address/internal_note/item_name của order. Trace chỉ ghi handoff đã sanitize, order view đã qua allowlist của `lookup_order`, quote, kết quả host và quyết định cuối.
7. **Bỏ `lookup_refund_history` khỏi investigator.** Bản đầu có gọi tool này nhưng kết quả không dùng cho quyết định nào, vì host đã tự trừ phần đã hoàn. Bỏ đi giảm cost/success khi chạy thử trên bộ public (16 claim × 5 seed) từ 56.57 xuống 47.28, trong khi test vẫn xanh.

## 4. Bằng chứng

Chạy trong `src/` với Python 3.13:

| Lệnh | Kết quả |
|---|---|
| `python -m lab8.smoke` | `lab8.smoke pass` |
| `python -m pytest -q` | 54 passed |
| `python -m pytest -q -m student -o addopts= -k orchestrator` | 94 passed (62 test ma trận T01–T14, T11, T12 và 32 test ranh giới) |

Benchmark chạy thử (`--shapes orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55`), output ra file tạm, không phải `src/reports/benchmark.json` chính thức:

| Shape | pass | pass^5 | variance | cost/success |
|---|---|---|---|---|
| orchestrator | 1.000 | 1.000 | 0 | 47.28 |
| swarm | 0.986 | 0.929 | 0.000816 | 49.57 |

Số chính thức và run id lấy từ `src/reports/benchmark.json` của nhóm, ghi trong `report/team/decision_adr.md`.

## 5. Công cụ AI đã dùng

- **Claude (Claude Code):** đọc và giải thích đề bài, đề xuất chia vai; hỗ trợ viết code, test
- **Cách tự kiểm tra:**
  - Chạy cổng host, ma trận student của orchestrator và test ranh giới; các kết quả ở mục 4.
  - Quét toàn bộ trace `traces/R-orchestrator-*` để chắc không còn `CANARY_SECRET` hay field PII.
  - Chạy benchmark so với swarm để kiểm pass rate và cost.
  - Đọc lại từng nhánh return trong code và đối chiếu với bảng output contract.

## 6. Tự đánh giá

...
