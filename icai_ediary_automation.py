"""
╔══════════════════════════════════════════════════════════════╗
║          ICAI e-Diary Automation Script  v6                  ║
║  KEY FIX: Popup modal lives inside iframe#frame1             ║
║  Script switches into the iframe before closing the modal    ║
╚══════════════════════════════════════════════════════════════╝

SETUP:
  1. Set USER_SRO and USER_PASSWORD below.
  2. Run:  python icai_ediary_automation.py
"""

import sys
import time
from datetime import datetime

import tkinter as tk
from tkinter import ttk, messagebox

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

# ──────────────────────────────────────────────────────────────
#  ★  SET YOUR CREDENTIALS HERE  ★
# ──────────────────────────────────────────────────────────────
USER_SRO      = "SRO0000000"      # e.g.  "SRO1234567"
USER_PASSWORD = "YourPassword"    # e.g.  "MySecret@123"
# ──────────────────────────────────────────────────────────────

STEP_PAUSE = 1.5   # seconds between every step

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


# ══════════════════════════════════════════════════════════════
#  LOW-LEVEL HELPERS
# ══════════════════════════════════════════════════════════════

def pace(extra: float = 0.0):
    time.sleep(STEP_PAUSE + extra)


def js_click(driver, el):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    driver.execute_script("arguments[0].click();", el)


def action_click(driver, el):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    ActionChains(driver).move_to_element(el).click().perform()


def clean_error(exc: Exception) -> str:
    msg = str(exc)
    for marker in ("Stacktrace:", "Backtrace:", "(No symbol)"):
        if marker in msg:
            msg = msg[:msg.index(marker)].strip()
    return msg[:700]


def build_chrome_options() -> webdriver.ChromeOptions:
    opts = webdriver.ChromeOptions()
    opts.add_argument("--start-maximized")
    opts.add_argument("--disable-notifications")
    opts.add_argument("--disable-save-password-bubble")
    opts.add_argument("--disable-password-manager-reauthentication")
    opts.add_argument("--disable-features=PasswordManager,AutofillServerCommunication")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_experimental_option("prefs", {
        "credentials_enable_service":                            False,
        "profile.password_manager_enabled":                      False,
        "profile.default_content_setting_values.notifications":  2,
        "autofill.profile_enabled":                              False,
        "autofill.credit_card_enabled":                          False,
    })
    return opts


# ══════════════════════════════════════════════════════════════
#  IFRAME-AWARE MODAL CLOSER
#  From DevTools screenshot the popup is confirmed inside:
#    iframe#frame1  →  div.modal#showResponseModal
#  Close buttons (both confirmed from DevTools):
#    <button class="close" data-dismiss="modal" aria-label="Close">×</button>
#    <button class="primary_butn small less_width" data-dismiss="modal">Close</button>
# ══════════════════════════════════════════════════════════════

def _remove_backdrop_in_current_frame(driver):
    """Strip Bootstrap modal leftovers in whatever frame is active."""
    try:
        driver.execute_script("""
            try {
                if (typeof $ !== 'undefined') {
                    $('.modal').each(function(){ $(this).modal('hide'); });
                }
            } catch(e) {}
            document.querySelectorAll('.modal').forEach(function(m){
                m.classList.remove('in', 'show');
                m.style.display = 'none';
                m.setAttribute('aria-hidden', 'true');
            });
            document.querySelectorAll('.modal-backdrop').forEach(function(b){
                b.parentNode && b.parentNode.removeChild(b);
            });
            document.body.classList.remove('modal-open');
            document.body.style.overflow    = '';
            document.body.style.paddingRight = '';
        """)
    except Exception:
        pass


# XPaths for the two confirmed close buttons inside the modal
_CLOSE_X_XPATH = (
    "//button[contains(@class,'close') and @data-dismiss='modal']"
)
_CLOSE_BTN_XPATH = (
    "//button[@data-dismiss='modal' and contains(@class,'primary_butn')]"
    "| //button[@data-dismiss='modal' and normalize-space(text())='Close']"
)
_ANY_CLOSE_XPATH = _CLOSE_X_XPATH + " | " + _CLOSE_BTN_XPATH


