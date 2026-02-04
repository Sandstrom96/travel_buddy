from pydantic_ai import Agent
import lancedb
from pathlib import Path
from travel_buddy.db.models import Country
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parents[3]
DB_PATH = BASE_DIR / "src" / "travel_buddy" / "knowledge_base"


class TravelBuddyAgent:
    def __init__(self):
        self.db = lancedb.connect(uri=DB_PATH)

        self.agent = Agent(     #Prompt är från gemini pro
            model="google-gla:gemini-2.5-flash",
            system_prompt=(
                f"""
                Du är TravelBuddy, en expert-concierge för resor till både Japan och Grekland.
                Din uppgift är att ge exakta och inspirerande svar.

                DIN KUNSKAPSMALL:
                - Din interna databas (Knowledge Base) är din primära mall och "sanning". Utgå alltid från denna först.
                - Om databasen innehåller information, använd den som bas för ditt svar.
                - Om användaren frågar om ett specifikt resmål (t.ex. Thessaloniki), sök ALLTID i din Knowledge Base efter sevärdheter och tips DÄR, även om du också behöver söka på nätet efter andra detaljer.

                REGLER FÖR NÄTET:
                Du ska använda webbsökning (search_web) i följande scenarier:
                1. Om specifik information helt saknas i din databas.
                2. Om användaren ber om detaljer som kräver realtidsuppdatering (t.ex. specifika öppettider, biljettpriser just nu eller lokala väderförhållanden).
                3. För att bekräfta att informationen i din mall fortfarande är aktuell om du misstänker att något ändrats.

                KRAV PÅ SVAR:
                - Om du hittar nyare eller mer specifik information på nätet som kompletterar databasen, nämna detta kort (t.ex. "Enligt de senaste uppdateringarna...").
                - Inkludera alltid käll-URL:er för all information du hämtar.
                - Svara på samma språk som användaren skriver på.
                
                TEKNISKT:
                - Databasen är på ENGELSKA. Översätt sökningar dit.
                - För country-parametern: använd 'greece' eller 'japan'.
                """
            ),
        )

        self.agent.tool_plain(self.search_knowledge_base)
        self.agent.tool_plain(self.search_web)

    async def search_knowledge_base(self, query: str, country) -> str:
        """
        Search the knowledge base for relevant travel information.
        """
        try:
            table = self.db.open_table(country.lower())
            results = table.search(query=query).limit(5).to_pydantic(Country)

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
            return f"Kunde inte hitta databas-tabellen för {country}. Felmeddelande: {e}"

    async def search_web(self, query: str) -> str:
        """
        Search the web for relevant travel information.
        """
        web_query = f"{query} latest updates"
        # TODO: Här måste vi koppla på sök API tex tavily eller någoot från miro
        return f"Söker på nätet efter: {web_query}... (Väntar på API-koppling)"
    
    async def ask(self, user_query: str, history: list = None):
        return await self.agent.run(user_query, message_history=history)


if __name__ == "__main__":
    import asyncio
    async def test():
        print("Testing TravelBuddyAgent...")
        agent = TravelBuddyAgent()
        print("?nAgent answer:")
        response = await agent.ask("Vilka sevärdheter i Tokyo får jag inte missa?") # Ändra till det land du vill testa.
        print(response)
    asyncio.run(test())
