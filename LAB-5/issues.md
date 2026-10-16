# Static Code Analysis Report

## 1. Initial Findings

The initial Pylint score was **5.47/10**. Bandit reported four potential security issues, and Flake8 reported four formatting violations. The line numbers below refer to the original, unmodified `address_book.py`.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Weak MD5 hashing (B324) | Security - High | 19 | MD5 was used to generate contact identifiers. | Replaced MD5 with SHA-256. |
| Unsafe pickle deserialization (B301) | Security - Medium | 67 | `pickle.load()` can execute unsafe operations when loading untrusted data. | Replaced pickle-based backup and restore with JSON. |
| Broad exception handling (W0718) | Code quality | 34 | Catching `Exception` can hide unexpected errors. | Caught the specific `KeyError` instead. |
| Missing documentation (C0114, C0116) | Code quality | 1, 10-70 | The module and functions lacked docstrings. | Added module and function docstrings. |
| Naming conventions (C0103) | Code quality | 10-70 | Function names and arguments used camelCase instead of snake_case. | Renamed functions and arguments to snake_case. |
| Inefficient iteration (C0200) | Code quality | 49 | The directory loop used `range()` with `len()`. | Used `enumerate()` for directory numbering. |
| Missing file encoding (W1514) | Code quality | 54 | A file was opened without an explicit encoding. | Specified UTF-8 encoding for text file operations. |
| Importing pickle (B403) | Security - Low | 3 | The program imported the pickle module. | Removed pickle and used JSON for backups. |
| Hardcoded password-like value (B105) | Security - Low | 6 | An unused password-like constant was present in the source. | Removed the unused constant. |
| Whitespace and line-length violations (E225, E303, E231, E501) | Formatting | 23, 47, 84-85 | Flake8 identified spacing, blank-line and line-length problems. | Corrected whitespace, blank lines and long lines. |

## 2. Improvements Made

- Added module and function docstrings.
- Renamed functions and arguments to use snake_case.
- Replaced broad exception handling with specific KeyError handling.
- Used enumerate() for directory numbering.
- Specified UTF-8 encoding for file operations.
- Replaced pickle backup and restore with JSON.
- Removed the unused hardcoded password-like constant.
- Replaced MD5 with SHA-256 for generating contact identifiers.
- Corrected the formatting violations reported by Flake8.

## 3. Before-and-After Results

| Tool | Before | After |
|---|---|---|
| Pylint | 5.47/10 | 10.00/10 |
| Bandit | 4 findings | 0 findings |
| Flake8 | 4 violations | 0 violations |

## 4. Conclusion

Static code analysis helped identify code-quality, naming, formatting and security concerns. After the fixes, the program ran successfully, the JSON backup was restored correctly, and all three analysis tools reported clean results.
