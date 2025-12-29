# Automated Gmail Recipient Extractor

This project automates Gmail using Python to extract all recipient email addresses from mails sent by a specific sender.  
It opens Gmail in Chrome, searches mails, opens each one, reads full headers using Gmail shortcuts, and exports unique recipients to an Excel file.

Built with Streamlit for UI and PyAutoGUI for browser control.

---

## What this tool does

1. Focuses the Gmail tab in Chrome  
2. Searches using from:sender@example.com  
3. Opens mails one by one  
4. Uses Gmail shortcut to open Show original headers  
5. Copies headers and extracts To, Cc, Bcc email IDs  
6. Stops automatically when it reaches x of y mails  
7. Saves all unique recipients to an Excel file  

---

## Project structure

project  
│  
│ main.py  
│ services  
│   │ agent_engine.py  
│   │ groq_parser.py  
│   │ logger.py  
│  
│ .env  
│ requirements.txt  

---

## Setup

### 1. Create virtual environment

python -m venv venv  
venv\Scripts\activate

### 2. Install dependencies

pip install streamlit pyautogui pyperclip pygetwindow pandas openpyxl python-dotenv

Make sure numpy version is below 2.

pip install "numpy<2"

---

## Environment variables

Create a file named .env in the root:

GROQ_API_KEY=your_key_here

Even though extraction uses regex, the key can stay for future extensions.

---

## Run the app

streamlit run main.py

---

## How to use

1. Open Gmail in Chrome and log in  
2. Make sure Gmail is in English and keyboard shortcuts are enabled  
3. Run the Streamlit app  
4. Enter sender email in sidebar  
5. Click Run Agent  
6. Do not touch mouse or keyboard while it runs  
7. Results will be saved as results_HHMMSS.xlsx  

---

## Gmail shortcut flow used

When a mail is open:

. opens More actions menu  
s opens Show original  
Ctrl A selects all  
Ctrl C copies headers  
Ctrl W closes the tab  
u goes back to thread list  

This is repeated for each mail.

---

## Known limitations

• Depends on Gmail UI and shortcuts  
• Requires Chrome and visible browser window  
• Timing sensitive under slow networks  
• Show original shortcut may vary across accounts  
• Not suitable for headless execution  
• Slower for very large inboxes  

These are documented intentionally for transparency.

---
## Screenshots

<img width="1889" height="896" alt="image" src="https://github.com/user-attachments/assets/9d38814b-946d-4719-aba4-6c557383ebc2" />

---




<img width="891" height="523" alt="image" src="https://github.com/user-attachments/assets/a1fc2a53-8fba-47c2-aad2-af59fe3cd9d5" />


## Safety

PyAutoGUI controls your mouse and keyboard.  
Keep mouse at top left corner to trigger failsafe if needed.

---

## Output

An Excel file is created in the project directory containing:

Recipient Emails

All values are unique.

## Author

Built by Kanishka.
