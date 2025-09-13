#!/usr/bin/env python3
"""
Web Scraping Utilities
A collection of web scraping tools with rate limiting, data extraction, and export capabilities.
"""

import requests
import time
import json
import csv
import re
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
from urllib.parse import urljoin, urlparse, parse_qs
from dataclasses import dataclass, asdict
import logging

try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_AVAILABLE = True
except ImportError:
    BEAUTIFULSOUP_AVAILABLE = False
    print("⚠️ BeautifulSoup not available. Install with: pip install beautifulsoup4")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

@dataclass
class ScrapingResult:
    """Data class for scraping results."""
    url: str
    title: str = ""
    content: str = ""
    links: List[str] = None
    images: List[str] = None
    metadata: Dict[str, Any] = None
    timestamp: str = ""
    status_code: int = 0
    
    def __post_init__(self):
        if self.links is None:
            self.links = []
        if self.images is None:
            self.images = []
        if self.metadata is None:
            self.metadata = {}
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

class WebScraper:
    """Advanced web scraping utility with rate limiting and export capabilities."""
    
    def __init__(self, delay: float = 1.0, user_agent: str = None):
        self.delay = delay
        self.session = requests.Session()
        self.results: List[ScrapingResult] = []
        
        # Set user agent
        if user_agent is None:
            user_agent = "Mozilla/5.0 (compatible; WebScraper/1.0)"
        
        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
    
    def scrape_url(self, url: str, extract_links: bool = True, extract_images: bool = True) -> Optional[ScrapingResult]:
        """Scrape a single URL and extract content."""
        try:
            self.logger.info(f"Scraping: {url}")
            
            # Rate limiting
            time.sleep(self.delay)
            
            # Make request
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            if not BEAUTIFULSOUP_AVAILABLE:
                # Basic text extraction without BeautifulSoup
                result = ScrapingResult(
                    url=url,
                    content=response.text,
                    status_code=response.status_code
                )
                self.results.append(result)
                return result
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_tag = soup.find('title')
            title = title_tag.get_text().strip() if title_tag else ""
            
            # Extract main content (remove script and style tags)
            for script in soup(["script", "style"]):
                script.decompose()
            
            content = soup.get_text()
            # Clean up whitespace
            content = re.sub(r'\s+', ' ', content).strip()
            
            # Extract links
            links = []
            if extract_links:
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urljoin(url, href)
                    links.append(absolute_url)
            
            # Extract images
            images = []
            if extract_images:
                for img in soup.find_all('img', src=True):
                    src = img['src']
                    absolute_url = urljoin(url, src)
                    images.append(absolute_url)
            
            # Extract metadata
            metadata = {}
            
            # Meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    metadata[name] = content
            
            # Headers
            headers = {}
            for i in range(1, 7):
                header_tags = soup.find_all(f'h{i}')
                if header_tags:
                    headers[f'h{i}'] = [tag.get_text().strip() for tag in header_tags]
            
            if headers:
                metadata['headers'] = headers
            
            result = ScrapingResult(
                url=url,
                title=title,
                content=content,
                links=links,
                images=images,
                metadata=metadata,
                status_code=response.status_code
            )
            
            self.results.append(result)
            self.logger.info(f"✅ Successfully scraped: {url}")
            return result
            
        except requests.RequestException as e:
            self.logger.error(f"❌ Request failed for {url}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Scraping failed for {url}: {e}")
            return None
    
    def scrape_urls(self, urls: List[str], **kwargs) -> List[ScrapingResult]:
        """Scrape multiple URLs."""
        results = []
        total = len(urls)
        
        for i, url in enumerate(urls, 1):
            self.logger.info(f"Progress: {i}/{total}")
            result = self.scrape_url(url, **kwargs)
            if result:
                results.append(result)
        
        return results
    
    def scrape_sitemap(self, sitemap_url: str, limit: int = None) -> List[ScrapingResult]:
        """Scrape URLs from a sitemap."""
        try:
            self.logger.info(f"Fetching sitemap: {sitemap_url}")
            response = self.session.get(sitemap_url)
            response.raise_for_status()
            
            if not BEAUTIFULSOUP_AVAILABLE:
                self.logger.error("BeautifulSoup required for sitemap parsing")
                return []
            
            soup = BeautifulSoup(response.content, 'xml')
            urls = []
            
            # Extract URLs from sitemap
            for loc in soup.find_all('loc'):
                urls.append(loc.get_text())
            
            if limit:
                urls = urls[:limit]
            
            self.logger.info(f"Found {len(urls)} URLs in sitemap")
            return self.scrape_urls(urls)
            
        except Exception as e:
            self.logger.error(f"❌ Sitemap scraping failed: {e}")
            return []
    
    def search_content(self, pattern: str, use_regex: bool = False) -> List[ScrapingResult]:
        """Search scraped content for specific patterns."""
        matching_results = []
        
        for result in self.results:
            content = result.content.lower() if not use_regex else result.content
            search_text = pattern.lower() if not use_regex else pattern
            
            if use_regex:
                if re.search(search_text, content, re.IGNORECASE):
                    matching_results.append(result)
            else:
                if search_text in content:
                    matching_results.append(result)
        
        self.logger.info(f"Found {len(matching_results)} results matching pattern: {pattern}")
        return matching_results
    
    def export_to_json(self, filename: str = None) -> str:
        """Export results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraping_results_{timestamp}.json"
        
        data = [asdict(result) for result in self.results]
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"✅ Results exported to: {filename}")
        return filename
    
    def export_to_csv(self, filename: str = None, include_metadata: bool = False) -> str:
        """Export results to CSV file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scraping_results_{timestamp}.csv"
        
        fieldnames = ['url', 'title', 'content', 'status_code', 'timestamp']
        if include_metadata:
            fieldnames.extend(['links_count', 'images_count'])
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(fieldnames)
            
            # Write data
            for result in self.results:
                row = [
                    result.url,
                    result.title,
                    result.content[:1000] + '...' if len(result.content) > 1000 else result.content,
                    result.status_code,
                    result.timestamp
                ]
                
                if include_metadata:
                    row.extend([
                        len(result.links),
                        len(result.images)
                    ])
                
                writer.writerow(row)
        
        self.logger.info(f"✅ Results exported to: {filename}")
        return filename
    
    def export_links(self, filename: str = None) -> str:
        """Export all found links to a text file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"extracted_links_{timestamp}.txt"
        
        all_links = set()
        for result in self.results:
            all_links.update(result.links)
        
        with open(filename, 'w', encoding='utf-8') as f:
            for link in sorted(all_links):
                f.write(f"{link}\n")
        
        self.logger.info(f"✅ {len(all_links)} unique links exported to: {filename}")
        return filename
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get scraping statistics."""
        if not self.results:
            return {}
        
        total_results = len(self.results)
        successful_results = [r for r in self.results if r.status_code == 200]
        total_links = sum(len(r.links) for r in self.results)
        total_images = sum(len(r.images) for r in self.results)
        
        avg_content_length = sum(len(r.content) for r in self.results) / total_results
        
        stats = {
            'total_pages_scraped': total_results,
            'successful_requests': len(successful_results),
            'success_rate': len(successful_results) / total_results * 100,
            'total_links_found': total_links,
            'total_images_found': total_images,
            'average_content_length': round(avg_content_length, 2),
            'unique_domains': len(set(urlparse(r.url).netloc for r in self.results))
        }
        
        return stats

