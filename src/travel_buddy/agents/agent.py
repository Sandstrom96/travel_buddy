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
        self.table = db.open_table(country)
        self.country_name = country

        os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
        tavily = tavily_search_tool(api_key=settings.TAVILY_API_KEY)

        self.agent = Agent(
            model="google-gla:gemini-2.5-flash",
            system_prompt=(
                f"""
                You are TravelBuddy, an expert travel concierge specializing in tourism to {country}.
                Your tone is professional, welcoming, and highly informative.

                ### WORKFLOW & TOOLS:
                1. For general recommendations (what to do, where to go): Use 'search_knowledge_base' ONLY.
                2. For specific real-time details (opening hours, ticket prices, or if the database info is incomplete): Use 'tavily'.
                3. Use the search engine ONLY as a supplement to the database or for real-time data.

                ### RULES:
                1. Prioritize internal knowledge base data over internet results.
                2. If NO information is found in either the knowledge base OR the internet, state: "I'm sorry, but I couldn't find official information regarding that specific request."
                3. Always include source URLs from whichever tool you used.
                4. Keep responses concise but evocative. For broad queries, provide the top 3 recommendations.
                5. Always respond in the same language as the user's query.
                6. CITY DETECTION: Always identify the primary city being discussed. 
                If the user asks about a city, or if you recommend a specific city, 
                set the 'detected_city' field in your output to that city's name (e.g., "Tokyo").
                If no specific city is central to the conversation, leave it as null.

                ### RESPONSE FORMAT RULES
                1. Use Markdown headings (###), bold text (**text**), and bullet points for readability.
                2. Do not write walls of text. Keep descriptions evocative but brief (2-3 sentences per recommendation).

                ### EXAMPLES (Follow this style)

                User: "What can you do in tokyo?"
                AI:
                Here are the top 3 must-visit attractions in Tokyo:

                ### 1. Senso-ji Temple
                Tokyo's oldest temple, located in Asakusa. Explore the vibrant Nakamise shopping street leading up to the temple, filled with traditional snacks and souvenirs.
                
                ### 2. Shibuya Crossing
                One of the busiest pedestrian crossings in the world. Experience the bustling energy of Tokyo as hundreds of people cross from all directions amidst towering neon signs.

                ### 3. Tsukiji Outer Market
                A food lover's paradise offering fresh sushi, seafood, and traditional Japanese street food. Don't miss trying a bowl of chirashi at one of the local eateries.

                ---

                User: "When is the Cherry Blossom season?"
                AI:
                The cherry blossom (Sakura) season typically occurs between **late March and early April**.

                The exact timing depends on the weather, but full bloom usually lasts for about a week. Popular spots like Ueno Park become very crowded during this time.
            """
            ),
            output_type=RagResponse,
            tools=[tavily],
        )

        self.agent.tool_plain(self.search_knowledge_base)

    async def search_knowledge_base(self, query: str) -> str:
        """
        Search the knowledge base for relevant travel information.
        """

        results = self.table.search(query=query).limit(3).to_pydantic(Country)

        if not results:
            return "Information not found in database. You may use the search engine to find specific details."

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

    async def ask(self, user_query: str, history: list = None):
        self.result = await self.agent.run(user_query, message_history=history)

        return {
            "user": user_query,
            "ai": self.result.output.result,
            "sources": self.result.output.sources,
            "detected_city": self.result.output.detected_city,
            "history": self.result.all_messages(),
        }
