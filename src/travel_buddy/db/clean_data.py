import re
import json
from travel_buddy.utils.settings import settings


## Used AI to help create this
def clean_markdown_content(raw_text):
    """
    Removes navigation, menus and boilerplate from markdown.
    """
    lines = raw_text.split("\n")
    cleaned_lines = []

    # Flag for knowing if we are in a "noise block"
    in_noise_block = False

    # Keywords that indicate start of large navigation menus
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
        # specific keywords for Greece data
        "###### CONTENTS",
        "_The artwork on the cover",
        "Follow us on",
        "Newsletter",
    ]

    # Regex to find headers that are actually content
    header_pattern = re.compile(r"^#+\s+")

    for line in lines:
        stripped_line = line.strip()

        # Check if we enter a known noise block
        if any(stripped_line.startswith(marker) for marker in noise_start_markers):
            in_noise_block = True
            continue

        # If we see a "real" header (the content), we can sometimes reset the noise
        # (This is a heuristic: If we see "# Hiroshima" we are probably in content)
        if in_noise_block and header_pattern.match(stripped_line):
            # But we don't want to re-enable if it's footer links
            if (
                "Related Links" not in stripped_line
                and "Explore Nearby" not in stripped_line
            ):
                in_noise_block = False

        # Specific cleaning of the huge lists with links (Destinations, Things to Do etc)
        # These files seem to have huge lists of links that are not body text.
        # We remove lines that are ONLY a markdown link or image.
        is_only_link = re.match(r"^\s*-\s*\[.*?\]\(.*?\)\s*$", stripped_line)
        is_only_image = re.match(r"^\s*\[?!\[.*?\]\(.*?\).*", stripped_line)

        if in_noise_block:
            continue

        # Skip lines that are only navigation links or images without context
        if is_only_link or is_only_image:
            continue

        # Remove template variables (e.g. ${v.title})
        if "${" in stripped_line:
            continue

        # Keep the line if it has content
        if stripped_line:
            cleaned_lines.append(stripped_line)

    # Join text and clean up link syntax in body text
    full_text = "\n".join(cleaned_lines)

    # Remove images but keep any alt-text if it's sensible, otherwise remove
    # Regex: ![alt text](url) -> alt text
    full_text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", full_text)

    # Remove regular links but keep the text: [text](url) -> text
    full_text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", full_text)

    # Remove excessive new lines (more than 2)
    full_text = re.sub(r"\n{3,}", "\n\n", full_text)

    return full_text.strip()


def extract_frontmatter(text):
    """
    Extracts URL and Title from YAML frontmatter if it exists.
    """
    metadata = {}
    # Made the regex more permissive for whitespace at start
    match = re.search(r"^\s*---\s*\n(.*?)\n\s*---", text, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        content_after = text[match.end() :].strip()

        for line in yaml_content.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                metadata[key.strip().lower()] = value.strip().strip('"').strip("'")
        return metadata, content_after

    return {}, text


def determine_category(url_or_filename):
    """Guesses category based on URL or filename."""
    s = url_or_filename.lower()
    if "destinations" in s:
        return "destination"
    elif "plan" in s or "guide" in s:
        return "practical_guide"
    elif "spot" in s:
        return "spot"  # Specific attractions
    elif "news" in s:
        return "news"
    else:
        return "general"


def process_all_folders():
    countries = [f for f in settings.RAW_DATA_DIR.iterdir() if f.is_dir()]

    if not countries:
        print(f"Warning: No countries found in {settings.RAW_DATA_DIR}")
        return

    total_files_processed = 0

    for country_path in countries:
        country_name = country_path.name
        print(f"--> Entering country: {country_name}")

        # --- STEP 1: Handle files directly in country folder (e.g. Visa, General info) ---
        # These get the region name "General"
        general_files = list(country_path.glob("*.md"))

        if general_files:
            print(f"    --> Processing {len(general_files)} general files (General)...")
            process_file_list(general_files, country_name, "General")
            total_files_processed += len(general_files)

        # --- STEP 2: Handle regions (subfolders) ---
        regions = [r for r in country_path.iterdir() if r.is_dir()]

        for region_path in regions:
            region_name = region_path.name
            print(f"    --> Processing region: {region_name}...")

            files = list(region_path.rglob("*.md"))
            process_file_list(files, country_name, region_name)
            total_files_processed += len(files)

    print(f"\nDone! Total {total_files_processed} files processed.")


# --- Helper function to avoid repeating code ---
def process_file_list(files, country_name, region_name):
    processed_entries = []

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                raw_content = f.read()

            metadata, body_content = extract_frontmatter(raw_content)

            # --- FIX 1: Handle missing URL ---
            url = metadata.get("url")
            if not url:
                # If URL is missing in file, build one from filename
                # e.g. www.japan.travel_en_spot_895.md -> https://www.japan.travel/en/spot/895/
                url_part = file_path.stem.replace("_", "/")
                url = f"https://{url_part}"

            # --- FIX 2: Handle title ---
            raw_title = metadata.get("title")
            if not raw_title:
                # If title is missing, use filename (without .md) as fallback
                clean_title = file_path.stem.split("_")[-1].capitalize()
            else:
                clean_title = raw_title.split("|")[0].strip()

            clean_text = clean_markdown_content(body_content)

            if clean_title.lower() == "page not found" or len(clean_text) < 50:
                continue

            entry = {
                "filename": file_path.name,
                "country": country_name,
                "region": region_name,  # Here it becomes "General" for visa files
                "url": url,
                "title": clean_title,
                "category": determine_category(url),
                "text": clean_text,
            }
            processed_entries.append(entry)

        except Exception as e:
            print(f"       Error in file {file_path.name}: {e}")

    # Save result if we found any files
    if processed_entries:
        # If region is "General", name the file e.g. "japan_general.jsonl"
        output_filename = f"{country_name}_{region_name.lower()}.jsonl"
        output_file = settings.PROCESSED_DATA_DIR / output_filename

        with open(output_file, "w", encoding="utf-8") as f:
            for entry in processed_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        print(
            f"       Saved {len(processed_entries)} articles to {output_filename}"
        )


if __name__ == "__main__":
    process_all_folders()