def _modal_visible_in_frame(driver) -> bool:
    try:
        mods = driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'modal') and "
            "(contains(@style,'display: block') or "
            " contains(@class,' in') or contains(@class,'show'))]"
        )
        for m in mods:
            if m.is_displayed():
                return True
    except Exception:
        pass
    return False


def close_modal_in_iframe(driver, timeout: int = 20) -> bool:
    """
    ★ KEY FIX ★
    The ICAI announcement popup lives inside iframe#frame1.
    This function:
      1. Switches INTO iframe#frame1
      2. Waits for the modal to appear
      3. Tries multiple close methods inside the iframe
      4. Switches BACK to default content
    """
    print("   [modal] Switching into iframe#frame1 …")
    iframe_found = False

    # Try to switch into the iframe (may be nested)
    try:
        # Primary: switch by id
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#frame1"))
        )
        driver.switch_to.frame("frame1")
        iframe_found = True
        print("   [modal] ✓ Switched into iframe#frame1.")
    except Exception:
        pass

    if not iframe_found:
        # Fallback: try all iframes and look for the modal inside each
        try:
            driver.switch_to.default_content()
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for iframe in iframes:
                try:
                    driver.switch_to.frame(iframe)
                    if _modal_visible_in_frame(driver):
                        iframe_found = True
                        iframe_id = iframe.get_attribute("id") or "(no id)"
                        print(f"   [modal] ✓ Found modal in iframe: {iframe_id}")
                        break
                    driver.switch_to.default_content()
                except Exception:
                    driver.switch_to.default_content()
        except Exception:
            pass

    if not iframe_found:
        print("   [modal] Could not find iframe with modal — trying in main frame.")

    # ── Wait for modal to appear in current frame ─────────────
    print("   [modal] Waiting for modal to appear …")
    deadline = time.time() + timeout
    appeared = False
    while time.time() < deadline:
        if _modal_visible_in_frame(driver):
            appeared = True
            break
        time.sleep(0.4)

    if not appeared:
        print("   [modal] No modal visible in this frame.")
        driver.switch_to.default_content()
        return False

    print("   [modal] Modal confirmed visible — closing …")
    time.sleep(0.5)

    closed = False

    # ── Strategy 1: jQuery Bootstrap hide (most reliable) ─────
    if not closed:
        try:
            driver.execute_script("""
                if (typeof $ !== 'undefined') {
                    $('#showResponseModal').modal('hide');
                    $('.conformationPopupModal').modal('hide');
                    $('.modal').modal('hide');
                }
            """)
            time.sleep(1.2)
            if not _modal_visible_in_frame(driver):
                print("   [modal] ✓ Closed via jQuery .modal('hide').")
                closed = True
        except Exception as ex:
            print(f"   [modal] jQuery strategy failed: {ex.__class__.__name__}")

    # ── Strategy 2: ActionChains click on × button ────────────
    if not closed:
        try:
            btns = driver.find_elements(By.XPATH, _CLOSE_X_XPATH)
            for btn in btns:
                if btn.is_displayed():
                    action_click(driver, btn)
                    time.sleep(1.2)
                    if not _modal_visible_in_frame(driver):
                        print("   [modal] ✓ Closed via ActionChains × button.")
                        closed = True
                    break
        except Exception as ex:
            print(f"   [modal] ActionChains × failed: {ex.__class__.__name__}")

    # ── Strategy 3: ActionChains click on Close button ────────
    if not closed:
        try:
            btns = driver.find_elements(By.XPATH, _CLOSE_BTN_XPATH)
            for btn in btns:
                if btn.is_displayed():
                    action_click(driver, btn)
                    time.sleep(1.2)
                    if not _modal_visible_in_frame(driver):
                        print("   [modal] ✓ Closed via ActionChains Close button.")
                        closed = True
                    break
        except Exception as ex:
            print(f"   [modal] ActionChains Close failed: {ex.__class__.__name__}")

    # ── Strategy 4: JS click on × button ─────────────────────
    if not closed:
        try:
            btns = driver.find_elements(By.XPATH, _CLOSE_X_XPATH)
            for btn in btns:
                js_click(driver, btn)
                time.sleep(1.2)
                if not _modal_visible_in_frame(driver):
                    print("   [modal] ✓ Closed via JS-click × button.")
                    closed = True
                break
        except Exception as ex:
            print(f"   [modal] JS × click failed: {ex.__class__.__name__}")

    # ── Strategy 5: JS click on Close button ─────────────────
    if not closed:
        try:
            btns = driver.find_elements(By.XPATH, _CLOSE_BTN_XPATH)
            for btn in btns:
                js_click(driver, btn)
                time.sleep(1.2)
                if not _modal_visible_in_frame(driver):
                    print("   [modal] ✓ Closed via JS-click Close button.")
                    closed = True
                break
        except Exception as ex:
            print(f"   [modal] JS Close click failed: {ex.__class__.__name__}")

    # ── Strategy 6: Escape key ────────────────────────────────
    if not closed:
        try:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1.2)
            if not _modal_visible_in_frame(driver):
                print("   [modal] ✓ Closed via Escape key.")
                closed = True
        except Exception as ex:
            print(f"   [modal] Escape key failed: {ex.__class__.__name__}")

    # ── Strategy 7: Force-hide all modals in DOM ──────────────
    if not closed:
        try:
            driver.execute_script("""
                document.querySelectorAll('.modal').forEach(function(m){
                    m.classList.remove('in','show');
                    m.style.display = 'none';
                    m.setAttribute('aria-hidden','true');
                });
                document.querySelectorAll('.modal-backdrop').forEach(function(b){
                    b.parentNode && b.parentNode.removeChild(b);
                });
                document.body.classList.remove('modal-open');
                document.body.style.overflow    = '';
                document.body.style.paddingRight = '';
            """)
            time.sleep(1.0)
            print("   [modal] ✓ Force-hidden all modals in iframe DOM.")
            closed = True
        except Exception as ex:
            print(f"   [modal] Force-hide failed: {ex.__class__.__name__}")

    # Clean up backdrop regardless
    _remove_backdrop_in_current_frame(driver)

    # ★ Always switch back to default content after iframe work ★
    print("   [modal] Switching back to default content …")
    try:
        driver.switch_to.default_content()
    except Exception:
        pass

    return closed


