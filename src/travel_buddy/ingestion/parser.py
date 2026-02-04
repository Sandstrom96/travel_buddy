from pathlib import Path
from datetime import datetime, timezone
import re

def parse_markdown(file_path: str) -> dict:
    """Parsing markdown file into structured sections."""
    content = Path(file_path).read_text(encoding='utf-8')

    
    sections = []
    current_heading = "Overview"
    current_content = []

    for line in content.split('\n'):
        if line.startswith('## ') or line.startswith('## '):
            if current_content:
            
                sections.append({
                    'heading': current_heading,
                    'content': '\n'.join(current_content).strip()
                })
            
            current_heading = line.lstrip('#').strip()
            current_content = []
            
        else:
            current_content.append(line)
        
    if current_content:
        sections.append({
            'heading': current_heading,
            'content': '\n'.join(current_content).strip()
        })

    title = sections[0]['heading'] if sections else Path(file_path).stem

    return {
        'title': title,
        'sections': sections,
        'metadata': {
            'source_file': file_path,
            'parsed_at': datetime.now(timezone.utc).isoformat()
        }
    }

        

    