from pydantic import Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model = get_registry().get("gemini-text").create(name="gemini-embedding-001")


class Country(LanceModel):
    filename: str = Field(description="Name of the source file")
    country: str = Field(description="Country name")
    region: str = Field(description="Region within the country")
    url: str = Field(description="Source URL")
    title: str = Field(description="Article or page title")
    category: str = Field(
        description="Content category (destination, practical_guide, spot, news, general)"
    )
    text: str = embedding_model.SourceField()
    embedding: Vector(3072) = embedding_model.VectorField()
