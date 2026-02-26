#!/usr/bin/env python3
"""
Create global conflict heatmap using Folium with recent events
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
    # Add more countries as needed
    "United States": [37.0902, -95.7129],
    "China": [35.8617, 104.1954],
    "Brazil": [-14.2350, -51.9253],
    "Germany": [51.1657, 10.4515],
    "France": [46.2276, 2.2137],
    "Japan": [36.2048, 138.2529],
    "South Korea": [35.9078, 127.7669],
    "Iran": [32.4279, 53.6880],
    "Iraq": [33.2232, 43.6793],
    "Libya": [26.3351, 17.2283],
    "Mali": [17.5707, -3.9962],
    "Chad": [15.4542, 18.7322],
    "Ethiopia": [9.1450, 40.4897],
    "DR Congo": [-4.0383, 21.7587],
    "Central African Republic": [6.6111, 20.9394],
    "Burkina Faso": [12.2383, -1.5616],
    "Niger": [17.6078, 8.0817],
    "Mozambique": [-18.6657, 35.5296],
    "Cameroon": [7.3697, 12.3547],
    "Lebanon": [33.8547, 35.8623],
    "Azerbaijan": [40.1431, 47.5769],
    "Armenia": [40.0691, 45.0382],
    "Georgia": [42.3154, 43.3569],
    "Kazakhstan": [48.0196, 66.9237],
    "Tajikistan": [38.8610, 71.2761],
    "Kyrgyzstan": [41.2044, 74.7661],
    "Uzbekistan": [41.3775, 64.5853],
    "Turkmenistan": [38.9697, 59.5563],
    "Belarus": [53.7098, 27.9534],
    "Moldova": [47.4116, 28.3699],
    "Bosnia and Herzegovina": [43.9159, 17.6791],
    "Serbia": [44.0165, 21.0059],
    "Kosovo": [42.6026, 20.9030],
    "North Korea": [40.3399, 127.5101],
    "Venezuela": [6.4238, -66.5897],
    "Peru": [-9.1900, -75.0152],
    "Ecuador": [-1.8312, -78.1834],
    "Bolivia": [-16.2902, -63.5887],
    "Paraguay": [-23.4425, -58.4438],
    "Uruguay": [-32.5228, -55.7658],
    "Argentina": [-38.4161, -63.6167],
    "Chile": [-35.6751, -71.5430],
    "Australia": [-25.2744, 133.7751],
    "New Zealand": [-40.9006, 174.8860],
    "Canada": [56.1304, -106.3468],
    "Greenland": [71.7069, -42.6043],
    "Iceland": [64.9631, -19.0208],
    "Norway": [60.4720, 8.4689],
    "Sweden": [60.1282, 18.6435],
    "Finland": [61.9241, 25.7482],
    "Denmark": [56.2639, 9.5018],
    "Netherlands": [52.1326, 5.2913],
    "Belgium": [50.5039, 4.4699],
    "Luxembourg": [49.8153, 6.1296],
    "Switzerland": [46.8182, 8.2275],
    "Austria": [47.5162, 14.5501],
    "Hungary": [47.1625, 19.5033],
    "Czech Republic": [49.8175, 15.4730],
    "Slovakia": [48.6690, 19.6990],
    "Poland": [51.9194, 19.1451],
    "Lithuania": [55.1694, 23.8813],
    "Latvia": [56.8796, 24.6032],
    "Estonia": [58.5953, 25.0136],
    "Portugal": [39.3999, -8.2245],
    "Spain": [40.4637, -3.7492],
    "Italy": [41.8719, 12.5674],
    "Greece": [39.0742, 21.8243],
    "Albania": [41.1533, 20.1683],
    "Montenegro": [42.7087, 19.3744],
    "Croatia": [45.1000, 15.2000],
    "Slovenia": [46.1512, 14.9955],
    "Malta": [35.9375, 14.3754],
    "Cyprus": [35.1264, 33.4299],
    "Egypt": [26.8206, 30.8025],
    "Tunisia": [33.8869, 9.5375],
    "Algeria": [28.0339, 1.6596],
    "Morocco": [31.7917, -7.0926],
    "Western Sahara": [24.2155, -12.8858],
    "Mauritania": [21.0079, -10.9408],
    "Senegal": [14.4974, -14.4524],
    "Gambia": [13.4432, -15.3101],
    "Guinea-Bissau": [11.8037, -15.1804],
    "Guinea": [9.9456, -9.6966],
    "Sierra Leone": [8.4606, -11.7799],
    "Liberia": [6.4281, -9.4295],
    "Ivory Coast": [7.5400, -5.5471],
    "Ghana": [7.9465, -1.0232],
    "Togo": [8.6195, 0.8248],
    "Benin": [9.3077, 2.3158],
    "Burundi": [-3.3731, 29.9189],
    "Rwanda": [-1.9403, 29.8739],
    "Uganda": [1.3733, 32.2903],
    "Kenya": [-0.0236, 37.9062],
    "Tanzania": [-6.3690, 34.8888],
    "Zambia": [-13.1339, 27.8493],
    "Zimbabwe": [-19.0154, 29.1549],
    "Botswana": [-22.3285, 24.6849],
    "Namibia": [-22.9576, 18.4904],
    "South Africa": [-30.5595, 22.9375],
    "Lesotho": [-29.6100, 28.2336],
    "Eswatini": [-26.5225, 31.4659],
    "Madagascar": [-18.7669, 46.8691],
    "Mauritius": [-20.3484, 57.5522],
    "Comoros": [-11.6455, 43.3333],
    "Seychelles": [-4.6796, 55.4920],
    "Djibouti": [11.8251, 42.5903],
    "Eritrea": [15.1794, 39.7823],
    "South Sudan": [6.8770, 31.3070],
    "Angola": [-11.2027, 17.8739],
    "Gabon": [-0.8037, 11.6094],
    "Republic of the Congo": [-0.2280, 15.8277],
    "Equatorial Guinea": [1.6508, 10.2679],
    "Sao Tome and Principe": [0.1864, 6.6131],
    "Cape Verde": [16.5388, -23.0418],
    "Sri Lanka": [7.8731, 80.7718],
    "Bangladesh": [23.6850, 90.3563],
    "Nepal": [28.3949, 84.1240],
    "Bhutan": [27.5142, 90.4336],
    "Maldives": [3.2028, 73.2207],
    "Brunei": [4.5353, 114.7277],
    "Singapore": [1.3521, 103.8198],
    "Malaysia": [4.2105, 101.9758],
    "Indonesia": [-0.7893, 113.9213],
    "Papua New Guinea": [-6.3150, 143.9555],
    "Fiji": [-16.5782, 179.4144],
    "Solomon Islands": [-9.6457, 160.1562],
    "Vanuatu": [-15.3767, 166.9592],
    "New Caledonia": [-20.9043, 165.6180],
    "French Polynesia": [-17.6797, -149.4068],
    "Samoa": [-13.7590, -172.1046],
    "Tonga": [-21.1790, -175.1982],
    "Kiribati": [1.8708, -157.3620],
    "Micronesia": [7.4256, 150.5508],
    "Marshall Islands": [7.1315, 171.1845],
    "Palau": [7.5150, 134.5825],
    "Nauru": [-0.5228, 166.9315],
    "Tuvalu": [-7.1095, 177.6493],
    "Antarctica": [-82.8628, 135.0000]
}

def create_conflict_heatmap(data_file="conflict_data.json", output_file="global_conflict_heatmap.html"):
    """Create a global conflict heatmap"""
    
    # Load conflict data
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Data file {data_file} not found. Using empty data.")
        data = {"last_updated": None, "conflict_data": {}, "recent_events": []}
    
    conflict_data = data.get("conflict_data", {})
    recent_events = data.get("recent_events", [])
    
    # Create base map
    m = folium.Map(
        location=[20, 0], 
        zoom_start=2,
        tiles="CartoDB positron",
        attr="Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    )
    
    # Prepare heatmap data
    heat_data = []
    marker_data = []
    
    for country, info in conflict_data.items():
        if country in COUNTRY_COORDINATES:
            lat, lon = COUNTRY_COORDINATES[country]
            intensity = info.get("intensity", 0)
            
            # Add to heatmap data (lat, lon, intensity)
            heat_data.append([lat, lon, intensity])
            
            # Create popup content
            popup_content = f"""
            <div style="font-family: Arial, sans-serif; font-size: 12px;">
                <h4>{country}</h4>
                <p><strong>Conflict Intensity:</strong> {intensity}/100</p>
                <p><strong>Events (Last 7 days):</strong> {info.get('events_last_7days', 'N/A')}</p>
                <p><strong>Type:</strong> {info.get('type', 'Unknown')}</p>
            </div>
            """
            marker_data.append((lat, lon, popup_content, country))
    
    # Add heatmap layer - THIS WAS MISSING!
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
    marker_dict = {}
    for lat, lon, popup, country in marker_data:
        marker = folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            popup=folium.Popup(popup, max_width=300),
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=0.7
        )
        marker.add_to(m)
        marker_dict[country] = [lat, lon]
    
    # Create recent events HTML
    events_html = '<div style="position: fixed; bottom: 50px; right: 50px; width: 400px; max-height: 300px; background-color: white; border: 2px solid grey; z-index:9999; font-size:12px; padding: 10px; overflow-y: auto;">'
    events_html += '<h4 style="margin-top: 0; color: #d32f2f;">Recent Conflict Events (Last 7 Days)</h4>'
    events_html += '<div style="max-height: 250px; overflow-y: auto;">'
    
    # Process recent events (now they are arrays)
    for event in recent_events[:10]:  # Show top 10 most recent
        if len(event) >= 5:
            date, country, description, killed, wounded = event[:5]
            casualties = f"{killed} killed, {wounded} wounded"
            
            # Create click handler to jump to map location
            js_click = ""
            if country in marker_dict:
                lat, lon = marker_dict[country]
                js_click = f"onclick=\"window.parent.document.getElementById('map').dispatchEvent(new CustomEvent('jumpToLocation', {{detail: {{lat: {lat}, lon: {lon}}}}}))\" style=\"cursor: pointer;\""
            
            events_html += f'''
            <div style="border-bottom: 1px solid #eee; padding: 5px 0; margin: 5px 0;" {js_click}>
                <strong>{date}</strong><br/>
                <span style="color: #d32f2f;"><strong>{country}</strong></span><br/>
                {description}<br/>
                <em>Casualties: {casualties}</em>
            </div>
            '''
    
    events_html += '</div></div>'
    
    # Add title and legend
    title_html = f'''
        <h3 align="center" style="font-size:20px; font-weight:bold; margin:10px;">
        Global Conflict Heatmap
        </h3>
        <p align="center" style="font-size:12px; margin:5px;">
        Last Updated: {data.get("last_updated", "Never")}
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
        // Add event listener for map jumping
        document.addEventListener('DOMContentLoaded', function() {{
            // This will be handled by the parent frame if embedded
        }});
        </script>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save map
    m.save(output_file)
    print(f"Heatmap saved to {output_file}")
    return output_file

if __name__ == "__main__":
    create_conflict_heatmap()