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
        print("No files found in data/processed")
        return

    # Configure text splitter
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
            print(f"Skipping file with incorrect name format: {filename}")

    for country, file_list in country_files.items():
        print(f"\n--- Importing data to table: {country} ---")

        # Set up database and create table with correct schema
        db = setup_db(settings.DB_PATH, country)
        table = db.open_table(country)

        total_chunks = 0

        for f in file_list:
            print(f"Processing: {f.name}")
            df = pd.read_json(f, lines=True)

            # List to hold all chunks for the file
            chunked_records = []

            # Loop through each row and create chunks
            for _, row in df.iterrows():
                original_text = row.get("text", "")

                if not original_text:
                    continue

                chunks = splitter.split_text(original_text)

                # For each chunk, create a new object to add to the database
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
                print(f"Created {len(chunked_records)} chunks from file {f.name}.")

        print(f"Done! Table '{country}' updated with {total_chunks} chunks.")


if __name__ == "__main__":
    ingest_db()
