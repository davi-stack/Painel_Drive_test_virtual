import pandas as pd
from datetime import datetime, timedelta

def classificar_linhas(csv_entrada='saida.csv', html_saida='resumo_temporal.html'):
    df = pd.read_csv(csv_entrada)
    df = df.reset_index().rename(columns={'index': 'linha_csv'})

    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True, errors='coerce')
    df['timestamp'] = df['timestamp'].dt.tz_convert('America/Sao_Paulo')
    df['timestamp_str'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df = df.dropna(subset=['timestamp'])

    contadores = {
        'ultimos_30_min': 0,
        'hoje': 0,
        'ontem': 0,
        'ultimo_7_dias': 0,
        'mais_que_7_dias': 0
    }

    agora = datetime.now().astimezone()

    for linha in df.itertuples():
        timestamp = linha.timestamp

        if agora - timestamp <= timedelta(minutes=30):
            contadores['ultimos_30_min'] += 1
        if timestamp.date() == agora.date():
            contadores['hoje'] += 1
        if timestamp.date() == (agora - timedelta(days=1)).date():
            contadores['ontem'] += 1
        if timestamp.date() >= (agora - timedelta(days=7)).date():
            contadores['ultimo_7_dias'] += 1
        else:
            contadores['mais_que_7_dias'] += 1

    total_linhas = len(df)

    # 🖨️ Imprime no terminal
    print(f"\n📊 Total de linhas analisadas: {total_linhas}")
    print(f"⏱️ Últimos 30 minutos: {contadores['ultimos_30_min']}")
    print(f"📅 Hoje: {contadores['hoje']}")
    print(f"📆 Ontem: {contadores['ontem']}")
    print(f"🗓️ Últimos 7 dias: {contadores['ultimo_7_dias']}")
    print(f"⏳ Mais de 7 dias: {contadores['mais_que_7_dias']}")

    # 💾 Salva CSV limpo
    df.to_csv('dados_formatados.csv', index=False)

    # 📝 Gera HTML de resumo
    hora_execucao = agora.strftime('%Y-%m-%d %H:%M:%S')

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Resumo Temporal dos Dados</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 30px; }}
            h1 {{ color: #333; }}
            .resumo {{
                background: #f9f9f9;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 5px rgba(0,0,0,0.1);
                max-width: 500px;
            }}
            .item {{ margin: 10px 0; }}
        </style>
    </head>
    <body>
        <h1>📊 Resumo Temporal dos Dados</h1>
        <div class="resumo">
            <div class="item"><b>⏱️ Últimos 30 minutos:</b> {contadores['ultimos_30_min']}</div>
            <div class="item"><b>📅 Hoje:</b> {contadores['hoje']}</div>
            <div class="item"><b>📆 Ontem:</b> {contadores['ontem']}</div>
            <div class="item"><b>🗓️ Últimos 7 dias:</b> {contadores['ultimo_7_dias']}</div>
            <div class="item"><b>⏳ Mais de 7 dias:</b> {contadores['mais_que_7_dias']}</div>
            <div class="item"><b>Total de linhas válidas:</b> {total_linhas}</div>
            <div class="item"><b>🕒 Geração:</b> {hora_execucao}</div>
        </div>
    </body>
    </html>
    """

    with open(html_saida, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ HTML de resumo salvo como: {html_saida}")


if __name__ == '__main__':
    classificar_linhas()
