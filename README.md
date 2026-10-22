# Spread Love Foundation - LinkedIn Automation Portal 🌱

## Overview
Automated system to convert **Spread Love Foundation**'s Instagram posts (`@spreadlove2030`) into professional, high-impact LinkedIn thought-leadership articles and automatically observe key **Environmental, Nature, Climate & Health Days**.

- **Instagram**: [https://www.instagram.com/spreadlove2030](https://www.instagram.com/spreadlove2030)
- **LinkedIn Profile**: [https://www.linkedin.com/in/spread-love-foundation-394085418](https://www.linkedin.com/in/spread-love-foundation-394085418)

---

## Features

1. **Environmental & Health Days Calendar (`special_days.json`)**:
   - Covers 25+ global and national observances (World Health Day, World Environment Day, Earth Day, World Water Day, Van Mahotsav, National Pollution Control Day, etc.).
   - Automatically detects today's date or allows 1-click selection of upcoming dates.

2. **Instagram ➔ LinkedIn Converter (`post_generator.py`)**:
   - Takes short Instagram captions, seed-ball activities, afforestation drives, or lake restoration summaries.
   - Automatically rewrites them with professional hooks, impact metrics, UN SDG tags (SDG 6, 13, 15, 17), and CSR collaboration call-to-actions.

3. **Human-in-the-Loop Review & Approval (`server.py`)**:
   - Complete visual dashboard on `http://127.0.0.1:5050`.
   - Realistic LinkedIn preview card.
   - 1-Click **"Approve & Post on LinkedIn"** opens LinkedIn share composer pre-copied with the approved text.

---

## How to Run

### Option 1: Web Portal (Recommended)
Double click `start_portal.bat` or run:
```bash
python -m uvicorn server:app --host 127.0.0.1 --port 5050 --app-dir "F:\Spread love\linkedin_automation"
```
Then visit **`http://127.0.0.1:5050`** in your browser.

### Option 2: Terminal / Console Runner
```bash
python "F:\Spread love\linkedin_automation\daily_runner.py"
```
