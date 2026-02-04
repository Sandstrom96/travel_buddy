import lancedb
from pathlib import Path
from sentence_transformers import SentenceTransformer
from google import genai
from travel_buddy.utils.settings import Settings, settings
import logging
logger = logging.getLogger(__name__)

class RAGService:

    def __init__(self):
        self.embedding_model = SentenceTransformer(settings.embedding_model)
        self.model = settings.GEMINI_MODEL_NAME

        db_path = Path(settings.lancedb_path)
        self.db = lancedb.connect(str(db_path))
        self.table = self.db.open_table("travel_chunks")

        self.client = genai.Client(api_key=settings.google_api_key)

    def query(self, question: str, destination: str = None, top_k: int = 5) -> dict:
        question_embedding = self.embedding_model.encode(question).tolist()
        results = self.table.search(question_embedding).limit(top_k)

        if destination:
            results = results.where(f"destination = '{destination}'")

        search_results = results.to_list()

        if not search_results:
            return {
                "answer": "I couldn`t find relevant information to answer your question.",
                "sources": []
            }
        
        context = "\n\n".join([
            f"[Source {i+1}] {chunk['text']}"
            for i, chunk in enumerate(search_results)
        ])

        # Prompt for LLM
        prompt = f"""You are a helpful travel guide assistant for Japan.
Answer the following question based on the provided context.
If the context doesn't contain enough information to fully answer the question, provide what information is available and politely indicate what additional details you cannot provide from the current context.
Be helpful, informative, and suggest related aspects that might help the user.

Context:
{context}

Question: {question}

Answer (be concise and helpful):"""

        try:
            print(f"DEBUG: Calling Gemini with model: {self.model}")
            print(f"DEBUG: Question: {question}")
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            print(f"DEBUG: Response type: {type(response)}")
            print(f"DEBUG: Response attributes: {dir(response)}")
            print(f"DEBUG: Full response: {response}")
            
            # Extract text from Gemini response
            try:
                answer = response.candidates[0].content.parts[0].text
                print(f"DEBUG: Got answer from candidates: {answer[:100]}")
            except (AttributeError, IndexError) as e:
                print(f"DEBUG: Candidates failed: {e}")
                try:
                    answer = response.text
                    print(f"DEBUG: Got answer from text: {answer[:100]}")
                except Exception as e2:
                    print(f"DEBUG: Text failed: {e2}")
                    answer = str(response)
                    
        except Exception as e:
            print(f"ERROR: Exception in Gemini call: {e}")
            import traceback
            traceback.print_exc()
            answer = f"Error generating response: {str(e)}"

        sources = [
            {
                "text": chunk['text'][:200] + "...",
                "destination": chunk['destination'],
                "source_url": chunk['source_url']
            }
            for chunk in search_results
        ]

        return {
            "answer": answer,
            "sources": sources,
            "context_used": len(search_results)
        }

