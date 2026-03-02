#!/usr/bin/env python3
"""
Create global conflict heatmap using Folium with proper event interaction
"""

import folium
import json
from datetime import datetime
import os

# Country coordinate mappings (ISO country codes to coordinates)
COUNTRY_COORDINATES = {
    "Ukraine": [48.3794, 31.1656],
    "Israel": [31.0461, 34.8516],
    "Gaza": [31.3547, 34.3088],
    "Sudan": [12.8628, 30.2176],
    "Myanmar": [21.9162, 95.9560],
    "Syria": [34.8021, 38.9968],
    "Yemen": [15.5527, 48.5164],
    "Afghanistan": [33.9391, 67.7100],
    "Somalia": [5.1521, 46.1996],
    "Nigeria": [9.0820, 8.6753],
    "Colombia": [4.5709, -74.2973],
    "Mexico": [23.6345, -102.5528],
    "Haiti": [18.9712, -72.2852],
    "Pakistan": [30.3753, 69.3451],
    "India": [20.5937, 78.9629],
    "Philippines": [12.8797, 121.7740],
    "Russia": [61.5240, 105.3188],
    "Turkey": [38.9637, 35.2433],
    "Iran": [32.4279, 53.6880],
    "United States": [37.0902, -95.7129],
    "China": [35.8617, 104.1954],
    "United Kingdom": [55.3781, -3.4360],
    "France": [46.2276, 2.2137],
    "Germany": [51.1657, 10.4515]
}

