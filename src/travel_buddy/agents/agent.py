from pydantic_ai import Agent
import lancedb
from pathlib import Path
from travel_buddy.db.models import Country
from dotenv import load_dotenv
import datetime

load_dotenv()

BASE_DIR = Path(__file__).parents[3]
DB_PATH = BASE_DIR / "src" / "travel_buddy" / "knowledge_base"


class TravelBuddyAgent:
    def __init__(self):
        self.db = lancedb.connect(uri=DB_PATH)
        self.cutoff_date = (datetime.date.today() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")

        self.agent = Agent(     #Prompt är från gemini pro
            model="google-gla:gemini-2.5-flash",
            system_prompt=(
                f"""
                Du är TravelBuddy, en expert-concierge för resor till både Japan och Grekland.
                Din uppgift är att ge exakta och inspirerande svar baserat på tillgänglig data.

                VIKTIGT FÖR SÖKNING:
                1. Din databas innehåller ENGELSK text. 
                2. När du använder `search_knowledge_base`, översätt ALLTID användarens fråga till ENGELSKA för att få bäst resultat.
                3. För `country`-parametern, använd ENDAST 'greece' eller 'japan'.

                REGLER FÖR INFORMATION:
                - DATABAS: Prioritera alltid information från den interna databasen (knowledge base).
                - NÄTET: Du får ENDAST använda information från nätet som är publicerad efter {self.cutoff_date}. 
                  Om info är äldre än ett år, ignorera den.
                - KÄLLOR: Du måste alltid inkludera käll-URL:er i dina svar så att användaren kan läsa mer.
                - ÄRLIGHET: Om informationen saknas i både databasen och i färska sökresultat, säg: 
                  "Jag hittade tyvärr ingen officiell eller tillräckligt uppdaterad information om detta."
                - SPRÅK: Svara på samma språk som användaren skriver på.
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
        web_query = f"{query} after: {self.cutoff_date}"
        # TODO: Här måste vi koppla på sök API tex tavily eller någoot från miro
        return f"Söker på nätet efter: {web_query}... (Väntar på API-koppling)"
    
    async def ask(self, user_query: str):
        return await self.agent.run(user_query)


if __name__ == "__main__":
    import asyncio
    async def test():
        print("Testing TravelBuddyAgent...")
        agent = TravelBuddyAgent()
        print("?nAgent answer:")
        response = await agent.ask("Vilka sevärdheter i Tokyo får jag inte missa?") # Ändra till det land du vill testa.
        print(response)
    asyncio.run(test())
