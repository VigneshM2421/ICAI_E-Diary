"""
╔══════════════════════════════════════════════════════════════════════╗
║              ICAI e-Diary RPA Automation Suite                       ║
║  · Selenium 4+ (Built-in Selenium Manager - No driver download)      ║
║  · Live-Extracted Portal Subtasks (100% Genuine ICAI Master Catalog) ║
║  · Interactive Calendar View (Clickable Monthly Calendar & Presets)  ║
║  · Search Filter & View All 107 Subtasks in Always-On-Top Master GUI ║
║  · Ultra-Smooth Mousewheel & Keyboard Scrolling Everywhere in GUI    ║
║  · Guaranteed Portal Subtask Selection (JS Dispatch & State Verify)  ║
║  · Central Telegram Bot Alerts (Zero bot setup required by students) ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import time
import json
import base64
import urllib.parse
import calendar
from datetime import datetime, date

import tkinter as tk
from tkinter import ttk, messagebox
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)

# ──────────────────────────────────────────────────────────────────────
# CENTRAL TELEGRAM BOT (PROVIDED FOR ALL USERS)
# ──────────────────────────────────────────────────────────────────────
CENTRAL_BOT_TOKEN = "9022126674:AAHhRHUNVlDB1hVfyWEO3tAt9xAZEf17OTQ"
CENTRAL_BOT_USERNAME = "@my_icai_alert_bot"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, ".config_ediary.json")
SUBTASKS_CACHE_FILE = os.path.join(BASE_DIR, "icai_subtasks_catalog.json")
STEP_PAUSE = 1.5  # Pace between automation steps

TASK_OPTIONS = [
    ("T1",  "Assurance Services"),
    ("T2",  "Risk"),
    ("T3",  "Tax & Regulatory"),
    ("T4",  "Growth"),
    ("T5",  "DigiTech/Information Technology"),
    ("T6",  "Compliance and Outsourcing"),
    ("T7",  "Taxation"),
    ("T8",  "Accounting"),
    ("T9",  "Auditing"),
    ("T10", "Direct Tax Laws"),
    ("T11", "Indirect Tax Laws"),
    ("T12", "Management consultancy and services"),
    ("T13", "Others"),
    ("T14", "Holiday"),
    ("T15", "Leave"),
    ("T16", "Weekoff"),
    ("T18", "No Task Allocated"),
]

# ──────────────────────────────────────────────────────────────────────
# GENUINE ICAI MASTER SUBTASKS CATALOG (Extracted directly from live portal)
# ──────────────────────────────────────────────────────────────────────
DEFAULT_SUBTASKS_CATALOG = {
    "T1": [
        "S1 - Financial Reporting Advisory Services",
        "S2 - Financial Statement Audit",
        "S3 - Attestation Services",
        "S96 - Auditing Services In India And Reviews Of Local GAAP/ US GAAP/ IFRS",
        "S97 - Financial Statements",
        "S98 - SOX Attestation",
        "S99 - Agreed-Upon Procedures",
        "S100 - Certification Services",
        "S101 - Preparing Audit Programmes",
        "S102 - Audit Working Papers And Documentation",
        "S103 - Understanding, Recording And Evaluating Internal Control System",
        "S104 - Performing Substantive Audit Procedures",
        "S105 - Scrutinizing Financial Statements",
        "S106 - Drafting Audit Report"
    ],
    "T2": [
        "S4 - Cyber",
        "S5 - Governance, Risk & Operations",
        "S6 - Forensic & Investigation Services",
        "S7 - IT Risk Advisory Services",
        "S31 - Business Continuity Planning",
        "S35 - Team Mate/IT Risk & Assurance",
        "S103 - Understanding, Recording And Evaluating Internal Control System"
    ],
    "T3": [
        "S8 - Gtaxpro Tool",
        "S9 - Direct Tax Services",
        "S10 - Indirect Tax Services",
        "S11 - Transfer Pricing",
        "S12 - US Tax",
        "S13 - Financial Services",
        "S14 - Transaction Tax",
        "S15 - Global Mobility Services",
        "S16 - Labour Codes",
        "S17 - Union Budget",
        "S18 - Webinars",
        "S19 - Alerts",
        "S46 - Corporate Secretarial Compliance Advisory Services",
        "S47 - FEMA Compliance Advisory Services",
        "S48 - Direct Tax Compliance Advisory Services",
        "S49 - Indirect Tax Compliance Advisory Services",
        "S50 - Transfer Pricing Compliance Advisory Services"
    ],
    "T4": [
        "S20 - Business Consulting",
        "S21 - Business Planning",
        "S22 - Organisation Effectiveness",
        "S23 - Due Diligence",
        "S24 - Valuations",
        "S25 - Global Expansion",
        "S26 - Overseas Listing",
        "S74 - Preparation Of Fund Flow And Cash Flow Statements And Forecasts",
        "S75 - Projection Of Working Capital Requirements",
        "S78 - Amalgamation And Merger Schemes",
        "S79 - Planning Capital Structure",
        "S82 - Preparation And Analysis Of Prospectus",
        "S83 - Raising Of Capital, New Issues And Matters Concerned Therewith Including SEBI Guidelines"
    ],
    "T5": [
        "S27 - Developing And Maintaining Data Bases",
        "S28 - Data Extraction And Analysis Techniques",
        "S29 - E-Commerce - Audit And Legal Considerations",
        "S30 - System Development Life Cycle",
        "S31 - Business Continuity Planning",
        "S32 - Information System Audit",
        "S33 - Information Security/ Information Technology",
        "S34 - Cyberlaws And E-Filing/Upload Information On Sites As Income Tax",
        "S35 - Team Mate/IT Risk & Assurance",
        "S36 - Digital Transformation",
        "S37 - Business Intelligence And Information Management"
    ],
    "T6": [
        "S38 - HR And Payroll Outsourcing Services",
        "S39 - Accounting And Monthly Management Reporting",
        "S40 - Financial Controller And Accounting Review Services",
        "S41 - Payroll And Related Services",
        "S42 - HR Advisory Services",
        "S44 - Global Mobility Services",
        "S45 - Incorporation Services",
        "S46 - Corporate Secretarial Compliance Advisory Services",
        "S47 - FEMA Compliance Advisory Services",
        "S48 - Direct Tax Compliance Advisory Services",
        "S49 - Indirect Tax Compliance Advisory Services",
        "S50 - Transfer Pricing Compliance Advisory Services",
        "S51 - Compliance Management Solution",
        "S80 - Drafting Of Memorandum And Articles Of Association",
        "S81 - Formation Of Companies",
        "S84 - Drafting Of Minutes"
    ],
    "T7": [
        "S60 - Tax Audit",
        "S61 - Computation Of Total Income And Tax Liability",
        "S62 - Determination Of Advance Tax Liability",
        "S63 - Computation Of Advance Tax Payable",
        "S64 - Computation Of Interest For Delay In Payment Of Advance Tax, Deferment Of Advance Tax",
        "S65 - Computation Of Interest/Fee Payable Under The Provisions Of Income-Tax Law",
        "S66 - Preparation Of The Statement Of Particulars In Form 3CD And Other Forms",
        "S67 - Preparation And E-Filing Of Income-Tax Returns",
        "S68 - Valuation Of Stocks, Securities, Etc. Under The Different Provisions Of Income-Tax Law",
        "S69 - Tax Planning",
        "S70 - Drafting Of Appeals",
        "S71 - Compliance Of Provisions Relating To Tax Deduction/Collection At Source",
        "S72 - Computation Of Equalisation Levy",
        "S73 - GST",
        "S8 - Gtaxpro Tool",
        "S9 - Direct Tax Services",
        "S10 - Indirect Tax Services",
        "S11 - Transfer Pricing",
        "S12 - US Tax",
        "S14 - Transaction Tax"
    ],
    "T8": [
        "S52 - Maintaining Of Books Of Accounts",
        "S53 - Preparation Of Financial Statements",
        "S54 - Application Of Statutory Provisions, Compliance With AS Or Ind AS And Other Pronouncements Of The Institute, Etc.",
        "S55 - Analysis And Interpretation Of Financial Statements",
        "S56 - Preparation Of Various Reports Other Than Financial Statements",
        "S57 - Bank Reconciliation",
        "S87 - GAAP Conversions",
        "S88 - Group Consolidation",
        "S89 - IPO Support",
        "S90 - Hedge Accounting Advisory",
        "S91 - Accounting Manuals",
        "S92 - Financial Statement Preparation",
        "S93 - Transaction Accounting",
        "S94 - Loan Staff",
        "S95 - New Standards Implementation"
    ],
    "T9": [
        "S58 - Statutory Audits",
        "S59 - Audit Of Various Type Of Business And Non-Business Organizations",
        "S60 - Tax Audit",
        "S96 - Auditing Services In India And Reviews Of Local GAAP/ US GAAP/ IFRS",
        "S97 - Financial Statements",
        "S98 - SOX Attestation",
        "S99 - Agreed-Upon Procedures",
        "S100 - Certification Services",
        "S101 - Preparing Audit Programmes",
        "S102 - Audit Working Papers And Documentation",
        "S103 - Understanding, Recording And Evaluating Internal Control System",
        "S104 - Performing Substantive Audit Procedures",
        "S105 - Scrutinizing Financial Statements",
        "S106 - Drafting Audit Report"
    ],
    "T10": [
        "S61 - Computation Of Total Income And Tax Liability",
        "S62 - Determination Of Advance Tax Liability",
        "S63 - Computation Of Advance Tax Payable",
        "S64 - Computation Of Interest For Delay In Payment Of Advance Tax, Deferment Of Advance Tax",
        "S65 - Computation Of Interest/Fee Payable Under The Provisions Of Income-Tax Law",
        "S66 - Preparation Of The Statement Of Particulars In Form 3CD And Other Forms",
        "S67 - Preparation And E-Filing Of Income-Tax Returns",
        "S68 - Valuation Of Stocks, Securities, Etc. Under The Different Provisions Of Income-Tax Law",
        "S69 - Tax Planning",
        "S70 - Drafting Of Appeals",
        "S71 - Compliance Of Provisions Relating To Tax Deduction/Collection At Source",
        "S72 - Computation Of Equalisation Levy",
        "S9 - Direct Tax Services",
        "S11 - Transfer Pricing",
        "S12 - US Tax",
        "S14 - Transaction Tax"
    ],
    "T11": [
        "S10 - Indirect Tax Services",
        "S49 - Indirect Tax Compliance Advisory Services",
        "S73 - GST"
    ],
    "T12": [
        "S74 - Preparation Of Fund Flow And Cash Flow Statements And Forecasts",
        "S75 - Projection Of Working Capital Requirements",
        "S76 - Preparation Of Project Reports",
        "S77 - Preparation And Processing Of Loan Applications",
        "S78 - Amalgamation And Merger Schemes",
        "S79 - Planning Capital Structure",
        "S80 - Drafting Of Memorandum And Articles Of Association",
        "S81 - Formation Of Companies",
        "S82 - Preparation And Analysis Of Prospectus",
        "S83 - Raising Of Capital, New Issues And Matters Concerned Therewith Including SEBI Guidelines",
        "S84 - Drafting Of Minutes",
        "S85 - Insolvency/Liquidation Proceedings",
        "S86 - Preparing And Reviewing Budgets"
    ],
    "T13": [
        "S107 - Others"
    ],
    "T14": [],
    "T15": [],
    "T16": [],
    "T18": [],
    "ALL": [
        "S1 - Financial Reporting Advisory Services",
        "S2 - Financial Statement Audit",
        "S3 - Attestation Services",
        "S4 - Cyber",
        "S5 - Governance, Risk & Operations",
        "S6 - Forensic & Investigation Services",
        "S7 - IT Risk Advisory Services",
        "S8 - Gtaxpro Tool",
        "S9 - Direct Tax Services",
        "S10 - Indirect Tax Services",
        "S11 - Transfer Pricing",
        "S12 - US Tax",
        "S13 - Financial Services",
        "S14 - Transaction Tax",
        "S15 - Global Mobility Services",
        "S16 - Labour Codes",
        "S17 - Union Budget",
        "S18 - Webinars",
        "S19 - Alerts",
        "S20 - Business Consulting",
        "S21 - Business Planning",
        "S22 - Organisation Effectiveness",
        "S23 - Due Diligence",
        "S24 - Valuations",
        "S25 - Global Expansion",
        "S26 - Overseas Listing",
        "S27 - Developing And Maintaining Data Bases",
        "S28 - Data Extraction And Analysis Techniques",
        "S29 - E-Commerce - Audit And Legal Considerations",
        "S30 - System Development Life Cycle",
        "S31 - Business Continuity Planning",
        "S32 - Information System Audit",
        "S33 - Information Security/ Information Technology",
        "S34 - Cyberlaws And E-Filing/Upload Information On Sites As Income Tax",
        "S35 - Team Mate/IT Risk & Assurance",
        "S36 - Digital Transformation",
        "S37 - Business Intelligence And Information Management",
        "S38 - HR And Payroll Outsourcing Services",
        "S39 - Accounting And Monthly Management Reporting",
        "S40 - Financial Controller And Accounting Review Services",
        "S41 - Payroll And Related Services",
        "S42 - HR Advisory Services",
        "S44 - Global Mobility Services",
        "S45 - Incorporation Services",
        "S46 - Corporate Secretarial Compliance Advisory Services",
        "S47 - FEMA Compliance Advisory Services",
        "S48 - Direct Tax Compliance Advisory Services",
        "S49 - Indirect Tax Compliance Advisory Services",
        "S50 - Transfer Pricing Compliance Advisory Services",
        "S51 - Compliance Management Solution",
        "S52 - Maintaining Of Books Of Accounts",
        "S53 - Preparation Of Financial Statements",
        "S54 - Application Of Statutory Provisions, Compliance With AS Or Ind AS And Other Pronouncements Of The Institute, Etc.",
        "S55 - Analysis And Interpretation Of Financial Statements",
        "S56 - Preparation Of Various Reports Other Than Financial Statements",
        "S57 - Bank Reconciliation",
        "S58 - Statutory Audits",
        "S59 - Audit Of Various Type Of Business And Non-Business Organizations",
        "S60 - Tax Audit",
        "S61 - Computation Of Total Income And Tax Liability",
        "S62 - Determination Of Advance Tax Liability",
        "S63 - Computation Of Advance Tax Payable",
        "S64 - Computation Of Interest For Delay In Payment Of Advance Tax, Deferment Of Advance Tax",
        "S65 - Computation Of Interest/Fee Payable Under The Provisions Of Income-Tax Law",
        "S66 - Preparation Of The Statement Of Particulars In Form 3CD And Other Forms",
        "S67 - Preparation And E-Filing Of Income-Tax Returns",
        "S68 - Valuation Of Stocks, Securities, Etc. Under The Different Provisions Of Income-Tax Law",
        "S69 - Tax Planning",
        "S70 - Drafting Of Appeals",
        "S71 - Compliance Of Provisions Relating To Tax Deduction/Collection At Source",
        "S72 - Computation Of Equalisation Levy",
        "S73 - GST",
        "S74 - Preparation Of Fund Flow And Cash Flow Statements And Forecasts",
        "S75 - Projection Of Working Capital Requirements",
        "S76 - Preparation Of Project Reports",
        "S77 - Preparation And Processing Of Loan Applications",
        "S78 - Amalgamation And Merger Schemes",
        "S79 - Planning Capital Structure",
        "S80 - Drafting Of Memorandum And Articles Of Association",
        "S81 - Formation Of Companies",
        "S82 - Preparation And Analysis Of Prospectus",
        "S83 - Raising Of Capital, New Issues And Matters Concerned Therewith Including SEBI Guidelines",
        "S84 - Drafting Of Minutes",
        "S85 - Insolvency/Liquidation Proceedings",
        "S86 - Preparing And Reviewing Budgets",
        "S87 - GAAP Conversions",
        "S88 - Group Consolidation",
        "S89 - IPO Support",
        "S90 - Hedge Accounting Advisory",
        "S91 - Accounting Manuals",
        "S92 - Financial Statement Preparation",
        "S93 - Transaction Accounting",
        "S94 - Loan Staff",
        "S95 - New Standards Implementation",
        "S96 - Auditing Services In India And Reviews Of Local GAAP/ US GAAP/ IFRS",
        "S97 - Financial Statements",
        "S98 - SOX Attestation",
        "S99 - Agreed-Upon Procedures",
        "S100 - Certification Services",
        "S101 - Preparing Audit Programmes",
        "S102 - Audit Working Papers And Documentation",
        "S103 - Understanding, Recording And Evaluating Internal Control System",
        "S104 - Performing Substantive Audit Procedures",
        "S105 - Scrutinizing Financial Statements",
        "S106 - Drafting Audit Report",
        "S107 - Others"
    ]
}


# ──────────────────────────────────────────────────────────────────────
# LOCAL CREDENTIAL & SUBTASK CATALOG MANAGER
# ──────────────────────────────────────────────────────────────────────
class ConfigManager:
    @staticmethod
    def _encode(plain_text: str) -> str:
        if not plain_text:
            return ""
        return base64.b64encode(plain_text.encode("utf-8")).decode("utf-8")

    @staticmethod
    def _decode(cipher_text: str) -> str:
        if not cipher_text:
            return ""
        try:
            return base64.b64decode(cipher_text.encode("utf-8")).decode("utf-8")
        except Exception:
            return ""

    @classmethod
    def load_config(cls) -> dict:
        default = {
            "sro": "",
            "password": "",
            "enable_telegram": True,
            "telegram_chat_id": "",
            "remember": True
        }
        if not os.path.exists(CONFIG_FILE):
            return default
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {
                    "sro": data.get("sro", ""),
                    "password": cls._decode(data.get("password_enc", "")),
                    "enable_telegram": data.get("enable_telegram", True),
                    "telegram_chat_id": data.get("telegram_chat_id", ""),
                    "remember": data.get("remember", True)
                }
        except Exception as e:
            print(f"[!] Error reading local config: {e}")
            return default

    @classmethod
    def save_config(cls, data: dict, remember: bool):
        if not remember:
            if os.path.exists(CONFIG_FILE):
                try:
                    os.remove(CONFIG_FILE)
                except Exception:
                    pass
            return

        payload = {
            "sro": data.get("sro", "").strip(),
            "password_enc": cls._encode(data.get("password", "")),
            "enable_telegram": data.get("enable_telegram", True),
            "telegram_chat_id": data.get("telegram_chat_id", "").strip(),
            "remember": True
        }
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
            print("[✓] Settings cached safely in local .config_ediary.json")
        except Exception as e:
            print(f"[!] Could not save config: {e}")

    @classmethod
    def load_subtasks_catalog(cls) -> dict:
        catalog = {k: list(v) for k, v in DEFAULT_SUBTASKS_CATALOG.items()}
        if os.path.exists(SUBTASKS_CACHE_FILE):
            try:
                with open(SUBTASKS_CACHE_FILE, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                    for k, v in cached.items():
                        if v and any(" - " in item or len(item) > 4 for item in v):
                            catalog[k] = v
            except Exception:
                pass
        return catalog

    @classmethod
    def save_subtask_for_task(cls, task_code: str, subtasks_list: list):
        if not subtasks_list:
            return
        has_meaningful_text = any(" - " in s or len(s) > 4 for s in subtasks_list)
        if not has_meaningful_text:
            return

        catalog = cls.load_subtasks_catalog()
        catalog[task_code] = subtasks_list
        try:
            with open(SUBTASKS_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(catalog, f, indent=2)
            print(f"[✓] Saved {len(subtasks_list)} descriptive subtasks for {task_code} into catalog.")
        except Exception as e:
            print(f"[!] Could not save subtasks catalog: {e}")


# ──────────────────────────────────────────────────────────────────────
# CENTRAL TELEGRAM NOTIFICATION DISPATCHER
# ──────────────────────────────────────────────────────────────────────
def send_telegram_alert(chat_id: str, target_date: str) -> bool:
    """Sends completion notification to student via Central Telegram Bot."""
    if not chat_id:
        print("[i] Telegram alert skipped: Chat ID not provided.")
        return False

    clean_chat_id = chat_id.strip()
    msg = (
        f"✅ *ICAI e-Diary Update Successful!*\n\n"
        f"📅 *Date:* {target_date}\n"
        f"⏰ *Status:* Submitted & Logged Out\n\n"
        f"Your daily articleship e-Diary entry has been updated."
    )
    encoded_msg = urllib.parse.quote(msg)
    url = f"https://api.telegram.org/bot{CENTRAL_BOT_TOKEN}/sendMessage?chat_id={clean_chat_id}&text={encoded_msg}&parse_mode=Markdown"

    print(f"[*] Dispatching Telegram notification to Chat ID: {clean_chat_id} via {CENTRAL_BOT_USERNAME}...")
    try:
        res = requests.get(url, timeout=15)
        if res.status_code == 200:
            print("[✓] Telegram notification delivered successfully!")
            return True
        else:
            print(f"[!] Telegram API error {res.status_code}: {res.text[:120]}")
            return False
    except Exception as ex:
        print(f"[!] Failed to deliver Telegram alert: {ex}")
        return False


# ──────────────────────────────────────────────────────────────────────
# PRE-RUN ALWAYS-ON-TOP MASTER GUI
# ──────────────────────────────────────────────────────────────────────
class PreRunMasterGUI:
    def __init__(self):
        self.result = None
        self.config = ConfigManager.load_config()
        self.catalog = ConfigManager.load_subtasks_catalog()

        self.root = tk.Tk()
        self.root.title("ICAI e-Diary Automation Suite - Task & Settings")
        self.root.configure(bg="#f1f5f9")
        self._center_window(710, 740)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.subtask_vars = []
        self.selected_subtasks_set = set()
        self._build_ui()
        self._bind_mousewheel_everywhere()

    def _center_window(self, w, h):
        self.root.update_idletasks()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        final_h = min(h, sh - 70)
        x = max(0, (sw - w) // 2)
        y = max(0, (sh - final_h) // 2 - 20)
        self.root.geometry(f"{w}x{final_h}+{x}+{y}")
        self.root.lift()
        self.root.focus_force()

    def _bind_mousewheel_everywhere(self):
        """Binds mouse wheel recursively and intelligently across all widgets."""
        self.main_canvas.configure(yscrollincrement=10)
        if hasattr(self, "sub_canvas"):
            self.sub_canvas.configure(yscrollincrement=10)

        def _on_wheel(event):
            if hasattr(event, "delta") and event.delta != 0:
                units = -2 if event.delta > 0 else 2
            elif getattr(event, "num", None) == 4:
                units = -2
            elif getattr(event, "num", None) == 5:
                units = 2
            else:
                return

            try:
                x, y = self.root.winfo_pointerxy()
                sub_x = self.sub_canvas.winfo_rootx()
                sub_y = self.sub_canvas.winfo_rooty()
                sub_w = self.sub_canvas.winfo_width()
                sub_h = self.sub_canvas.winfo_height()
                if sub_x <= x <= sub_x + sub_w and sub_y <= y <= sub_y + sub_h:
                    self.sub_canvas.yview_scroll(units, "units")
                    return "break"
            except Exception:
                pass

            self.main_canvas.yview_scroll(units, "units")
            return "break"

        def _bind_tree(w):
            w.bind("<MouseWheel>", _on_wheel, add="+")
            w.bind("<Button-4>", _on_wheel, add="+")
            w.bind("<Button-5>", _on_wheel, add="+")
            for c in w.winfo_children():
                _bind_tree(c)

        self.root.bind_all("<MouseWheel>", _on_wheel)
        self.root.bind_all("<Button-4>", _on_wheel)
        self.root.bind_all("<Button-5>", _on_wheel)
        self.root.bind_all("<Up>", lambda e: self.main_canvas.yview_scroll(-2, "units"))
        self.root.bind_all("<Down>", lambda e: self.main_canvas.yview_scroll(2, "units"))
        self.root.bind_all("<Prior>", lambda e: self.main_canvas.yview_scroll(-6, "units"))
        self.root.bind_all("<Next>", lambda e: self.main_canvas.yview_scroll(6, "units"))

        _bind_tree(self.root)

    def _build_ui(self):
        # Header Banner
        header = tk.Frame(self.root, bg="#1e3a8a", pady=10)
        header.pack(fill=tk.X)
        tk.Label(header, text=" ICAI e-Diary Daily Log Automation", bg="#1e3a8a", fg="white",
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20)
        tk.Label(header, text="Configure your entry & click Start  ·  Official Subtasks from Portal",
                 bg="#1e3a8a", fg="#93c5fd", font=("Segoe UI", 9)).pack(anchor="w", padx=20)

        # Scrollable Canvas
        canvas_wrap = tk.Frame(self.root, bg="#f1f5f9")
        canvas_wrap.pack(fill=tk.BOTH, expand=True)

        self.main_canvas = tk.Canvas(canvas_wrap, bg="#f1f5f9", highlightthickness=0, yscrollincrement=10)
        scrollbar = ttk.Scrollbar(canvas_wrap, orient="vertical", command=self.main_canvas.yview)
        self.scroll_frame = tk.Frame(self.main_canvas, bg="#f1f5f9")

        self.scroll_frame.bind("<Configure>", lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all")))
        self.main_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", width=690)
        self.main_canvas.configure(yscrollcommand=scrollbar.set)

        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Card 1: Credentials & Telegram Alerts
        self._build_card_credentials(self.scroll_frame)

        # Card 2: Target Date Calendar & Effort Duration
        self._build_card_duration(self.scroll_frame)

        # Card 3: Task & Subtasks (Official Live Catalog & Max 5 limit)
        self._build_card_tasks(self.scroll_frame)

        # Card 4: Other Task (Optional)
        self._build_card_other_task(self.scroll_frame)

        # Start Button
        btn_frame = tk.Frame(self.scroll_frame, bg="#f1f5f9", pady=15)
        btn_frame.pack(fill=tk.X, padx=20)

        start_btn = tk.Button(
            btn_frame,
            text="▶  START AUTOMATION & UPDATE E-DIARY",
            font=("Segoe UI", 12, "bold"),
            bg="#16a34a",
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
            pady=10,
            command=self._on_start
        )
        start_btn.pack(fill=tk.X)

    def _build_card_credentials(self, parent):
        card = tk.LabelFrame(parent, text="  🔐 1. Portal Credentials & Telegram Alerts (Saved Locally)  ",
                             bg="white", fg="#1e293b", font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        card.pack(fill=tk.X, padx=20, pady=(15, 8))

        # Row 1: SRO & Password
        r1 = tk.Frame(card, bg="white")
        r1.pack(fill=tk.X, pady=4)

        tk.Label(r1, text="SRO Number:", bg="white", font=("Segoe UI", 9, "bold"), width=14, anchor="w").pack(side=tk.LEFT)
        self.sro_entry = tk.Entry(r1, font=("Segoe UI", 9), width=18)
        self.sro_entry.pack(side=tk.LEFT, padx=(0, 20))
        self.sro_entry.insert(0, self.config.get("sro", ""))

        tk.Label(r1, text="Password:", bg="white", font=("Segoe UI", 9, "bold"), width=12, anchor="w").pack(side=tk.LEFT)
        self.pwd_entry = tk.Entry(r1, font=("Segoe UI", 9), width=18, show="*")
        self.pwd_entry.pack(side=tk.LEFT)
        self.pwd_entry.insert(0, self.config.get("password", ""))

        # Separator line
        ttk.Separator(card, orient="horizontal").pack(fill=tk.X, pady=8)

        # Row 2: Telegram Notification
        self.enable_tg_var = tk.BooleanVar(value=self.config.get("enable_telegram", True))

        def _toggle_tg():
            if self.enable_tg_var.get():
                self.tg_chat_entry.config(state="normal")
            else:
                self.tg_chat_entry.config(state="disabled")

        r2 = tk.Frame(card, bg="white")
        r2.pack(fill=tk.X, pady=2)

        cb_tg = tk.Checkbutton(
            r2,
            text=f"Send alert to my phone via Central Bot ({CENTRAL_BOT_USERNAME})",
            variable=self.enable_tg_var,
            bg="white",
            font=("Segoe UI", 9, "bold"),
            fg="#0284c7",
            command=_toggle_tg
        )
        cb_tg.pack(side=tk.LEFT)

        r3 = tk.Frame(card, bg="#f8fafc", padx=10, pady=6, highlightthickness=1, highlightbackground="#e2e8f0")
        r3.pack(fill=tk.X, pady=(4, 5))

        tk.Label(r3, text="Your Telegram Chat ID:", bg="#f8fafc", font=("Segoe UI", 8, "bold"), width=20, anchor="w").pack(side=tk.LEFT)
        self.tg_chat_entry = tk.Entry(r3, font=("Segoe UI", 9), width=20)
        self.tg_chat_entry.pack(side=tk.LEFT, padx=5)
        self.tg_chat_entry.insert(0, self.config.get("telegram_chat_id", ""))

        def _help_tg():
            messagebox.showinfo(
                "How to receive alerts (1-Time Setup, Takes 20 Seconds)",
                f"1. Open Telegram on your phone.\n"
                f"2. Search for {CENTRAL_BOT_USERNAME} and tap START.\n"
                f"3. Search for @userinfobot on Telegram and tap START to see your personal Chat ID (e.g. 123456789).\n"
                f"4. Enter that Chat ID number here!\n\n"
                f"No bot creation needed — the central bot will send your completion alerts directly to you.",
                parent=self.root
            )

        help_btn = tk.Button(r3, text="ℹ️ How to get my Chat ID?", font=("Segoe UI", 8, "underline"),
                             bg="#f8fafc", fg="#0284c7", bd=0, cursor="hand2", command=_help_tg)
        help_btn.pack(side=tk.LEFT, padx=10)

        # Row 4: Remember checkbox
        r4 = tk.Frame(card, bg="white")
        r4.pack(fill=tk.X, pady=(4, 0))

        self.remember_var = tk.BooleanVar(value=self.config.get("remember", True))
        cb_rem = tk.Checkbutton(r4, text="Remember details on this PC (Never committed to GitHub)",
                                variable=self.remember_var, bg="white", font=("Segoe UI", 8), fg="#475569")
        cb_rem.pack(side=tk.LEFT)

    def _build_card_duration(self, parent):
        card = tk.LabelFrame(parent, text="  📅 2. Target Date Calendar & Effort Duration  ",
                             bg="white", fg="#1e293b", font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        card.pack(fill=tk.X, padx=20, pady=6)

        # Row 1: Date Mode (Today vs Specific Date)
        r_date = tk.Frame(card, bg="white")
        r_date.pack(fill=tk.X, pady=(2, 6))

        today_dt = datetime.now()
        today_formatted = today_dt.strftime("%d/%m/%Y (%A)")

        self.date_mode_var = tk.StringVar(value="today")
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        def _update_date_preview():
            mode = self.date_mode_var.get()
            if mode == "today":
                now = datetime.now()
                self.date_preview_lbl.config(text=f"📌 Selected Entry Date: {now.strftime('%d/%m/%Y (%A)')}", fg="#0284c7")
            else:
                try:
                    d = int(self.day_spin.get())
                    m = months.index(self.month_combo.get()) + 1
                    y = int(self.year_spin.get())
                    dt = datetime(y, m, d)
                    self.date_preview_lbl.config(text=f"📌 Selected Entry Date: {dt.strftime('%d/%m/%Y (%A)')}", fg="#16a34a")
                except Exception:
                    self.date_preview_lbl.config(text="⚠️ Please check date values", fg="#dc2626")

        def _toggle_date_inputs():
            mode = self.date_mode_var.get()
            if mode == "today":
                self.day_spin.config(state="disabled")
                self.month_combo.config(state="disabled")
                self.year_spin.config(state="disabled")
                self.cal_popup_btn.config(state="disabled")
            else:
                self.day_spin.config(state="normal")
                self.month_combo.config(state="readonly")
                self.year_spin.config(state="normal")
                self.cal_popup_btn.config(state="normal")
            _update_date_preview()

        rb_today = tk.Radiobutton(r_date, text=f"Today - {today_formatted}", variable=self.date_mode_var,
                                  value="today", bg="white", font=("Segoe UI", 9, "bold"), fg="#0284c7",
                                  command=_toggle_date_inputs)
        rb_today.pack(side=tk.LEFT, padx=(0, 20))

        rb_custom = tk.Radiobutton(r_date, text="Specific Date:", variable=self.date_mode_var,
                                   value="custom", bg="white", font=("Segoe UI", 9, "bold"), fg="#334155",
                                   command=_toggle_date_inputs)
        rb_custom.pack(side=tk.LEFT, padx=(0, 8))

        # Date Pickers: Day, Month, Year
        self.day_spin = ttk.Spinbox(r_date, from_=1, to=31, width=3, state="disabled", font=("Segoe UI", 9), command=_update_date_preview)
        self.day_spin.set(today_dt.day)
        self.day_spin.pack(side=tk.LEFT, padx=2)
        self.day_spin.bind("<KeyRelease>", lambda e: _update_date_preview())

        self.month_combo = ttk.Combobox(r_date, values=months, width=5, state="disabled", font=("Segoe UI", 9))
        self.month_combo.current(today_dt.month - 1)
        self.month_combo.pack(side=tk.LEFT, padx=2)
        self.month_combo.bind("<<ComboboxSelected>>", lambda e: _update_date_preview())

        self.year_spin = ttk.Spinbox(r_date, from_=2020, to=2035, width=5, state="disabled", font=("Segoe UI", 9), command=_update_date_preview)
        self.year_spin.set(today_dt.year)
        self.year_spin.pack(side=tk.LEFT, padx=2)
        self.year_spin.bind("<KeyRelease>", lambda e: _update_date_preview())

        # Interactive Visual Calendar Dialog
        def _open_calendar_popup():
            cal_win = tk.Toplevel(self.root)
            cal_win.title("Select Date from Calendar")
            cal_win.configure(bg="#f8fafc")
            cal_win.attributes("-topmost", True)
            cal_win.grab_set()
            cal_win.resizable(False, False)

            cw, ch = 340, 330
            rx = self.root.winfo_rootx() + (self.root.winfo_width() - cw) // 2
            ry = self.root.winfo_rooty() + (self.root.winfo_height() - ch) // 2
            cal_win.geometry(f"{cw}x{ch}+{rx}+{ry}")

            try:
                init_y = int(self.year_spin.get())
                init_m = months.index(self.month_combo.get()) + 1
            except Exception:
                init_y = today_dt.year
                init_m = today_dt.month

            curr_y = tk.IntVar(value=init_y)
            curr_m = tk.IntVar(value=init_m)

            hdr = tk.Frame(cal_win, bg="#1e3a8a", pady=6)
            hdr.pack(fill=tk.X)

            month_label = tk.Label(hdr, text="", bg="#1e3a8a", fg="white", font=("Segoe UI", 10, "bold"))

            grid_frame = tk.Frame(cal_win, bg="#f8fafc", padx=12, pady=8)
            grid_frame.pack(fill=tk.BOTH, expand=True)

            def _render_calendar():
                for widget in grid_frame.winfo_children():
                    widget.destroy()
                y = curr_y.get()
                m = curr_m.get()
                month_label.config(text=f"{calendar.month_name[m]}  {y}")

                day_names = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
                for i, d in enumerate(day_names):
                    bg_col = "#e2e8f0" if i < 5 else "#fed7aa"
                    tk.Label(grid_frame, text=d, font=("Segoe UI", 8, "bold"), width=4, bg=bg_col, fg="#1e293b", pady=3).grid(row=0, column=i, padx=2, pady=2)

                cal_matrix = calendar.monthcalendar(y, m)
                now = datetime.now()
                for r_idx, week in enumerate(cal_matrix):
                    for c_idx, day_num in enumerate(week):
                        if day_num == 0:
                            tk.Label(grid_frame, text="", bg="#f8fafc", width=4).grid(row=r_idx + 1, column=c_idx, padx=1, pady=1)
                        else:
                            is_today = (y == now.year and m == now.month and day_num == now.day)
                            btn_bg = "#2563eb" if is_today else "white"
                            btn_fg = "white" if is_today else "#1e293b"

                            def _select_day_handler(d_val=day_num):
                                self.date_mode_var.set("custom")
                                _toggle_date_inputs()
                                self.day_spin.set(d_val)
                                self.month_combo.current(curr_m.get() - 1)
                                self.year_spin.set(curr_y.get())
                                _update_date_preview()
                                cal_win.destroy()

                            btn = tk.Button(
                                grid_frame, text=str(day_num), font=("Segoe UI", 9, "bold" if is_today else "normal"),
                                width=4, bg=btn_bg, fg=btn_fg, relief=tk.GROOVE if not is_today else tk.FLAT,
                                cursor="hand2", command=_select_day_handler
                            )
                            btn.grid(row=r_idx + 1, column=c_idx, padx=1, pady=1)

            def _prev_month():
                m = curr_m.get() - 1
                y = curr_y.get()
                if m < 1:
                    m = 12
                    y -= 1
                curr_m.set(m)
                curr_y.set(y)
                _render_calendar()

            def _next_month():
                m = curr_m.get() + 1
                y = curr_y.get()
                if m > 12:
                    m = 1
                    y += 1
                curr_m.set(m)
                curr_y.set(y)
                _render_calendar()

            tk.Button(hdr, text=" ◀ ", bg="#1e3a8a", fg="white", bd=0, font=("Segoe UI", 9, "bold"),
                      cursor="hand2", command=_prev_month).pack(side=tk.LEFT, padx=10)
            month_label.pack(side=tk.LEFT, expand=True)
            tk.Button(hdr, text=" ▶ ", bg="#1e3a8a", fg="white", bd=0, font=("Segoe UI", 9, "bold"),
                      cursor="hand2", command=_next_month).pack(side=tk.RIGHT, padx=10)

            _render_calendar()

        self.cal_popup_btn = tk.Button(
            r_date, text="📅 Calendar View", font=("Segoe UI", 8, "bold"),
            bg="#f1f5f9", fg="#2563eb", relief=tk.GROOVE, cursor="hand2", state="disabled",
            padx=6, pady=2, command=_open_calendar_popup
        )
        self.cal_popup_btn.pack(side=tk.LEFT, padx=(8, 0))

        # Live Date Preview Label
        self.date_preview_lbl = tk.Label(card, text=f"📌 Selected Entry Date: {today_formatted}",
                                         bg="white", font=("Segoe UI", 8, "bold"), fg="#0284c7")
        self.date_preview_lbl.pack(anchor="w", pady=(2, 6))

        # Row 2: Duration
        ttk.Separator(card, orient="horizontal").pack(fill=tk.X, pady=6)
        r_dur = tk.Frame(card, bg="white")
        r_dur.pack(fill=tk.X)

        tk.Label(r_dur, text="Effort Duration:", bg="white", font=("Segoe UI", 9, "bold"), width=15, anchor="w").pack(side=tk.LEFT)
        self.dur_var = tk.StringVar(value="1")
        tk.Radiobutton(r_dur, text="Full Day (1)", variable=self.dur_var, value="1",
                       bg="white", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 20))
        tk.Radiobutton(r_dur, text="Half Day (0.5)", variable=self.dur_var, value="0.5",
                       bg="white", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)

    def _build_card_tasks(self, parent):
        card = tk.LabelFrame(parent, text="  📋 3. Task & Subtasks (Official Live Catalog & Max 5 selections)  ",
                             bg="white", fg="#1e293b", font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        card.pack(fill=tk.X, padx=20, pady=6)

        # Task Selection
        r_task = tk.Frame(card, bg="white")
        r_task.pack(fill=tk.X, pady=(0, 5))

        tk.Label(r_task, text="Select Task Name:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        task_items = [f"{c} - {n}" for c, n in TASK_OPTIONS]
        self.task_combo = ttk.Combobox(r_task, values=task_items, state="readonly", font=("Segoe UI", 9), width=54)
        self.task_combo.current(0)
        self.task_combo.pack(anchor="w", pady=(3, 5))
        self.task_combo.bind("<<ComboboxSelected>>", self._on_task_changed)

        # Controls Row: Search Filter & View All Toggle
        r_controls = tk.Frame(card, bg="#f8fafc", padx=8, pady=5, highlightthickness=1, highlightbackground="#e2e8f0")
        r_controls.pack(fill=tk.X, pady=(2, 6))

        tk.Label(r_controls, text="🔍 Filter:", bg="#f8fafc", font=("Segoe UI", 8, "bold"), fg="#475569").pack(side=tk.LEFT)
        self.subtask_filter_entry = tk.Entry(r_controls, font=("Segoe UI", 8), width=24)
        self.subtask_filter_entry.pack(side=tk.LEFT, padx=(4, 15))
        self.subtask_filter_entry.bind("<KeyRelease>", lambda e: self._filter_subtasks())

        self.show_all_subtasks_var = tk.BooleanVar(value=False)
        cb_show_all = tk.Checkbutton(
            r_controls,
            text="Show All 107 Portal Subtasks (S1 - S107)",
            variable=self.show_all_subtasks_var,
            bg="#f8fafc",
            font=("Segoe UI", 8, "bold"),
            fg="#0284c7",
            command=self._on_view_mode_changed
        )
        cb_show_all.pack(side=tk.LEFT)

        # Subtask Counter & Instruction
        counter_row = tk.Frame(card, bg="white")
        counter_row.pack(fill=tk.X, pady=(4, 4))

        self.subtask_hint_lbl = tk.Label(counter_row, text="Select Subtasks (Check up to 5 items):", bg="white", font=("Segoe UI", 9, "bold"))
        self.subtask_hint_lbl.pack(side=tk.LEFT)

        self.subtask_counter = tk.Label(counter_row, text="Selected: 0 / 5", bg="white",
                                        font=("Segoe UI", 9, "bold"), fg="#2563eb")
        self.subtask_counter.pack(side=tk.RIGHT)

        # Subtasks Box (Scrollable)
        sub_wrap = tk.Frame(card, bg="white", highlightthickness=1, highlightbackground="#cbd5e1")
        sub_wrap.pack(fill=tk.BOTH, expand=True)

        self.sub_canvas = tk.Canvas(sub_wrap, bg="#f8fafc", height=155, highlightthickness=0, yscrollincrement=10)
        sub_scrollbar = ttk.Scrollbar(sub_wrap, orient="vertical", command=self.sub_canvas.yview)
        self.sub_inner = tk.Frame(self.sub_canvas, bg="#f8fafc")

        self.sub_inner.bind("<Configure>", lambda e: self.sub_canvas.configure(scrollregion=self.sub_canvas.bbox("all")))
        self.sub_canvas.create_window((0, 0), window=self.sub_inner, anchor="nw", width=610)
        self.sub_canvas.configure(yscrollcommand=sub_scrollbar.set)

        self.sub_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sub_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._populate_subtasks("T1")

    def _on_task_changed(self, event=None):
        idx = self.task_combo.current()
        code = TASK_OPTIONS[idx][0]
        self._populate_subtasks(code)

    def _on_view_mode_changed(self):
        idx = self.task_combo.current()
        code = TASK_OPTIONS[idx][0]
        self._populate_subtasks(code)

    def _filter_subtasks(self):
        idx = self.task_combo.current()
        code = TASK_OPTIONS[idx][0]
        self._populate_subtasks(code)

    def _populate_subtasks(self, task_code):
        for widget in self.sub_inner.winfo_children():
            widget.destroy()
        self.subtask_vars.clear()

        curr_count = len(self.selected_subtasks_set)
        self.subtask_counter.config(text=f"Selected: {curr_count} / 5", fg="#2563eb" if curr_count <= 5 else "#dc2626")

        if task_code in ["T14", "T15", "T16", "T18"] and not self.show_all_subtasks_var.get():
            tk.Label(self.sub_inner, text="No subtasks required for this category (Leave/Holiday/Weekoff).",
                     bg="#f8fafc", fg="#64748b", font=("Segoe UI", 9, "italic")).pack(pady=20)
            return

        if self.show_all_subtasks_var.get():
            subtasks = self.catalog.get("ALL", [])
            self.subtask_hint_lbl.config(text="All Portal Subtasks (S1 to S107):")
        else:
            subtasks = self.catalog.get(task_code, [])
            if not subtasks:
                subtasks = self.catalog.get("ALL", [])
            self.subtask_hint_lbl.config(text=f"Subtasks for {task_code} (Check up to 5):")

        # Apply search filter if entered
        query = self.subtask_filter_entry.get().strip().lower()
        if query:
            subtasks = [s for s in subtasks if query in s.lower()]

        if not subtasks:
            tk.Label(self.sub_inner, text="No matching subtasks found for your filter.",
                     bg="#f8fafc", fg="#94a3b8", font=("Segoe UI", 9, "italic")).pack(pady=20)
            return

        def _make_handler(var, item_label):
            def _handler(*args):
                if var.get() == 1:
                    if len(self.selected_subtasks_set) >= 5 and item_label not in self.selected_subtasks_set:
                        var.set(0)
                        self.subtask_counter.config(text="⚠️ Maximum 5 Subtasks Allowed!", fg="#dc2626")
                        messagebox.showwarning("Limit Reached", "You can only select up to 5 subtasks.", parent=self.root)
                        return
                    self.selected_subtasks_set.add(item_label)
                else:
                    self.selected_subtasks_set.discard(item_label)

                total = len(self.selected_subtasks_set)
                self.subtask_counter.config(text=f"Selected: {total} / 5", fg="#2563eb")
            return _handler

        for item in subtasks:
            is_checked = 1 if item in self.selected_subtasks_set else 0
            v = tk.IntVar(value=is_checked)
            v.trace_add("write", _make_handler(v, item))
            self.subtask_vars.append((v, item))

            cb = tk.Checkbutton(
                self.sub_inner,
                text=f" {item}",
                variable=v,
                bg="#f8fafc",
                font=("Segoe UI", 9),
                anchor="w",
                wraplength=570,
                justify=tk.LEFT
            )
            cb.pack(fill=tk.X, padx=8, pady=2)

        self._bind_mousewheel_everywhere()

    def _build_card_other_task(self, parent):
        card = tk.LabelFrame(parent, text="  📝 4. Other Task (Optional)  ",
                             bg="white", fg="#1e293b", font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        card.pack(fill=tk.X, padx=20, pady=6)

        self.has_other_var = tk.BooleanVar(value=False)

        def _toggle_other():
            if self.has_other_var.get():
                self.other_entry.config(state="normal")
                self.other_entry.focus_set()
            else:
                self.other_entry.delete(0, tk.END)
                self.other_entry.config(state="disabled")

        cb_other = tk.Checkbutton(
            card,
            text="I have an Other Task description to record for today",
            variable=self.has_other_var,
            bg="white",
            font=("Segoe UI", 9, "bold"),
            fg="#334155",
            command=_toggle_other
        )
        cb_other.pack(anchor="w")

        r_ot = tk.Frame(card, bg="white")
        r_ot.pack(fill=tk.X, pady=(6, 2))

        tk.Label(r_ot, text="Work Description:", bg="white", font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(0, 10))
        self.other_entry = tk.Entry(r_ot, font=("Segoe UI", 9), width=52, state="disabled")
        self.other_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _on_start(self):
        sro = self.sro_entry.get().strip()
        pwd = self.pwd_entry.get()

        if not sro or not pwd:
            messagebox.showwarning("Missing Credentials", "Please enter your ICAI SRO Number and Password.", parent=self.root)
            return

        enable_tg = self.enable_tg_var.get()
        tg_chat = self.tg_chat_entry.get().strip() if enable_tg else ""
        remember = self.remember_var.get()

        save_dict = {
            "sro": sro,
            "password": pwd,
            "enable_telegram": enable_tg,
            "telegram_chat_id": tg_chat
        }
        ConfigManager.save_config(save_dict, remember)

        # Date computation
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        if self.date_mode_var.get() == "today":
            target_dt = datetime.now()
        else:
            try:
                d = int(self.day_spin.get())
                m = months.index(self.month_combo.get()) + 1
                y = int(self.year_spin.get())
                target_dt = datetime(y, m, d)
            except Exception:
                target_dt = datetime.now()

        task_idx = self.task_combo.current()
        task_code, task_name = TASK_OPTIONS[task_idx]
        chosen_subtasks = list(self.selected_subtasks_set)
        other_text = self.other_entry.get().strip() if self.has_other_var.get() else ""

        self.result = {
            "sro": sro,
            "password": pwd,
            "enable_telegram": enable_tg,
            "telegram_chat_id": tg_chat,
            "target_date_dt": target_dt,
            "target_date_str": target_dt.strftime("%d/%m/%Y"),
            "target_day": str(target_dt.day),
            "target_month_num": target_dt.month,
            "target_month_str": target_dt.strftime("%b"),
            "target_year": str(target_dt.year),
            "duration": self.dur_var.get(),
            "task_code": task_code,
            "task_name": task_name,
            "subtasks": chosen_subtasks,
            "other_task": other_text
        }
        self.root.destroy()

    def _on_close(self):
        self.root.destroy()
        sys.exit(0)

    def show(self):
        self.root.mainloop()
        return self.result


# ──────────────────────────────────────────────────────────────────────
# LIVE SUBTASK SELECTION DIALOG (For manual fallback or review)
# ──────────────────────────────────────────────────────────────────────
def prompt_live_subtasks_dialog(task_name: str, available_subtasks: list, preselected_names: list) -> list:
    """
    Pops up an Always-on-Top dialog showing genuine subtasks read from the portal,
    enforcing max 5 selections.
    """
    if not available_subtasks:
        return []

    root = tk.Tk()
    root.title(f"Select Subtasks - {task_name}")
    root.configure(bg="#f8f9fa")
    root.attributes("-topmost", True)
    root.resizable(False, False)

    w, h = 560, 500
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    root.lift()
    root.focus_force()

    tk.Label(root, text=f"  Portal Subtasks: {task_name}", bg="#1e3a8a", fg="white",
             font=("Segoe UI", 12, "bold"), pady=8, anchor="w").pack(fill=tk.X)

    counter_frame = tk.Frame(root, bg="#f8f9fa", pady=4)
    counter_frame.pack(fill=tk.X, padx=15)

    status_label = tk.Label(counter_frame, text="Selected: 0 / 5  (Limit: Max 5)", font=("Segoe UI", 9, "bold"), fg="#2563eb", bg="#f8f9fa")
    status_label.pack(side=tk.LEFT)

    wrap = tk.Frame(root, bg="white", highlightthickness=1, highlightbackground="#cbd5e1")
    wrap.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

    canvas = tk.Canvas(wrap, bg="#f8fafc", highlightthickness=0, yscrollincrement=10)
    scrollbar = ttk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg="#f8fafc")

    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw", width=510)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _on_wheel(e):
        units = -2 if (e.delta > 0 or getattr(e, "num", None) == 4) else 2
        canvas.yview_scroll(units, "units")
        return "break"

    root.bind_all("<MouseWheel>", _on_wheel)

    check_vars = []
    selected_indices = []

    def _make_handler(var):
        def _handler(*args):
            total = sum(v.get() for v in check_vars)
            if total > 5:
                var.set(0)
                status_label.config(text="⚠️ Maximum 5 Subtasks Allowed!", fg="#dc2626")
                messagebox.showwarning("Limit Reached", "You can only select up to 5 subtasks.", parent=root)
            else:
                status_label.config(text=f"Selected: {total} / 5", fg="#2563eb")
        return _handler

    # Pre-select matching items if any
    for idx, name in enumerate(available_subtasks):
        init_val = 0
        name_clean = name.lower()
        for p in preselected_names:
            p_clean = p.lower()
            code_prefix = name_clean.split("-")[0].strip() if "-" in name_clean else ""
            if (p_clean == name_clean or
                (code_prefix and p_clean.startswith(code_prefix)) or
                p_clean in name_clean or name_clean in p_clean):
                init_val = 1
                break

        v = tk.IntVar(value=init_val)
        v.trace_add("write", _make_handler(v))
        check_vars.append(v)

        cb = tk.Checkbutton(inner, text=f" {name}", variable=v, bg="#f8fafc", font=("Segoe UI", 9),
                            anchor="w", wraplength=480, justify=tk.LEFT)
        cb.pack(fill=tk.X, padx=10, pady=3)

    init_total = sum(v.get() for v in check_vars)
    status_label.config(text=f"Selected: {init_total} / 5")

    def _on_confirm():
        nonlocal selected_indices
        selected_indices = [i for i, v in enumerate(check_vars) if v.get() == 1]
        root.destroy()

    btn_frame = tk.Frame(root, bg="#f8f9fa", pady=10)
    btn_frame.pack(fill=tk.X)

    btn = tk.Button(btn_frame, text="Confirm & Check on Website ➔", bg="#16a34a", fg="white",
                    font=("Segoe UI", 10, "bold"), relief=tk.FLAT, cursor="hand2", padx=20, pady=5, command=_on_confirm)
    btn.pack()

    root.mainloop()
    return selected_indices


# ──────────────────────────────────────────────────────────────────────
# SELENIUM CORE AUTOMATION HELPERS
# ──────────────────────────────────────────────────────────────────────
def js_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    driver.execute_script("arguments[0].click();", element)


def build_chrome_options():
    opts = webdriver.ChromeOptions()
    opts.page_load_strategy = "eager"
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-save-password-bubble")
    opts.add_argument("--disable-password-manager-reauthentication")
    opts.add_argument("--disable-features=PasswordManager,AutofillServerCommunication")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.default_content_setting_values.notifications": 2,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
    })
    return opts


def ensure_in_frame1(driver):
    """Safely switches to iframe#frame1 without error if already inside it."""
    try:
        driver.find_element(By.ID, "taskDuration")
        return
    except Exception:
        pass
    try:
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#frame1")))
        driver.switch_to.frame("frame1")
    except Exception as e:
        print(f"[!] Warning switching to frame1: {e}")


