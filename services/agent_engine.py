import pyautogui
import pyperclip
import time
import re
import pygetwindow as gw
from typing import List, Set
from services.logger import LiveLogger


class GmailAgent:
    def __init__(self, logger: LiveLogger):
        self.logger = logger
        self.abort = False
        pyautogui.FAILSAFE = True

    def request_abort(self):
        self.abort = True

    def _focus_gmail(self) -> bool:
        titles = gw.getAllTitles()
        gmail_titles = [t for t in titles if "gmail" in t.lower() or "mail" in t.lower()]
        if gmail_titles:
            win = gw.getWindowsWithTitle(gmail_titles[0])[0]
            if win.isMinimized:
                win.restore()
            win.activate()
            time.sleep(2)
            return True
        return False

    def _copy_normal_view(self) -> str:
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.3)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.5)
        return pyperclip.paste()

    def _extract_pos(self, text: str):
        m = re.search(r"(\d+)\s+of\s+(\d+)", text)
        if m:
            return int(m.group(1)), int(m.group(2))
        return None, None

    def _copy_show_original(self) -> str:
        before = gw.getActiveWindow().title

        pyautogui.press(".")
        time.sleep(0.8)
        pyautogui.press("s")
        time.sleep(3)

        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.3)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.5)
        text = pyperclip.paste()

        after = gw.getActiveWindow().title
        if after != before:
            pyautogui.hotkey("ctrl", "w")
            time.sleep(1.5)
            self._focus_gmail()

        return text

    def process_extraction(self, sender_email: str, parser, max_limit: int = 30) -> List[str]:
        if not self._focus_gmail():
            raise ConnectionError("Gmail not detected. Open Gmail in Chrome first.")

        self.logger.log("Searching sender", "Agent", "STARTED")
        pyautogui.press("/")
        time.sleep(0.5)
        pyautogui.write(f"from:{sender_email}", interval=0.05)
        pyautogui.press("enter")
        time.sleep(4)

        pyautogui.press("u")
        time.sleep(1)

        results: Set[str] = set()

        for i in range(max_limit):
            if self.abort:
                self.logger.log("Abort requested. Stopping.", "Agent", "FAILED")
                break

            if i > 0:
                pyautogui.press("j")
                time.sleep(1)

            pyautogui.press("enter")
            time.sleep(3)

            # Copy normal view to read "x of y"
            normal_text = self._copy_normal_view()
            cur, total = self._extract_pos(normal_text)

            self.logger.log(
                f"Processing mail {cur or i+1} of {total or '?'}",
                "Agent",
                "STARTED"
            )

            raw = self._copy_show_original()
            emails = parser.extract_emails([raw])
            for e in emails:
                results.add(e)

            pyautogui.press("u")
            time.sleep(2)

            # Stop if x of y says we reached the end
            if cur and total and cur >= total:
                self.logger.log("Reached last mail based on x of y.", "Logic", "SUCCESS")
                break

        return sorted(results)
