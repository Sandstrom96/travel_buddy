import lancedb
import pandas as pd
import time
from pathlib import Path
from models import Country

BASE_DIR = Path(__file__).parents[2]
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
DB_PATH = BASE_DIR / "data" / "lancedb"


def setup_db(path, table_name):
    Path(path).mkdir(exist_ok=True)
    db = lancedb.connect(uri=str(path))
    db.create_table(table_name, schema=Country, exist_ok=True)

    return db


def ingest_db():
    files = list(PROCESSED_DATA_DIR.glob("*.jsonl"))

    if not files:
        print("Inga filer hittades i data/processed")
        return

    country_files = {}

    for file_path in files:
        filename = file_path.name
        if "_" in filename:
            country = filename.split("_")[0]

            if country not in country_files:
                country_files[country] = []

            country_files[country].append(file_path)
        else:
            print(f"Hoppar över fil med felaktigt namnformat: {filename}")

    for country, file_list in country_files.items():
        print(f"\n--- Importerar data till tabellen: {country} ---")

        # Sätt upp databasen och skapa tabell med rätt schema
        db = setup_db(DB_PATH, country)

        # Samla all data för detta land i en lista
        dfs = []
        for f in file_list:
            print(f"   Läser in: {f.name}")
            df = pd.read_json(f, lines=True)
            dfs.append(df)

        if dfs:
            # Slå ihop till en stor DataFrame
            full_df = pd.concat(dfs, ignore_index=True)

            # Populera tabellen med data i batches
            try:
                table = db.open_table(country)
                batch_size = 20
                total_rows = len(full_df)

                for i in range(0, total_rows, batch_size):
                    batch_df = full_df.iloc[i : i + batch_size]
                    table.add(batch_df)

                    current_batch = (i // batch_size) + 1
                    total_batches = (total_rows + batch_size - 1) // batch_size
                    print(
                        f"   Batch {current_batch}/{total_batches} tillagd ({len(batch_df)} rader)"
                    )

                    # Vänta mellan batches (utom efter den sista)
                    if i + batch_size < total_rows:
                        time.sleep(
                            60
                        )  # 1 minut mellan batches för att inte slå i gemini rate limit

                print(
                    f"   ✅ Klar! Tabell '{country}' uppdaterad med {total_rows} rader."
                )
            except Exception as e:
                print(f"   ❌ Fel vid inmatning av data: {e}")


if __name__ == "__main__":
    ingest_db()
