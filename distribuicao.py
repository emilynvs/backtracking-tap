import json

with open ('dados.json', encoding='utf-8') as json_file:
    dados = json.load(json_file)

disciplinas = dados["disciplinas"]
disponibilidade_prof = dados["disponibilidade_prof"]
salas = dados["salas"]
horarios_possiveis = ["h1", "h2", "h3", "h4", "h5"]

lista_aulas = []
for d in disciplinas:
    for i in range(d["aulas"]):
        lista_aulas.append({
            "disciplina": d["nome"],
            "prof": d["prof"],
            "tipo": d["tipo"],
            "id_aula": i + 1
        })
salas_possiveis = list(salas.keys())

def validacao(aula, horario, sala, atribuicao):
    print('OLHA A SALA', sala)
    prof = aula["prof"]
    disciplinaAula = aula["disciplina"]

    if horario not in disponibilidade_prof[prof]:
        return False;

    if aula["tipo"] == "Laboratorio" and salas[sala] != "Laboratorio":
        return False;

    for atribui in atribuicao:
        if atribui["horario"] == horario:
            if atribui["prof"] == prof:
                return False;
            if atribui["sala"] == sala:
                return False;

    for atribui in atribuicao:
        if atribui["disciplina"] == disciplinaAula and atribui["horario"] == horario:
            return False

    return True
