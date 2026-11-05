"""
Hinglish and Code-Mixed Grievance Normalizer.
Translates colloquial Romanized Hindi and civic slang across 10 domains into canonical semantic tokens.
"""
import re
from typing import Dict, Any, List, Tuple

HINGLISH_CIVIC_LEXICON = {
    # Water & Sanitation
    'paani': 'water', 'pani': 'water', 'jal': 'water', 'nal': 'tap faucet',
    'peene': 'drinking', 'ganda': 'contaminated dirty', 'badboo': 'foul odor stench',
    'badbu': 'foul odor', 'kichad': 'mud sludge', 'phat': 'burst', 'phata': 'burst',
    'leakage': 'leakage burst', 'tanker': 'water tanker', 'motar': 'motor pump',
    # Electricity & Fire
    'bijli': 'electricity power', 'batti': 'electricity light', 'taar': 'wire live cable',
    'khamba': 'electric pole pillar', 'current': 'electric current shock hazard',
    'chingari': 'sparking fire sparks', 'dhua': 'smoke burning air pollution', 'dhamaka': 'blast explosion',
    'transformer': 'transformer power station', 'aag': 'fire breakout blaze',
    # Roads & Infrastructure
    'sadak': 'road street highway', 'rasta': 'road route', 'gali': 'street lane',
    'gaddha': 'pothole crater pit', 'gadhe': 'potholes craters', 'toota': 'broken damaged',
    'dhas': 'caved in sinkhole collapse', 'jam': 'traffic congestion blockage', 'pul': 'bridge flyover',
    'divider': 'road divider barrier', 'footpath': 'pedestrian footpath pavement',
    'kachra': 'garbage trash solid waste', 'kooda': 'garbage dump refuse',
    'dhalao': 'garbage bin collection point', 'safai': 'cleaning sanitation sweep',
    'gandagi': 'filth unhygienic dirt', 'naala': 'drain storm sewer', 'nali': 'drain gutter',
    'gutter': 'manhole sewer gutter', 'gutar': 'sewer manhole', 'dhakkan': 'manhole lid cover',
    # Health & Disease
    'machhar': 'mosquitoes vector pests', 'dengue': 'dengue vector disease outbreak',
    'malaria': 'malaria fever infection', 'bimar': 'sick illness disease infection',
    'aspatal': 'hospital clinic medical', 'khana': 'food adulteration safety',
    # Animals
    'kutte': 'stray dogs pack bites menace', 'kutta': 'stray dog', 'gay': 'cow cattle animal',
    'pashu': 'animal welfare veterinary', 'beemar': 'sick injured animal',
    # Women Safety
    'ladki': 'woman girl student female', 'mahila': 'women female safety',
    'chedte': 'eve teasing harassment molest', 'chedkhani': 'harassment eve teasing stalking',
    'chhedkhani': 'harassment eve teasing sexual misconduct', 'picha': 'stalking following suspiciously',
    'andhera': 'darkness unlit unsafe streets', 'gunde': 'miscreants rogue eve teasers',
    'daru': 'alcohol drinking hooligans', 'sharab': 'drunk miscreants harassment',
    'dar': 'fear unsafe terrified panic', 'sos': 'emergency sos rapid police help',
    # Children & Schools
    'bacche': 'children school kids students', 'bacha': 'child kid minor',
    'school': 'school education zone safety', 'gayab': 'missing lost child alert',
    'majdoori': 'child labour exploitation illegal', 'dhabe': 'dhaba child labour',
    # Senior Citizens
    'buzurg': 'elderly senior citizen geriatric', 'buddhe': 'elderly aged grandfather',
    'dadi': 'grandmother abandoned senior', 'dada': 'grandfather aged senior',
    'bedridden': 'paralyzed bedridden medical support',
    # Disability & Accessibility
    'divyang': 'disabled wheelchair accessibility', 'vikalang': 'handicapped disabled ramp',
    'wheelchair': 'wheelchair barrier disabled ramp', 'ramp': 'disability access wheelchair ramp',
    # Environment & Disasters
    'ped': 'tree deforestation illegal chopping', 'shor': 'noise pollution late night loudspeaker',
    'pradushan': 'pollution toxic smoke emissions', 'jheel': 'lake toxic sewage pollution',
    'baadh': 'flooding waterlogging deluge disaster', 'toofan': 'storm cyclone disaster damage',
    # Corruption & Governance
    'rishwat': 'bribe bribery corruption demand', 'ghoos': 'bribe cash extortion',
    'afsar': 'officer public servant misconduct', 'nakli': 'fake fraudulent closure complaint',
    'kam': 'service delayed duty negligence',
    # Urgency Modifiers
    'khatarnaak': 'dangerous life threatening emergency', 'khatra': 'danger hazard risk',
    'jaldi': 'urgent immediate fast priority', 'turant': 'instant immediate critical',
    'madad': 'emergency assistance help needed', 'pareshan': 'suffering severely distressed',
    'shikayat': 'formal complaint grievance'
}

