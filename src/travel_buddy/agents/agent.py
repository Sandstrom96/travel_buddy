from pydantic_ai import Agent
import lancedb
from pathlib import Path
from travel_buddy.db.models import Country
from travel_buddy.agents.models import RagResponse
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parents[3]
DB_PATH = BASE_DIR / "src" / "travel_buddy" / "knowledge_base"


class TravelBuddyAgent:
    def __init__(self, country: str):
        db = lancedb.connect(uri=DB_PATH)
        self.table = db.open_table(country)
        self.country_name = country

        self.agent = Agent(
            model="google-gla:gemini-2.5-flash",
            system_prompt=(
                """
                You are TravelBuddy, an expert travel concierge specializing in tourism to {country}.
                Your tone is professional, welcoming, and highly informative.

                RULES:
                1. Answer questions ONLY using the information provided in the retrieved context. 
                Do not use outside knowledge or hallucinations.
                2. If the context does not contain the answer, state: "I'm sorry, but I couldn't find official information regarding that specific request in my records."
                3. Prioritize details like seasons, opening hours, and entry requirements.
                4. Keep responses concise but evocative. For broad queries, provide the top 3 recommendations.
                5. Always respond in the same language as the user's query.
            """
            ),
            output_type=RagResponse,
        )

        self.agent.tool_plain(self.search_knowledge_base)

    async def search_knowledge_base(self, query: str) -> str:
        """
        Search the knowledge base for relevant travel information.
        """

        results = self.table.search(query=query).limit(3).to_pydantic(Country)

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

    async def ask(self, user_query: str):
        message_history = self.result.all_messages() if self.result else None
        self.result = await self.agent.run_async(
            user_query, message_history=message_history
        )

        return {
            "user": user_query,
            "ai": self.result.output.result,
            "sources": self.result.output.sources,
            "regions": self.result.output.regions,
        }


if __name__ == "__main__":
    agent = TravelBuddyAgent(country="japan")
    import asyncio

    response = asyncio.run(
        agent.ask("What are the top 3 must-visit spots in Kyoto during spring?")
    )
    print(response)
