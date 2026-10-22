Set WshShell = CreateObject("WScript.Shell")
' Run uvicorn server completely silently with pythonw (no terminal window)
WshShell.Run "C:\Users\Admin\AppData\Local\Programs\Python\Python312\pythonw.exe -m uvicorn server:app --host 127.0.0.1 --port 5050 --app-dir ""F:\Spread love\linkedin_automation""", 0, False
