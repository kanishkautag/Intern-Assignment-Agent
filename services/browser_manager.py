import os
import json
import re
from groq import Groq
from typing import List

class GroqParser:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile" # Llama 3.3 for reasoning

    def extract_emails(self, thread_list: List[str]) -> List[str]:
        if not thread_list: return []
        
        combined_text = "\n---HEADER_START---\n".join(thread_list)
        prompt = f"""
        Extract unique recipient email addresses from 'To:', 'Cc:', and 'Bcc:' headers.
        Return ONLY a JSON array of strings. Exclude the sender's address.
        
        TEXT:
        {combined_text[:12000]}
        """

        try:
            # Deterministic output for data extraction
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0,
            )
            content = completion.choices[0].message.content
            # Regex fallback to find the JSON array
            match = re.search(r'\[.*\]', content, re.DOTALL)
            if match:
                emails = json.loads(match.group(0))
                return sorted(list(set(str(e).lower().strip() for e in emails if "@" in str(e))))
            return []
        except:
            return []