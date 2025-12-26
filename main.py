import streamlit as st
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from services.logger import LiveLogger
from services.agent_engine import GmailAgent
from services.groq_parser import GroqParser

load_dotenv()
st.set_page_config(page_title="WorkCortex | Source Agent", layout="wide")

if "logs" not in st.session_state:
    st.session_state.logs = []

if "agent" not in st.session_state:
    st.session_state.agent = None

st.title("Autonomous Gmail Intelligence")
st.caption("Shortcut Driven Recipient Extraction")

with st.sidebar:
    st.header("Config")
    sender = st.text_input("Target Email", "newsletter@github.com")

    if st.button("Reset Dashboard"):
        st.session_state.logs = []
        st.session_state.agent = None
        st.rerun()

log_ui = st.empty()
logger = LiveLogger(log_ui)

col1, col2 = st.columns(2)
run_clicked = col1.button("🚀 Run Agent")
abort_clicked = col2.button("🛑 Abort")

if abort_clicked and st.session_state.agent:
    st.session_state.agent.request_abort()
    st.warning("Abort requested. Finishing current step...")

if run_clicked:
    try:
        agent = GmailAgent(logger)
        st.session_state.agent = agent

        parser = GroqParser()
        emails = agent.process_extraction(sender, parser)

        if emails:
            df = pd.DataFrame(emails, columns=["Recipient Emails"])
            path = f"results_{datetime.now().strftime('%H%M%S')}.xlsx"
            df.to_excel(path, index=False)

            logger.log("Generating Excel", "Pandas", "SUCCESS")
            st.success(f"Extracted {len(emails)} IDs.")
            st.dataframe(df, width="stretch")
        else:
            st.warning("No recipients found.")

    except Exception as e:
        st.error(f"Error: {e}")

    finally:
        st.session_state.agent = None
