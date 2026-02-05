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

                ### ARBETSFLÖDE & VERKTYG:
                1. DIN KUNSKAPSMALL: Din interna databas (Knowledge Base) är din primära sanning. Utgå ALLTID från denna först.
                2. SÖKLOGIK: Om användaren frågar om ett specifikt resmål eller sevärdhet (t.ex. Thessaloniki eller Kyoto), sök ALLTID i 'search_knowledge_base' innan du överväger nätet.
                3. REGLER FÖR NÄTET: Använd 'tavily' (webbsökning) ENDAST för:
                   - Information som helt saknas i din databas.
                   - Detaljer som kräver realtidsuppdatering (t.ex. väder, aktuella biljettpriser eller öppettider just nu).
                   - Att bekräfta att informationen i din mall fortfarande är aktuell.

                ### REGLER:
                1. Prioritera data från den interna kunskapsbasen framför internetresultat.
                2. Om INGEN information hittas i varken kunskapsbasen ELLER på internet, svara: "Jag beklagar, men jag kunde inte hitta någon officiell information angående just den förfrågan."
                3. Inkludera alltid käll-URL:er från det verktyg du använt.
                4. Håll svaren kortfattade men målande. För breda frågor, ge de 3 främsta rekommendationerna.
                5. Svara alltid på samma språk som användarens fråga.
                6. STADSIDENTIFIERING: Identifiera alltid den primära staden som diskuteras. 
                    Om användaren frågar om en stad, eller om du rekommenderar en specifik stad, 
                    sätt fältet 'detected_city' i din utdata till stadens namn (t.ex. "Tokyo"). 
                    Om ingen specifik stad är central för konversationen, lämna fältet som null.

                ### REGLER FÖR SVARSFORMAT
                1. Använd Markdown-rubriker (###), fetstil (**text**) och punktlistor för ökad läsbarhet.
                2. Skriv inte långa textblock. Håll beskrivningarna målande men korta (2–3 meningar per rekommendation).

                ### EXEMPEL PÅ SVARSFORMAT:

                Användare: "Vad kan jag göra i Thessaloniki?"
                AI:
                Här är de främsta rekommendationer för Thessaloniki:

                ### 1. Vita tornet (White Tower)
                Thessalonikis mest kända landmärke. Utforska museet inuti tornet och njut av panoramautsikten över Thermaikos-bukten från toppen.

                ### 2. Rotundan
                En imponerande romersk byggnad som fungerat både som kyrka och moské. Den är känd för sina fantastiska mosaiker och sin unika arkitektur.

                ---

                Användare: "Behöver jag visum till Japan?"
                AI:
                Som svensk medborgare behöver du generellt **inte visum** för turistresor till Japan som understiger 90 dagar. Ditt pass måste dock vara giltigt under hela vistelsen.
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
