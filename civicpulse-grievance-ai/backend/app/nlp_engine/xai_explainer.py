"""
Explainable AI (XAI) Engine for Civic Grievance Triage across 10 Domains.
Provides token-level attribution highlights, distress analysis, and rationale scoring.
"""
import re
from typing import Dict, Any, List

EMERGENCY_TRIGGERS = [
    # Life Safety & Disasters
    "live wire", "sparking", "electrocution", "shock", "fire", "blast", "explosion",
    "open manhole", "death trap", "toxic", "poisonous", "dengue", "epidemic", "hospital",
    "bleeding", "collapse", "emergency", "ambulance", "flooding", "submerged",
    # Women Safety
    "stalking", "harassment", "eve teasing", "sos", "following me", "molestation", "chedkhani",
    "unsafe street", "dark alley", "terror",
    # Child & Senior Safety
    "missing child", "child labour", "school gate", "abandoned elderly", "paralyzed", "oxygen",
    # Animal & Public Hazard
    "dog attack", "dog bite", "rabies", "injured animal", "bribe demand", "extortion"
]

HIGH_SEVERITY_TRIGGERS = [
    "3 days", "4 days", "5 days", "1 week", "no water", "blackout", "contaminated",
    "foul smell", "rotting", "carcass", "dead animal", "waterlogged", "overflowing",
    "massive", "dangerous", "sewage", "gutter", "stray dogs", "wheelchair", "broken ramp",
    "air pollution", "chemical smoke", "lake pollution", "tree cutting", "fake closure", "bribe"
]

SENTIMENT_NEGATIVE_WORDS = [
    "suffering", "terrible", "worst", "pathetic", "horrible", "disgusting", "neglect",
    "unbearable", "dying", "hopeless", "urgent", "danger", "ruined", "disaster",
    "crying", "angry", "frustrated", "shameful", "useless", "pareshan", "harassed", "scared"
]

def compute_xai_and_sentiment(raw_text: str, category_key: str, priority_level: str) -> Dict[str, Any]:
    text_lower = raw_text.lower()
    tokens = re.findall(r'\b[a-zA-Z0-9_-]+\b', raw_text)
    
    token_attributions = []
    matched_triggers = []
    distress_score = 0.0
    
    for tok in tokens:
        tok_low = tok.lower()
        weight = 0.05
        role = "neutral"
        
        for trig in EMERGENCY_TRIGGERS:
            if trig in tok_low or tok_low in trig:
                weight = 0.95
                role = "emergency_trigger"
                matched_triggers.append(tok)
                distress_score += 0.35
                break
            
        if role == "neutral":
            for trig in HIGH_SEVERITY_TRIGGERS:
                if trig in tok_low or tok_low in trig:
                    weight = 0.70
                    role = "severity_driver"
                    matched_triggers.append(tok)
                    distress_score += 0.20
                    break
            
        if role == "neutral":
            for neg in SENTIMENT_NEGATIVE_WORDS:
                if neg in tok_low:
                    weight = 0.55
                    role = "distress_marker"
                    matched_triggers.append(tok)
                    distress_score += 0.15
                    break
                    
        token_attributions.append({
            'token': tok,
            'weight': weight,
            'role': role
        })
        
    normalized_sentiment = round(max(-1.0, min(1.0, 0.2 - distress_score)), 2)
    
    # Generate Natural Language Justification
    if priority_level == 'P1':
        rationale = f"Assigned P1 Critical Priority due to detected emergency and life-safety markers: {', '.join(set(matched_triggers[:4])) or 'Immediate Action Required'}."
    elif priority_level == 'P2':
        rationale = f"Assigned P2 High Priority based on civic disruption severity indicators: {', '.join(set(matched_triggers[:3])) or 'Significant public impact'}."
    elif priority_level == 'P3':
        rationale = f"Assigned P3 Standard Priority for standard municipal inspection and maintenance."
    else:
        rationale = f"Assigned P4 Routine Priority for scheduled municipal servicing."
        
    return {
        'token_attributions': token_attributions,
        'matched_emergency_tokens': list(set(matched_triggers)),
        'distress_sentiment_score': normalized_sentiment,
        'sentiment_label': 'Highly Distressed / Critical' if normalized_sentiment < -0.4 else 'Moderate Distress' if normalized_sentiment < 0 else 'Neutral',
        'decision_rationale': rationale
    }
