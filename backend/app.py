from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os
import re
from datetime import datetime

app = FastAPI()
BASE = os.path.dirname(os.path.abspath(__file__))

FAQ_FILE = os.environ.get("FAQ_FILE", "business_faq.json")
with open(os.path.join(BASE, FAQ_FILE)) as f:
    FAQ = json.load(f)

LEADS_FILE = os.path.join(BASE, "leads.jsonl")

STOPWORDS = set(
    "a an the is are was were be been do does did will would can could "
    "should have has had i you he she it we they my your his her its our "
    "their me him us them this that these those and or but of in on at to "
    "for with as by from what when where which who how many much there here".split()
)


def stem(t: str) -> str:
    # naive stemming so "patients" matches "patient", "hours" matches "hour"
    if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
        return t[:-1]
    return t


def tokens(s: str):
    return [stem(t) for t in re.findall(r"[a-z0-9]+", s.lower()) if t not in STOPWORDS]


for item in FAQ["faqs"]:
    item["_tokens"] = set(tokens(item["q"] + " " + " ".join(item.get("keywords", []))))

# session_id -> {"awaiting_contact": bool, "last_q": str}
sessions = {}


class ChatIn(BaseModel):
    message: str
    session_id: str = "anon"


@app.post("/chat")
def chat(inp: ChatIn):
    state = sessions.get(inp.session_id, {})

    # Step 2 of lead capture: they just gave contact info, save it.
    if state.get("awaiting_contact"):
        lead = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "session": inp.session_id,
            "question": state.get("last_q", ""),
            "contact": inp.message,
        }
        with open(LEADS_FILE, "a") as f:
            f.write(json.dumps(lead) + "\n")
        sessions[inp.session_id] = {}
        return {
            "reply": (
                f"Thanks! Someone from {FAQ['business_name']} will reach out to you "
                "shortly. Anything else I can help with?"
            )
        }

    q_tokens = set(tokens(inp.message))
    best, best_score = None, 0
    for item in FAQ["faqs"]:
        score = len(q_tokens & item["_tokens"])
        if score > best_score:
            best, best_score = item, score

    if best and best_score >= 1:
        return {"reply": best["a"]}

    # No good answer: capture the lead instead of saying "I don't know".
    sessions[inp.session_id] = {"awaiting_contact": True, "last_q": inp.message}
    return {"reply": FAQ["fallback"]}


@app.get("/leads")
def leads():
    """Business owner checks captured leads here."""
    if not os.path.exists(LEADS_FILE):
        return []
    with open(LEADS_FILE) as f:
        return [json.loads(line) for line in f if line.strip()]


app.mount("/widget", StaticFiles(directory=os.path.join(BASE, "..", "widget")), name="widget")


@app.get("/")
def demo_page():
    return FileResponse(os.path.join(BASE, "demo.html"))
