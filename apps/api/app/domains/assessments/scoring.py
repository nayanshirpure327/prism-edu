from typing import List, Dict, Any


def score_aptitude_assessment(answers: List[Dict[str, Any]], questions: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Score aptitude assessment answers by category.
    Questions contain options with assigned score (0-3).
    Returns normalized scores (0-100) per category.
    """
    # Map question_id to question
    q_map = {str(q.get("id")): q for q in questions}
    categories = ["logical", "verbal", "numerical", "spatial", "analytical"]
    raw_scores = {c: 0.0 for c in categories}
    max_scores = {c: 0.0 for c in categories}

    for q in questions:
        cat = q.get("category", "").lower()
        # Normalize category name
        matched_cat = None
        for c in categories:
            if c in cat:
                matched_cat = c
                break
        if not matched_cat:
            matched_cat = "analytical"

        options = q.get("options") or []
        # Find maximum possible score for this question
        max_opt = max([opt.get("score", 0) for opt in options], default=3)
        max_scores[matched_cat] += max_opt

    for ans in answers:
        q_id = str(ans.get("question_id"))
        q = q_map.get(q_id)
        if not q:
            continue
        cat = q.get("category", "").lower()
        matched_cat = None
        for c in categories:
            if c in cat:
                matched_cat = c
                break
        if not matched_cat:
            matched_cat = "analytical"

        raw_scores[matched_cat] += float(ans.get("raw_score", 0))

    # Normalize to 0-100
    normalized = {}
    for c in categories:
        if max_scores[c] > 0:
            normalized[c] = round((raw_scores[c] / max_scores[c]) * 100, 1)
        else:
            normalized[c] = round(raw_scores[c], 1)

    return normalized


def score_interest_assessment(answers: List[Dict[str, Any]], questions: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Score interest assessment on 1-5 rating scale questions.
    Returns normalized scores (0-100) per interest category.
    """
    categories = ["science", "arts", "commerce", "technology", "social", "outdoor", "creative"]
    totals = {c: 0.0 for c in categories}
    counts = {c: 0 for c in categories}
    q_map = {str(q.get("id")): q for q in questions}

    for ans in answers:
        q_id = str(ans.get("question_id"))
        q = q_map.get(q_id)
        if not q:
            continue
        cat = q.get("category", "").lower()
        matched_cat = None
        for c in categories:
            if c in cat:
                matched_cat = c
                break
        if not matched_cat:
            matched_cat = "creative"

        val = float(ans.get("raw_score", 3))
        totals[matched_cat] += val
        counts[matched_cat] += 1

    # Convert average 1-5 to percentage (1 -> 0%, 5 -> 100%)
    res = {}
    for c in categories:
        if counts[c] > 0:
            avg = totals[c] / counts[c]
            res[c] = round(max(0.0, min(100.0, (avg - 1) / 4.0 * 100)), 1)
        else:
            res[c] = 50.0

    return res


def compute_top_aptitudes(scores: Dict[str, float]) -> List[str]:
    """Returns top 3 aptitude categories sorted by score descending."""
    sorted_items = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [k for k, v in sorted_items[:3]]


def compute_recommended_streams(interest_scores: Dict[str, float], aptitude_scores: Dict[str, float]) -> List[Dict[str, Any]]:
    """
    Synthesize interest and aptitude scores to recommend Class 11-12 streams / degree pathways.
    """
    streams = []

    # Science (PCM / Engineering / Tech)
    stem_score = (
        interest_scores.get("technology", 0) * 0.4 +
        interest_scores.get("science", 0) * 0.3 +
        aptitude_scores.get("numerical", 0) * 0.15 +
        aptitude_scores.get("logical", 0) * 0.15
    )
    streams.append({
        "stream": "Science (PCM - Engineering & Technology)",
        "fit_score": round(stem_score, 1),
        "rationale": "High affinity for technological problem-solving, structured logic, and mathematical thinking."
    })

    # Science (PCB - Medical & Life Sciences)
    med_score = (
        interest_scores.get("science", 0) * 0.5 +
        interest_scores.get("social", 0) * 0.2 +
        aptitude_scores.get("analytical", 0) * 0.15 +
        aptitude_scores.get("verbal", 0) * 0.15
    )
    streams.append({
        "stream": "Science (PCB - Medicine & Healthcare)",
        "fit_score": round(med_score, 1),
        "rationale": "Strong biological and natural science interest combined with service orientation."
    })

    # Commerce (Finance, Accounting & Economics)
    comm_score = (
        interest_scores.get("commerce", 0) * 0.5 +
        aptitude_scores.get("numerical", 0) * 0.25 +
        aptitude_scores.get("analytical", 0) * 0.25
    )
    streams.append({
        "stream": "Commerce (Finance, Business & Analytics)",
        "fit_score": round(comm_score, 1),
        "rationale": "Good interest in markets, economic systems, and quantitative business models."
    })

    # Humanities & Social Sciences
    arts_score = (
        interest_scores.get("arts", 0) * 0.35 +
        interest_scores.get("social", 0) * 0.35 +
        interest_scores.get("creative", 0) * 0.1 +
        aptitude_scores.get("verbal", 0) * 0.2
    )
    streams.append({
        "stream": "Humanities, Law & Social Sciences",
        "fit_score": round(arts_score, 1),
        "rationale": "High empathy, verbal agility, and interest in social dynamics and cultural expression."
    })

    # Design & Creative Media
    design_score = (
        interest_scores.get("creative", 0) * 0.5 +
        interest_scores.get("arts", 0) * 0.3 +
        aptitude_scores.get("spatial", 0) * 0.2
    )
    streams.append({
        "stream": "Design, Media & Visual Communication",
        "fit_score": round(design_score, 1),
        "rationale": "Strong visual-spatial reasoning and inventive ideation potential."
    })

    streams.sort(key=lambda x: x["fit_score"], reverse=True)
    return streams
