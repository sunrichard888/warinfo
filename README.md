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

## 🚀 Deployment

### Automatic Updates
- GitHub Actions runs daily at 02:00 UTC
- Fetches latest conflict data and recent events
- Regenerates heatmap with updated timeline
- Commits and pushes updates automatically

## 📁 Project Structure

```
warinfo/
├── .github/workflows/          # GitHub Actions workflows
│   └── daily-conflict-update.yml
├── conflict_data.py           # Conflict data and recent events fetcher
├── create_heatmap.py          # Heatmap generator with events timeline
├── recent_conflicts.py        # Recent events data structure
├── global_conflict_heatmap.html  # Main heatmap file with events
├── conflict_data.json         # Current conflict data and events
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Update data and generate heatmap
python conflict_data.py
python create_heatmap.py

# View in browser
open global_conflict_heatmap.html
```

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Note**: This project uses sample data by default. For real-time data integration with ACLED API, you'll need to register for an API key and configure it in the workflow secrets.