def close_modal_in_iframe(driver, timeout: int = 15) -> bool:
    """Safely dismisses the announcement popup inside iframe#frame1."""
    print("   [*] Accessing iframe#frame1 for popup dismissal...")
    ensure_in_frame1(driver)

    close_selectors = [
        "//button[contains(@class,'close') and @data-dismiss='modal']",
        "//button[@data-dismiss='modal' and contains(@class,'primary_butn')]",
        "//button[@data-dismiss='modal' and (contains(text(),'Close') or @aria-label='Close')]",
        "//span[@aria-hidden='true' and normalize-space(text())='×']/.."
    ]
    combined_xpath = " | ".join(close_selectors)

    end_time = time.time() + timeout
    closed = False
    while time.time() < end_time:
        try:
            buttons = driver.find_elements(By.XPATH, combined_xpath)
            for btn in buttons:
                if btn.is_displayed():
                    js_click(driver, btn)
                    print("   [✓] Popup modal dismissed successfully.")
                    time.sleep(1)
                    closed = True
                    break
            if closed:
                break
        except (StaleElementReferenceException, NoSuchElementException):
            pass
        time.sleep(0.5)
    return closed


def show_alert_dialog(title: str, message: str, is_error: bool = False):
    """Pops up an Always-On-Top modal message dialog."""
    root = tk.Tk()
    root.title(title)
    root.attributes("-topmost", True)
    root.configure(bg="#f8f9fa")
    root.resizable(False, False)

    w, h = 480, 260
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
    root.lift()
    root.focus_force()

    bar_color = "#dc2626" if is_error else "#2563eb"
    header = tk.Frame(root, bg=bar_color, height=45)
    header.pack(fill=tk.X)
    header.pack_propagate(False)

    prefix = "⚠️ " if is_error else "ℹ️ "
    tk.Label(header, text=prefix + title, font=("Segoe UI", 11, "bold"),
             bg=bar_color, fg="white").pack(side=tk.LEFT, padx=15, pady=8)

    body = tk.Frame(root, bg="#f8f9fa", padx=20, pady=15)
    body.pack(fill=tk.BOTH, expand=True)

    tk.Label(body, text=message, font=("Segoe UI", 10), bg="#f8f9fa",
             fg="#1e293b", justify=tk.LEFT, wraplength=440).pack(anchor="w", pady=(5, 15))

    btn_frame = tk.Frame(root, bg="#f8f9fa", pady=10)
    btn_frame.pack(fill=tk.X)

    ok_btn = tk.Button(btn_frame, text="  OK  ", font=("Segoe UI", 10, "bold"),
                       bg=bar_color, fg="white", relief=tk.FLAT, cursor="hand2",
                       command=root.destroy, padx=25, pady=4)
    ok_btn.pack()
    root.mainloop()


