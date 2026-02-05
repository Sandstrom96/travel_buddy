from pydantic import Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector

embedding_model = (
    get_registry()
    .get("sentence-transformers")
    .create(name="BAAI/bge-small-en-v1.5", device="cpu")
)


class Country(LanceModel):
    filename: str = Field(description="Name of the source file")
    country: str = Field(description="Country name")
    region: str = Field(description="Region within the country")
    url: str = Field(description="Source URL")
    title: str = Field(description="Article or page title")
    category: str = Field(
        description="Content category (destination, practical_guide, spot, news, general)"
    )
    chunk_index: int = Field(description="Index of the text chunk")
    text: str = embedding_model.SourceField()

    # Here we use embedding_model.ndims() to define the vector dimensions. We write "# type:ignore" to 
    # avoid type errors in the editor as the dimension is calculated dynamically.
    embedding: Vector(embedding_model.ndims()) = embedding_model.VectorField() # type: ignore