def handle_response_error(driver):
    """
    Check #responseDataBody (inside iframe#frame1) for error messages.
    If found, alert user and close the modal.
    """
    # Try inside iframe first
    try:
        driver.switch_to.frame("frame1")
        resp = driver.find_element(By.ID, "responseDataBody")
        if resp.is_displayed() and resp.text.strip():
            txt = resp.text.strip()
            driver.switch_to.default_content()
            print(f"[!] Portal notice: {txt}")
            show_dialog("e-Diary Portal Notice", txt, kind="warning")
            close_modal_in_iframe(driver, timeout=8)
            return True
        driver.switch_to.default_content()
    except Exception:
        try:
            driver.switch_to.default_content()
        except Exception:
            pass
    return False


# ══════════════════════════════════════════════════════════════
#  TKINTER GUI HELPERS  (all windows pinned Always-On-Top)
# ══════════════════════════════════════════════════════════════

def _center(win, w: int, h: int):
    win.update_idletasks()
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
    win.attributes("-topmost", True)
    win.lift()
    win.focus_force()
    win.resizable(False, False)


def _header(parent, text: str, bg: str = "#0d6efd"):
    tk.Label(parent, text=f"  {text}", bg=bg, fg="white",
             font=("Segoe UI", 12, "bold"), pady=10,
             anchor="w").pack(fill=tk.X)


