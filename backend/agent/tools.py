from langchain.tools import tool
# from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime
import math
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import TAVILY_API_KEY

os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

# ── Tool 1: Web Search ──────────────────────────────────────────
web_search_tool = TavilySearch(
    max_results=5,
    description="Search the web for current information, news, internships, frameworks, anything real-time."
)

# ── Tool 2: Wikipedia Search ────────────────────────────────────
wikipedia_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1000),
)

# ── Tool 3: Calculator ──────────────────────────────────────────
@tool
def calculator(expression: str) -> str:
    """Evaluates a math expression. Input must be a plain math expression string like '2+2' or '10*5'. Nothing else."""
    try:
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

# ── Tool 4: DateTime Tool ───────────────────────────────────────
@tool
def datetime_tool(dummy: str = "") -> str:
    """Returns the current date, time, and day of week. Call this whenever you need to know today's date or current time. No input required."""
    now = datetime.now()
    return (
        f"Current datetime: {now.strftime('%A, %B %d, %Y %I:%M %p')}\n"
        f"Day of week: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%Y-%m-%d')}"
    )

# ── Tool 5: Email Draft Tool ────────────────────────────────────
@tool
def email_draft_tool(input: str) -> str:
    """
    Drafts a complete professional email.
    Input format: 'to:<email> | subject:<subject> | body:<body>'
    If body is not provided, generate a professional email body automatically.
    Example: 'to:rahul@gmail.com | subject:Meeting Agenda | body:discuss project updates'
    """
    try:
        parts = dict(p.strip().split(":", 1) for p in input.split("|"))
        to = parts.get("to", "recipient@email.com").strip()
        subject = parts.get("subject", "No Subject").strip()
        body_hint = parts.get("body", "").strip()

        # Build full drafted email
        drafted_email = f"""
            ✅ Email Drafted Successfully!
            {'='*45}
            To      : {to}
            Subject : {subject}
            {'='*45}

            Dear {to.split('@')[0].capitalize()},

            {body_hint}

            Please let me know if you need anything else.

            Best regards,
            Abhishek Godara
            {'='*45}
            [Simulated — connects to Gmail API in production]
                    """

        return drafted_email.strip()

    except Exception as e:
        return f"Error drafting email: {str(e)}"

# ── Tool 6: Reminder Tool ───────────────────────────────────────
reminders = []

@tool
def reminder_tool(input: str) -> str:
    """Saves a reminder for the user. Input format: 'task:<task> | date:<date>'"""
    try:
        parts = dict(p.strip().split(":", 1) for p in input.split("|"))
        task = parts.get("task", "").strip()
        date = parts.get("date", "").strip()
        reminders.append({"task": task, "date": date})
        return f"✅ Reminder saved!\nTask: {task}\nDate: {date}"
    except Exception as e:
        return f"Error: {str(e)}"

# ── All tools list (imported by agent) ─────────────────────────
all_tools = [
    web_search_tool,
    wikipedia_tool,
    calculator,
    datetime_tool,
    email_draft_tool,
    reminder_tool,
]