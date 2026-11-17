# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-TenNhom-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Chu Văn Nhật | 2A202603848 | moyymochi11@gmail.com | chunhat | Shape D & Evaluation Lead |
|   2 |        |      |       |        |         |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Chu Văn Nhật | Shape D & Evaluation Lead | d73b2c3 | tests/test_swarm_chunhat.py::test_swarm_seed_variance_across_all_public_seeds |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603848_ChuVanNhat

### Phần việc phụ trách

- Phụ trách đối chứng Shape D (Swarm), kiểm thử độ an toàn (Crash test 20/20) và đo lường baseline benchmark.

### Đóng góp cụ thể

- Commit d73b2c3: Bộ test `src/tests/test_swarm_chunhat.py` với 4 test case chuyên sâu cho Swarm, chạy crash suite 20/20 và benchmark baseline.

### Bằng chứng

- File test `src/tests/test_swarm_chunhat.py`, báo cáo cá nhân `report/team/2A202603848_ChuVanNhat.md`, các file `reports/crash.json` và `reports/benchmark_swarm.json`.
