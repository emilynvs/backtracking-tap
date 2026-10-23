import json

with open ('dados.json', encoding='utf-8') as json_file:
    dados = json.load(json_file)

disciplinas = dados["disciplinas"]
disponibilidade_prof = dados["disponibilidade_prof"]
salas = dados["salas"]
