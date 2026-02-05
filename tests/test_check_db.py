import lancedb
from travel_buddy.utils.settings import settings

db = lancedb.connect(uri=settings.DB_PATH)
table = db.open_table("japan")
print(f"Antal rader i Japan-tabellen: {len(table.to_pandas())}")
print(table.to_pandas().head()) # Se de första raderna