PHRASE_MAPPINGS = [
    # Women Safety
    (r'\b(ladkiyon\s+ko\s+ched|chedkhani\s+kar\s+rahe|chhedkhani|eve\s+teasing|ladki\s+ko\s+pareshan)\b', 'eve teasing women harassment public places police squad emergency'),
    (r'\b(koi\s+picha\s+kar\s+raha|stalking|following\s+me|andhera\s+hai\s+dar\s+lag\s+raha)\b', 'stalking suspicious person unsafe dark street women emergency sos'),
    (r'\b(bus\s+stop\s+pe\s+andhera|bus\s+stop\s+pe\s+gunde|college\s+ke\s+bahar\s+ched)\b', 'poor lighting near bus stops colleges harassment unsafe women transport spot'),
    # Child Safety
    (r'\b(school\s+ke\s+bahar\s+gutter|school\s+gate\s+pe\s+khula\s+manhole)\b', 'open manhole drain danger near school zone child safety hazard'),
    (r'\b(bacha\s+gayab\s+hai|chota\s+bacha\s+kho\s+gaya|missing\s+child)\b', 'missing child emergency alert urgent search rescue'),
    (r'\b(chote\s+bacche\s+se\s+majdoori|child\s+labour|dhaba\s+pe\s+bacha)\b', 'illegal child labour hazardous employment rescue report'),
    # Senior Citizen
    (r'\b(buzurg\s+kele\s+madad|buddhe\s+dadi\s+ko\s+chhod\s+diya|elderly\s+medical)\b', 'abandoned elderly medical emergency senior citizen welfare assistance'),
    # Corruption & Vigilance
    (r'\b(rishwat\s+maang\s+raha|ghoos\s+maanga|bribe\s+demand|paisa\s+maang\s+rahe)\b', 'bribe demand corruption vigilance lokayukta complaint public servant extortion'),
    (r'\b(bina\s+kaam\s+ke\s+resolved\s+kar\s+diya|fake\s+closure|jhootha\s+resolved)\b', 'fake closure of complaint without work officer misconduct vigilance'),
    # Water & Electricity
    (r'\b(paani\s+nahi\s+aa\s+raha|pani\s+nahi\s+hai|supply\s+band\s+hai)\b', 'total water supply outage no water'),
    (r'\b(ganda\s+pani|badboodar\s+paani|peele\s+rang\s+ka\s+pani)\b', 'contaminated foul toxic drinking water supply disease risk'),
    (r'\b(taar\s+tut\s+ke\s+gira|live\s+wire|nanga\s+taar|taar\s+latak\s+raha)\b', 'live hanging electric wire electrocution life hazard public safety'),
    (r'\b(khula\s+gutter|manhole\s+ka\s+dhakkan\s+gayab|toota\s+gutter)\b', 'open uncovered manhole death trap severe accident hazard public safety'),
    (r'\b(sadak\s+pe\s+kachra|kooda\s+sad\s+raha\s+hai|dhalao\s+overflow)\b', 'overflowing rotting garbage dump severe sanitation hazard health hygiene'),
    (r'\b(sadak\s+pe\s+gaddhe|bade\s+gaddhe|sadak\s+tooti\s+hai)\b', 'dangerous road potholes broken craters vehicle damage hazard'),
    (r'\b(dengue\s+ke\s+machhar|machhar\s+bohot\s+hai|fogging\s+nahi\s+hui)\b', 'dengue epidemic risk severe mosquito infestation public health hygiene'),
    (r'\b(kutta\s+kaat\s+raha|kutte\s+ka\s+aatanak|stray\s+dogs\s+biting)\b', 'aggressive stray dog attacks animal safety veterinary squad'),
    (r'\b(ramp\s+toota\s+hai|wheelchair\s+nahi\s+ja\s+sakti|footpath\s+blocked)\b', 'broken wheelchair ramp blocked footpath disability accessibility equal access'),
    (r'\b(ped\s+kaat\s+rahe|tree\s+cutting|dhuan\s+chhod\s+rahe|loudspeaker\s+shor)\b', 'illegal tree cutting air noise pollution environmental protection board'),
    (r'\b(baadh\s+aa\s+gayi|ghar\s+me\s+paani\s+bhar\s+gaya|aag\s+lag\s+gayi|building\s+girne\s+wali)\b', 'flooding fire building collapse risk disaster emergency rescue authority')
]

def normalize_grievance_text(raw_text: str) -> Dict[str, Any]:
    if not raw_text or not raw_text.strip():
        return {
            'raw_text': '',
            'normalized_text': '',
            'detected_language': 'Unknown',
            'vernacular_tokens_found': []
        }

    text_lower = raw_text.lower().strip()
    matched_vernacular_tokens = []

    # Step 1: Replace Multi-word idiomatic patterns
    normalized = text_lower
    for pattern, replacement in PHRASE_MAPPINGS:
        if re.search(pattern, normalized, re.IGNORECASE):
            normalized = re.sub(pattern, f" {replacement} ", normalized, flags=re.IGNORECASE)
            matched_vernacular_tokens.append(pattern)

    # Step 2: Lexicon Token Replacement
    tokens = re.findall(r'\b[a-zA-Z]+\b', normalized)
    translated_tokens = []
    vernacular_count = 0

    for token in tokens:
        if token in HINGLISH_CIVIC_LEXICON:
            translated = HINGLISH_CIVIC_LEXICON[token]
            translated_tokens.append(translated)
            vernacular_count += 1
            if token not in matched_vernacular_tokens:
                matched_vernacular_tokens.append(token)
        else:
            translated_tokens.append(token)

    final_text = " ".join(translated_tokens)
    final_text = re.sub(r'\s+', ' ', final_text).strip()

    # Step 3: Determine Language Classification
    total_tokens = max(len(tokens), 1)
    vernacular_ratio = vernacular_count / total_tokens

    if vernacular_ratio >= 0.35:
        detected_language = "Hinglish (Code-Mixed Hindi-English)"
    elif vernacular_count > 0 or len(matched_vernacular_tokens) > 0:
        detected_language = "English with Vernacular Terms"
    else:
        detected_language = "English"

    return {
        'raw_text': raw_text,
        'normalized_text': final_text,
        'detected_language': detected_language,
        'vernacular_tokens_found': matched_vernacular_tokens,
        'code_mix_ratio': round(vernacular_ratio, 2)
    }
