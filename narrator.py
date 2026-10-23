"""Resolve low-confidence decisions and narrate them.
NARRATOR=stub    -> no AWS; accepts Decider's choice (development only)
NARRATOR=bedrock -> Amazon Bedrock picks the action and writes one story line
"""
import json, os

PROVIDER = os.environ.get("NARRATOR", "stub")
MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "")
REGION = os.environ.get("AWS_REGION", "us-east-1")
STATS = {"provider": PROVIDER, "escalated": 0, "agreed": 0, "overruled": 0, "errors": 0}
_client = None


def _stub(name, d):
    return d.choice, f"{name} hesitates, then decides to {d.choice}."


def _bedrock(name, text, d):
    global _client
    if _client is None:
        import boto3
        _client = boto3.client("bedrock-runtime", region_name=REGION)
    from patterns.next_action import ACTIONS
    top = sorted(d.probabilities.items(), key=lambda kv: -kv[1])[:3]
    prompt = (
        "You run a tiny medieval town simulation. A small decision model was unsure what this villager "
        "should do next.\n\n"
        f"Situation: {text}\n"
        f"Allowed actions: {', '.join(ACTIONS)}\n"
        f"The decision model's top guesses: {', '.join(f'{k} ({v:.2f})' for k, v in top)}\n\n"
        'Reply with ONLY JSON: {"action": "<one allowed action>", "story": "<one short, vivid sentence about the villager>"}'
    )
    resp = _client.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 120, "temperature": 0.7},
    )
    raw = resp["output"]["message"]["content"][0]["text"].strip()
    raw = raw[raw.find("{"): raw.rfind("}") + 1]
    out = json.loads(raw)
    action = out["action"] if out.get("action") in ACTIONS else d.choice
    return action, out.get("story")


def resolve(name, text, d):
    """Returns (final_action, story_or_None). High-confidence decisions pass straight through."""
    if not d.escalate:
        return d.choice, None
    STATS["escalated"] += 1
    try:
        final, story = _stub(name, d) if PROVIDER == "stub" else _bedrock(name, text, d)
    except Exception as e:  # never let a failed narrator call stop the town
        STATS["errors"] += 1
        print(f"      ! narrator error: {type(e).__name__}: {e}")
        return d.choice, None
    STATS["agreed" if final == d.choice else "overruled"] += 1
    return final, story
