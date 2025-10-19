# 🚀 Cybersecurity News Aggregator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-blue?style=for-the-badge)

Aplikasi desktop modern untuk mengagregasi berita cybersecurity real-time dari multiple sources dengan UI yang elegan dan responsif.

[Features](#-features) • [Installation](#-instalasi) • [Usage](#-penggunaan) • [Export](#-export-data) • [Screenshots](#-screenshots)

</div>

---

## ✨ Features

- **📊 Real-time Dashboard** - Statistik live dari 6 sumber berita berbeda
- **🔄 Multi-Source Scraping** - Mengagregasi dari GB Hackers, The Hacker News, Security Week, Dark Reading, Bleeping Computer, dan Krebs Security
- **⚡ Dual Mode Scraping**
  - **Async Mode**: Full web scraping untuk konten komprehensif
  - **RSS Mode**: Feed parsing yang cepat dan reliable
- **📝 Live Log Display** - Pantau proses scraping real-time dengan color-coded messages
- **📰 Articles Table** - Tampilkan semua artikel dengan columns Source, Title, dan URL
- **🔗 Direct URL Opening** - Double-click artikel untuk membuka di browser
- **💾 Multi-Format Export** - Simpan hasil ke CSV dan/atau JSON
- **⚙️ Customizable Settings**
  - Atur jumlah articles per domain (5-30)
  - Pilih scraping mode (Async/RSS)
  - Tentukan format export
- **🎨 Modern Dark Theme UI** - Interface yang eye-friendly dan profesional

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Tkinter** - GUI Framework
- **Feedparser** - RSS/Atom feed parsing
- **BeautifulSoup4** - HTML parsing
- **aiohttp** - Async HTTP requests
- **Asyncio** - Async programming

---

## 📋 Prerequisites

- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- Koneksi internet

---

## 📥 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/cybersecurity-news-aggregator.git
cd cybersecurity-news-aggregator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Atau install manual:

```bash
pip install feedparser beautifulsoup4 aiohttp requests
```

### 3. Jalankan Aplikasi

```bash
python3 cybersecurity_news_ui.py
```

Atau dari terminal ZSH:

```bash
python3 cybersecurity_news_ui.py
```

---

## 🚀 Penggunaan

### 1. **Memulai Scraping**

- Klik tombol **▶ START SCRAPING** di header
- Aplikasi akan mulai mengumpulkan artikel dari 6 sumber
- Pantau progress di tab **📝 Live Log**

### 2. **Monitor Dashboard**

Tab **📊 Dashboard** menampilkan:
- Jumlah artikel per source
- Status setiap source (✅ Success / ❌ Error)
- Total artikel yang terkumpul

### 3. **View Articles**

Tab **📰 Articles** menampilkan:
- Tabel semua artikel yang dikumpulkan
- Sortable dan scrollable (horizontal & vertical)
- **Double-click URL** untuk buka artikel di browser

### 4. **Customize Settings**

Tab **⚙️ Settings** memungkinkan:
- **Articles per source**: Atur jumlah (5-30)
- **Scraping mode**: 
  - Async (full scraping, lebih lambat tapi komprehensif)
  - RSS only (lebih cepat, sangat reliable)
- **Export format**: Pilih CSV, JSON, atau keduanya

### 5. **Export Results**

- Klik tombol **💾 EXPORT**
- Pilih folder destination
- Hasil tersimpan sebagai:
  - `cybersecurity_news_YYYYMMDD_HHMMSS.csv`
  - `cybersecurity_news_YYYYMMDD_HHMMSS.json`

---

## 📊 Data Sources

| Source | Type | Reliability |
|--------|------|-------------|
| [GB Hackers](https://gbhackers.com) | RSS Feed | ⭐⭐⭐⭐⭐ |
| [The Hacker News](https://thehackernews.com) | RSS Feed | ⭐⭐⭐⭐⭐ |
| [Security Week](https://www.securityweek.com) | RSS Feed | ⭐⭐⭐⭐⭐ |
| [Dark Reading](https://www.darkreading.com) | RSS Feed | ⭐⭐⭐⭐⭐ |
| [Bleeping Computer](https://www.bleepingcomputer.com) | RSS Feed | ⭐⭐⭐⭐⭐ |
| [Krebs on Security](https://krebsonsecurity.com) | Async Web Scrape | ⭐⭐⭐⭐ |

---

## 📤 Export Format

### CSV Output
```csv
title,url,summary,published,source
"Title Artikel","https://example.com","Summary...","2025-10-19 19:39","GB Hackers"
```

### JSON Output
```json
{
  "metadata": {
    "scraped_at": "2025-10-19T19:39:57.123456",
    "total_articles": 60
  },
  "articles": [
    {
      "title": "Title Artikel",
      "url": "https://example.com",
      "summary": "Summary...",
      "published": "2025-10-19 19:39",
      "source": "GB Hackers"
    }
  ]
}
```

---

## 🎨 UI Features

### Header
- Real-time status indicator
- Quick action buttons (Start, Stop, Export)
- Aplikasi title dan subtitle

### Dashboard Tab
- 6 stat cards untuk setiap source
- Real-time update saat scraping
- Total articles counter

### Live Log Tab
- Timestamped log messages
- Color-coded output (Info, Success, Warning, Error)
- Auto-scroll ke bottom

### Articles Tab
- Treeview dengan 3 columns
- Horizontal & vertical scrollbars
- Double-click untuk open URL
- Support large datasets

### Settings Tab
- Adjustable article limit (slider 5-30)
- Mode selection (Async/RSS)
- Export format checkboxes
- Informative labels

---

## 🔧 Configuration

### Default Settings
```python
# Articles per source
limit = 10

# Scraping mode
mode = "async"  # atau "rss"

# Export formats
export_csv = True
export_json = True
```

### Customize Sources

Edit `RSSFeedAggregator.__init__()`:
```python
self.rss_feeds = {
    'your_source': 'https://yoursource.com/feed/',
    # ... more sources
}
```

---

## 🐛 Troubleshooting

### Masalah: Scraping lambat
**Solusi**: Gunakan RSS mode di Settings tab

### Masalah: Network timeout
**Solusi**: 
- Cek koneksi internet
- Tingkatkan timeout di `AsyncWebScraper.setup_session()`

### Masalah: No articles dikumpulkan
**Solusi**:
- Periksa Live Log tab untuk error details
- Coba kurangi article limit di Settings
- Cek apakah sources masih aktif

### Masalah: Export error
**Solusi**:
- Pastikan folder destination writable
- Gunakan path yang valid (hindari special characters)
- Cek disk space tersedia

---

## 📝 Logging

Aplikasi menghasilkan log dengan format:
```
[HH:MM:SS] [LEVEL] Message
```

Levels: `INFO`, `DEBUG`, `WARNING`, `ERROR`

Lihat console output untuk full debugging information.

---

## 📦 Project Structure

```
cybersecurity-news-aggregator/
├── cybersecurity_news_ui.py    # Main application file
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
└── .gitignore                   # Git ignore rules
```

---

## 🚀 Performance Tips

1. **Gunakan RSS Mode** untuk scraping lebih cepat
2. **Reduce Article Limit** jika perlu response cepat
3. **Run pada Off-Peak Hours** untuk avoid rate limiting
4. **Close Browser Windows** lain untuk free up resources
5. **Check Internet Speed** sebelum bulk scraping

---

## 📄 License

Project ini dilicense di bawah MIT License - lihat [LICENSE](LICENSE) file untuk details.

---

## 🤝 Contributing

Contributions sangat diterima! Untuk major changes, silakan buka issue terlebih dahulu untuk discuss tentang proposed changes.

### Steps untuk Contribute:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 🐛 Report Issues

Temukan bug? Silakan buka [GitHub Issue](https://github.com/yourusername/cybersecurity-news-aggregator/issues) dengan:
- Deskripsi detail tentang issue
- Steps untuk reproduce
- Expected behavior
- Screenshots jika applicable

---

## 💡 Feature Requests

Punya ide fitur baru? Buka [GitHub Discussion](https://github.com/yourusername/cybersecurity-news-aggregator/discussions) untuk discuss!

Possible future features:
- 🔔 Desktop notifications
- 📧 Email alerts untuk artikel penting
- 🔍 Advanced filtering dan search
- 📊 Analytics dashboard
- ⏰ Scheduled scraping
- 🌐 Web interface
- 🗄️ Database storage

---

## 📞 Contact & Support

- **GitHub Issues**: [Report bugs](https://github.com/yourusername/cybersecurity-news-aggregator/issues)
- **GitHub Discussions**: [Share ideas](https://github.com/yourusername/cybersecurity-news-aggregator/discussions)
- **Email**: your.email@example.com

---

## 🙏 Acknowledgments

- **Data Sources**: GB Hackers, The Hacker News, Security Week, Dark Reading, Bleeping Computer, Krebs on Security
- **Libraries**: feedparser, beautifulsoup4, aiohttp, tkinter
- **Community**: Thanks untuk semua contributors dan users!

---

## 📸 Screenshots

### Dashboard View
![Dashboard]([screenshots/dashboard.png](https://i.ibb.co.com/whBFYbHN/Cuplikan-layar-dari-2025-10-19-20-07-08.png))

### Live Log
![Live Log]([screenshots/live-log.png](https://i.ibb.co.com/N205Cmnm/Cuplikan-layar-dari-2025-10-19-20-07-15.png))

### Articles Table
![Articles](https://i.ibb.co.com/VY2qZ0tx/Cuplikan-layar-dari-2025-10-19-20-07-20.png)

---

## 📊 Statistics

- ✅ 6 Active News Sources
- 📰 Supports 1000+ articles per scraping session
- ⚡ Real-time processing
- 💾 Dual export formats (CSV & JSON)
- 🎨 Modern dark-themed UI

---

**Made with ❤️ for Cybersecurity Enthusiasts**

⭐ Don't forget to give this project a star if you find it useful!

---

<div align="center">

[⬆ back to top](#-cybersecurity-news-aggregator)

</div>
