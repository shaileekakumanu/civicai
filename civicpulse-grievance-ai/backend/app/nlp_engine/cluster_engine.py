"""
Spatio-Temporal & Semantic Incident Clustering & Spike Detection.
"""
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class IncidentClusterEngine:
    def __init__(self):
        self.clusters: Dict[str, Dict[str, Any]] = {}
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')

    def assign_or_create_cluster(self, ticket_data: Dict[str, Any]) -> Dict[str, Any]:
        ticket_id = ticket_data.get('ticket_id')
        ward_id = ticket_data.get('ward_id')
        dept_id = ticket_data.get('department_id')
        text = ticket_data.get('raw_text', '')
        
        best_cluster_id = None
        best_sim = 0.0
        
        # Check all active clusters in same ward & department
        for cluster_id, cluster in self.clusters.items():
            if cluster['ward_id'] == ward_id and cluster['department_id'] == dept_id:
                cluster_texts = " ".join(cluster['complaint_texts'])
                try:
                    tfidf_mat = self.vectorizer.fit_transform([text, cluster_texts])
                    sim = float(cosine_similarity(tfidf_mat[0:1], tfidf_mat[1:2])[0][0])
                    if sim > best_sim:
                        best_sim = sim
                        best_cluster_id = cluster_id
                except Exception:
                    pass
        
        # If similarity >= 0.30 (related complaint in same ward and department), merge into cluster
        if best_cluster_id and best_sim >= 0.30:

            target_cluster = self.clusters[best_cluster_id]
            target_cluster['ticket_ids'].append(ticket_id)
            target_cluster['complaint_texts'].append(text)
            target_cluster['affected_citizens_count'] += 1
            target_cluster['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            count = target_cluster['affected_citizens_count']
            if count >= 5:
                target_cluster['spike_level'] = "Critical Spike Alert"
                target_cluster['priority'] = "P1"
            elif count >= 3:
                target_cluster['spike_level'] = "Moderate Surge"
                if target_cluster['priority'] in ["P3", "P4"]:
                    target_cluster['priority'] = "P2"
            else:
                target_cluster['spike_level'] = "Normal / Isolated"
            
            return {
                'is_new_cluster': False,
                'cluster_id': best_cluster_id,
                'master_ticket_id': target_cluster['master_ticket_id'],
                'affected_citizens_count': target_cluster['affected_citizens_count'],
                'spike_level': target_cluster['spike_level'],
                'similarity_score': round(best_sim, 2)
            }
        
        # Create new Master Incident Cluster
        new_cluster_id = f"CLUSTER-{str(uuid.uuid4())[:6].upper()}"
        new_cluster = {
            'cluster_id': new_cluster_id,
            'master_ticket_id': ticket_id,
            'ward_id': ward_id,
            'ward_name': ticket_data.get('ward_name', 'Ward 1'),
            'department_id': dept_id,
            'department_name': ticket_data.get('department_name', 'Municipal'),
            'category_name': ticket_data.get('category_name', 'Civic Issue'),
            'subcategory': ticket_data.get('subcategory', 'General'),
            'priority': ticket_data.get('priority', 'P3'),
            'ticket_ids': [ticket_id],
            'complaint_texts': [text],
            'affected_citizens_count': 1,
            'spike_level': "Normal / Isolated",
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'status': "Active"
        }
        self.clusters[new_cluster_id] = new_cluster
        
        return {
            'is_new_cluster': True,
            'cluster_id': new_cluster_id,
            'master_ticket_id': ticket_id,
            'affected_citizens_count': 1,
            'spike_level': "Normal / Isolated",
            'similarity_score': 1.0
        }

    def get_active_clusters(self) -> List[Dict[str, Any]]:
        return sorted(self.clusters.values(), key=lambda x: x['affected_citizens_count'], reverse=True)

    def get_all_clusters(self) -> List[Dict[str, Any]]:
        return self.get_active_clusters()

