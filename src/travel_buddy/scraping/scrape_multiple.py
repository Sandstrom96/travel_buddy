import time
from pathlib import Path
from firecrawl import FirecrawlApp
from travel_buddy.utils.settings import settings


PAGES_TO_SCRAPE = {
    "destinations": [
        {
            "name": "tokyo_overview",
            "url": "https://www.japan-guide.com/e/e2164.html",
            "destination": "tokyo",
            "category": "destination"
        },
        {
            "name": "kyoto_overview",
            "url": "https://www.japan-guide.com/e/e2401.html",
            "destination": "osaka",
            "category": "destination"
        },
    ],
    "attractions": [
        {
            "name": "sensoji_temple",
            "url": "https://www.japan-guide.com/e/e3900.html",
            "destination": "tokyo",
            "category": "attraction"
        },
        {
            "name": "fushimi_inari",
            "url": "https://www.japan-guide.com/e/e3900.html",
            "destination": "kyoto",
            "category": "attraction"
        },
        {
            "name": "kinkakuji",
            "url": "https://www.japan-guide.com/e/e3902.html",
            "destination": "kyoto",
            "category": "attraction"
        },
        {
            "name": "osaka_castle",
            "url": "https://www.japan-guide.com/e/e4000.html",
            "destination": "osaka",
            "category": "attraction"
        },
    ],
    "events": [
        {
            "name": "cherry_blossoms",
            "url": "https://www.japan-guide.com/e/e2011.html",
            "destination": None,
            "category": "event"
        },
        {
            "name": "gion_matsuri",
            "url":"https://www.japan-guide.com/e/e2063.html",
            "destination": "kyoto",
            "category": "event"
        },
    ],
    "practical": [
        {
            "name": "visa_entry_requirements",
            "url": "https://www.japan-guide.com/e/e2014.html",
            "destination": None, 
            "category": "practical"
        },
    ],
}


class TravelBuddyScraper:
    def __init__(self):
        self.app = FirecrawlApp(api_key=settings.firecrawl_api_key)
        self.output_dir = Path("data/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.delay_seconds = 2
        self.results = {
            "success": [],
            "failed": []
        }

    def scrape_page(self, page_config: dict) -> bool:
        """Scrapeing a single page and saving as a markdown"""
        name = page_config["name"]
        url = page_config["url"]

        try: 
            print(f"\n🔄 Scraping: {name}")
            print(f"  URL: {url}")

            response = self.app.scrape_url(url, params={'formats': ['markdown']})
            markdown_content = response.get('markdown', '')

            if not markdown_content:
                print(f"  ⚠️ No content returned")
                self.results["failed"].append({
                    "name": name,
                    "reason": "Empty response"
                })
                return False
            
            file_path = self.output_dir / f"{name}_raw.md"
            file_path.write_text(markdown_content, encoding='utf-8')
            
            file_size = len(markdown_content) / 1024 # Convert to KB
            print(f"  ✅ Saved: {file_path.name} ({file_size: .1f} KB)")

            self.results["success"].append({
                "name": name,
                "path": str(file_path),
                "size_kb": file_size,
                "category": page_config["category"],
                "destination": page_config["destination"]
            })

            return True
        
        except Exception as e:
            print (f"  ❌ Error: {str(e)}")
            self.results["failed"].append({
                "name": name,
                "reason": str(e)
            })
            return False
        
    def run(self):
        """Scrape all pages with rate limiting"""
        print("=" * 60)
        print("🚀 Travel Buddy FireCrawl Batch Scraper")
        print("=" * 60)

        
        all_pages = []
        for category, pages in PAGES_TO_SCRAPE.items():
            all_pages.extend(pages)

        total_pages = len(all_pages)
        print(f"\n📋 Scraping {total_pages} pages...")

        for i, page_config in enumerate(all_pages, 1):
            print(f"\n[{i}/{total_pages}]", end="")

            success = self.scrape_page(page_config)

            if i < total_pages:
                print(f"  ⏳ Waiting {self.delay_seconds}s before next request...")
                time.sleep(self.delay_seconds)

        self.print_summary()
    
    def print_summary(self):
        """Printing scrpaing results summary."""
        print("\n" + "=" * 60)
        print("📊 Scraping Summary")
        print("=" * 60)

        success_count = len(self.results["success"])
        failed_count = len(self.results["failed"])

        print(f"\n ✅ Successful: {success_count}")
        for result in self.results["success"]:
            print(f"  • {result['name']} ({result['category']}) - {result['size_kb']:.1f} KB")

        if failed_count > 0:
            print(f"\n❌ Failed: {failed_count}")
            for result in self.results["failed"]:
                print(f"  • {result['name']} - {result['reason']}")
            
        print(f"\n📁 All files saved to: {self.output_dir}/")
        print("\n" + "=" * 60)
        print("✨ Next step: Run ingestion pipeline")
        print(" cd src && uv run python -m travel_buddy.ingestion.run_ingestion_batch")
        print("=" * 60)


def main():
    scraper = TravelBuddyScraper()
    scraper.run()

if __name__ == "__main__":
    main()