"""
Civic-NER Engine: Extracts Ward, Sector/Colony, Landmarks, Public Assets, and Durations.
"""
import re
from typing import Dict, Any, List

WARD_PATTERNS = [
    r'\b(ward\s*[-#]?\s*0?[1-8]|ward\s*0?[1-8])\b',
    r'\b(zone\s*[-#]?\s*[1-4]|north\s+zone|south\s+zone|east\s+zone|west\s+zone)\b'
]

LOCALITY_PATTERNS = [
    r'\b(sector\s*[-#]?\s*\d+[a-zA-Z]?)\b',
    r'\b(lajpat\s+nagar|defense\s+colony|indiranagar|model\s+town|green\s+park|koramangala|civil\s+lines|central\s+market|saket|rohini|dwarka|mayur\s+vihar|vasant\s+kunj|karol\s+bagh)\b',
    r'\b(pocket\s*[-#]?\s*[a-zA-Z0-9]+|block\s*[-#]?\s*[a-zA-Z0-9]+)\b'
]

LANDMARK_PATTERNS = [
    r'\b(?:near|opposite|opp|behind|front\s+of|adjacent\s+to|beside)\s+([a-zA-Z0-9\s]{3,35}?)(?:,|\.|and|for|since|$)',
    r'\b(metro\s+station|metro\s+pillar\s*\d+|bus\s+stop|bus\s+stand|central\s+market|school|hospital|dispensary|community\s+center|police\s+station|water\s+tank|temple|mosque|gurudwara)\b'
]

ASSET_PATTERNS = [
    r'\b(pole\s*[-#]?\s*\d+|khamba\s*[-#]?\s*\d+|transformer\s*[-#]?\s*[a-zA-Z0-9]+|manhole\s*[-#]?\s*\d+|meter\s*[-#]?\s*\d+)\b'
]

DURATION_PATTERNS = [
    r'\b(?:for|since|past|last)\s+(\d+\s*(?:days?|hours?|weeks?|months?|din|ghante|hafte))\b',
    r'\b(\d+\s*(?:days?|hours?|weeks?|months?|din|ghante)\s*(?:se|ago|ongoing))\b',
    r'\b(since\s+yesterday|kal\s+se|aaj\s+subah\s+se|last\s+night)\b'
]

def extract_civic_entities(text: str) -> Dict[str, Any]:
    text_clean = text.strip()
    extracted_wards = []
    for pat in WARD_PATTERNS:
        for m in re.finditer(pat, text_clean, re.IGNORECASE):
            extracted_wards.append(m.group(0).title())

    extracted_localities = []
    for pat in LOCALITY_PATTERNS:
        for m in re.finditer(pat, text_clean, re.IGNORECASE):
            extracted_localities.append(m.group(0).title())

    extracted_landmarks = []
    for pat in LANDMARK_PATTERNS:
        for m in re.finditer(pat, text_clean, re.IGNORECASE):
            lm = m.group(1) if m.groups() and m.group(1) else m.group(0)
            cleaned_lm = lm.strip()
            if len(cleaned_lm) > 2 and cleaned_lm.lower() not in ['for', 'since', 'and', 'the']:
                extracted_landmarks.append(cleaned_lm.title())

    extracted_assets = []
    for pat in ASSET_PATTERNS:
        for m in re.finditer(pat, text_clean, re.IGNORECASE):
            extracted_assets.append(m.group(0).upper())

    extracted_durations = []
    for pat in DURATION_PATTERNS:
        for m in re.finditer(pat, text_clean, re.IGNORECASE):
            extracted_durations.append(m.group(0))

    loc_str = ' '.join(extracted_localities).lower()
    if 'sector 14' in loc_str or 'civil lines' in loc_str:
        assigned_ward_id = 'WARD-02'
    elif 'green park' in loc_str or 'metro' in loc_str:
        assigned_ward_id = 'WARD-03'
    elif 'lajpat' in loc_str or 'defense' in loc_str:
        assigned_ward_id = 'WARD-04'
    elif 'indiranagar' in loc_str or 'tech park' in loc_str:
        assigned_ward_id = 'WARD-05'
    elif 'model town' in loc_str or 'industrial' in loc_str:
        assigned_ward_id = 'WARD-06'
    elif 'sector 21' in loc_str or 'resident' in loc_str:
        assigned_ward_id = 'WARD-07'
    elif 'koramangala' in loc_str or 'lake' in loc_str:
        assigned_ward_id = 'WARD-08'
    elif 'central market' in loc_str or 'old city' in loc_str:
        assigned_ward_id = 'WARD-01'
    elif extracted_wards:
        w_num = re.search(r'\d+', extracted_wards[0])
        if w_num:
            assigned_ward_id = f'WARD-0{int(w_num.group(0)):01d}'
        else:
            assigned_ward_id = 'WARD-01'
    else:
        assigned_ward_id = 'WARD-02'

    return {
        'wards': list(set(extracted_wards)),
        'localities': list(set(extracted_localities)),
        'landmarks': list(set(extracted_landmarks))[:2],
        'assets': list(set(extracted_assets)),
        'durations': list(set(extracted_durations)),
        'inferred_ward_id': assigned_ward_id
    }
