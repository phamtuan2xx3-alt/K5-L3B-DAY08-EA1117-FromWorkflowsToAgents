# Research card

| Field | Nhóm điền |
| --- | --- |
| CÂU | R4 · Evaluation confounders |
| SOURCE | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency*; bằng chứng benchmark public trong `src/reports/benchmark.json` |
| CLAIM | So sánh các topology chỉ có ý nghĩa khi model, tool, seed, corpus, pricing và evaluator được giữ cố định. |
| BOUNDARY | Chỉ áp dụng cho MockLLM, 14 public claims, 5 seed và pricing hiện tại của lab; không suy rộng thành model production. |
| HYPOTHESIS | Khi giữ nguyên model, tool, seed, corpus và evaluator, workflow sẽ có pass rate tương đương nhưng cost/success thấp hơn orchestrator và swarm. |
| METHOD | Chạy `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`; chỉ thay shape. |
| FAILURE / METRIC | Đo pass rate, pass^5, seed variance và cost/success; kiểm tra thêm crash safety và secret leak. |

## Kết quả ablation

- Lệnh đã chạy: `python -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json`
- Run id / file report: `src/reports/benchmark.json`
- Kết quả: workflow/single/orchestrator đạt pass rate 1.000; swarm đạt 0.986, pass^5 0.929, variance 0.000816. Workflow có cost/success 27.86 VND, thấp hơn single 28.64, orchestrator 47.28 và swarm 49.57.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`.