def show_dialog(title: str, message: str, kind: str = "error"):
    palette = {"error": "#dc3545", "info": "#198754", "warning": "#fd7e14"}
    color   = palette.get(kind, "#0d6efd")
    root = tk.Tk()
    root.title(title)
    root.configure(bg="#f8f9fa")
    _center(root, 490, 250)
    _header(root, title, color)
    tk.Label(root, text=message, bg="#f8f9fa", fg="#212529",
             font=("Segoe UI", 10), wraplength=450,
             justify=tk.LEFT).pack(padx=24, pady=20)
    tk.Button(root, text="OK", command=root.destroy,
              bg=color, fg="white", relief=tk.FLAT, cursor="hand2",
              font=("Segoe UI", 10, "bold"), width=16).pack(pady=4)
    root.mainloop()


def gui_credentials(default_sro: str, default_pwd: str):
    placeholders = {"SRO0000000", "YourPassword", ""}
    if default_sro not in placeholders and default_pwd not in placeholders:
        return default_sro, default_pwd

    out = {"sro": "", "pwd": "", "ok": False}
    root = tk.Tk()
    root.title("ICAI e-Diary — Credentials")
    root.configure(bg="#f8f9fa")
    _center(root, 440, 295)
    root.protocol("WM_DELETE_WINDOW", sys.exit)

    _header(root, "Enter Portal Credentials")
    tk.Label(root, text="Credentials not set in script — please enter below:",
             bg="#f8f9fa", fg="#6c757d", font=("Segoe UI", 9)).pack(pady=(10, 4))

    frm = tk.Frame(root, bg="#f8f9fa", padx=28); frm.pack(fill=tk.X)
    tk.Label(frm, text="SRO Number:", bg="#f8f9fa",
             font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8)
    tk.Label(frm, text="Password:", bg="#f8f9fa",
             font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w", pady=8)
    sro_e = tk.Entry(frm, font=("Segoe UI", 10), width=28)
    sro_e.grid(row=0, column=1, pady=8, padx=8)
    if default_sro not in placeholders:
        sro_e.insert(0, default_sro)
    pwd_e = tk.Entry(frm, font=("Segoe UI", 10), width=28, show="*")
    pwd_e.grid(row=1, column=1, pady=8, padx=8)

    def _submit():
        s, p = sro_e.get().strip(), pwd_e.get().strip()
        if not s or not p:
            messagebox.showwarning("Incomplete",
                                   "Enter both SRO and Password.", parent=root)
            return
        out.update(sro=s, pwd=p, ok=True)
        root.destroy()

    tk.Button(root, text="▶  Start Automation", command=_submit,
              bg="#0d6efd", fg="white", relief=tk.FLAT, cursor="hand2",
              font=("Segoe UI", 10, "bold"), width=22).pack(pady=22)
    root.mainloop()

    if not out["ok"]:
        sys.exit(0)
    return out["sro"], out["pwd"]


def gui_duration_and_task():
    out = {"dur": "1", "code": "T1", "name": "Assurance Services"}
    root = tk.Tk()
    root.title("e-Diary — Duration & Task")
    root.configure(bg="#f8f9fa")
    _center(root, 520, 410)
    root.protocol("WM_DELETE_WINDOW", sys.exit)

    _header(root, "Step 1 of 3 — Select Duration & Task")
    body = tk.Frame(root, bg="#f8f9fa", padx=30, pady=18)
    body.pack(fill=tk.BOTH, expand=True)

    tk.Label(body, text="Duration:", bg="#f8f9fa",
             font=("Segoe UI", 11, "bold")).pack(anchor="w")
    dur_var = tk.StringVar(value="1")
    row_d = tk.Frame(body, bg="#f8f9fa"); row_d.pack(anchor="w", padx=12, pady=(5, 20))
    for txt, val in [("Full Day (1)", "1"), ("Half Day (0.5)", "0.5")]:
        tk.Radiobutton(row_d, text=txt, variable=dur_var, value=val,
                       bg="#f8f9fa", activebackground="#f8f9fa",
                       font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 30))

    tk.Label(body, text="Task Name:", bg="#f8f9fa",
             font=("Segoe UI", 11, "bold")).pack(anchor="w")
    items = [f"{c}  —  {n}" for c, n in TASK_OPTIONS]
    combo = ttk.Combobox(body, values=items, state="readonly",
                         font=("Segoe UI", 10), width=48)
    combo.current(0)
    combo.pack(anchor="w", padx=12, pady=(5, 24))

    def _next():
        idx = combo.current()
        out.update(dur=dur_var.get(),
                   code=TASK_OPTIONS[idx][0],
                   name=TASK_OPTIONS[idx][1])
        root.destroy()

    tk.Button(root, text="Next — Select Subtasks  ➜", command=_next,
              bg="#198754", fg="white", relief=tk.FLAT, cursor="hand2",
              font=("Segoe UI", 11, "bold"), padx=16, pady=8).pack(pady=6)
    root.mainloop()
    return out["dur"], out["code"], out["name"]


