import re
from typing import List

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

class GroqParser:
    def __init__(self):
        pass

    def extract_emails(self, texts: List[str]) -> List[str]:
        results = set()
        for text in texts:
            found = re.findall(EMAIL_REGEX, text or "")
            for e in found:
                results.add(e.lower().strip())
        return sorted(results)
