import re
from pathlib import Path
import json

BASE_DIR = Path(__file__).parents[3]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"


## Tog hjälp av AI för att skapa detta
def clean_markdown_content(raw_text):
    """
    Rensar bort navigering, menyer och boilerplate från japan.travel markdown.
    """
    lines = raw_text.split("\n")
    cleaned_lines = []

    # Flaggor för att veta om vi är inne i ett "skräp-block"
    in_noise_block = False

    # Nyckelord som indikerar start av stora navigeringsmenyer
    noise_start_markers = [
        "- Select Language",
        "- [Trade](",
        "- [Media](",
        "My Favorites",
        "Use the",
        "What is the primary reason to visit",
        "Copyright ©",
        "Thank you!",
        "Please Choose Your Language",
        "Travel Widgets",
        "Helpful Links",
        "Related JNTO Sites",
        "About JNTO",
        "social-media",
        "## Planning a Trip to Japan",
        "## Recommended for You",
        "## Related Links",
        "### Did this information help you",
        "### Thank you for your feedback",
        "## Near",
        #specifika nyckelord för grekland-data
        "###### CONTENTS",
        "_The artwork on the cover",
        "Follow us on",
        "Newsletter"
    ]

    # Regex för att hitta rubriker som faktiskt är innehåll
    header_pattern = re.compile(r"^#+\s+")

    for line in lines:
        stripped_line = line.strip()

        # Kolla om vi går in i ett känt skräpblock
        if any(stripped_line.startswith(marker) for marker in noise_start_markers):
            in_noise_block = True
            continue

        # Om vi ser en "riktig" rubrik (innehållet), kan vi ibland nollställa bruset
        # (Detta är en heuristik: Om vi ser "# Hiroshima" är vi troligen i content)
        if in_noise_block and header_pattern.match(stripped_line):
            # Men vi vill inte återaktivera om det är sidfotsrubriker
            if (
                "Related Links" not in stripped_line
                and "Explore Nearby" not in stripped_line
            ):
                in_noise_block = False

        # Specifik rensning av de enorma listorna med länkar (Destinations, Things to Do etc)
        # Dessa filer verkar ha enorma listor av länkar som inte är brödtext.
        # Vi tar bort rader som BARA är en markdown-länk eller bild.
        is_only_link = re.match(r"^\s*-\s*\[.*?\]\(.*?\)\s*$", stripped_line)
        is_only_image = re.match(r"^\s*\[?!\[.*?\]\(.*?\).*", stripped_line)

        if in_noise_block:
            continue

        # Hoppa över rader som bara är navigeringslänkar eller bilder utan kontext
        if is_only_link or is_only_image:
            continue

        # Ta bort template-variabler (t.ex. ${v.title})
        if "${" in stripped_line:
            continue

        # Behåll raden om den har innehåll
        if stripped_line:
            cleaned_lines.append(stripped_line)

    # Slå ihop text och städa upp länk-syntax i brödtexten
    full_text = "\n".join(cleaned_lines)

    # Ta bort bilder men behåll eventuell alt-text om den är vettig, annars ta bort
    # Regex: ![alt text](url) -> alt text
    full_text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", full_text)

    # Ta bort vanliga länkar men behåll texten: [text](url) -> text
    full_text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", full_text)

    # Ta bort överflödiga nya rader (mer än 2)
    full_text = re.sub(r"\n{3,}", "\n\n", full_text)

    return full_text.strip()


def extract_frontmatter(text):
    """
    Extraherar URL och Title från YAML frontmatter.
    """
    metadata = {}
    # Hitta blocket mellan första --- och andra ---
    match = re.search(r"^---\s+(.*?)\s+---", text, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        for line in yaml_content.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip().strip('"')
    return metadata, text[match.end() :] if match else text


def determine_category(url):
    """Gissar kategori baserat på URL-strukturen."""
    if "destinations" in url:
        return "destination"
    elif "plan" in url or "guide" in url:
        return "practical_guide"
    elif "spot" in url:
        return "spot"  # Specifika sevärdheter
    elif "news" in url:
        return "news"
    else:
        return "general"


def process_all_folders():
    countries = [f for f in RAW_DATA_DIR.iterdir() if f.is_dir()]

    if not countries:
        print(f"Varning: Hittade inga länder i {RAW_DATA_DIR}")
        return

    total_files_processed = 0

    for country_path in countries:
        country_name = country_path.name
        print(f"--> Går in i land: {country_name}")

        # --- STEG 1: Hantera filer direkt i landsmappen (t.ex. Visum, Allmän info) ---
        # Dessa får regionnamnet "General"
        general_files = list(country_path.glob("*.md"))

        if general_files:
            print(f"    --> Bearbetar {len(general_files)} allmänna filer (General)...")
            process_file_list(general_files, country_name, "General")
            total_files_processed += len(general_files)

        # --- STEG 2: Hantera regioner (undermappar) ---
        regions = [r for r in country_path.iterdir() if r.is_dir()]

        for region_path in regions:
            region_name = region_path.name
            print(f"    --> Bearbetar region: {region_name}...")

            files = list(region_path.rglob("*.md"))
            process_file_list(files, country_name, region_name)
            total_files_processed += len(files)

    print(f"\nKlar! Totalt {total_files_processed} filer behandlade.")


# --- Hjälpfunktion för att slippa upprepa koden ---
def process_file_list(files, country_name, region_name):
    processed_entries = []

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()

            metadata, body_content = extract_frontmatter(raw_content)

            raw_title = metadata.get("title", "Unknown")
            clean_title = raw_title.split("|")[0].strip()
            clean_text = clean_markdown_content(body_content)

            if clean_title.lower() == "page not found":
                continue

            if len(clean_text) < 50:
                continue

            entry = {
                "filename": file_path.name,
                "country": country_name,
                "region": region_name,  # Här blir det "General" för visum-filerna
                "url": metadata.get("url", ""),
                "title": clean_title,
                "category": determine_category(metadata.get("url", "")),
                "text": clean_text,
            }
            processed_entries.append(entry)

        except Exception as e:
            print(f"       Fel vid fil {file_path.name}: {e}")

    # Spara resultatet om vi hittade några filer
    if processed_entries:
        # Om regionen är "General", döp filen till t.ex. "japan_general.jsonl"
        output_filename = f"{country_name}_{region_name.lower()}.jsonl"
        output_file = PROCESSED_DATA_DIR / output_filename

        with open(output_file, "w", encoding="utf-8") as f:
            for entry in processed_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        print(
            f"       Sparade {len(processed_entries)} artiklar till {output_filename}"
        )


if __name__ == "__main__":
    process_all_folders()