def gui_select_subtasks(labels: list) -> list:
    if not labels:
        return []
    selected = []
    root = tk.Tk()
    root.title("e-Diary — Select Subtasks (max 5)")
    root.configure(bg="#f8f9fa")
    _center(root, 550, 480)
    root.protocol("WM_DELETE_WINDOW", sys.exit)

    _header(root, "Step 2 of 3 — Select Subtasks  (maximum 5)")
    counter = tk.Label(root, text="Selected: 0 / 5", bg="#f8f9fa",
                       fg="#0d6efd", font=("Segoe UI", 10, "bold"))
    counter.pack(anchor="w", padx=18, pady=(6, 2))

    wrap   = tk.Frame(root, bg="#f8f9fa"); wrap.pack(fill=tk.BOTH, expand=True, padx=14, pady=4)
    canvas = tk.Canvas(wrap, bg="white", highlightthickness=1, highlightbackground="#ced4da")
    sb     = ttk.Scrollbar(wrap, orient="vertical", command=canvas.yview)
    inner  = tk.Frame(canvas, bg="white")
    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    sb.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.bind_all("<MouseWheel>",
                    lambda e: canvas.yview_scroll(-int(e.delta / 120), "units"))
    vars_ = []

    def _make_trace(var):
        def _cb(*_):
            total = sum(v.get() for v in vars_)
            if total > 5:
                var.set(0)
                counter.config(text="⚠  Max 5 selections!", fg="#dc3545")
                messagebox.showwarning("Limit Reached",
                                       "You can select at most 5 subtasks.",
                                       parent=root)
            else:
                counter.config(text=f"Selected: {total} / 5", fg="#0d6efd")
        return _cb

    for lbl in labels:
        v = tk.IntVar()
        v.trace_add("write", _make_trace(v))
        vars_.append(v)
        tk.Checkbutton(inner, text=f"  {lbl}", variable=v, bg="white",
                       activebackground="#e9ecef", anchor="w",
                       font=("Segoe UI", 9), pady=5).pack(fill=tk.X)

    def _confirm():
        nonlocal selected
        selected = [i for i, v in enumerate(vars_) if v.get()]
        canvas.unbind_all("<MouseWheel>")
        root.destroy()

    tk.Button(root, text="Confirm Subtasks  ➜", command=_confirm,
              bg="#198754", fg="white", relief=tk.FLAT, cursor="hand2",
              font=("Segoe UI", 10, "bold"), padx=20, pady=6).pack(pady=10)
    root.mainloop()
    return selected


