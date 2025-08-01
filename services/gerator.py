import pandas as pd
import folium
import branca.colormap as cm
from datetime import datetime
from datetime import datetime

def inserir_info_no_html(arquivo_html, tipo, total_pontos, minimo, maximo, nome_arquivo):
    with open(arquivo_html, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    agora = datetime.now()
    timestamp_visivel = agora.strftime('%Y-%m-%d %H:%M:%S')
    timestamp_oculto = agora.isoformat()

    bloco_info = f"""
    <div data-gerado-em="{timestamp_oculto}" style="display:none;"></div>
    <div style='padding:10px;font-family:sans-serif;font-size:14px;background:#f9f9f9;border-bottom:1px solid #ccc;'>
        <b>🕒 Mapa gerado em:</b> {timestamp_visivel}<br>
        <b>📄 Arquivo CSV:</b> {nome_arquivo}<br>
        <b>📍 Total de pontos:</b> {total_pontos}<br>
        <b>📊 Faixa de {tipo}:</b> {minimo} a {maximo}
    </div>
    """

    conteudo = conteudo.replace("<body>", f"<body>\n{bloco_info}", 1)

    with open(arquivo_html, 'w', encoding='utf-8') as f:
        f.write(conteudo)


def gerar_mapa_por_rsrp(csv_entrada='teste_filtrado.csv', saida_html='mapa_rsrp.html'):
    df = pd.read_csv(csv_entrada)

    if df.empty:
        print("⚠️ Nenhum dado no CSV.")
        return

    mapa = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], zoom_start=15)

    min_rsrp = df['rsrp'].min()
    max_rsrp = df['rsrp'].max()
    colormap = cm.linear.RdYlGn_11.scale(min_rsrp, max_rsrp).to_step(n=10)
    colormap.caption = 'RSRP (dBm)'
    colormap.add_to(mapa)

    count = 0
    for _, row in df.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']) and pd.notnull(row['rsrp']):
            color = colormap(row['rsrp'])
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=7,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                popup=folium.Popup(f"""
                    <b>Timestamp:</b> {row['timestamp']}<br>
                    <b>RSRP:</b> {row['rsrp']} dBm<br>
                    <b>RSRQ:</b> {row['rsrq']} dB<br>
                    <b>Cell ID:</b> {row['cellId']}<br>
                    <b>Tecnologia:</b> {row['technology']}
                """, max_width=250),
                tooltip=f"RSRP: {row['rsrp']} dBm"
            ).add_to(mapa)
            count += 1

    mapa.save(saida_html)

    inserir_info_no_html(
        arquivo_html=saida_html,
        tipo='RSRP (dBm)',
        total_pontos=count,
        minimo=min_rsrp,
        maximo=max_rsrp,
        nome_arquivo=csv_entrada
    )

    print(f"✅ Mapa por RSRP salvo como {saida_html}")
    print(f"📍 Total de pontos plotados: {count}")


def gerar_mapa_por_rsrq(csv_entrada='teste_filtrado.csv', saida_html='mapa_rsrq.html'):
    df = pd.read_csv(csv_entrada)

    if df.empty:
        print("⚠️ Nenhum dado no CSV.")
        return

    mapa = folium.Map(location=[df.latitude.mean(), df.longitude.mean()], zoom_start=15)

    min_rsrq = df['rsrq'].min()
    max_rsrq = df['rsrq'].max()
    colormap = cm.linear.RdYlGn_11.scale(min_rsrq, max_rsrq).to_step(n=10)
    colormap.caption = 'RSRQ (dB)'
    colormap.add_to(mapa)

    count = 0
    for _, row in df.iterrows():
        if pd.notnull(row['latitude']) and pd.notnull(row['longitude']) and pd.notnull(row['rsrq']):
            color = colormap(row['rsrq'])
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=7,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8,
                popup=folium.Popup(f"""
                    <b>Timestamp:</b> {row['timestamp']}<br>
                    <b>RSRP:</b> {row['rsrp']} dBm<br>
                    <b>RSRQ:</b> {row['rsrq']} dB<br>
                    <b>Cell ID:</b> {row['cellId']}<br>
                    <b>Tecnologia:</b> {row['technology']}
                """, max_width=250),
                tooltip=f"RSRQ: {row['rsrq']} dB"
            ).add_to(mapa)
            count += 1

    mapa.save(saida_html)

    inserir_info_no_html(
        arquivo_html=saida_html,
        tipo='RSRQ (dB)',
        total_pontos=count,
        minimo=min_rsrq,
        maximo=max_rsrq,
        nome_arquivo=csv_entrada
    )

    print(f"✅ Mapa por RSRQ salvo como {saida_html}")
    print(f"📍 Total de pontos plotados: {count}")
