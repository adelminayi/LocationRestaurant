import folium

loc = [36.778259, -119.417931]
m = folium.Map(location=loc, height=400, width=800, zoom_start=12)
folium.ClickForMarker().add_to(m)
m.save('map.html')
