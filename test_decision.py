import time
import httpx

URL = "http://127.0.0.1:8000/v1/systemone"

# Option name -> description. The model reads these descriptions.
ACTIONS = {
    "work": "Do your job: bake, farm, forge, or serve at the tavern.",
    "eat": "Get food or a drink because you are hungry.",
    "sleep": "Go rest because you are tired or it is night.",
    "socialize": "Talk with other villagers and spend time together.",
    "wander": "Walk around with no particular goal.",
    "trade": "Buy or sell goods at the market.",
}

QUESTION = {
    "next_action": {
        "type": "choice",
        "instructions": "Which action should this villager take next?",
        "criteria": ACTIONS,
    }
}

def decide(state):
    body = {"state": state, "questions": QUESTION}
    start = time.perf_counter()
    r = httpx.post(URL, json=body, timeout=120)
    ms = (time.perf_counter() - start) * 1000
    r.raise_for_status()
    return r.json()["answers"]["next_action"], ms

TEST_STATES = [
    {"name": "Mira", "job": "baker", "time": "12:30", "hunger": 9, "energy": 7,
     "mood": "cheerful", "nearby": [], "last_action": "work"},
    {"name": "Tomas", "job": "farmer", "time": "23:50", "hunger": 2, "energy": 1,
     "mood": "tired", "nearby": [], "last_action": "work"},
    {"name": "Lena", "job": "bard", "time": "20:15", "hunger": 3, "energy": 8,
     "mood": "lonely", "nearby": ["Mira", "Tomas"], "last_action": "wander"},
]

if __name__ == "__main__":
    for state in TEST_STATES:
        for run in range(3):  # one at a time: the Mac server can crash on concurrent requests
            answer, ms = decide(state)
            top = sorted(answer["probabilities"].items(), key=lambda kv: -kv[1])[:3]
            print(f'{state["name"]:6} run {run + 1}: {answer["choice"]:10} '
                  f'confidence={answer["confidence"]:.2f}  {ms:6.0f} ms  top3={top}')
