#!/usr/bin/env python3
"""
🚀 CYBERSECURITY NEWS AGGREGATOR - MODERN UI
Beautiful desktop interface for news scraping with integrated scraper
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import asyncio
import threading
from datetime import datetime
import json
import csv
from pathlib import Path
import webbrowser
import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import re
import random
import aiohttp
from dataclasses import dataclass
from typing import List, Dict, Optional

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ScrapingResult:
    """Data class for scraping results"""
    source: str
    articles: List[Dict]
    status: str
    error: Optional[str] = None

class AsyncWebScraper:
    """Async web scraper with advanced features"""
    
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        ]
        self.retry_config = {'max_retries': 3, 'base_delay': 1, 'max_delay': 10, 'backoff_factor': 2}
    
    async def setup_session(self):
        headers = {'User-Agent': random.choice(self.user_agents)}
        timeout = aiohttp.ClientTimeout(total=30)
        session = aiohttp.ClientSession(headers=headers, timeout=timeout)
        return session
    
    async def scrape_with_retry(self, url: str, session):
        for attempt in range(self.retry_config['max_retries']):
            try:
                delay = min(
                    self.retry_config['base_delay'] * (self.retry_config['backoff_factor'] ** attempt),
                    self.retry_config['max_delay']
                )
                
                if attempt > 0:
                    await asyncio.sleep(delay)
                
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} error: {e}")
        
        return None
    
    async def scrape_dark_reading(self, limit: int = 10):
        """Scrape Dark Reading using feed"""
        try:
            # Use RSS feed instead of HTML scraping for reliability
            feed_url = 'https://www.darkreading.com/rss.xml'
            feed = await asyncio.to_thread(feedparser.parse, feed_url)
            
            articles = []
            for entry in feed.entries[:limit]:
                try:
                    article = {
                        'title': entry.get('title', 'N/A')[:100],
                        'url': entry.get('link', 'N/A'),
                        'summary': entry.get('summary', '')[:250],
                        'published': entry.get('published', datetime.now().strftime('%Y-%m-%d %H:%M')),
                        'source': 'Dark Reading'
                    }
                    articles.append(article)
                except Exception as e:
                    logger.debug(f"Error parsing Dark Reading entry: {e}")
                    continue
            
            return ScrapingResult('dark_reading', articles, 'success')
        except Exception as e:
            logger.error(f"Error scraping Dark Reading: {e}")
            return ScrapingResult('dark_reading', [], 'error', str(e))
    
    async def scrape_bleeping_computer(self, limit: int = 10):
        """Scrape Bleeping Computer using feed"""
        try:
            # Use RSS feed for reliability
            feed_url = 'https://www.bleepingcomputer.com/feed/'
            feed = await asyncio.to_thread(feedparser.parse, feed_url)
            
            articles = []
            for entry in feed.entries[:limit]:
                try:
                    article = {
                        'title': entry.get('title', 'N/A')[:100],
                        'url': entry.get('link', 'N/A'),
                        'summary': entry.get('summary', '')[:250],
                        'published': entry.get('published', datetime.now().strftime('%Y-%m-%d %H:%M')),
                        'source': 'Bleeping Computer'
                    }
                    articles.append(article)
                except Exception as e:
                    logger.debug(f"Error parsing BC entry: {e}")
                    continue
            
            return ScrapingResult('bleeping_computer', articles, 'success')
        except Exception as e:
            logger.error(f"Error scraping Bleeping Computer: {e}")
            return ScrapingResult('bleeping_computer', [], 'error', str(e))
    
    async def scrape_krebs_security(self, limit: int = 10):
        try:
            session = await self.setup_session()
            html = await self.scrape_with_retry("https://krebsonsecurity.com", session)
            
            if not html:
                await session.close()
                return ScrapingResult('krebs_security', [], 'error', 'Failed to fetch')
            
            soup = BeautifulSoup(html, 'html.parser')
            articles = []
            story_elements = soup.find_all('article')[:limit]
            
            for element in story_elements:
                try:
                    title_elem = element.find('h2', class_='entry-title')
                    if not title_elem:
                        title_elem = element.find(['h2', 'h3'])
                    
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    link_elem = title_elem.find('a')
                    
                    if link_elem and link_elem.get('href'):
                        url = link_elem['href']
                    else:
                        continue
                    
                    summary_elem = element.find('div', class_='entry-summary')
                    if not summary_elem:
                        summary_elem = element.find('p')
                    
                    summary = summary_elem.get_text(strip=True) if summary_elem else ''
                    
                    articles.append({
                        'title': title,
                        'url': url,
                        'summary': summary[:300],
                        'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                        'source': 'Krebs on Security'
                    })
                except:
                    continue
            
            await session.close()
            return ScrapingResult('krebs_security', articles, 'success')
        except Exception as e:
            logger.error(f"Error scraping Krebs on Security: {e}")
            return ScrapingResult('krebs_security', [], 'error', str(e))

class RSSFeedAggregator:
    """RSS feed aggregator"""
    
    def __init__(self):
        self.rss_feeds = {
            'gb_hackers': 'https://gbhackers.com/feed/',
            'the_hacker_news': 'https://feeds.feedburner.com/TheHackersNews',
            'security_week': 'https://www.securityweek.com/feed/',
            'dark_reading': 'https://www.darkreading.com/rss.xml',
            'bleeping_computer': 'https://www.bleepingcomputer.com/feed/',
            'krebs_security': 'https://krebsonsecurity.com/feed/'
        }
    
    def fetch_rss_feed(self, source: str, limit: int = 20) -> ScrapingResult:
        try:
            feed_url = self.rss_feeds.get(source)
            if not feed_url:
                return ScrapingResult(source, [], 'error', 'No RSS feed configured')
            
            feed = feedparser.parse(feed_url)
            articles = []
            
            for entry in feed.entries[:limit]:
                try:
                    # Get the URL
                    url = entry.get('link', 'N/A')
                    
                    article = {
                        'title': entry.get('title', 'N/A')[:100],
                        'url': str(url),
                        'summary': entry.get('summary', '')[:250],
                        'published': entry.get('published', datetime.now().strftime('%Y-%m-%d %H:%M')),
                        'source': source.replace('_', ' ').title()
                    }
                    
                    if hasattr(entry, 'author'):
                        article['author'] = entry.author
                    
                    articles.append(article)
                except Exception as e:
                    logger.debug(f"Error parsing {source} entry: {e}")
                    continue
            
            return ScrapingResult(source, articles, 'success')
        except Exception as e:
            logger.error(f"Error fetching RSS for {source}: {e}")
            return ScrapingResult(source, [], 'error', str(e))

class CybersecurityAggregator:
    """Main aggregator class"""
    
    def __init__(self):
        self.async_scraper = AsyncWebScraper()
        self.rss_aggregator = RSSFeedAggregator()
    
    async def scrape_all_async(self, limit: int = 20, callback=None):
        """Scrape all sources asynchronously"""
        logger.info("Starting async scraping...")
        
        async_tasks = [
            self.async_scraper.scrape_dark_reading(limit),
            self.async_scraper.scrape_bleeping_computer(limit),
            self.async_scraper.scrape_krebs_security(limit)
        ]
        
        rss_tasks = [
            asyncio.to_thread(self.rss_aggregator.fetch_rss_feed, 'gb_hackers', limit),
            asyncio.to_thread(self.rss_aggregator.fetch_rss_feed, 'the_hacker_news', limit),
            asyncio.to_thread(self.rss_aggregator.fetch_rss_feed, 'security_week', limit)
        ]
        
        all_tasks = async_tasks + rss_tasks
        results_list = await asyncio.gather(*all_tasks, return_exceptions=True)
        
        results = {}
        for result in results_list:
            if isinstance(result, ScrapingResult):
                source_key = result.source.lower().replace(' ', '_')
                results[source_key] = result
                if callback:
                    callback(source_key, result)
        
        return results
    
    def save_results(self, results: Dict[str, ScrapingResult], format_type: str = 'both'):
        """Save results to files"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        all_articles = []
        for result in results.values():
            if result.status == 'success':
                all_articles.extend(result.articles)
        
        if not all_articles:
            logger.warning("No articles to save")
            return None, None
        
        csv_file = None
        json_file = None
        
        if format_type in ['csv', 'both']:
            csv_filename = f"cybersecurity_news_{timestamp}.csv"
            fieldnames = set()
            for article in all_articles:
                fieldnames.update(article.keys())
            fieldnames = sorted(list(fieldnames))
            
            with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_articles)
            
            logger.info(f"✅ Saved {len(all_articles)} articles to {csv_filename}")
            csv_file = csv_filename
        
        if format_type in ['json', 'both']:
            json_filename = f"cybersecurity_news_{timestamp}.json"
            with open(json_filename, 'w', encoding='utf-8') as jsonfile:
                json.dump({
                    'metadata': {
                        'scraped_at': datetime.now().isoformat(),
                        'total_articles': len(all_articles)
                    },
                    'articles': all_articles
                }, jsonfile, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Saved results to {json_filename}")
            json_file = json_filename
        
        return csv_file, json_file

class ModernNewsAggregatorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 Cybersecurity News Aggregator")
        self.root.geometry("1400x900")
        self.root.configure(bg="#0f172a")
        
        self.setup_styles()
        
        self.is_running = False
        self.results = {}
        self.all_articles = []
        self.aggregator = CybersecurityAggregator()
        
        self.build_ui()
    
    def setup_styles(self):
        """Configure modern color scheme"""
        style = ttk.Style()
        style.theme_use('clam')
        
        bg_primary = "#0f172a"
        bg_secondary = "#1e293b"
        bg_tertiary = "#334155"
        accent = "#3b82f6"
        accent_light = "#60a5fa"
        text_primary = "#f1f5f9"
        text_secondary = "#cbd5e1"
        success = "#10b981"
        warning = "#f59e0b"
        error = "#ef4444"
        
        style.configure('Dark.TFrame', background=bg_primary)
        style.configure('Secondary.TFrame', background=bg_secondary)
        style.configure('Title.TLabel', background=bg_primary, foreground=text_primary, 
                       font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', background=bg_primary, foreground=text_secondary,
                       font=('Segoe UI', 10))
        style.configure('Info.TLabel', background=bg_secondary, foreground=text_primary,
                       font=('Segoe UI', 10))
        style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'))
        style.map('Accent.TButton',
                 background=[('pressed', accent_light), ('active', accent_light)])
        style.configure('TNotebook', background=bg_primary, borderwidth=0)
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Segoe UI', 10))
        
        self.colors = {
            'bg_primary': bg_primary,
            'bg_secondary': bg_secondary,
            'bg_tertiary': bg_tertiary,
            'accent': accent,
            'accent_light': accent_light,
            'text_primary': text_primary,
            'text_secondary': text_secondary,
            'success': success,
            'warning': warning,
            'error': error
        }
    
    def build_ui(self):
        """Build the complete UI"""
        self.create_header()
        self.create_notebook()
        self.create_statusbar()
    
    def create_header(self):
        """Create header section"""
        header = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        title = tk.Label(title_frame, text="🚀 Cybersecurity News Aggregator",
                        font=('Segoe UI', 18, 'bold'), 
                        fg=self.colors['accent_light'],
                        bg=self.colors['bg_secondary'])
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Real-time security news from multiple sources",
                          font=('Segoe UI', 9),
                          fg=self.colors['text_secondary'],
                          bg=self.colors['bg_secondary'])
        subtitle.pack()
        
        btn_frame = tk.Frame(header, bg=self.colors['bg_secondary'])
        btn_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.start_btn = tk.Button(btn_frame, text="▶ START SCRAPING",
                                   command=self.start_scraping,
                                   bg=self.colors['success'], fg="white",
                                   font=('Segoe UI', 10, 'bold'),
                                   padx=15, pady=8, relief=tk.FLAT,
                                   cursor="hand2")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(btn_frame, text="⏹ STOP",
                                  command=self.stop_scraping,
                                  bg=self.colors['error'], fg="white",
                                  font=('Segoe UI', 10, 'bold'),
                                  padx=15, pady=8, relief=tk.FLAT,
                                  state=tk.DISABLED,
                                  cursor="hand2")
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = tk.Button(btn_frame, text="💾 EXPORT",
                                    command=self.export_results,
                                    bg=self.colors['accent'], fg="white",
                                    font=('Segoe UI', 10, 'bold'),
                                    padx=15, pady=8, relief=tk.FLAT,
                                    state=tk.DISABLED,
                                    cursor="hand2")
        self.export_btn.pack(side=tk.LEFT, padx=5)
    
    def create_notebook(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.dashboard_tab = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(self.dashboard_tab, text="📊 Dashboard")
        self.create_dashboard()
        
        self.log_tab = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(self.log_tab, text="📝 Live Log")
        self.create_log_tab()
        
        self.articles_tab = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(self.articles_tab, text="📰 Articles")
        self.create_articles_tab()
        
        self.settings_tab = tk.Frame(self.notebook, bg=self.colors['bg_primary'])
        self.notebook.add(self.settings_tab, text="⚙️ Settings")
        self.create_settings_tab()
    
    def create_dashboard(self):
        """Create dashboard with statistics"""
        stats_frame = tk.Frame(self.dashboard_tab, bg=self.colors['bg_primary'])
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        title = tk.Label(stats_frame, text="Scraping Statistics",
                        font=('Segoe UI', 14, 'bold'),
                        fg=self.colors['accent'],
                        bg=self.colors['bg_primary'])
        title.pack(anchor=tk.W, pady=(0, 15))
        
        container = tk.Frame(stats_frame, bg=self.colors['bg_primary'])
        container.pack(fill=tk.BOTH, expand=True)
        
        self.stat_cards = {}
        sources = ['gb_hackers', 'the_hacker_news', 'security_week', 
                   'dark_reading', 'bleeping_computer', 'krebs_security']
        
        for idx, source in enumerate(sources):
            row, col = divmod(idx, 3)
            card = self.create_stat_card(container, source, row, col)
            self.stat_cards[source] = card
        
        total_frame = tk.Frame(stats_frame, bg=self.colors['bg_secondary'],
                              relief=tk.FLAT, padx=20, pady=15)
        total_frame.pack(fill=tk.X, pady=(15, 0))
        
        tk.Label(total_frame, text="Total Articles Collected:",
                fg=self.colors['text_secondary'], bg=self.colors['bg_secondary'],
                font=('Segoe UI', 10)).pack(side=tk.LEFT)
        
        self.total_label = tk.Label(total_frame, text="0",
                                   fg=self.colors['accent_light'],
                                   bg=self.colors['bg_secondary'],
                                   font=('Segoe UI', 14, 'bold'))
        self.total_label.pack(side=tk.RIGHT)
    
    def create_stat_card(self, parent, source, row, col):
        """Create individual stat card"""
        card = tk.Frame(parent, bg=self.colors['bg_secondary'],
                       relief=tk.FLAT, padx=15, pady=15)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        source_label = tk.Label(card, text=source.replace('_', ' ').title(),
                               fg=self.colors['accent'], bg=self.colors['bg_secondary'],
                               font=('Segoe UI', 11, 'bold'))
        source_label.pack(anchor=tk.W)
        
        count_label = tk.Label(card, text="0 articles",
                              fg=self.colors['text_secondary'],
                              bg=self.colors['bg_secondary'],
                              font=('Segoe UI', 10))
        count_label.pack(anchor=tk.W, pady=(5, 0))
        
        status_label = tk.Label(card, text="⏳ Pending",
                               fg=self.colors['text_secondary'],
                               bg=self.colors['bg_secondary'],
                               font=('Segoe UI', 9))
        status_label.pack(anchor=tk.W, pady=(3, 0))
        
        return {'count': count_label, 'status': status_label}
    
    def create_log_tab(self):
        """Create live log display"""
        header = tk.Label(self.log_tab, text="Live Scraping Log",
                         font=('Segoe UI', 12, 'bold'),
                         fg=self.colors['accent'],
                         bg=self.colors['bg_primary'])
        header.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        self.log_text = scrolledtext.ScrolledText(
            self.log_tab,
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary'],
            font=('Courier New', 9),
            relief=tk.FLAT,
            padx=10, pady=10,
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.log_text.tag_config('info', foreground=self.colors['accent_light'])
        self.log_text.tag_config('success', foreground=self.colors['success'])
        self.log_text.tag_config('error', foreground=self.colors['error'])
        self.log_text.tag_config('warning', foreground=self.colors['warning'])
    
    def create_articles_tab(self):
        """Create articles display"""
        header = tk.Label(self.articles_tab, text="Latest Articles",
                         font=('Segoe UI', 12, 'bold'),
                         fg=self.colors['accent'],
                         bg=self.colors['bg_primary'])
        header.pack(anchor=tk.W, padx=15, pady=(15, 10))
        
        # Create frame for treeview with scrollbars
        tree_frame = tk.Frame(self.articles_tab, bg=self.colors['bg_primary'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        columns = ('source', 'title', 'url')
        self.articles_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            height=20,
            selectmode='browse'
        )
        
        self.articles_tree.column('#0', width=0, stretch=tk.NO)
        self.articles_tree.column('source', anchor=tk.W, width=120)
        self.articles_tree.column('title', anchor=tk.W, width=500)
        self.articles_tree.column('url', anchor=tk.W, width=400)
        
        self.articles_tree.heading('source', text='Source', anchor=tk.W)
        self.articles_tree.heading('title', text='Title', anchor=tk.W)
        self.articles_tree.heading('url', text='URL', anchor=tk.W)
        
        self.articles_tree.bind('<Double-1>', self.open_url)
        
        # Vertical scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL,
                           command=self.articles_tree.yview)
        # Horizontal scrollbar
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL,
                           command=self.articles_tree.xview)
        
        self.articles_tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        
        # Grid layout for scrollbars
        self.articles_tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def create_settings_tab(self):
        """Create settings panel"""
        options_frame = tk.LabelFrame(self.settings_tab, text="Scraping Options",
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['accent'],
                                     font=('Segoe UI', 10, 'bold'),
                                     padx=15, pady=15)
        options_frame.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(options_frame, text="Articles per source:",
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.limit_var = tk.IntVar(value=10)
        limit_scale = tk.Scale(options_frame, from_=5, to=30, orient=tk.HORIZONTAL,
                              bg=self.colors['bg_tertiary'],
                              fg=self.colors['accent'],
                              variable=self.limit_var,
                              highlightthickness=0,
                              troughcolor=self.colors['bg_secondary'])
        limit_scale.pack(fill=tk.X, pady=(5, 15))
        
        # Display current limit value
        limit_display = tk.Label(options_frame, text="Default: 10 articles per domain (dapat diubah)",
                                fg=self.colors['text_secondary'],
                                bg=self.colors['bg_secondary'],
                                font=('Segoe UI', 8))
        limit_display.pack(anchor=tk.W)
        
        tk.Label(options_frame, text="Scraping mode:",
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor=tk.W)
        
        self.mode_var = tk.StringVar(value='async')
        modes = [('Async (Full Scraping)', 'async'), ('RSS Only (Faster)', 'rss')]
        for text, mode in modes:
            rb = tk.Radiobutton(options_frame, text=text, variable=self.mode_var,
                              value=mode, bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'],
                              selectcolor=self.colors['accent'],
                              activebackground=self.colors['bg_tertiary'],
                              activeforeground=self.colors['accent'])
            rb.pack(anchor=tk.W, pady=3)
        
        tk.Label(options_frame, text="Export format:",
                fg=self.colors['text_primary'],
                bg=self.colors['bg_secondary']).pack(anchor=tk.W, pady=(15, 5))
        
        format_frame = tk.Frame(options_frame, bg=self.colors['bg_secondary'])
        format_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.export_csv = tk.BooleanVar(value=True)
        self.export_json = tk.BooleanVar(value=True)
        
        tk.Checkbutton(format_frame, text="CSV", variable=self.export_csv,
                      bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['accent'],
                      activebackground=self.colors['bg_tertiary']).pack(side=tk.LEFT, padx=5)
        
        tk.Checkbutton(format_frame, text="JSON", variable=self.export_json,
                      bg=self.colors['bg_secondary'], fg=self.colors['text_primary'],
                      selectcolor=self.colors['accent'],
                      activebackground=self.colors['bg_tertiary']).pack(side=tk.LEFT, padx=5)
    
    def create_statusbar(self):
        """Create status bar"""
        statusbar = tk.Frame(self.root, bg=self.colors['bg_secondary'], height=40)
        statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        statusbar.pack_propagate(False)
        
        self.status_label = tk.Label(statusbar, text="Ready",
                                    fg=self.colors['text_secondary'],
                                    bg=self.colors['bg_secondary'],
                                    font=('Segoe UI', 9))
        self.status_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.time_label = tk.Label(statusbar, text="",
                                  fg=self.colors['text_secondary'],
                                  bg=self.colors['bg_secondary'],
                                  font=('Segoe UI', 9))
        self.time_label.pack(side=tk.RIGHT, padx=15, pady=10)
    
    def start_scraping(self):
        """Start scraping process"""
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.export_btn.config(state=tk.DISABLED)
        
        self.update_log("🚀 Starting scraping process...", 'info')
        self.update_log(f"📊 Mode: {self.mode_var.get().upper()} | Limit: {self.limit_var.get()} articles", 'info')
        self.status_label.config(text="⏳ Scraping in progress...")
        
        # Clear previous articles
        for item in self.articles_tree.get_children():
            self.articles_tree.delete(item)
        
        thread = threading.Thread(target=self.run_scraping, daemon=True)
        thread.start()
    
    def run_scraping(self):
        """Run scraping in background thread"""
        try:
            # Reset stats
            for source in self.stat_cards:
                self.stat_cards[source]['count'].config(text="0 articles")
                self.stat_cards[source]['status'].config(text="⏳ Loading...", fg=self.colors['warning'])
            
            self.total_label.config(text="0")
            self.all_articles = []
            
            # Run async scraping
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            mode = self.mode_var.get()
            limit = self.limit_var.get()
            
            if mode == 'async':
                self.update_log("🔄 Using async scraping mode (full scraping)...", 'info')
                self.results = loop.run_until_complete(
                    self.aggregator.scrape_all_async(limit, self.update_stat_card)
                )
            else:
                self.update_log("🔄 Using RSS mode (faster)...", 'info')
                # RSS only mode
                rss_tasks = []
                sources = ['gb_hackers', 'the_hacker_news', 'security_week', 
                          'dark_reading', 'bleeping_computer', 'krebs_security']
                for source in sources:
                    rss_tasks.append(
                        loop.run_until_complete(
                            asyncio.to_thread(
                                self.aggregator.rss_aggregator.fetch_rss_feed, 
                                source, limit
                            )
                        )
                    )
                
                self.results = {}
                for result in rss_tasks:
                    source_key = result.source.lower().replace(' ', '_')
                    self.results[source_key] = result
                    self.update_stat_card(source_key, result)
            
            loop.close()
            
            # Collect all articles
            total_count = 0
            for result in self.results.values():
                if result.status == 'success':
                    self.all_articles.extend(result.articles)
                    total_count += len(result.articles)
            
            self.total_label.config(text=str(total_count))
            self.update_log(f"✨ Scraping completed! Total: {total_count} articles", 'success')
            self.status_label.config(text="✅ Ready (Completed)")
            self.export_btn.config(state=tk.NORMAL)
            
            # Populate articles tree
            self.populate_articles()
            
        except Exception as e:
            self.update_log(f"❌ Error: {str(e)}", 'error')
            self.status_label.config(text="❌ Error occurred")
        finally:
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def update_stat_card(self, source_key, result: ScrapingResult):
        """Update stat card with results"""
        if source_key in self.stat_cards:
            count = len(result.articles) if result.status == 'success' else 0
            status_icon = "✅" if result.status == 'success' else "❌"
            
            self.stat_cards[source_key]['count'].config(text=f"{count} articles")
            self.stat_cards[source_key]['status'].config(
                text=f"{status_icon} {result.status.upper()}",
                fg=self.colors['success'] if result.status == 'success' else self.colors['error']
            )
            
            if count > 0:
                self.update_log(f"✅ {source_key.replace('_', ' ').title()}: {count} articles", 'success')
            else:
                self.update_log(f"⚠️ {source_key.replace('_', ' ').title()}: {result.error or 'No articles'}", 'warning')
    
    def populate_articles(self):
        """Populate articles tree with data"""
        self.articles_tree.delete(*self.articles_tree.get_children())
        
        for article in self.all_articles[:200]:  # Limit to 200 for performance
            source = article.get('source', 'Unknown')
            title = article.get('title', 'N/A')[:80]
            url = article.get('url', '')
            
            self.articles_tree.insert('', 'end', 
                                     values=(source, title, url))
    
    def open_url(self, event):
        """Open URL in browser on double click"""
        item = self.articles_tree.selection()[0]
        values = self.articles_tree.item(item, 'values')
        if values and len(values) > 2:
            url = values[2]
            if url and url.startswith('http'):
                webbrowser.open(url)
    
    def stop_scraping(self):
        """Stop scraping"""
        self.is_running = False
        self.update_log("⏹️ Scraping stopped by user", 'warning')
        self.status_label.config(text="⏹️ Stopped")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def update_log(self, message, level='info'):
        """Update log display"""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry, level)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
    
    def export_results(self):
        """Export results"""
        if not self.all_articles:
            messagebox.showwarning("Export", "No articles to export. Please scrape first.")
            return
        
        folder = filedialog.askdirectory(title="Select export folder")
        if folder:
            try:
                format_type = 'both'
                if not (self.export_csv.get() and self.export_json.get()):
                    format_type = 'csv' if self.export_csv.get() else 'json'
                
                csv_file, json_file = self.aggregator.save_results(self.results, format_type)
                
                self.update_log(f"💾 Exporting results...", 'info')
                
                if csv_file:
                    self.update_log(f"✅ CSV exported: {csv_file}", 'success')
                
                if json_file:
                    self.update_log(f"✅ JSON exported: {json_file}", 'success')
                
                messagebox.showinfo("Export", f"Results exported successfully!\n\nFolder: {folder}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting: {str(e)}")
                self.update_log(f"❌ Export error: {str(e)}", 'error')
    
    def update_time(self):
        """Update time in statusbar"""
        current_time = datetime.now().strftime('%H:%M:%S')
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernNewsAggregatorUI(root)
    app.update_time()
    root.mainloop()
