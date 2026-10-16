# Lab 5 — Reflection Answers

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest issues to fix were formatting errors reported by Flake8, such as missing newlines, trailing whitespace, and lines exceeding the recommended length. These required only small changes to the code. The hardest issues were improving exception handling, validating user input, and managing global variables because these changes required understanding the program's logic and ensuring that the existing functionality was preserved.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

During the analysis, Pylint reported warnings about the use of global variables, while Flake8 reported formatting issues. Bandit did not identify any security issues in the tested version. I did not confirm any false positives during this lab. In the final analysis, Pylint gave the code a score of 10.00/10, Bandit reported no security issues, and Flake8 produced an empty report. This showed me that static analysis tools help identify potential problems, although their findings should always be reviewed carefully.

### 3. How would you integrate static analysis tools into your actual software development workflow?

I would integrate Pylint, Bandit, and Flake8 into my regular development workflow. I would run them locally before committing code and configure them to run automatically through a continuous integration pipeline whenever code is pushed to GitHub or a pull request is created. This would help identify code quality, security, and formatting issues early, reduce debugging time, and maintain consistent coding standards across a project.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The fixes improved the readability, maintainability, and robustness of the program. Input validation helps prevent invalid meter readings, specific exception handling makes errors easier to diagnose, and proper file handling improves reliability when loading and saving meter data. Formatting corrections made the code more consistent and readable. The final analysis gave a Pylint score of 10.00/10, Bandit reported no security findings, and Flake8 produced an empty report, indicating no reported style violations.
