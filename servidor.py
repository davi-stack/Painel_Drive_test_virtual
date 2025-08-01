from flask import Flask, send_file, render_template
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import subprocess
import os
from regen import regen

app = Flask(__name__)

ARQUIVOS = {
    'mapa_rsrp.html': 'mapa_rsrp.html',
    'mapa_rsrq.html': 'mapa_rsrq.html',
    'resumo_temporal.html': 'resumo_temporal.html'
}

CAMINHO_GERAR = "gerar_mapas.py"  # seu script de geração de mapas

def precisa_regenerar(html_path):
    if not os.path.exists(html_path):
        print("Motivo 1: Arquivo não existe")
        return True

    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        div_tag = soup.find('div', {'data-gerado-em': True})  # Busca a div com o atributo
        
        if not div_tag:
            print("Motivo 2: Div 'data-gerado-em' não encontrada")
            return True

        try:
            gerado_em = datetime.strptime(div_tag['data-gerado-em'], "%Y-%m-%dT%H:%M:%S.%f")
            return datetime.now() - gerado_em > timedelta(hours=2)
        except Exception as e:
            print(f"Motivo 3: Erro ao parsear data ({e})")
            return True
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/<arquivo>')
def servir_arquivo(arquivo):
    if arquivo not in ARQUIVOS:
        return "Arquivo não encontrado", 404

    caminho = ARQUIVOS[arquivo]

    if precisa_regenerar(caminho):
        print(f"[INFO] Arquivo {arquivo} desatualizado. Regenerando...")
        # subprocess.run(['python3', CAMINHO_GERAR])
        regen()

    return send_file(caminho)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)