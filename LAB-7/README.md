# L6_L7_27 — Traffic Fine Calculator

Lab 7: Fuzz Testing

## About

A small Python module that parses traffic ticket details, totals fines and measures how far over the limit a driver was.

## Files

| File | Description |
|------|-------------|
| `traffic_fine.py` | The code under test |
| `test_traffic_fine.py` | Starter test file |

Refer to the lab handout for instructions.

## Lab 7 submission (Leesha R)

| Path | Contents |
|------|----------|
| `traffic_fine.py` | Fixed code (input validation; returns `None` for invalid input) |
| `test_traffic_fine.py` | 19 Hypothesis fuzz/property tests covering all three functions |
| `requirements.txt` | `hypothesis`, `pytest` |
| `screenshots/` | Terminal captures: original run, failing tests, fixed run, passing tests |
| `evidence/` | Original buggy code and full plain-text logs of every run |
| `report/Lab7_Fuzz_Testing_Report_Leesha_R.pdf` | Final report |

Run:

```bash
pip install -r requirements.txt
python traffic_fine.py
python -m pytest -v test_traffic_fine.py
```
