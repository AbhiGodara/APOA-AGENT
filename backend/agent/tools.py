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
    """
    Evaluates a mathematical expression and returns the result.
    Input should be a valid Python math expression like '2 + 2' or 'math.sqrt(16)'.
    """
    try:
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"

# ── Tool 4: DateTime Tool ───────────────────────────────────────
@tool
def datetime_tool(query: str) -> str:
    """
    Returns the current date and time.
    Use this when user asks about current date, time, day, or wants to schedule something.
    """
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
    Drafts and simulates sending an email.
    Input format: 'to:<email> | subject:<subject> | body:<body>'
    Example: 'to:rahul@gmail.com | subject:Meeting Agenda | body:Hi Rahul, ...'
    """
    try:
        parts = dict(p.strip().split(":", 1) for p in input.split("|"))
        to = parts.get("to", "unknown@email.com").strip()
        subject = parts.get("subject", "No Subject").strip()
        body = parts.get("body", "").strip()

        return (
            f"✅ Email drafted successfully!\n"
            f"To: {to}\n"
            f"Subject: {subject}\n"
            f"Body preview: {body[:100]}...\n"
            f"[Simulated send — in production, connects to Gmail API]"
        )
    except Exception as e:
        return f"Error drafting email: {str(e)}"

# ── Tool 6: Reminder Tool ───────────────────────────────────────
reminders = []

@tool
def reminder_tool(input: str) -> str:
    """
    Saves a reminder for the user.
    Input format: 'task:<task> | date:<date>'
    Example: 'task:Submit report | date:Monday March 16'
    """
    try:
        parts = dict(p.strip().split(":", 1) for p in input.split("|"))
        task = parts.get("task", "").strip()
        date = parts.get("date", "").strip()

        reminders.append({"task": task, "date": date})

        return (
            f"✅ Reminder saved!\n"
            f"Task: {task}\n"
            f"Date: {date}\n"
            f"Total reminders stored: {len(reminders)}"
        )
    except Exception as e:
        return f"Error saving reminder: {str(e)}"

# ── All tools list (imported by agent) ─────────────────────────
all_tools = [
    web_search_tool,
    wikipedia_tool,
    calculator,
    datetime_tool,
    email_draft_tool,
    reminder_tool,
]