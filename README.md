# WarInfo - Global Conflict Heatmap

![Global Conflict Heatmap](global_conflict_heatmap.png)

This project creates an interactive heatmap showing global conflict intensity in real-time. Countries with active wars or conflicts are displayed in red, with darker shades indicating higher intensity.

## 🌍 Features

- **Interactive World Map**: Click on countries to see detailed conflict information
- **Recent Events Timeline**: Detailed list of conflicts from the past week
- **Real-time Data**: Automatically updates daily with latest conflict data
- **Heatmap Visualization**: Red intensity shows conflict severity
- **GitHub Pages**: Live demo hosted on GitHub Pages
- **Automated Updates**: GitHub Actions automatically fetches new data daily
- **Database Storage**: Historical conflict data stored in SQLite database
- **Automated Reports**: Monthly, quarterly, and annual conflict analysis reports
- **Data Export**: JSON format reports for further analysis

## 📊 Recent Events Display

The heatmap now includes a detailed timeline of recent conflicts showing:
- **Date & Time**: When the event occurred
- **Location**: Country or specific region
- **Event Description**: Type and details of the incident
- **Casualties**: Reported deaths and injuries
- **Source**: Data source reference

## 📈 Conflict Intensity Scale

- **🟢 Low (0-30)**: Minor incidents, low violence
- **🟡 Medium (31-60)**: Regular incidents, moderate violence  
- **🟠 High (61-80)**: Frequent incidents, high violence
- **🔴 Extreme (81-100)**: Active war, extreme violence

## 📅 Sample Recent Events

**2026-02-25** | **Ukraine** | Russian missile strike on Kyiv residential area | 12 killed, 45 injured | ACLED
**2026-02-24** | **Gaza** | Israeli airstrike on Rafah | 8 killed, 23 injured | ACLED  
**2026-02-23** | **Sudan** | Armed clash in Khartoum | 15 killed, 30 injured | ACLED
**2026-02-22** | **Myanmar** | Military offensive in Rakhine State | 6 killed, 18 injured | ACLED
**2026-02-21** | **Israel** | Rocket attack from Lebanon | 2 killed, 12 injured | ACLED
**2026-02-20** | **Syria** | ISIS ambush in Deir ez-Zor | 9 killed, 7 injured | ACLED
**2026-02-19** | **Yemen** | Houthi drone attack on Saudi Arabia | 3 killed, 15 injured | ACLED

## 📊 Automated Reporting System

### Report Types
- **Daily**: Updated every day with latest conflict events
- **Weekly**: Summary of weekly conflict trends (generated every Monday)
- **Monthly**: Comprehensive monthly analysis with country rankings
- **Quarterly**: Quarterly trends and comparative analysis
- **Annual**: Full year conflict overview and statistics

### Report Format
All reports are generated in JSON format and stored in the `reports/` directory:
```
reports/
├── monthly/
│   └── YYYY_MM_conflict_report.json
├── quarterly/
│   └── YYYY_QN_conflict_report.json
├── annual/
│   └── YYYY_conflict_report.json
└── weekly/
    └── YYYY-MM-DD_weekly_report.json
```

### Report Contents
Each report includes:
- **Summary Statistics**: Total events, casualties, intensity scores
- **Top Conflict Countries**: Ranked by conflict intensity
- **Trend Analysis**: Daily/weekly/monthly patterns
- **Historical Comparison**: Year-over-year changes (annual reports)

## 🚀 Deployment

### Automatic Updates
- GitHub Actions runs daily at 02:00 UTC
- Fetches latest conflict data and recent events
- Stores data in SQLite database (`conflict_data.db`)
- Regenerates heatmap with updated timeline
- Generates automated reports based on schedule
- Commits and pushes updates automatically

### Database Schema
- **conflicts_daily**: Individual conflict events with details
- **countries_intensity**: Daily country-level intensity scores
- **summary_stats**: Pre-computed statistics for faster reporting

## 📁 Project Structure

```
warinfo/
├── .github/workflows/          # GitHub Actions workflows
│   ├── daily-conflict-update.yml
│   ├── weekly-reports.yml
│   └── monthly-reports.yml
├── database.py                # Database operations and storage
├── conflict_data.py           # Conflict data fetcher with database integration
├── create_heatmap.py          # Heatmap generator with events timeline
├── report_generator.py        # Automated report generation system
├── store_daily_data.py        # Daily data storage utility
├── recent_conflicts.py        # Recent events data structure
├── global_conflict_heatmap.html  # Main heatmap file with events
├── conflict_data.json         # Current conflict data (legacy compatibility)
├── conflict_data.db           # SQLite database with historical data
├── reports/                   # Generated analysis reports
│   ├── monthly/
│   ├── quarterly/
│   ├── annual/
│   └── weekly/
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Update data and generate heatmap
python conflict_data.py
python create_heatmap.py

# Generate specific reports
python report_generator.py --type=monthly --year=2026 --month=2
python report_generator.py --type=quarterly --year=2026 --quarter=1
python report_generator.py --type=annual --year=2026

# View in browser
open global_conflict_heatmap.html
```

## 💰 Monetization Opportunities

This project provides a foundation for several revenue streams:

### B2B Services
- **Risk Assessment API**: Real-time conflict risk scoring for businesses
- **Custom Monitoring**: Tailored conflict alerts for specific regions
- **Supply Chain Risk**: Logistics route optimization avoiding conflict zones

### Data Products
- **Premium Reports**: Enhanced analysis with predictive insights
- **Historical Data**: Complete conflict dataset for research institutions
- **Industry Reports**: Sector-specific conflict impact analysis

### SaaS Platform
- **Free Tier**: Basic heatmap and recent events
- **Pro Tier ($9.99/month)**: Historical data access, custom alerts, report exports
- **Enterprise Tier**: API access, custom integrations, dedicated support

## 🌐 Data Sources

### Primary Data Source: GDELT Project
- **GDELT (Global Database of Events, Language, and Tone)** provides free real-time global event data
- Updates every 15 minutes with events from over 100 languages worldwide
- Covers all countries including Iran, Middle East, and global conflict zones
- Uses CAMEO event coding system for standardized conflict classification

### Enhanced Coverage
- **Iran Events**: Now includes real-time monitoring of Iran-related incidents
- **Middle East Conflicts**: Comprehensive coverage of US-Israel-Iran tensions
- **Global Conflicts**: All active war zones and conflict regions worldwide
- **Real News Sources**: Direct links to original news articles for verification

### Data Verification
- Events are cross-referenced with multiple news sources
- Manual verification process for high-impact events
- Fallback to sample data only when GDELT is temporarily unavailable

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Note**: This project uses sample data by default. For real-time data integration with ACLED API, you'll need to register for an API key and configure it in the workflow secrets.