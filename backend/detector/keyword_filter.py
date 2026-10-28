import json
from pathlib import Path


# Locate the rules file independently of the terminal's working directory.
RULES_FILE = (
    Path(__file__).resolve().parent.parent
    / "rules"
    / "attack_patterns.json"
)


def load_rules() -> dict:
    """Load and validate the attack-pattern configuration."""

    with RULES_FILE.open("r", encoding="utf-8") as file:
        rules = json.load(file)

    if not isinstance(rules, dict):
        raise ValueError("Attack patterns must be a JSON object.")

    keywords = rules.get("danger_keywords")

    if not isinstance(keywords, list):
        raise ValueError(
            "'danger_keywords' must be a list."
        )

    if not all(
        isinstance(keyword, str) and keyword.strip()
        for keyword in keywords
    ):
        raise ValueError(
            "Every danger keyword must be a non-empty string."
        )

    # Normalize and remove duplicate entries.
    rules["danger_keywords"] = list(
        dict.fromkeys(
            keyword.strip().casefold()
            for keyword in keywords
        )
    )

    return rules


RULES = load_rules()


def keyword_scan(text: str) -> dict:
    """Find configured keyword indicators in webpage text."""

    if not isinstance(text, str):
        raise TypeError("text must be a string.")

    normalized_text = text.casefold()

    matched_keywords = [
        keyword
        for keyword in RULES["danger_keywords"]
        if keyword in normalized_text
    ]

    score = min(len(matched_keywords) * 15, 100)

    return {
        "score": score,
        "matched_keywords": matched_keywords,
    }