import lancedb
import pandas as pd
from pathlib import Path
from travel_buddy.db.models import Country
from langchain_text_splitters import RecursiveCharacterTextSplitter
from travel_buddy.utils.settings import settings


def setup_db(path, table_name):
    Path(path).mkdir(exist_ok=True)
    db = lancedb.connect(uri=path)
    db.create_table(table_name, schema=Country, exist_ok=True)

    return db


def ingest_db():
    files = list(settings.PROCESSED_DATA_DIR.glob("*.jsonl"))

    if not files:
        print("Inga filer hittades i data/processed")
        return

    # Konfigurera text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ".  ", " ", ""]
    )

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
        db = setup_db(settings.DB_PATH, country)
        table = db.open_table(country)

        total_chunks = 0

        for f in file_list:
            print(f"Bearbetar: {f.name}")
            df = pd.read_json(f, lines=True)

            # Lista för att hålla alla chunks för filen
            chunked_records = []

            # Loopa igenom varje rad och skapa chunks
            for _, row in df.iterrows():
                original_text = row.get("text", "")

                if not original_text:
                    continue

                chunks = splitter.split_text(original_text)

                # För varje chunk, skapa ett nytt objekt att lägga till i databasen
                for index, chunk_text in enumerate(chunks):
                    record = {
                        "filename": row.get("filename", f.name),
                        "country": row.get("country", country),
                        "region": row.get("region", ""),
                        "url": row.get("url", ""),
                        "title": row.get("title", ""),
                        "category": row.get("category", ""),
                        "text": chunk_text,
                        "chunk_index": index,
                    }
                    chunked_records.append(record)
            if chunked_records:
                table.add(chunked_records)
                total_chunks += len(chunked_records)
                print(f"Skapade {len(chunked_records)} chunks från filen {f.name}.")

        print(f"Klar! Tabell '{country}' uppdaterad med {total_chunks} chunks.")


if __name__ == "__main__":
    ingest_db()
