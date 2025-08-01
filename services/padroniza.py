import csv

# Nome do arquivo original e do novo
input_file = "teste_filtrado.csv"
output_file = "saida.csv"

# Abrir o arquivo de entrada para leitura
with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# Separar o cabeçalho dos dados
header = rows[0]
data_rows = rows[1:]

# Processar as datas
for i, row in enumerate(data_rows):
    timestamp = row[0]
    if '.' in timestamp and len(timestamp.split('.')[-1]) >= 4:
        row[0] = timestamp[:-5]  # remove os últimos 5 caracteres

# Escrever o novo CSV
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)      # escreve o cabeçalho
    writer.writerows(data_rows)  # escreve os dados processados

print("Arquivo salvo como", output_file)