def create_conflict_heatmap(data_file="conflict_data.json", output_file="global_conflict_heatmap.html"):
    """Create a global conflict heatmap with proper event interaction"""
    
    # Load conflict data
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            conflict_data = data.get("conflict_data", {})
            recent_events = data.get("recent_events", [])
            data_source = data.get("data_source", "Real-time GDELT Data")
    except FileNotFoundError:
        print(f"Data file {data_file} not found. Using empty data.")
        conflict_data = {}
        recent_events = []
        data_source = "No Data Available"
    
    # Create base map
    m = folium.Map(
        location=[20, 0], 
        zoom_start=2,
        tiles="CartoDB positron",
        attr="Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    )
    
    # Prepare heatmap data
    heat_data = []
    
    for country, info in conflict_data.items():
        if country in COUNTRY_COORDINATES:
            lat, lon = COUNTRY_COORDINATES[country]
            intensity = info.get("intensity", 0)
            if intensity > 0:  # Only show countries with actual conflict
                heat_data.append([lat, lon, intensity])
    
    # Add heatmap layer
    from folium.plugins import HeatMap
    if heat_data:
        HeatMap(
            heat_data, 
            radius=25, 
            blur=15, 
            gradient={
                0.0: '#00FF00',   # Green - Low intensity
                0.3: '#FFFF00',   # Yellow - Medium intensity  
                0.6: '#FFA500',   # Orange - High intensity
                0.8: '#FF4500',   # Orange-red - Very high intensity
                1.0: '#FF0000'    # Red - Extreme intensity
            }
        ).add_to(m)
    
    # Add markers with popups
    for country, info in conflict_data.items():
        if country in COUNTRY_COORDINATES and info.get("intensity", 0) > 0:
            lat, lon = COUNTRY_COORDINATES[country]
            popup_content = f"""
            <div style="font-family: Arial, sans-serif; font-size: 12px;">
                <h4>{country}</h4>
                <p><strong>Conflict Intensity:</strong> {info.get('intensity', 0)}/100</p>
                <p><strong>Events (Last 7 days):</strong> {info.get('events_last_7days', 'N/A')}</p>
                <p><strong>Type:</strong> {info.get('type', 'Unknown')}</p>
                <p><em>Data Source: {data_source}</em></p>
            </div>
            """
            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                popup=folium.Popup(popup_content, max_width=300),
                color='red',
                fill=True,
                fillColor='red',
                fillOpacity=0.7
            ).add_to(m)
    
    # Create events HTML with proper JavaScript for interaction
    events_html = '<div style="position: fixed; bottom: 50px; right: 50px; width: 400px; max-height: 300px; background-color: white; border: 2px solid grey; z-index:9999; font-size:12px; padding: 10px; overflow-y: auto;"><h4 style="margin-top: 0; color: #d32f2f;">Recent Conflict Events (Last 7 Days)</h4><div style="max-height: 250px; overflow-y: auto;">'
    
    # Sample news sources for demo
    news_sources = {
        "Ukraine": "https://www.reuters.com/world/europe/",
        "Gaza": "https://www.aljazeera.com/news/middle-east/",
        "Sudan": "https://www.bbc.com/news/world-africa",
        "Myanmar": "https://www.channelnewsasia.com/asia",
        "Syria": "https://www.cnn.com/middleeast",
        "Yemen": "https://www.theguardian.com/world/yemen",
        "Afghanistan": "https://apnews.com/hub/afghanistan",
        "Somalia": "https://www.voanews.com/africa",
        "Nigeria": "https://www.premiumtimesng.com/",
        "Colombia": "https://colombiareports.com/",
        "Mexico": "https://mexiconewsdaily.com/",
        "Haiti": "https://haitiantimes.com/",
        "Pakistan": "https://www.dawn.com/",
        "India": "https://indianexpress.com/",
        "Philippines": "https://www.rappler.com/",
        "Russia": "https://www.themoscowtimes.com/",
        "Turkey": "https://www.hurriyetdailynews.com/",
        "Iran": "https://www.al-monitor.com/topics/iran",
        "United States": "https://www.washingtonpost.com/world/",
        "China": "https://www.scmp.com/news/china",
        "United Kingdom": "https://www.theguardian.com/uk-news",
        "France": "https://www.france24.com/en/france/",
        "Germany": "https://www.dw.com/en/germany/s-1001"
    }
    
    for event in recent_events[:15]:  # Limit to 15 most recent events
        if len(event) >= 9:  # Real GDELT format
            date, country, region, description, killed, wounded, details, url, event_id = event[:9]
            casualties = f"{killed} killed, {wounded} wounded"
            
            # Get coordinates for the country
            coords = COUNTRY_COORDINATES.get(country, [20, 0])
            lat, lon = coords
            
            # Get news source
            source_url = news_sources.get(country, url if url else "https://news.google.com/")
            
            # Create event HTML with proper onclick and source link
            event_html = f'''
            <div style="border-bottom: 1px solid #eee; padding: 5px 0; margin: 5px 0; cursor: pointer;" 
                 onclick="jumpToLocation({lat}, {lon})">
                <strong>{date}</strong><br/>
                <span style="color: #d32f2f;"><strong>{country}</strong></span><br/>
                {description}<br/>
                <em>Casualties: {casualties}</em><br/>
                <a href="{source_url}" target="_blank" style="font-size: 10px; color: #1976d2;">Source: News</a>
            </div>
            '''
            events_html += event_html
        elif len(event) >= 5:  # Legacy format
            date, country, description, killed, wounded = event[:5]
            casualties = f"{killed} killed, {wounded} wounded"
            
            coords = COUNTRY_COORDINATES.get(country, [20, 0])
            lat, lon = coords
            source_url = news_sources.get(country, "https://news.google.com/")
            
            event_html = f'''
            <div style="border-bottom: 1px solid #eee; padding: 5px 0; margin: 5px 0; cursor: pointer;" 
                 onclick="jumpToLocation({lat}, {lon})">
                <strong>{date}</strong><br/>
                <span style="color: #d32f2f;"><strong>{country}</strong></span><br/>
                {description}<br/>
                <em>Casualties: {casualties}</em><br/>
                <a href="{source_url}" target="_blank" style="font-size: 10px; color: #1976d2;">Source: News</a>
            </div>
            '''
            events_html += event_html
    
    events_html += '</div></div>'
    
    # Add title and legend
    title_html = f'''
        <h3 align="center" style="font-size:20px; font-weight:bold; margin:10px;">
        Global Conflict Heatmap - {data_source}
        </h3>
        <p align="center" style="font-size:12px; margin:5px;">
        Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </p>
        <div style="position: fixed; bottom: 50px; left: 50px; width: 200px; background-color: white; 
                    border: 2px solid grey; z-index:9999; font-size:14px; padding: 10px;">
            <p><strong>Legend:</strong></p>
            <p>🟢 Low Intensity</p>
            <p>🟡 Medium Intensity</p>
            <p>🟠 High Intensity</p>
            <p>🔴 Extreme Intensity</p>
        </div>
        {events_html}
        
        <script>
        // Function to jump to specific location on the map
        function jumpToLocation(lat, lon) {{
            var maps = document.querySelectorAll('.folium-map');
            if (maps.length > 0) {{
                // Find the map object
                var scriptTags = document.getElementsByTagName('script');
                for (var i = 0; i < scriptTags.length; i++) {{
                    var scriptText = scriptTags[i].text;
                    if (scriptText && scriptText.includes('L.map')) {{
                        var match = scriptText.match(/var (map_[a-z0-9]+) = L\\.map/);
                        if (match && match[1]) {{
                            var mapObj = window[match[1]];
                            if (mapObj) {{
                                mapObj.flyTo([lat, lon], 6);
                            }}
                            break;
                        }}
                    }}
                }}
            }}
        }}
        </script>
    '''
    
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save map
    m.save(output_file)
    print(f"Heatmap saved to {output_file}")
    return output_file

if __name__ == "__main__":
    create_conflict_heatmap()