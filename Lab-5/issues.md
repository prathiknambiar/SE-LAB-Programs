# Lab 5 — Static Code Analysis Issues

**Student:** PES2UG24CS371  
**Assigned repository:** https://github.com/SETAPESU26/L5_03_energy_tariff  
**Source file:** `energy_system.py`

> Line numbers below refer to the original starter file from the assigned repository. Confirm exact tool messages and line numbers by running Pylint, Bandit, and Flake8 locally.

| Issue | Type / severity | Original line(s) | Description | Fix approach |
|---|---|---:|---|---|
| Unsafe `eval()` on user input | Security / High | 428 | Evaluating an expression supplied by a user can execute arbitrary Python code. | Replaced `eval()` with `float()` conversion and handled invalid input. |
| Broad bare exception | Reliability | 395–397 | `except:` hides unrelated failures and makes debugging difficult. | Handle `FileNotFoundError` separately and log/re-raise JSON and I/O errors. |
| Mutable default argument | Bug risk | 341 | `history=[]` reuses the same list between calls, so readings can leak across calls. | Removed the mutable default; the cleaned function updates the meter store directly. |
| Unvalidated negative readings | Logic / data integrity | 413, 426–428 | Negative usage can reduce a meter total and produce misleading bills. | Validate meter ID and require a non-negative numeric reading. |
| File handling without context managers | Reliability / style | 392–393, 401–405 | Files may not be closed reliably if an error occurs. | Use `with open(...)` and UTF-8 encoding for loading and saving JSON. |
| Missing main guard | Maintainability | 436 | Importing the module runs the demonstration and prompts for input. | Put execution behind `if __name__ == "__main__":`. |
| Unused import / poor formatting and output style | Style | 326–328, throughout | `sys` is unused; blank lines and older `%` formatting reduce consistency. | Remove unused import, use consistent spacing and logging with format placeholders. |
| Missing meter lookup validation | Bug / robustness | 351 | An unknown meter ID raises an unhelpful `KeyError` during bill calculation. | Check meter existence and raise a descriptive `KeyError`. |

## Verification record

Run the commands below in the repository after replacing `energy_system.py` with the cleaned version. Save the real output in the report files; do not claim a score or zero warnings unless the tools actually show it.

```bash
python -m venv venv
source venv/bin/activate       # Windows: venv\\Scripts\\activate
python -m pip install pylint bandit flake8
python energy_system.py
pylint energy_system.py
bandit -r energy_system.py
flake8 energy_system.py
```

Optional saved reports:

```bash
pylint energy_system.py > pylint_report.txt
bandit -r energy_system.py > bandit_report.txt
flake8 energy_system.py > flake8_report.txt
```
