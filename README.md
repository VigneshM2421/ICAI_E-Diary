# ⚡ ICAI Articleship e-Diary RPA Automation

A secure, fully automated Python RPA solution for Chartered Accountancy (CA) students to record their daily articleship e-Diary entries on the official **ICAI e-Services Portal** (`eservices.icai.org`).

---

## 🌟 Key Features

- **No Passwords in Code (GitHub Safe)**: Your SRO and Password are never hardcoded in the Python source. When you run the application, enter your credentials in the GUI once; they are securely remembered locally on your computer in `.config_ediary.json` (protected by `.gitignore`).
- **All-in-One Pre-Run Master GUI**: Configure your daily logging details in a single **Always-On-Top** interface **before** the browser opens:
  - **Interactive Date Calendar**: Choose `Today` or pick any date with Day/Month/Year spinboxes or the built-in **`📅 Calendar View`** (a clickable visual monthly calendar grid).
  - **Effort Duration**: `Full Day (1)` or `Half Day (0.5)`.
  - **Official Subtasks Catalog**: Populates genuine, descriptive subtasks for every functional area (Assurance, Direct Tax, Indirect Tax, Auditing, Accounting, Compliance & Outsourcing, etc.) matching ICAI's practical training competency guidelines.
  - **Strict 5-Subtask Limit**: Enforces ICAI's 5-subtask rule with live counters and automatic warning guards.
  - **Other Task**: Optional text entry for custom work.
  - **Ultra-Smooth Mousewheel Scrolling**: Responsive scrolling across all cards and subtask boxes on Windows mice and precision laptop trackpads.
- **Guaranteed Portal Subtask Selection**: Uses native JavaScript dispatchers and jQuery triggers to check selected subtasks on the portal and verify their states before saving.
- **Central Telegram Bot Alerts (Zero Bot Creation Needed)**:
  - You do **NOT** need to create your own bot or get API tokens.
  - Uses the central alert bot **`@my_icai_alert_bot`**.
  - Just enter your personal **Chat ID** once, and you will receive an instant completion message on your phone every day:
    > *"✅ ICAI e-Diary Update Successful! The E-Diary is Updated Successfully for DD/MM/YYYY"*
- **`iframe#frame1` Navigation**: Handles internal frames where the modal, calendar, and task elements reside.
- **Selenium 4+ Auto-Manager**: No manual driver downloads (`chromedriver.exe`) required.

---

## 📱 How to Receive Mobile Alerts (1-Time Setup, 20 Seconds)

1. Open Telegram on your phone and search for **`@my_icai_alert_bot`** (or open [t.me/my_icai_alert_bot](https://t.me/my_icai_alert_bot)) and tap **Start**.
2. Search for **`@userinfobot`** on Telegram and tap **Start** to see your personal numeric `Id` (e.g. `123456789`).
3. Enter that numeric Chat ID in the automation GUI.
4. That's it! Every time you run the script, you'll receive your confirmation alert on Telegram.

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install selenium requests
```

### 2. Run the Script
```powershell
python icai_ediary_automation.py
```

### 3. Enter Your Details in the Master GUI
- Fill in your SRO, Password, and Telegram Chat ID.
- Choose your date (Today or click `📅 Calendar View` to pick a custom date).
- Select your Task and check up to 5 Subtasks.
- Click **`▶ START AUTOMATION & UPDATE E-DIARY`**.

The script will launch the browser, log in, switch into `iframe#frame1`, close the announcement popup, apply your date, duration, task, and checked subtasks, save, log out, close Chrome, and send your Telegram completion confirmation!

---

## 🔒 Privacy & Security

- Credentials and Chat IDs are saved strictly on your local computer in `.config_ediary.json`.
- `.gitignore` ensures that `.config_ediary.json` is never tracked or pushed to GitHub.
