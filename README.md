# ICAI e-Diary Automation

This Python automation script follows the exact workflow on the ICAI e-Services Portal (`https://eservices.icai.org`) using Selenium (latest version with built-in Selenium Manager - no external driver downloads required) and `tkinter` Always-On-Top GUIs.

## Features & Implementation Details

1. **Selenium Manager**: Uses Selenium 4.x built-in driver manager, automatically matching your installed Google Chrome browser without downloading `chromedriver.exe`.
2. **Tab Handling**: Switches automatically to the new tab opened by `<a class="btn-primary-sp3" ... target="_blank">Click Here</a>`.
3. **Smart Suffix Handling**: Automatically appends `@ICAI.ORG` to the SRO number if omitted.
4. **Login Error Detection**: Automatically checks `<span id="loginPwdMsg">` and pops up an Always-On-Top GUI error window if credentials are incorrect.
5. **Modal & Announcement Dismissal**: Auto-clicks the `<button class="primary_butn small less_width" data-dismiss="modal">Close</button>` modal upon login.
6. **Current Date Selection**: Automatically clicks `<span class="glyphicon glyphicon-calendar"></span>` and selects today's date from the datepicker.
7. **Always-On-Top GUI Interface**:
   - **Duration & Task Selection**: Lets you choose Duration (Full Day `1` or Half Day `0.5`) and Task (`T1` to `T18`) in a clean dialog.
   - **Subtasks Selection**: Extracts available subtasks dynamically from `#subTaskList` and allows selecting up to **5 subtasks maximum**.
   - **Other Task Prompt**: Asks *"Do you have an Other Task?"* with **Yes** and **No** buttons. If Yes, gives a text bar to type the work done and populates `<input id="other_task">`.
8. **Server Effort Error Alert**: Detects `<i id="responseDataBody">` (*"The duration of filled effort for the selected date should be either 1 full day or 2 half days"*), presents an Always-On-Top notice, and clicks the Close button.
9. **Save & Profile Logout**: Clicks Save (`#submitTaskData`), clicks Profile (`#dLabel`), and logs out (`logoutProfile()`).

## How to Run

1. Open `icai_ediary_automation.py`.
2. Enter your SRO number and password in the script:
   ```python
   USER_SRO = "SRO1234567"
   USER_PASSWORD = "YourActualPassword"
   ```
3. Run the script:
   ```powershell
   python "d:\My Projects\icai_ediary_automation.py"
   ```
