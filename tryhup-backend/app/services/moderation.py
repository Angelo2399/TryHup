from typing import Dict


# ===============================
# AI MODERATION PIPELINE (V1)
# ===============================
def moderate_comment(text: str) -> Dict[str, object]:
    """
    Moderation pipeline centralizzata.
    In futuro verrà sostituita / estesa con AI reale (LLM).
    """

    lowered = text.lower()

    # 🔴 blacklist iniziale (placeholder)
    banned_words = [
        "idiot",
        "stupid",
        "hate",
        "fuck",
        "shit",
        "bastard",
    ]

    score = 0
    is_flagged = False
    is_approved = True
    note = "Approved automatically"

    for word in banned_words:
        if word in lowered:
            score += 50
            is_flagged = True
            is_approved = False
            note = "Toxic language detected"
            break

    # 🟠 Controllo aggressività passiva (placeholder)
    if "!!!" in text or text.isupper():
        score += 20
        is_flagged = True
        is_approved = False
        note = "Aggressive tone detected"

    # 🟢 Default: educato / neutro
    if score == 0:
        note = "Clean comment"

    return {
        "is_approved": is_approved,
        "is_flagged": is_flagged,
        "score": score,
        "note": note,
    }
