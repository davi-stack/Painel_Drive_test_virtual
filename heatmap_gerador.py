import pandas as pd
import folium
from folium.plugins import MarkerCluster
import branca.colormap as cm

# 1. Carrega o CSV
df = pd.read_csv("teste.csv")

# 2. Remove linhas com coordenadas zeradas
df = df[(df['latitude'] != 0.0) & (df['longitude'] != 0.0)]

# 3. Cria o mapa centralizado no primeiro ponto válido
if df.empty:
    print("⚠️ Nenhum dado com coordenada válida.")
    exit()

mapa = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], zoom_start=13)

# 4. Cria colormap para RSRP
min_rsrp = df['rsrp'].min()
max_rsrp = df['rsrp'].max()
colormap = cm.linear.YlOrRd_09.scale(min_rsrp, max_rsrp)
colormap.caption = 'RSRP (dBm)'
colormap.add_to(mapa)

# 5. Agrupamento por célula (para filtro via JS depois)
marker_cluster = MarkerCluster().add_to(mapa)

# 6. Cria marcadores
for _, row in df.iterrows():
    color = colormap(row['rsrp']) if pd.notnull(row['rsrp']) else 'gray'
    popup_text = f"""
    <b>Timestamp:</b> {row['timestamp']}<br>
    <b>RSRP:</b> {row['rsrp']}<br>
    <b>RSRQ:</b> {row['rsrq']}<br>
    <b>Cell ID:</b> {row['cellId']}<br>
    <b>Tecnologia:</b> {row['technology']}
    """
    marker = folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=7,
        fill=True,
        fill_opacity=0.8,
        color=color,
        fill_color=color,
        popup=folium.Popup(popup_text, max_width=250),
        tooltip=f"CellID: {row['cellId']}"
    )
    marker.add_to(marker_cluster)

# 7. Salva mapa
mapa.save("mapa_interativo.html")
print("✅ Mapa interativo salvo como mapa_interativo.html")
