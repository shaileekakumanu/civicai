"""
CivicPulse Hierarchical NLP Classifier & Urgency Prioritizer for 10 Civic Domains.
"""
import json
import os
import re
from typing import Dict, Any, Tuple, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from app.nlp_engine.hinglish_normalizer import normalize_grievance_text
from app.nlp_engine.ner_extractor import extract_civic_entities
from app.nlp_engine.xai_explainer import compute_xai_and_sentiment
from app.nlp_engine.dispatch_generator import generate_official_work_order, generate_citizen_acknowledgement
from app.data.benchmark_dataset import BENCHMARK_GRIEVANCES

class CivicGrievanceClassifier:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'departments_config.json')
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.dept_config = json.load(f)
        
        self.departments = self.dept_config.get('departments', {})
        self.wards = self.dept_config.get('wards', [])
        self._build_and_train_models()

    def _build_and_train_models(self):
        X_texts = []
        y_depts = []
        y_subcats = []
        
        for item in BENCHMARK_GRIEVANCES:
            norm_res = normalize_grievance_text(item['text'])
            enriched = f"{item['text']} {norm_res['normalized_text']}"
            X_texts.append(enriched)
            y_depts.append(item['category'])
            y_subcats.append(item.get('subcategory', 'General'))
        
        # Train Multi-Class Department Classifier
        self.dept_clf = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ('clf', LogisticRegression(C=2.0, max_iter=500, random_state=42))
        ])
        self.dept_clf.fit(X_texts, y_depts)
        
        # Train Subcategory Classifier
        self.subcat_clf = Pipeline([
            ('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ('clf', MultinomialNB(alpha=0.1))
        ])
        self.subcat_clf.fit(X_texts, y_subcats)

    def _calculate_urgency_priority(self, raw_text: str, dept_id: str, subcat: str) -> Tuple[str, int, int]:
        text_low = raw_text.lower()
        risk_score = 40
        
        # Critical Emergency Triggers across all 10 Domains (P1)
        emergency_terms = [
            'live wire', 'electric wire', 'wire', 'sparking', 'electrocution', 'shock', 'fire', 'blast', 'explosion',
            'open manhole', 'manhole', 'death trap', 'toxic', 'poisonous', 'dengue', 'hospital', 'bleeding',
            'stalking', 'harassment', 'eve teasing', 'sos', 'following me', 'molestation',
            'chedkhani', 'missing child', 'child labour', 'abandoned elderly', 'oxygen',
            'dog attack', 'dog bite', 'bribe demand', 'bribe', 'extortion', 'flooding', 'collapse'
        ]
        for trig in emergency_terms:
            if trig in text_low:
                risk_score += 45
                break

        
        # High Urgency Triggers (P2)
        high_terms = [
            '3 days', '4 days', '5 days', '1 week', 'no water', 'power cut', 'blackout',
            'overflowing', 'waterlogged', 'pipeline burst', 'sewage', 'foul smell', 'carcass',
            'broken ramp', 'wheelchair', 'air pollution', 'noise pollution', 'tree cutting', 'fake closure'
        ]
        for trig in high_terms:
            if trig in text_low:
                risk_score += 25
                break
        
        risk_score = min(100, max(10, risk_score))
        
        if risk_score >= 80 or dept_id in ['WOMEN_SAFETY', 'DISASTER_EMERGENCY']:
            priority = 'P1'
        elif risk_score >= 60:
            priority = 'P2'
        elif risk_score >= 35:
            priority = 'P3'
        else:
            priority = 'P4'
        
        dept_info = self.departments.get(dept_id, {})
        sla_map = dept_info.get('sla_hours', {'P1': 2, 'P2': 12, 'P3': 24, 'P4': 72})
        sla_hours = sla_map.get(priority, 24)
        
        return priority, risk_score, sla_hours

    def analyze_grievance(self, raw_text: str, force_ward: str = None) -> Dict[str, Any]:
        norm_res = normalize_grievance_text(raw_text)
        enriched_text = f"{raw_text} {norm_res['normalized_text']}"
        
        # Predict Department
        dept_id = self.dept_clf.predict([enriched_text])[0]
        dept_probs = self.dept_clf.predict_proba([enriched_text])[0]
        classes = self.dept_clf.classes_
        confidence = round(float(max(dept_probs)), 3)
        
        # Predict Subcategory
        subcat = self.subcat_clf.predict([enriched_text])[0]
        
        # Civic NER
        ner_res = extract_civic_entities(raw_text)
        assigned_ward_id = force_ward if force_ward else ner_res.get('inferred_ward_id', 'WARD-01')
        
        # Urgency & SLA
        priority, risk_score, sla_hours = self._calculate_urgency_priority(raw_text, dept_id, subcat)
        
        # XAI & Sentiment
        xai_res = compute_xai_and_sentiment(raw_text, dept_id, priority)
        
        dept_details = self.departments.get(dept_id, {})
        ward_info = next((w for w in self.wards if w['id'] == assigned_ward_id), self.wards[0])
        
        return {
            'raw_text': raw_text,
            'normalization': norm_res,
            'department_id': dept_id,
            'department_name': dept_details.get('name', 'Municipal Dept'),
            'department_short': dept_details.get('short_code', 'MUN'),
            'department_color': dept_details.get('color', '#0284c7'),
            'helpline': dept_details.get('helpline', '112 / 100'),
            'icon': dept_details.get('icon', 'activity'),
            'nodal_officer': dept_details.get('nodal_officer', 'Zonal Engineer'),
            'confidence': confidence,
            'subcategory': subcat,
            'priority': priority,
            'risk_score': risk_score,
            'sla_hours': sla_hours,
            'ward_id': assigned_ward_id,
            'ward_name': ward_info.get('name', 'Ward 1'),
            'ward_lat': ward_info.get('coords', {}).get('lat', 28.65),
            'ward_lon': ward_info.get('coords', {}).get('lng', 77.23),
            'entities': ner_res,
            'xai': xai_res
        }
