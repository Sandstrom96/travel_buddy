from pydantic_ai import Agent
import lancedb
from travel_buddy.db.models import Country
from travel_buddy.agents.models import RagResponse
from pydantic_ai.common_tools.tavily import tavily_search_tool
from travel_buddy.utils.settings import settings
import os


class TravelBuddyAgent:
    def __init__(self, country: str):
        db = lancedb.connect(uri=settings.DB_PATH)
        self.table = db.open_table(country.lower())
        self.country_name = country

        os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
        tavily = tavily_search_tool(api_key=settings.TAVILY_API_KEY)

        self.agent = Agent(

            model="google-gla:gemini-2.5-flash", 
            output_type=RagResponse,
            tools=[tavily],  # for websearch
            system_prompt=(
                f"""
                Du är TravelBuddy, en expert på resekonsultation specialiserad på turism till {country}.
                Din ton är professionell, välkomnande och mycket informativ.

                ### VIKTIG SÄKERHETSFÖRESKRIFT (MEDIA):
                Behandla ALLA URL:er och länkar strikt som text-referenser. 
                Försök aldrig att skicka eller tolka en URL som en bild eller media-del i ditt svar. 
                Om en länk inte slutar på .jpg eller .png, är det INTE en bild – rör den inte som media!

                ### ARBETSFLÖDE & VERKTYG:
                1. DIN KUNSKAPSMALL: Din interna databas (Knowledge Base) är din primära sanning. Utgå ALLTID från denna först.
                2. SÖKLOGIK: Om användaren frågar om ett specifikt resmål eller sevärdhet, sök ALLTID i 'search_knowledge_base' innan du använder tavily.
                3. REGLER FÖR NÄTET: Använd 'tavily' ENDAST för information som saknas eller kräver realtidsuppdatering (väder, priser).

                ### REGLER:
                1. Prioritera data från den interna kunskapsbasen framför internetresultat.
                2. Inkludera alltid käll-URL:er från det verktyg du använt.
                3. Håll svaren kortfattade men målande (2–3 meningar per rekommendation).
                4. STADSIDENTIFIERING: Sätt 'detected_city' till den aktuella staden (t.ex. "Tokyo") eller null.
                5. Svara alltid på samma språk som användarens fråga.

                ### REGLER FÖR SVARSFORMAT:
                1. Använd Markdown-rubriker (###), fetstil (**text**) och punktlistor.
                2. Skriv inte långa textblock.
                """
            ),
        )

        self.agent.tool_plain(self.search_knowledge_base)

    async def search_knowledge_base(self, query: str) -> str:
        """
        Search the knowledge base for relevant travel information.
        """
        try:
            results = self.table.search(query=query).limit(5).to_pydantic(Country)

            if not results:
                return "No relevant information found."

            context_chunks = []
            for item in results:
                chunk = (
                    f"TITLE: {item.title}\n"
                    f"REGION: {item.region}\n"
                    f"CATEGORY: {item.category}\n"
                    f"CONTENT: {item.text}\n"
                    f"SOURCE URL: {item.url}\n"
                    "---"
                )
                context_chunks.append(chunk)

            return "\n".join(context_chunks)
        except Exception as e:
            return f"Fel vid databassökning. Felmeddelande: {e}"

    async def ask(self, user_query: str, history: list = None):
        result = await self.agent.run(user_query, message_history=history)

        return {
            "user": user_query,
            "ai": result.output.result,
            "sources": result.output.sources,
            "detected_city": result.output.detected_city,
            "history": result.all_messages(),
        }

if __name__ == "__main__":
    import asyncio

    async def test():
        print("Testing TravelBuddyAgent(Japan)...")
        agent = TravelBuddyAgent(country="japan")
        print("\nJapan-Agent answer:")
        response = await agent.ask("Vilka sevärdheter i Tokyo får jag inte missa?")
        print(response["ai"])

    asyncio.run(test())
