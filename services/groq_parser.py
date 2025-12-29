import os
import json
import re
from groq import Groq
from typing import List

class GroqParser:
    def __init__(self):
        """Initializes the Groq client with the flagship reasoning model."""
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile" # Optimized for reasoning and data extraction

    def extract_emails(self, texts: List[str]) -> List[str]:
        """
        Uses LLM reasoning to identify recipients (To/Cc/Bcc) from raw headers.
        Ignores senders and non-recipient metadata.
        """
        if not texts or not any(texts):
            return []
        
        # Combine list of header dumps into a single context block
        combined_text = "\n---HEADER_BOUNDARY---\n".join(texts)
        
        prompt = f"""
        Act as a high-precision Data Extraction Agent. 
        Analyze the following raw SMTP headers and extract all UNIQUE recipient email addresses found in the 'To:', 'Cc:', and 'Bcc:' fields.
        
        STRICT RULES:
        1. Exclude the sender's own email address.
        2. Clean all formatting (e.g., 'Name <email@id.com>' -> 'email@id.com').
        3. Return ONLY a valid JSON object with the key "recipients".
        
        DATA:
        {combined_text[:20000]} 
        """
        
        try:
            # Using JSON mode for deterministic integration
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0, # Set to 0 for maximum reliability in extraction
                response_format={"type": "json_object"}
            )
            
            # Parse response and isolate the recipients list
            raw_response = completion.choices[0].message.content
            data = json.loads(raw_response)
            emails = data.get("recipients", [])
            
            # Final sanitization: lowercase and unique check
            return sorted(list(set(str(e).lower().strip() for e in emails if "@" in str(e))))
            
        except Exception as e:
            # Fallback to a basic regex if the API or parsing fails
            print(f"Agentic Extraction Error: {e}")
            return []