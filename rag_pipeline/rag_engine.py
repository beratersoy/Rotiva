"""
RAG Engine - Retrieval-Augmented Generation Motoru (LangChain Powered)
Kullanıcı sorgusuna göre alakalı etkinlikleri bulup, Gemini AI ile yanıt üretir

PROJE GEREKSİNİMLERİ:
✅ Generation Model: Google Gemini 2.5 Flash (LangChain integration)
✅ Embedding Model: Sentence-Transformers (paraphrase-multilingual)
✅ Vektor Database: FAISS
✅ RAG Framework: LangChain
"""

from rag_pipeline.retriever import FAISSRetriever
from utils.llm_client import OpenAIClient
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import os


class RAGEngine:
    """
    LangChain tabanlı RAG (Retrieval-Augmented Generation) pipeline
    FAISS vektor DB + Embeddings + Gemini AI = Akıllı etkinlik asistanı
    """
    
    def __init__(self, events):
        # 🗄️ FAISS + Embedding tabanlı arama motoru (yeni!)
        self.retriever = FAISSRetriever(events)
        
        # 🤖 Gemini AI istemcisi (eski sistem için yedek)
        self.llm_client = OpenAIClient()
        
        # 🦜 LangChain + Gemini entegrasyonu (proje gereksinimi)
        api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyBKe8kUhQIV6kOYZxtW6Bfc9KVoUVIdAsc')
        self.langchain_llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=api_key,
            temperature=0.7
        )
        
        # 📝 LangChain Prompt Template (LİNK DESTEKLİ)
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""Sen Rotiva AI'sın, Türkiye'deki etkinliklerin uzmanı bir asistansın.

Kullanıcının sorusuna aşağıdaki etkinlik bilgilerine dayanarak yanıt ver:

{context}

Kullanıcı Sorusu: {question}

Yanıt Kuralları:
- Doğal, samimi ve yardımsever ol
- Emoji kullan (🎭🎵🎬🎨)
- Her etkinlik yeni satırda
- ÖNEMLİ: Etkinlik adını [Etkinlik İsmi](link) formatında markdown link yap
- Link varsa mutlaka kullan, yoksa sadece etkinlik ismi yaz
- Tarih, yer ve kaynak bilgilerini paylaş
- Kullanıcıya soru sor (ilgi alanlarını keşfet)

Yanıt:"""
        )
        
        # 🔗 LangChain ile RAG zinciri oluştur
        self.rag_chain = LLMChain(
            llm=self.langchain_llm,
            prompt=self.prompt_template
        )
        
        print("✅ LangChain RAG Engine başlatıldı (FAISS + Embeddings + Gemini)\n")
    
    def answer_question(self, query, city_filter=None, top_k=5):
        """
        Kullanıcı sorusuna LangChain RAG tabanlı yanıt üret
        
        Args:
            query: Kullanıcının sorusu
            city_filter: Şehir filtresi (örn: "Kocaeli", "Sakarya")
            top_k: Kaç etkinlik alınacak (varsayılan: 5)
        
        Returns:
            dict: {'answer': str, 'sources': list} - AI yanıtı ve kullanılan kaynaklar
        """
        try:
            # 1. RETRIEVAL: En alakalı etkinlikleri bul (FAISS + Embeddings ile semantik arama)
            results = self.retriever.retrieve(query, k=top_k, city_filter=city_filter)
            
            if not results:
                return {
                    'answer': 'Üzgünüm, kriterlerine uygun etkinlik bulunamadı. Farklı bir arama yapmak ister misin?',
                    'sources': []
                }
            
            # 2. CONTEXT OLUŞTURMA: Bulunan etkinlikleri metin formatına çevir (LİNK DAHİL)
            context_text = "İlgili Etkinlikler:\n\n"
            for i, result in enumerate(results, 1):
                event = result['event']
                context_text += f"{i}. {event['title']}\n"
                context_text += f"   Tarih: {event['date']}\n"
                context_text += f"   Yer: {event['location']}\n"
                context_text += f"   Şehir: {event['city']}\n"
                context_text += f"   Link: {event.get('link', 'Yok')}\n"
                context_text += f"   Kaynak: {event['source']}\n\n"
            
            # 3. GENERATION: LangChain + Gemini AI ile doğal dil yanıtı üret (PROJE GEREKSİNİMİ)
            try:
                # LangChain RAG chain kullan
                response = self.rag_chain.invoke({
                    "context": context_text,
                    "question": query
                })
                answer = response['text'] if isinstance(response, dict) else str(response)
            except Exception as lc_error:
                # LangChain hatası olursa, eski sisteme geri dön
                print(f"⚠️ LangChain hatası, fallback aktif: {lc_error}")
                answer = self.llm_client.generate_response(context_text, query)
            
            return {
                'answer': answer,
                'sources': [r['event'] for r in results]
            }
            
        except Exception as e:
            return {
                'answer': f"Hata: {e}",
                'sources': []
            }