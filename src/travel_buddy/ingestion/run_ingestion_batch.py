from pathlib import Path
from travel_buddy.ingestion.parser import parse_markdown
from travel_buddy.ingestion.chunker import chunk_text
from travel_buddy.ingestion.embedder import EmbeddingService
from travel_buddy.ingestion.lancedb_storage import store_chunks


def get_metadata_from_filename(filename: str) -> dict:
    """Extract metadata from filename (e.g., tokyo_sensoji_temple_raw.md)."""

    name = filename.replace("_raw.md", "")

    mapping = {
        "tokyo_overview": {"destination": "tokyo", "category": "destination"},
        "kyoto_overview": {"destination": "kyoto", "category": "destination"},
        "osaka_overview": {"destination": "osaka", "category": "destination"},
        "sensoji_temple": {"destination": "tokyo", "category": "attraction"},
        "fushimi_inari": {"destination": "kyoto", "category": "attraction"},
        "kinkakuji": {"destination": "kyoto", "category": "attraction"},
        "osaka_castle": {"destination": "osaka", "category": "attraction"},
        "dotonbori": {"destination": "osaka", "category": "attraction"},
        "cherry_blossoms": {"destination": "japan", "category": "event"},
        "gion_matsuri": {"destination": "kyoto", "category": "event"},
        "visa_entry_requirements": {"destination": "japan", "category": "practical"},
    }

    return mapping.get(name, {"destination": "unknown", "category": "unknown"})

def main():
    raw_dir = Path("data/raw")

    if not raw_dir.exists():
        print(f"❌ Directory not found: {raw_dir}/")
        return
    
    raw_files = list(raw_dir.glob("*raw.md"))

    if not raw_files:
        print(f"❌ No markdown files found in {raw_dir}/")
        return
    
    print("=" * 60)
    print("🔄 Travel buddy Ingestion Pipeline")
    print("=" * 60)
    print(f"\n📂 Found {len(raw_files)} files to process\n")

    print("📦 Loading embedding model...")
    embedding_service = EmbeddingService()


    for i, file_path in enumerate(raw_files, 1):
        print(f"\n[{i}/{len(raw_files)}] Processing: {file_path.name}")

        try:
            metadata = get_metadata_from_filename(file_path.name)
            destination = metadata["destination"]
            category = metadata["category"]

            print(f"   Parsing...")
            parsed_data = parse_markdown(str(file_path))

            print(f"  Extracting text ({len(parsed_data['sections'])} sections)...")
            all_text = "\n\n".join([
                f"{section['heading']}\n{section['content']}"
                for section in parsed_data['sections']
            ])

            print(f"  Chunking...")
            chunks = chunk_text(all_text)
            print(f"  Created {len(chunks)} chunks")

            print(f"  Embedding ({len(chunks)} chunks)...")
            chunks_with_embeddings = embedding_service.embed_chunks(chunks)

            print(f"  Storing in LanceDB...")
            source_url = f"https://japan-guide.com (from: {file_path.name})"
            store_chunks(chunks_with_embeddings, destination, source_url)

            print(f"  ✅ Complete")

        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue

    print("\n" + "=" * 60)
    print("✨ Ingestion complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()