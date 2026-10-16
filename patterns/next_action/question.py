"""The typed question and option set for the 'next action' decision."""

# Option name -> when to choose it. The model reads these descriptions,
# so they say WHEN to pick each option, not just what it is.
ACTIONS = {
    "work": "Do your job. Choose this when the villager is rested and not hungry during working hours, from morning to late afternoon.",
    "eat": "Get food or a drink. Choose this when the villager is hungry or starving, at any time of day.",
    "sleep": "Go to bed or rest. Choose this when the villager is tired or exhausted, or it is the middle of the night.",
    "socialize": "Talk with other villagers who are nearby. Choose this when others are nearby and the villager is lonely or cheerful with free time.",
    "wander": "Stroll around aimlessly. Choose this only when nothing else is needed and nobody is nearby to talk to.",
    "trade": "Go to the market to sell goods. Choose this whenever the villager is carrying goods such as fish, cloth, spices or produce, during market hours (morning to late afternoon).",
}

def build_question(actions=None):
    return {
        "next_action": {
            "type": "choice",
            "instructions": "Which action should this villager take next?",
            "criteria": actions or ACTIONS,
        }
    }