def gui_other_task():
    out = {"text": None}
    root = tk.Tk()
    root.title("e-Diary — Other Task")
    root.configure(bg="#f8f9fa")
    _center(root, 480, 275)
    root.protocol("WM_DELETE_WINDOW", sys.exit)

    _header(root, "Step 3 of 3 — Other Task")
    body = tk.Frame(root, bg="#f8f9fa", padx=24, pady=18)
    body.pack(fill=tk.BOTH, expand=True)

    q_lbl = tk.Label(body, text="Do you have another task to record?",
                     bg="#f8f9fa", fg="#1e293b", font=("Segoe UI", 12, "bold"))
    q_lbl.pack(pady=(10, 22))

    btn_row   = tk.Frame(body, bg="#f8f9fa"); btn_row.pack()
    input_row = tk.Frame(body, bg="#f8f9fa")
    entry     = tk.Entry(input_row, font=("Segoe UI", 10), width=44)

    def _yes():
        btn_row.pack_forget()
        q_lbl.config(text="Enter the work you have done:")
        input_row.pack(pady=10)
        entry.pack(pady=4)
        entry.focus_set()

        def _save():
            out["text"] = entry.get().strip()
            root.destroy()

        tk.Button(input_row, text="Save & Continue", command=_save,
                  bg="#198754", fg="white", relief=tk.FLAT, cursor="hand2",
                  font=("Segoe UI", 10, "bold"), padx=16, pady=5).pack(pady=8)

    def _no():
        root.destroy()

    tk.Button(btn_row, text="  Yes  ", command=_yes, width=10,
              bg="#0d6efd", fg="white", relief=tk.FLAT, cursor="hand2",
              font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=16)
    tk.Button(btn_row, text="  No  ", command=_no, width=10,
              bg="#6c757d", fg="white", relief=tk.FLAT, cursor="hand2",
              font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=16)

    root.mainloop()
    return out["text"]


# ══════════════════════════════════════════════════════════════
#  IFRAME-AWARE ELEMENT HELPERS
#  (all dashboard elements also live inside iframe#frame1)
# ══════════════════════════════════════════════════════════════

def switch_to_frame1(driver, timeout: int = 15):
    """Switch into iframe#frame1 (the main app iframe)."""
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe#frame1"))
    )
    driver.switch_to.frame("frame1")


def find_in_frame1(driver, by, value, timeout: int = 20):
    """Switch to frame1 and return the located element."""
    switch_to_frame1(driver)
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


# ══════════════════════════════════════════════════════════════
#  MAIN AUTOMATION
# ══════════════════════════════════════════════════════════════

