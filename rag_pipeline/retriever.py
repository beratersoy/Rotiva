"""
FAISS + Embedding Retriever - Kullanıcı sorgusuna göre en alakalı etkinlikleri bulur
PROJE GEREKSİNİMLERİ: ✅ Embedding Model (Sentence-Transformers) + ✅ Vektor Database (FAISS)
"""

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os


class FAISSRetriever:
    """
    FAISS vektor database + Sentence-Transformers embedding modeli ile semantik arama
    
    ✅ Embedding Model: paraphrase-multilingual-MiniLM-L12-v2 (Türkçe desteği)
    ✅ Vektor Database: FAISS (Facebook AI Similarity Search)
    """
    
    def __init__(self, events, model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        """
        Args:
            events: Etkinlik listesi
            model_name: Huggingface embedding model (varsayılan: çok dilli model)
        """
        self.events = events
        
        # 🤖 Embedding Model yükle (ilk seferde ~120MB indirecek)
        print(f"🔄 Embedding model yükleniyor: {model_name}")
        self.model = SentenceTransformer(model_name)
        print(f"✅ Embedding model hazır (boyut: {self.model.get_sentence_embedding_dimension()})")
        
        # Her etkinlik için aranabilir metin oluştur
        self.texts = [
            f"{e['title']} {e['description']} {e['city']} {e.get('category', '')}"
            for e in events
        ]
        
        # 📊 Tüm etkinlikleri embedding'e çevir (vektör temsili)
        print(f"🔄 {len(events)} etkinlik vektörlere dönüştürülüyor...")
        self.embeddings = self.model.encode(self.texts, show_progress_bar=True)
        
        # 🗄️ FAISS vektor database oluştur (hızlı benzerlik araması için)
        dimension = self.embeddings.shape[1]  # Vektör boyutu (384)
        self.index = faiss.IndexFlatL2(dimension)  # L2 mesafe metriği
        self.index.add(self.embeddings.astype('float32'))  # Vektörleri FAISS'e ekle
        
        print(f"✅ FAISS Retriever hazır: {len(events)} etkinlik indekslendi")
    
    def retrieve(self, query, k=5, city_filter=None):
        """
        Kullanıcı sorgusuna en yakın etkinlikleri bul (semantik arama)
        
        Args:
            query: Kullanıcının arama sorgusu
            k: Kaç etkinlik döndürülecek (varsayılan: 5)
            city_filter: Şehir filtresi (örn: "Kocaeli", "Sakarya")
        
        Returns:
            list: Her biri {'event': dict, 'score': float} içeren liste (benzerlik skoruna göre sıralı)
        """
        try:
            # 🔍 Kullanıcı sorgusunu embedding'e çevir
            query_embedding = self.model.encode([query])[0].astype('float32')
            
            # 🗄️ FAISS ile en yakın vektörleri bul (k*2 al, filtreleme için)
            distances, indices = self.index.search(
                query_embedding.reshape(1, -1),
                min(k * 2, len(self.events))
            )
            
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                event = self.events[idx]
                
                # Şehir filtresi varsa uygula
                if city_filter and event.get('city') != city_filter:
                    continue
                
                # FAISS L2 mesafesini benzerlik skoruna çevir (0-1 arası)
                # Düşük mesafe = yüksek benzerlik
                similarity_score = 1 / (1 + float(dist))
                
                results.append({
                    'event': event,
                    'score': similarity_score
                })
                
                # Yeterli sonuç toplandıysa dur
                if len(results) >= k:
                    break
            
            return results
            
        except Exception as e:
            print(f"❌ Retrieval hatası: {e}")
            return []