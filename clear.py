import pandas as pd
import os

def limpar_csv_zerados(arquivo_entrada='network_data.csv', arquivo_saida='saida.csv'):
    if not os.path.exists(arquivo_entrada):
        print(f"❌ Arquivo de entrada '{arquivo_entrada}' não encontrado.")
        return

    df = pd.read_csv(arquivo_entrada)

    # Filtra as linhas com lat/lon != 0
    df_filtrado = df[(df['latitude'] != 0.0) & (df['longitude'] != 0.0)]

    if df_filtrado.empty:
        print("⚠️ Nenhuma linha válida encontrada.")
        return

    # Append no arquivo de saída, ou cria se não existir
    if os.path.exists(arquivo_saida):
        df_filtrado.to_csv(arquivo_saida, mode='a', header=False, index=False)
    else:
        df_filtrado.to_csv(arquivo_saida, index=False)

    # Remove as linhas já usadas do original
    df_restante = df[~df.index.isin(df_filtrado.index)]
    df_restante.to_csv(arquivo_entrada, index=False)

    print(f"✅ {len(df_filtrado)} linhas adicionadas a '{arquivo_saida}' e removidas de '{arquivo_entrada}'.")

if __name__ == "__main__":
    limpar_csv_zerados()
