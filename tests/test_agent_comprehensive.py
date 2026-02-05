import asyncio
import sys
from pathlib import Path

# Lägg till src i path
root_dir = Path(__file__).parents[1]
sys.path.append(str(root_dir / "src"))

from travel_buddy.agents.agent import TravelBuddyAgent

async def run_comprehensive_test():
    print("\n" + "="*70)
    print("KÖR STRESS-TEST: INTEGRATION & MINNE (STATELESS)")
    print("="*70)

    # --- TEST 1: JAPAN (KONTEXT-KONTROLL) ---
    print("\n[TEST 1] Japan: Kan den koppla ihop platser?")
    agent_jp = TravelBuddyAgent(country="japan")
    
    # Första frågan skapar kontext
    res1 = await agent_jp.ask("Berätta om Sensoji-templet i Tokyo.")
    print(f"AI (Svar 1): {res1['ai'][:100]}...") # Visar bara början

    # Följdfråga: Använder 'dit' och 'där'
    print("\n[TEST 2] Japan Minne: Förstår den 'dit'?")
    res2 = await agent_jp.ask("Hur tar jag mig dit från Shinjuku?", history=res1['history'])
    
    if "Sensoji" in res2['ai'] or "Asakusa" in res2['ai']:
        print(" SUCCESS: Agenten minns att vi pratar om Sensoji/Asakusa.")
    else:
        print(" FAIL: Agenten verkar ha glömt kontexten.")
    print(f"AI: {res2['ai'][:150]}...")

    # --- TEST 2: GREKLAND (VÄDER-INTEGRATION & MINNE) ---
    print("\n" + "-"*50)
    print("[TEST 3] Grekland: Kan den hitta i databasen?")
    agent_gr = TravelBuddyAgent(country="greece")
    
    res3 = await agent_gr.ask("Berätta kort om Thessaloniki.")
    print(f"AI (Svar 3): {res3['ai'][:100]}...")

    # Följdfråga: Testar väder-verktyget via kontext
    print("\n[TEST 4] Grekland Minne: Förstår den 'där' och kollar väder?")
    res4 = await agent_gr.ask("Hur är vädret där just nu?", history=res3['history'])
    
    if "Thessaloniki" in res4['ai']:
        print(" SUCCESS: Agenten fattade att 'där' är Thessaloniki.")
    else:
        print(" FAIL: Agenten tappade bort staden.")
    
    print(f"AI: {res4['ai']}")

    # --- TEST 3: TEKNISK VALIDERING ---
    print("\n" + "-"*50)
    print("[TEST 5] Teknisk kontroll av historik-formatet")
    if isinstance(res4['history'], list) and len(res4['history']) > 0:
        print(f" SUCCESS: Historiken returneras som en lista med {len(res4['history'])} meddelanden.")
    else:
        print(" FAIL: Historik-formatet är felaktigt eller tomt.")

    print("\n" + "="*70)
    print("TESTER SLUTFÖRDA")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(run_comprehensive_test())