def run():
    sro, pwd = gui_credentials(USER_SRO, USER_PASSWORD)
    sro = sro.strip()
    user_id = sro if sro.upper().endswith("@ICAI.ORG") else f"{sro}@ICAI.ORG"

    sep = "═" * 60
    print(f"\n{sep}\n   ICAI e-Diary Automation — Starting\n{sep}")
    print(f"   User ID : {user_id}  |  Pace : {STEP_PAUSE}s\n{sep}")

    driver = None
    try:
        print("\n[*] Launching Chrome …")
        driver = webdriver.Chrome(options=build_chrome_options())
        W = WebDriverWait(driver, 25)

        # ─── STEP 1 ─ Navigate to portal ─────────────────────
        print("\n[Step 1] Opening https://eservices.icai.org …")
        driver.get("https://eservices.icai.org")
        pace(1)

        # ─── STEP 2 ─ Click "Click Here" (opens new tab) ─────
        print("[Step 2] Clicking the e-Diary 'Click Here' link …")
        tabs_before = set(driver.window_handles)
        link = W.until(EC.presence_of_element_located(
            (By.XPATH,
             "//a[contains(@class,'btn-primary-sp3') and contains(@href,'Ediary')]"
             "| //a[contains(@class,'btn-primary-sp3')"
             "   and normalize-space(text())='Click Here']")
        ))
        js_click(driver, link)
        pace()

        W.until(lambda d: len(d.window_handles) > len(tabs_before))
        new_tab = (set(driver.window_handles) - tabs_before).pop()
        driver.switch_to.window(new_tab)
        pace(1)
        print("[✓] Switched to e-Diary login tab.")

        # ─── STEP 3 ─ Enter User ID ───────────────────────────
        # Login elements are in the OUTER page (not inside iframe yet)
        print(f"[Step 3] Entering User ID: {user_id}")
        uid_inp = W.until(EC.presence_of_element_located((By.ID, "accountname")))
        uid_inp.clear()
        uid_inp.send_keys(user_id)
        pace()

        # ─── STEP 4 ─ Enter Password ──────────────────────────
        print("[Step 4] Entering Password …")
        pwd_inp = W.until(EC.presence_of_element_located((By.ID, "password")))
        pwd_inp.clear()
        pwd_inp.send_keys(pwd)
        pace()

        # ─── STEP 5 ─ Click Sign In ───────────────────────────
        print("[Step 5] Clicking Sign In …")
        sign_in = W.until(EC.presence_of_element_located(
            (By.XPATH,
             "//button[contains(@class,'loginBtn')]"
             "| //button[normalize-space(text())='Sign In']")
        ))
        js_click(driver, sign_in)

        # Portal takes ~5-6 s to authenticate and load iframe with popup
        print("[*] Waiting 6 s for dashboard and popup to appear …")
        time.sleep(6)
        driver.switch_to.default_content()

        # Login error check (in outer page)
        try:
            err_el = driver.find_element(By.ID, "loginPwdMsg")
            if err_el.is_displayed():
                err_txt = err_el.text.strip()
                if err_txt:
                    print(f"[!] LOGIN FAILED — {err_txt}")
                    show_dialog("Login Error",
                                f"{err_txt}\n\nCheck your SRO Number and Password.",
                                kind="error")
                    return
        except NoSuchElementException:
            pass
        print("[✓] Login successful.")
        pace()

        # ─── STEPS 6 & 7 ─ Close announcement popup ──────────
        # ★ The modal is inside iframe#frame1 ★
        print("\n[Steps 6–7] Closing announcement popup (inside iframe#frame1) …")
        close_modal_in_iframe(driver, timeout=20)
        driver.switch_to.default_content()
        pace()

        # ─── STEP 8 ─ Calendar → select today ────────────────
        # Calendar elements are inside iframe#frame1
        print("\n[Step 8] Selecting today's date …")
        switch_to_frame1(driver)
        cal = W.until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(@class,'glyphicon-calendar')]")
        ))
        js_click(driver, cal)
        pace(0.5)

        today = str(datetime.now().day)
        try:
            cell = driver.find_element(By.XPATH, "//td[contains(@class,'today')]")
            js_click(driver, cell)
            print(f"[✓] Today selected via .today cell.")
        except NoSuchElementException:
            cell = driver.find_element(
                By.XPATH,
                f"//td[contains(@class,'day')"
                f" and not(contains(@class,'old'))"
                f" and not(contains(@class,'new'))"
                f" and normalize-space(text())='{today}']"
            )
            js_click(driver, cell)
            print(f"[✓] Today selected: day {today}.")
        driver.switch_to.default_content()
        pace()

        handle_response_error(driver)

        # ─── STEPS 9 & 10 ─ GUI: Duration + Task ─────────────
        print("\n[Steps 9–10] Opening GUI for Duration & Task …")
        duration, task_code, task_name = gui_duration_and_task()
        print(f"[✓] Duration={duration}  Task={task_code} ({task_name})")
        pace()

        # Apply values inside iframe#frame1
        switch_to_frame1(driver)

        dur_el = W.until(EC.presence_of_element_located((By.ID, "taskDuration")))
        Select(dur_el).select_by_value(duration)
        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", dur_el)
        pace()

        task_el = W.until(EC.presence_of_element_located((By.ID, "taskName")))
        Select(task_el).select_by_value(task_code)
        driver.execute_script(
            "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", task_el)
        pace(0.5)

        # ─── STEP 11 ─ GUI: Subtasks (max 5) ─────────────────
        print("\n[Step 11] Handling subtasks …")
        # Still inside iframe#frame1
        raw_cbs = []
        try:
            open_btn = driver.find_element(By.ID, "openSubTasks")
            if open_btn.is_enabled():
                sub_div = driver.find_element(By.ID, "subTaskList")
                if not sub_div.is_displayed():
                    js_click(driver, open_btn)
                    pace()
                for cb in sub_div.find_elements(
                        By.CSS_SELECTOR, "input[type='checkbox']"):
                    label_txt = ""
                    cb_id = cb.get_attribute("id")
                    if cb_id:
                        lbls = driver.find_elements(
                            By.CSS_SELECTOR, f"label[for='{cb_id}']")
                        if lbls:
                            label_txt = lbls[0].text.strip()
                    if not label_txt:
                        try:
                            label_txt = cb.find_element(By.XPATH, "..").text.strip()
                        except Exception:
                            pass
                    label_txt = label_txt or \
                        f"Subtask ({cb.get_attribute('value') or '?'})"
                    raw_cbs.append((cb, label_txt))
            else:
                print("[i] Subtask button disabled for this task type.")
        except NoSuchElementException:
            print("[i] No subtasks for this task category.")

        driver.switch_to.default_content()

        if raw_cbs:
            chosen = gui_select_subtasks([t for _, t in raw_cbs])
            print(f"[✓] {len(chosen)} subtask(s) selected.")
            switch_to_frame1(driver)
            for idx in chosen:
                cb_el = raw_cbs[idx][0]
                try:
                    if not cb_el.is_selected():
                        js_click(driver, cb_el)
                        pace(0.3)
                except Exception as ex:
                    print(f"[!] Subtask click error #{idx}: {ex}")
            driver.switch_to.default_content()
        else:
            print("[i] No subtasks to select.")
        pace()

        # ─── STEP 12 ─ GUI: Other Task ───────────────────────
        print("\n[Step 12] Asking about Other Task …")
        other_text = gui_other_task()
        if other_text:
            print(f"[✓] Other task: '{other_text}'")
            try:
                switch_to_frame1(driver)
                ot = W.until(EC.presence_of_element_located((By.ID, "other_task")))
                ot.clear()
                ot.send_keys(other_text)
                driver.switch_to.default_content()
            except Exception as ex:
                print(f"[!] Could not set #other_task: {ex}")
                driver.switch_to.default_content()
        else:
            print("[i] No other task entered.")
        pace()

        # ─── STEP 13 ─ Save ───────────────────────────────────
        print("\n[Step 13] Clicking Save …")
        switch_to_frame1(driver)
        save_btn = W.until(EC.presence_of_element_located((By.ID, "submitTaskData")))
        js_click(driver, save_btn)
        driver.switch_to.default_content()
        pace(2)

        handle_response_error(driver)
        pace()

        # ─── STEP 14 ─ Profile dropdown ───────────────────────
        print("[Step 14] Opening profile dropdown …")
        switch_to_frame1(driver)
        profile = W.until(EC.presence_of_element_located(
            (By.XPATH,
             "//a[@id='dLabel']"
             "| //span[@id='studentShortName']/..")
        ))
        js_click(driver, profile)
        pace()

        # ─── STEP 15 ─ Logout ─────────────────────────────────
        print("[Step 15] Clicking Logout …")
        logout = W.until(EC.presence_of_element_located(
            (By.XPATH,
             "//button[contains(@onclick,'logoutProfile')]"
             "| //button[normalize-space(text())='Logout']")
        ))
        js_click(driver, logout)
        driver.switch_to.default_content()
        pace(1)
        print("[✓] Logged out successfully.")

        show_dialog("All Done! ✔",
                    "e-Diary entry saved and logout completed!",
                    kind="info")

    except Exception as exc:
        msg = clean_error(exc)
        print(f"\n[!] Unexpected error:\n{msg}")
        try:
            driver.switch_to.default_content()
        except Exception:
            pass
        show_dialog("Automation Error", msg, kind="error")

    finally:
        if driver:
            print("\n[*] Closing browser …")
            try:
                driver.quit()
            except Exception:
                pass
        print("[*] Script finished.")


# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    run()
