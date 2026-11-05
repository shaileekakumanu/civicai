"""
Unit Tests for CivicPulse NLP Engine across 10 Civic Domains.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.nlp_engine.hinglish_normalizer import normalize_grievance_text
from app.nlp_engine.ner_extractor import extract_civic_entities
from app.nlp_engine.classifier import CivicGrievanceClassifier
from app.nlp_engine.cluster_engine import IncidentClusterEngine

def test_hinglish_normalizer():
    text = "Bus stop pe ladkiyon ko chedte hain gunde log, andhera hai"
    res = normalize_grievance_text(text)
    assert "eve teasing" in res['normalized_text'] or "harassment" in res['normalized_text']
    assert "Hinglish" in res['detected_language'] or "Vernacular" in res['detected_language']
    print("[PASS] Hinglish Normalizer (10 Domains)")

def test_ner_extraction():
    text = "Live wire hanging near Bal Bharti School in Sector 14 for 2 days on Pole #12"
    ents = extract_civic_entities(text)
    assert any("Sector 14" in l for l in ents['localities'])
    assert ents['inferred_ward_id'] == "WARD-02"
    print("[PASS] Civic NER Extraction")

def test_classifier_and_urgency():
    clf = CivicGrievanceClassifier()
    
    # 1. Women Safety
    res1 = clf.analyze_grievance("Men are drinking and eve teasing women near Lajpat Nagar bus stop every evening after 7 PM")
    assert res1['department_id'] == "WOMEN_SAFETY"
    assert res1['priority'] == "P1"
    assert "1091" in res1['helpline']
    
    # 2. Child Safety
    res2 = clf.analyze_grievance("Large deep open manhole right outside DAV Public School main gate in Sector 14")
    assert res2['department_id'] == "CHILD_SAFETY"
    assert res2['priority'] == "P1"
    assert "1098" in res2['helpline']
    
    # 3. Senior Citizen
    res3 = clf.analyze_grievance("82-year-old paralyzed senior citizen living alone in Sector 21 requires emergency oxygen")
    assert res3['department_id'] == "SENIOR_CITIZEN"
    assert res3['priority'] == "P1"
    assert "14567" in res3['helpline']
    
    # 4. Public Safety Hazard
    res4 = clf.analyze_grievance("High voltage live electric wire snapped and hanging at head height near school in Sector 14")
    assert res4['department_id'] == "PUBLIC_SAFETY"
    assert res4['priority'] == "P1"

    # 5. Corruption
    res5 = clf.analyze_grievance("Municipal building inspector demanding 50,000 INR cash bribe to process building map approval in Ward 02")
    assert res5['department_id'] == "CORRUPTION_VIGILANCE"
    assert res5['priority'] == "P1"
    assert "1064" in res5['helpline']
    
    print("[PASS] 10-Domain Multi-Task Classifier & Urgency Scoring")

def test_clustering_deduplication():
    engine = IncidentClusterEngine()
    t1 = {'ticket_id': 'T1', 'ward_id': 'WARD-04', 'department_id': 'WOMEN_SAFETY', 'raw_text': 'Eve teasing and harassment near bus stop in Lajpat Nagar'}
    t2 = {'ticket_id': 'T2', 'ward_id': 'WARD-04', 'department_id': 'WOMEN_SAFETY', 'raw_text': 'Men stalking and eve teasing women near Lajpat Nagar bus stop'}
    
    c1 = engine.assign_or_create_cluster(t1)
    assert c1['is_new_cluster'] == True
    
    c2 = engine.assign_or_create_cluster(t2)
    assert c2['is_new_cluster'] == False
    assert c2['affected_citizens_count'] == 2
    print("[PASS] Incident Clustering & Deduplication")

if __name__ == '__main__':
    test_hinglish_normalizer()
    test_ner_extraction()
    test_classifier_and_urgency()
    test_clustering_deduplication()
    print("\n=== All 10-Domain NLP Engine Tests Passed Successfully! ===")
