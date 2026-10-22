
import os, time
from dataclasses import dataclass
import httpx
from .question import build_question

URL = os.environ.get("DECIDER_URL", "http://127.0.0.1:8000/v1/systemone")
ESCALATE_BELOW = 0.30  # below this confidence, hand the decision to Bedrock
_client = httpx.Client(timeout=120)

@dataclass
class Decision:
    choice: str
    confidence: float
    probabilities: dict
    latency_ms: float
    escalate: bool

def decide(state_text, escalate_below=ESCALATE_BELOW, actions=None):
    start = time.perf_counter()
    r = _client.post(URL, json={"state": state_text, "questions": build_question(actions)})
    ms = (time.perf_counter() - start) * 1000
    r.raise_for_status()
    a = r.json()["answers"]["next_action"]
    return Decision(a["choice"], a["confidence"], a["probabilities"], ms, a["confidence"] < escalate_below)
