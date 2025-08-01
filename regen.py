from services.gerator import gerar_mapa_por_rsrp, gerar_mapa_por_rsrq
from services.painel_interativo import classificar_linhas
from clear import limpar_csv_zerados
def regen():
    limpar_csv_zerados()
    # Gera mapas interativos
    gerar_mapa_por_rsrp(csv_entrada='saida.csv', saida_html='mapa_rsrp.html')
    gerar_mapa_por_rsrq(csv_entrada='saida.csv', saida_html='mapa_rsrq.html')
    classificar_linhas()
    print("✅ Mapas gerados com sucesso!")

# regen()