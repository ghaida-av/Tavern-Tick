"""Tavern Tick: a tiny town where Strands Decider picks every villager's next action."""
import argparse, json, os, statistics
from collections import Counter
from patterns.next_action import decide, state_to_text

WORKPLACE = {"baker": "bakery", "farmer": "farm", "bard": "tavern", "merchant": "market",
             "innkeeper": "tavern", "blacksmith": "forge", "fishmonger": "docks", "retired": "square"}
GOODS = {"baker": "tray of fresh bread", "farmer": "sack of produce",
         "fishmonger": "basket of fresh fish", "merchant": "cart of cloth and spices"}


class Villager:
    def __init__(self, name, job, hunger, energy, since_social=0):
        self.name, self.job = name, job
        self.hunger, self.energy = hunger, energy
        self.carrying = GOODS["merchant"] if job == "merchant" else None
        self.place = f"home:{name}"
        self.last, self.mood, self.since_social = "sleep", "calm", since_social

    def state(self, hour, nearby):
        s = {"name": self.name, "job": self.job, "time": f"{hour:02d}:00",
             "hunger": self.hunger, "energy": self.energy, "mood": self.mood,
             "nearby": nearby, "last_action": self.last}
        if self.carrying:
            s["carrying"] = self.carrying
        return s

    def apply(self, action):
        self.hunger = min(10, self.hunger + 0.6)
        self.energy = max(0, self.energy - 0.35)
        self.since_social += 1
        if action == "work":
            self.energy = max(0, self.energy - 0.4)
            self.place = WORKPLACE[self.job]
            if self.job in GOODS:
                self.carrying = GOODS[self.job]
        elif action == "eat":
            self.hunger = max(0, self.hunger - 6)
            self.place = "tavern"
        elif action == "sleep":
            self.energy = min(10, self.energy + 4)
            self.hunger = max(0, self.hunger - 0.3)  # resting slows hunger a little
            self.place = f"home:{self.name}"
        elif action == "socialize":
            self.since_social = 0
            self.place = "tavern"
        elif action == "wander":
            self.place = "square"
        elif action == "trade":
            self.place = "market"
            self.carrying = None
        self.last = action
        if self.energy <= 3: self.mood = "tired"
        elif self.hunger >= 8: self.mood = "grumpy"
        elif self.since_social >= 6: self.mood = "lonely"
        elif action in ("socialize", "eat", "trade"): self.mood = "cheerful"
        else: self.mood = "calm"


def make_town():
    return [Villager("Mira", "baker", 4, 9), Villager("Tomas", "farmer", 3, 9),
            Villager("Lena", "bard", 3, 8, since_social=8), Villager("Odo", "merchant", 2, 9),
            Villager("Greta", "innkeeper", 5, 8), Villager("Hale", "blacksmith", 2, 10),
            Villager("Wren", "fishmonger", 4, 9), Villager("Old Bram", "retired", 1, 8, since_social=4)]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ticks", type=int, default=24)
    ap.add_argument("--start-hour", type=int, default=6)
    ap.add_argument("--out", default="runs/day1.jsonl")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    town = make_town()
    decide(state_to_text(town[0].state(args.start_hour, [])))  # warm-up, not logged
    lat, actions, asks, total = [], Counter(), 0, 0
    with open(args.out, "w") as log:
        for t in range(args.ticks):
            hour = (args.start_hour + t) % 24
            places = {v.name: v.place for v in town}  # who is where at the start of the tick
            for v in town:
                nearby = [o.name for o in town if o is not v and places[o.name] == places[v.name]]
                text = state_to_text(v.state(hour, nearby))
                d = decide(text)
                v.apply(d.choice)
                total += 1; asks += d.escalate; lat.append(d.latency_ms); actions[d.choice] += 1
                print(f'{hour:02d}:00 {v.name:9} {d.choice:10} conf={d.confidence:.2f} '
                      f'{"ASK" if d.escalate else "   "} {d.latency_ms:4.0f}ms  now at {v.place}')
                log.write(json.dumps({"tick": t, "hour": hour, "villager": v.name, "state": text,
                                      "choice": d.choice, "confidence": round(d.confidence, 3),
                                      "latency_ms": round(d.latency_ms), "escalate": d.escalate,
                                      "place": v.place}) + "\n")
            print()
    lat.sort()
    print(f"decisions: {total}   median latency: {statistics.median(lat):.0f} ms   "
          f"p95: {lat[int(len(lat) * 0.95) - 1]:.0f} ms")
    print(f"flagged for escalation (confidence < 0.30): {asks} ({100 * asks / total:.0f}%)")
    print("actions:", dict(actions.most_common()))