class NewsArticleScraper(WebScraper):
    """Specialized scraper for news articles."""
    
    def extract_article_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract article-specific data."""
        result = self.scrape_url(url)
        if not result or not BEAUTIFULSOUP_AVAILABLE:
            return None
        
        try:
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract article-specific elements
            article_data = {
                'url': url,
                'title': result.title,
                'publish_date': None,
                'author': None,
                'content': result.content,
                'summary': None
            }
            
            # Try to find publish date
            date_selectors = [
                'time[datetime]',
                '[datetime]',
                '.publish-date',
                '.date',
                '.article-date'
            ]
            
            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    article_data['publish_date'] = date_elem.get('datetime') or date_elem.get_text()
                    break
            
            # Try to find author
            author_selectors = [
                '.author',
                '.byline',
                '[rel="author"]',
                '.article-author'
            ]
            
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    article_data['author'] = author_elem.get_text().strip()
                    break
            
            # Try to find summary/description
            summary_selectors = [
                'meta[name="description"]',
                '.summary',
                '.excerpt',
                '.article-summary'
            ]
            
            for selector in summary_selectors:
                summary_elem = soup.select_one(selector)
                if summary_elem:
                    article_data['summary'] = summary_elem.get('content') or summary_elem.get_text()
                    break
            
            return article_data
            
        except Exception as e:
            self.logger.error(f"❌ Article extraction failed for {url}: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description="Web Scraping Utilities")
    parser.add_argument('--urls', nargs='+', help='URLs to scrape')
    parser.add_argument('--file', help='File containing URLs (one per line)')
    parser.add_argument('--sitemap', help='Sitemap URL to scrape')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between requests (seconds)')
    parser.add_argument('--output', help='Output filename')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Output format')
    parser.add_argument('--search', help='Search pattern in scraped content')
    parser.add_argument('--regex', action='store_true', help='Use regex for search')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    parser.add_argument('--export-links', action='store_true', help='Export found links to file')
    parser.add_argument('--limit', type=int, help='Limit number of URLs to scrape')
    
    args = parser.parse_args()
    
    if not any([args.urls, args.file, args.sitemap]):
        parser.print_help()
        return
    
    # Initialize scraper
    scraper = WebScraper(delay=args.delay)
    
    # Collect URLs to scrape
    urls_to_scrape = []
    
    if args.urls:
        urls_to_scrape.extend(args.urls)
    
    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip()]
                urls_to_scrape.extend(file_urls)
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
            return
    
    if args.sitemap:
        print(f"🗺️ Scraping sitemap: {args.sitemap}")
        scraper.scrape_sitemap(args.sitemap, limit=args.limit)
    
    # Scrape regular URLs
    if urls_to_scrape:
        if args.limit:
            urls_to_scrape = urls_to_scrape[:args.limit]
        
        print(f"🚀 Starting to scrape {len(urls_to_scrape)} URLs...")
        scraper.scrape_urls(urls_to_scrape)
    
    # Search content if pattern provided
    if args.search:
        print(f"🔍 Searching for pattern: {args.search}")
        matching_results = scraper.search_content(args.search, args.regex)
        print(f"Found {len(matching_results)} matching results")
    
    # Export results
    if scraper.results:
        if args.format == 'json':
            output_file = scraper.export_to_json(args.output)
        else:
            output_file = scraper.export_to_csv(args.output, include_metadata=True)
        
        print(f"📄 Results exported to: {output_file}")
    
    # Export links if requested
    if args.export_links and scraper.results:
        links_file = scraper.export_links()
        print(f"🔗 Links exported to: {links_file}")
    
    # Show statistics
    if args.stats and scraper.results:
        stats = scraper.get_statistics()
        print("\n📊 SCRAPING STATISTICS")
        print("=" * 30)
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    main()