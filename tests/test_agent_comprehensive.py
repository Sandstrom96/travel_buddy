import asyncio
import sys
from pathlib import Path

root_dir = Path(__file__).parents[1]
sys.path.append(str(root_dir / "src"))

from travel_buddy.agents.agent import TravelBuddyAgent

async def run_comprehensive_test():
    print("\n" + "="*70)
    print("KÖR INTEGRATIONSTEST: TRAVELBUDDY")
    print("="*70)

    # TEST 1: Japan (Kunskapsmall)
    print("\n[TEST 1] Verifierar Japan-databas...")
    agent_jp = TravelBuddyAgent(country="japan")
    res1 = await agent_jp.ask("Vilka tempel rekommenderas i Tokyo?")
    print(f"AI: {res1['ai']}")
    print(f"Källor: {res1['sources']}")

    # TEST 2: Grekland (Din data)
    print("\n[TEST 2] Verifierar Grekland-databas...")
    agent_gr = TravelBuddyAgent(country="greece")
    res2 = await agent_gr.ask("Berätta om Thessaloniki.")
    print(f"AI: {res2['ai']}")
    print(f"Källor: {res2['sources']}")

    # TEST 3: Webb (Tavily)
    print("\n[TEST 3] Verifierar Tavily (Realtid)...")
    res3 = await agent_gr.ask("Vad är vädret i Aten just nu?")
    print(f"AI: {res3['ai']}")

    # TEST 4: Minne (Historik)
    print("\n[TEST 4] Verifierar Chatthistorik...")
    res4 = await agent_gr.ask("Hur tar jag mig dit från flygplatsen?", history=res3['history'])
    print(f"AI: {res4['ai']}")

    print("\n" + "="*70)
    print("TESTER SLUTFÖRDA")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())