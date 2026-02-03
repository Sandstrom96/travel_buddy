# This was written by Gemini Pro


import asyncio
import sys
from pathlib import Path

root_dir = Path(__file__).parents[1]
sys.path.append(str(root_dir / "src"))

from travel_buddy.agents.agent import TravelBuddyAgent

async def run_comprehensive_test():
    agent = TravelBuddyAgent()
    
    print("\n" + "="*60)
    print("KÖR OMFATTANDE INTEGRATIONSTEST: TRAVELBUDDY")
    print("="*60)

    # TEST 1: Japan (Kunskapsmall)
    print("\n[TEST 1] Söker i Japan-datan...")
    res1 = await agent.ask("Vilka tempel rekommenderas i Tokyo?")
    print(f"SVAR: {res1.output}")

    # TEST 2: Grekland (Din nya data)
    print("\n[TEST 2] Söker i Grekland-datan...")
    res2 = await agent.ask("Vad kan man göra på de Joniska öarna?")
    print(f"SVAR: {res2.output}")

    # TEST 3: Realtid/Webb (Ska trigga webbsök-logiken)
    print("\n[TEST 3] Testar behov av nätet (öppettider)...")
    res3 = await agent.ask("När öppnar Akropolismuseet imorgon?")
    print(f"SVAR: {res3.output}")

    # TEST 4: Historik (Minne)
    print("\n[TEST 4] Testar kontext och historik...")
    res4 = await agent.ask("Hur tar jag mig dit från centrum?", history=res3.all_messages())
    print(f"SVAR: {res4.output}")

    print("\n" + "="*60)
    print("TESTER SLUTFÖRDA")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())