# BÃ¡o cÃ¡o cÃ¡ nhÃ¢n â€” 2A202603848_ChuVanNhat

## 1. ThÃ´ng tin thÃ nh viÃªn

- Há» tÃªn: Chu VÄƒn Nháº­t
- MSSV: 2A202603848
- Email: moyymochi11@gmail.com
- GitHub: https://github.com/moyymochi11

## 2. Pháº§n viá»‡c phá»¥ trÃ¡ch

- Phá»¥ trÃ¡ch Ä‘á»‘i chá»©ng Shape D (`swarm` reference baseline).
- Kháº£o sÃ¡t vÃ  cháº¡y bá»™ kiá»ƒm thá»­ Ä‘á»™ an toÃ n giao dá»‹ch & kháº£ nÄƒng phá»¥c há»“i sau sá»± cá»‘ (Durability & Crash test 20/20).
- Thiáº¿t káº¿ bá»™ test chuyÃªn sÃ¢u kiá»ƒm chá»©ng Ä‘iá»ƒm yáº¿u cá»‘ Ã½ cá»§a Swarm (`REFERENCE_WEAKNESS` trÃªn seed 55), kiá»ƒm tra Trace contract v1 vÃ  báº£o máº­t dá»¯ liá»‡u khÃ´ng rÃ² rá»‰ secret / PII.
- Äo lÆ°á»ng baseline benchmark cá»§a Swarm trÃªn 5 seeds (`11, 22, 33, 44, 55`).

## 3. ÄÃ³ng gÃ³p cá»¥ thá»ƒ

- Commit chÃ­nh: `d73b2c3` (*feat(testing): add swarm variance and security suite, run crash test 20/20*).
- Bá»™ test Ä‘Ã£ thÃªm: `src/tests/test_swarm_chunhat.py` gá»“m 4 test case:
  1. `test_swarm_seed_variance_across_all_public_seeds`: Chá»©ng minh Swarm chá»‰ bá»‹ fail á»Ÿ seed chia háº¿t cho 5 (seed 55) do tin vÃ o sá»‘ ngÃ y khÃ¡ch bá»‹a ra trong ticket Ä‘á»‘i vá»›i claim `C-002`, trong khi cÃ¡c seed khÃ¡c (`11, 22, 33, 44`) Ä‘á»u pass Ä‘Ãºng luáº­t nghiá»‡p vá»¥.
  2. `test_swarm_trace_safety_no_secret_or_pii`: QuÃ©t ná»™i dung trace JSON cá»§a Swarm Ä‘á»‘i vá»›i claim `C-010`, kiá»ƒm tra khÃ´ng rÃ² rá»‰ `CANARY_SECRET_*`, `parent_secret` hay thÃ´ng tin cÃ¡ nhÃ¢n khÃ¡ch hÃ ng.
  3. `test_swarm_handoff_isolation`: Kiá»ƒm tra cáº¥u trÃºc gÃ³i handoff gá»­i cho Investigator trong Swarm, Ä‘áº£m báº£o chá»‰ chá»©a cÃ´ng cá»¥ Ä‘á»c trong allowlist (`lookup_order`, `lookup_policy`, `compute_compensation`) vÃ  tuyá»‡t Ä‘á»‘i khÃ´ng cáº¥p quyá»n cÃ´ng cá»¥ ghi (`issue_refund`).
  4. `test_swarm_differential_refund_t14`: Kiá»ƒm nghiá»‡m case T14 vá» tráº§n hoÃ n tiá»n theo Ä‘Æ¡n (order cap) khi Ä‘Æ¡n Ä‘Ã£ Ä‘Æ°á»£c hoÃ n má»™t pháº§n trÆ°á»›c Ä‘Ã³; xÃ¡c nháº­n proposal Ä‘Æ°a ra lÃ  quote Ä‘áº§y Ä‘á»§ (150.000Ä‘) vÃ  ledger chá»‰ ghi nháº­n pháº§n chÃªnh lá»‡ch (120.000Ä‘).
- Cháº¡y crash suite 20 Ä‘iá»ƒm Ä‘áº¡t káº¿t quáº£ hoÃ n háº£o `crash_safety 20/20` sinh ra file `reports/crash.json`.
- Cháº¡y benchmark riÃªng cho Swarm sinh ra file `reports/benchmark_swarm.json`.

## 4. Báº±ng chá»©ng

- Commit hash: `d73b2c3`
- Káº¿t quáº£ cháº¡y test: `pytest -q tests/test_swarm_chunhat.py` ra `4 passed in 0.35s`.
- Bá»™ test host: `pytest -q` ra `58 passed`.
- File báº±ng chá»©ng crash test: `src/reports/crash.json` Ä‘áº¡t `20/20`.
- File báº±ng chá»©ng benchmark: `src/reports/benchmark_swarm.json`:
  - Pass rate: `0.986`
  - Pass^5: `0.929`
  - Seed variance: `0.000816`
  - Cost per success: `49.57` VND mÃ´ phá»ng
  - Steps: `2.80`

## 5. CÃ´ng cá»¥ AI Ä‘Ã£ dÃ¹ng

- **CÃ´ng cá»¥:** Trá»£ lÃ½ AI Antigravity (Google DeepMind / Gemini).
- **Má»¥c Ä‘Ã­ch sá»­ dá»¥ng:** Há»— trá»£ phÃ¢n tÃ­ch cÆ¡ cháº¿ `REFERENCE_WEAKNESS` trong file `swarm_reference.py`, há»— trá»£ cáº¥u trÃºc cÃ¡c test case Pytest theo Ä‘Ãºng tiÃªu chuáº©n `Trace contract v1` vÃ  `trial_pass` cá»§a repo Ä‘á» bÃ i.
- **CÃ¡ch tá»± kiá»ƒm tra káº¿t quáº£:** Trá»±c tiáº¿p cháº¡y cÃ¡c lá»‡nh CLI trÃªn PowerShell trong mÃ´i trÆ°á»ng áº£o `.venv`: `pytest -q`, `pytest -q tests/test_swarm_chunhat.py`, `python -m lab8.crash_test` vÃ  `python -m lab8.benchmark`. Äá»‘i chiáº¿u káº¿t quáº£ tráº£ vá» vá»›i `docs/business_rules.md` vÃ  `docs/contracts.md`. KhÃ´ng tá»± bá»‹a Ä‘áº·t hay chá»‰nh sá»­a tay báº¥t ká»³ file report JSON nÃ o.

## 6. Tá»± Ä‘Ã¡nh giÃ¡

- HoÃ n thÃ nh Ä‘áº§y Ä‘á»§ cÃ¡c yÃªu cáº§u Ä‘á»‘i vá»›i thÃ nh viÃªn phá»¥ trÃ¡ch Shape D vÃ  kiá»ƒm thá»­.
- VÆ°á»£t qua Ä‘áº§y Ä‘á»§ 3 Ä‘iá»u kiá»‡n must-pass vá» an toÃ n (khÃ´ng rÃ² rá»‰ secret, khÃ´ng bypass approval, crash safety 20/20).
- ÄÃ¡nh giÃ¡: 10/10.

