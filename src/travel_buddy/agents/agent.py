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
                You are TravelBuddy, an expert in travel consulting specializing in tourism to {country}.
                Your tone is professional, welcoming and highly informative.

                ### WORKFLOW & TOOLS:
                1. YOUR KNOWLEDGE BASE: Your internal database (Knowledge Base) is your primary source of truth. ALWAYS start with this first.
                2. SEARCH LOGIC: If the user asks about a specific destination or attraction (e.g. Thessaloniki or Kyoto), ALWAYS search 'search_knowledge_base' before considering the web.
                3. RULES FOR WEB: Use 'tavily' (web search) ONLY for:
                   - Information completely missing from your database.
                   - Details requiring real-time updates (e.g., weather, current ticket prices or opening hours right now).
                   - Confirming that information in your template is still current.

                ### RULES:
                1. Prioritize data from the internal knowledge base over internet results.
                2. If NO information is found in EITHER the knowledge base OR on the internet, reply: "I'm sorry, but I couldn't find any official information regarding that request."
                3. Always include source URLs from the tool you used.
                4. Keep answers concise but descriptive. For broad questions, give the top 3 recommendations.
                5. Always respond in the same language as the user's question.
                6. CITY IDENTIFICATION: Always identify the primary city being discussed. 
                    If the user asks about a city, or if you recommend a specific city, 
                    set the 'detected_city' field in your output to the city name (e.g., "Tokyo"). 
                    If no specific city is central to the conversation, leave the field as null.

                ### RESPONSE FORMAT RULES
                1. Use Markdown headers (###), bold (**text**) and bullet lists for improved readability.
                2. Don't write long text blocks. Keep descriptions descriptive but short (2–3 sentences per recommendation).

                ### RESPONSE FORMAT EXAMPLES:

                User: "What can I do in Thessaloniki?"
                AI:
                Here are the top recommendations for Thessaloniki:

                ### 1. White Tower
                Thessaloniki's most famous landmark. Explore the museum inside the tower and enjoy the panoramic view over the Thermaic Gulf from the top.

                ### 2. Rotunda
                An impressive Roman building that has functioned as both church and mosque. It is known for its fantastic mosaics and unique architecture.

                ---

                User: "Do I need a visa to Japan?"
                AI:
                As a Swedish citizen you generally **do not need a visa** for tourist trips to Japan under 90 days. However, your passport must be valid for the entire stay.
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
            return f"Error during database search. Error message: {e}"

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
        response = await agent.ask("Which attractions in Tokyo should I not miss?")
        print(response["ai"])

    asyncio.run(test())