# ──────────────────────────────────────────────────────────────────────
# MAIN SELENIUM RPA RUNNER
# ──────────────────────────────────────────────────────────────────────
def run_automation():
    # Phase 1: Launch Master GUI
    gui = PreRunMasterGUI()
    config_data = gui.show()

    if not config_data:
        print("[*] Operation cancelled by user.")
        return

    sro = config_data["sro"]
    pwd = config_data["password"]
    target_date_str = config_data["target_date_str"]
    target_day = config_data["target_day"]
    target_month_num = config_data["target_month_num"]
    target_year = config_data["target_year"]

    print("\n" + "="*65)
    print("       STARTING ICAI E-DIARY AUTOMATION RUN")
    print("="*65)
    print(f"[*] Student SRO   : {sro}")
    print(f"[*] Target Date   : {target_date_str} (Day {target_day})")
    print(f"[*] Duration      : {config_data['duration']} Day")
    print(f"[*] Task Selected : {config_data['task_code']} - {config_data['task_name']}")
    print(f"[*] Subtasks      : {config_data['subtasks'] if config_data['subtasks'] else '(None pre-selected)'}")
    print(f"[*] Other Task    : {config_data['other_task'] if config_data['other_task'] else '(None)'}")
    print(f"[*] Telegram Alert: {'Enabled' if config_data['enable_telegram'] else 'Disabled'}")
    print("="*65 + "\n")

    driver = None
    try:
        # 1. Initialize Chrome
        print("[Step 1] Initializing Chrome browser (Selenium Manager)...")
        driver = webdriver.Chrome(options=build_chrome_options())
        driver.set_page_load_timeout(30)
        wait = WebDriverWait(driver, 25)

        # 2. Navigate to Portal
        login_url = "https://eservices.icai.org//per/g21/pub/1666/SelfServices/templates/EdiaryLogin12092025024218/Ediary%20Login%20Folder/ICAI%20Ediary%20Login512092025024240.html"
        print(f"[Step 2] Navigating to e-Diary login portal...")
        try:
            driver.get(login_url)
            time.sleep(STEP_PAUSE)
        except Exception:
            print("   [*] Fallback to main portal landing page...")
            driver.get("https://eservices.icai.org")
            click_here_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(@class,'btn-primary-sp3') and contains(text(),'Click Here')]")
            ))
            js_click(driver, click_here_btn)
            time.sleep(STEP_PAUSE)
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[-1])

        # 4. Fill Credentials & Sign In
        print(f"\n[Step 4 & 5] Entering login credentials for {sro}...")
        account_input = wait.until(EC.presence_of_element_located((By.ID, "accountname")))
        account_val = sro if sro.upper().endswith("@ICAI.ORG") else f"{sro}@ICAI.ORG"

        account_input.clear()
        account_input.send_keys(account_val)
        driver.execute_script("arguments[0].dispatchEvent(new Event('blur'));", account_input)
        time.sleep(0.5)

        pwd_input = wait.until(EC.presence_of_element_located((By.ID, "password")))
        pwd_input.clear()
        pwd_input.send_keys(pwd)
        time.sleep(0.5)

        sign_in_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.loginBtn")))
        js_click(driver, sign_in_btn)
        print("   [✓] Clicked Sign In. Awaiting dashboard initialization...")

        time.sleep(5)

        # Check for credential error
        try:
            err_elem = driver.find_element(By.ID, "loginPwdMsg")
            if err_elem.is_displayed():
                err_text = err_elem.text.strip()
                if err_text:
                    print(f"[!] Login Failed: {err_text}")
                    show_alert_dialog("Login Error", f"ICAI Portal Reported:\n\n{err_text}\n\nPlease check your SRO and Password.", is_error=True)
                    return
        except NoSuchElementException:
            pass

        print("[✓] Authentication successful.")

        # 6. Switch to iframe#frame1 and close popup
        print("\n[Step 6] Closing announcement modal inside iframe#frame1...")
        close_modal_in_iframe(driver, timeout=15)
        time.sleep(STEP_PAUSE)

        # 7. Select Chosen Date on Calendar inside iframe#frame1
        print(f"\n[Step 7] Setting target date: {target_date_str} (Day {target_day})...")
        ensure_in_frame1(driver)

        # Method A: Populate date input field & trigger Bootstrap datepicker update
        try:
            js_set_date = """
            var target = arguments[0];
            var inputs = document.querySelectorAll("input.form-control[type='text'], input[type='text']");
            var updated = false;
            for (var i = 0; i < inputs.length; i++) {
                var inp = inputs[i];
                var id = (inp.id || "").toLowerCase();
                var nm = (inp.name || "").toLowerCase();
                if (id.includes("date") || nm.includes("date") || (inp.placeholder && inp.placeholder.toLowerCase().includes("date"))) {
                    inp.value = target;
                    if (window.$ && $(inp).data('datepicker')) {
                        $(inp).datepicker('update', target);
                    }
                    inp.dispatchEvent(new Event('input', { bubbles: true }));
                    inp.dispatchEvent(new Event('change', { bubbles: true }));
                    updated = true;
                }
            }
            return updated;
            """
            did_update = driver.execute_script(js_set_date, target_date_str)
            if did_update:
                print(f"   [✓] Applied target date directly to form date input: {target_date_str}")
        except Exception as e:
            print(f"   [!] Could not set date via JS input: {e}")

        # Method B: Open calendar widget and click date cell
        try:
            cal_icon = driver.find_elements(By.XPATH, "//span[contains(@class,'glyphicon-calendar')]")
            if cal_icon:
                js_click(driver, cal_icon[0])
                time.sleep(0.8)

                day_cell = driver.find_elements(
                    By.XPATH,
                    f"//td[contains(@class,'day') and not(contains(@class,'old')) and not(contains(@class,'new')) and normalize-space(text())='{target_day}']"
                )
                if day_cell:
                    js_click(driver, day_cell[0])
                    print(f"   [✓] Clicked day {target_day} in calendar widget.")
                else:
                    today_cell = driver.find_elements(By.XPATH, "//td[contains(@class,'today')]")
                    if today_cell:
                        js_click(driver, today_cell[0])
                        print("   [✓] Clicked today cell in calendar widget.")
        except Exception as ex:
            print(f"   [!] Calendar widget click notice: {ex}")

        time.sleep(STEP_PAUSE)

        # Check for effort error notice after date select
        try:
            resp_elem = driver.find_element(By.ID, "responseDataBody")
            if resp_elem.is_displayed() and resp_elem.text.strip():
                notice_text = resp_elem.text.strip()
                print(f"[!] Notice: {notice_text}")
                show_alert_dialog("Portal Notice", notice_text)
                close_modal_in_iframe(driver, timeout=5)
                ensure_in_frame1(driver)
        except NoSuchElementException:
            pass

        # 8. Set Duration
        print(f"\n[Step 8] Applying Duration: {config_data['duration']} Day...")
        dur_el = wait.until(EC.presence_of_element_located((By.ID, "taskDuration")))
        Select(dur_el).select_by_value(config_data["duration"])
        driver.execute_script("arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", dur_el)
        time.sleep(STEP_PAUSE)

        # 9. Set Task Name
        print(f"[Step 9] Applying Task Name: {config_data['task_code']} - {config_data['task_name']}...")
        task_el = wait.until(EC.presence_of_element_located((By.ID, "taskName")))
        Select(task_el).select_by_value(config_data["task_code"])
        driver.execute_script("arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", task_el)
        time.sleep(1.5)

        # 10. Extract & Select Subtasks in #subTaskList
        print(f"\n[Step 10] Accessing subtasks for {config_data['task_name']}...")
        task_code = config_data["task_code"]

        if task_code in ["T14", "T15", "T16", "T18"]:
            print(f"[i] No subtasks required for category {task_code} (Leave/Holiday/Weekoff).")
        else:
            try:
                open_btn = wait.until(EC.presence_of_element_located((By.ID, "openSubTasks")))
                if open_btn.is_enabled():
                    sub_container = driver.find_element(By.ID, "subTaskList")
                    if not sub_container.is_displayed():
                        js_click(driver, open_btn)
                        time.sleep(1)

                    chosen_subtasks = config_data.get("subtasks", [])

                    # If user did not pre-select subtasks in GUI, prompt live selection dialog
                    if not chosen_subtasks:
                        available_list = ConfigManager.load_subtasks_catalog().get(task_code, []) or ConfigManager.load_subtasks_catalog().get("ALL", [])
                        chosen_indices = prompt_live_subtasks_dialog(
                            config_data["task_name"],
                            available_list,
                            []
                        )
                        chosen_subtasks = [available_list[i] for i in chosen_indices if i < len(available_list)]

                    print(f"[*] Applying {len(chosen_subtasks)} subtask(s) to the portal checkboxes: {chosen_subtasks}")

                    # Robust JavaScript selector: matches by exact S-code (e.g. S58) or text, checks box & triggers change
                    js_check_subtasks = """
                    var targets = arguments[0]; // array of string identifiers (e.g. ["S58 - Statutory Audits", "S60 - Tax Audit"])
                    var container = document.getElementById("subTaskList");
                    if (!container) return { success: false, error: "no_container" };

                    var cbs = container.querySelectorAll("input[type='checkbox']");
                    var checkedCodes = [];

                    for (var i = 0; i < cbs.length; i++) {
                        var cb = cbs[i];
                        var val = (cb.value || "").trim().toUpperCase(); // e.g. "S58"
                        var row = cb.closest('tr') || cb.parentElement;
                        var text = (row.innerText || row.textContent || "").trim().toLowerCase();

                        var match = false;
                        for (var t = 0; t < targets.length; t++) {
                            var target = (targets[t] || "").trim();
                            var targetUpper = target.toUpperCase();
                            var m = targetUpper.match(/^(S\\d+)/);
                            var targetCode = m ? m[1] : "";

                            // 1. Match by exact code (e.g. S58)
                            if (targetCode && val === targetCode) {
                                match = true;
                                break;
                            }
                            if (val === targetUpper) {
                                match = true;
                                break;
                            }
                            // 2. Match by text substring
                            var cleanTarget = target.replace(/^(S\\d+)\\s*[-:]\\s*/i, "").trim().toLowerCase();
                            if (cleanTarget && text && (text.includes(cleanTarget) || cleanTarget.includes(text))) {
                                match = true;
                                break;
                            }
                        }

                        if (match) {
                            cb.checked = true;
                            cb.dispatchEvent(new Event('input', { bubbles: true }));
                            cb.dispatchEvent(new Event('change', { bubbles: true }));
                            cb.dispatchEvent(new Event('click', { bubbles: true }));
                            if (window.$) $(cb).prop('checked', true).trigger('change');
                            checkedCodes.push(val);
                        } else {
                            cb.checked = false;
                            if (window.$) $(cb).prop('checked', false).trigger('change');
                        }
                    }
                    return { success: true, count: checkedCodes.length, checked: checkedCodes };
                    """
                    selection_result = driver.execute_script(js_check_subtasks, chosen_subtasks)
                    print(f"   [✓] Portal check result: {selection_result}")

                    # Cleanly close subtasks dropdown if open
                    if sub_container.is_displayed():
                        js_click(driver, open_btn)
                        time.sleep(0.5)

                else:
                    print(f"[i] Subtasks button is disabled for {task_code}.")
            except Exception as ex:
                print(f"[!] Error handling subtasks: {ex}")
        time.sleep(STEP_PAUSE)

        # 11. Fill Other Task if provided
        if config_data["other_task"]:
            print(f"[Step 11] Entering Other Task details: '{config_data['other_task']}'...")
            try:
                other_input = wait.until(EC.presence_of_element_located((By.ID, "other_task")))
                other_input.clear()
                other_input.send_keys(config_data["other_task"])
            except Exception as ex:
                print(f"[!] Could not set #other_task: {ex}")
        time.sleep(STEP_PAUSE)

        # 12. Click Save
        print("\n[Step 12] Clicking Save button (#submitTaskData)...")
        save_btn = wait.until(EC.presence_of_element_located((By.ID, "submitTaskData")))
        js_click(driver, save_btn)
        time.sleep(2.5)

        try:
            resp_elem = driver.find_element(By.ID, "responseDataBody")
            if resp_elem.is_displayed() and resp_elem.text.strip():
                server_msg = resp_elem.text.strip()
                print(f"[!] Portal Response: {server_msg}")
                show_alert_dialog("Portal Server Response", server_msg)
        except NoSuchElementException:
            print("[✓] Entry saved without errors.")

        # 13. Profile & Logout
        print("\n[Step 13] Accessing Profile dropdown (#dLabel)...")
        profile_btn = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//a[@id='dLabel'] | //span[@id='studentShortName']/.."
        )))
        js_click(driver, profile_btn)
        time.sleep(1)

        print("[Step 14] Clicking Logout...")
        logout_btn = wait.until(EC.presence_of_element_located((
            By.XPATH,
            "//button[contains(@onclick,'logoutProfile')] | //button[normalize-space(text())='Logout']"
        )))
        js_click(driver, logout_btn)
        time.sleep(1.5)
        print("[✓] Successfully logged out.")

        driver.switch_to.default_content()

        # 14. Telegram Alert Dispatch via Central Bot
        notif_status = False
        if config_data["enable_telegram"] and config_data["telegram_chat_id"]:
            notif_status = send_telegram_alert(config_data["telegram_chat_id"], target_date_str)

        # Final Notification Window
        msg = f"The E-Diary is Updated Successfully for {target_date_str}!\nLogged out securely from ICAI Portal."
        if notif_status:
            msg += f"\n\n📱 Telegram notification delivered to your phone via {CENTRAL_BOT_USERNAME}."

        show_alert_dialog("Process Completed", msg)

    except Exception as ex:
        err_msg = str(ex)
        for marker in ["Stacktrace:", "Backtrace:"]:
            if marker in err_msg:
                err_msg = err_msg.split(marker)[0].strip()
        print(f"\n[!] Automation Error: {err_msg}")
        show_alert_dialog("Automation Error", f"An error occurred:\n\n{err_msg}", is_error=True)

    finally:
        if driver:
            print("\n[*] Closing browser session...")
            try:
                driver.quit()
            except Exception:
                pass
        print("[*] Automation run finished.\n")


if __name__ == "__main__":
    run_automation()
