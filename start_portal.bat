@echo off
title Spread Love Foundation - LinkedIn Automation Portal
echo ========================================================
echo   Spread Love Foundation - LinkedIn Automation Hub
echo ========================================================
echo Starting local automation server at http://127.0.0.1:5050 ...
start http://127.0.0.1:5050
python -m uvicorn server:app --host 127.0.0.1 --port 5050 --app-dir "F:\Spread love\linkedin_automation"
pause
