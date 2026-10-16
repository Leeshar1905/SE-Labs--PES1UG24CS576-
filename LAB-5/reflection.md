# Reflection on Static Code Analysis

This lab helped me understand how static code analysis tools identify code-quality, formatting and security issues.

Pylint highlighted problems with naming conventions, missing docstrings, exception handling and iteration. Flake8 identified formatting violations, while Bandit highlighted potentially unsafe deserialization and weak hashing.

I improved the code by following Python naming conventions, adding documentation, correcting formatting, and replacing pickle-based backups with JSON. I also replaced MD5 with SHA-256 for contact identifiers.

The final Pylint score improved from 5.47/10 to 10/10. Bandit reported no issues, and Flake8 reported no violations. Running the program confirmed that the contact search, city grouping and backup restoration still worked.

I learned that static analysis is useful for finding problems early, but the program must also be executed and tested to check its behavior.
