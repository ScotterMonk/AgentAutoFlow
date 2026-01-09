# All modes

**Running Python commands in Windows PowerShell via execute_command**
When running complex Python one-liners on Windows PowerShell via execute_command, the terminal often doesn't capture or display output properly (commands complete with exit code 0 but show no output).
The solution is to redirect both stdout and stderr to a file, then read that file:
```
python -c "complex script here" > D:\test_output.txt 2>&1
type D:\test_output.txt
```