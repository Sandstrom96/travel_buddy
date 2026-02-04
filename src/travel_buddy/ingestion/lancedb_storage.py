import lancedb
from datetime import datetime, timezone
from pathlib import Path
from travel_buddy.utils.settings import settings


def store_chunks(chunks: list[dict], destination: str, source_url: str):
    """Store chunks in LanceDB."""
    db_path = Path(settings.lancedb_path)
    db_path.mkdir(parents=True, exist_ok=True)

    db = lancedb.connect(str(db_path))

    enriched_chunks = []
    for chunk in chunks:
        enriched_chunks.append({
            'text': chunk['text'],
            'embedding': chunk['embedding'],
            'destination': destination,
            'source_url': source_url,
            'stored_at': datetime.now(timezone.utc).isoformat(),
            'chunk_id': chunk['chunk_id']
        })

    
    try:
        table = db.open_table("travel_chunks")
        table.add(enriched_chunks)
        print(f" Added {len(enriched_chunks)} chunks to existing table")
    
    except Exception:
        table = db.create_table("travel_chunks", enriched_chunks)
        print(f" Created new table with {len(enriched_chunks)} chunks")