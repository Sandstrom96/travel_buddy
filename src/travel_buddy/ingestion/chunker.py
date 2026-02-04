from travel_buddy.utils.settings import settings

def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> list[dict]:
    chunk_size = chunk_size or settings.chunk_size
    overlap = overlap or settings.chunk_overlap

    sentences = text.replace('\n', '').split('. ')

    chunks = []
    current_chunk = []
    current_length = 0
    chunk_id = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        sentence_length = len(sentence)

        if current_length + sentence_length > chunk_size and current_chunk:
            chunk_text = '. '.join(current_chunk) + '.'
            chunks.append({
                'chunk_id': f"chunk_{chunk_id}",
                'text': chunk_text,
                'char_count': len(chunk_text)
            })
            chunk_id += 1

            overlap_text = chunk_text[-overlap:] if len(chunk_text) > overlap else chunk_text
            current_chunk = [overlap_text, sentence]
            current_length = len(overlap_text) + sentence_length
        else:
            current_chunk.append(sentence)
            current_length += sentence_length
    
    if current_chunk:
        chunk_text = '. '.join(current_chunk) + '.'
        chunks.append({
            'chunk_id': f"chunk_{chunk_id}",
            'text': chunk_text,
            'char_count': len(chunk_text)
        })
    
    return chunks