# Decision record

- Shape chọn: workflow
- Commit hash: 0731dfe
- Run id dẫn chứng: benchmark.json (workflow, seeds 11/22/33/44/55)
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0.000000
- Cost per success (mô phỏng, VND): 27.86
- Crash safety: 20/20 (src/reports/crash.json)
- Secret leak / approval bypass: 0 leak, 0 bypass

## Vì sao shape này

Workflow đạt pass rate và pass^5 tuyệt đối trên cùng corpus và năm seed, đồng thời có cost/success thấp nhất trong benchmark. Đây là lựa chọn phù hợp khi ưu tiên tính ổn định, khả năng kiểm soát và chi phí.

## Có đáng đổi lấy multi-agent không

Không đổi shape được chọn trong setup này. Single cũng đạt 100% nhưng workflow có chi phí thấp hơn; orchestrator và swarm có chi phí cao hơn, còn swarm có một lỗi seed 55 và variance khác 0. Chỉ đổi khi task cần phân tích song song và lợi ích chất lượng vượt chi phí.

## Trace và bằng chứng

Trace ghi các quyết định, quote, trạng thái host và crash event cần thiết. Nhóm không ghi parent secret, raw headers, số điện thoại, địa chỉ, internal note hoặc tên hàng để giữ ranh giới bảo mật.

## Giới hạn

MockLLM không phải model sản xuất. Latency là `unavailable`; cost là số mô phỏng. Benchmark public không thay thế hidden grading.


