import json

with open ('dados.json', encoding='utf-8') as json_file:
    dados = json.load(json_file)

disciplinas = dados["disciplinas"]
disponibilidade_prof = dados["disponibilidade_prof"]
salas = dados["salas"]
bloqueios_salas = dados["bloqueios_salas"]
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
print (lista_aulas)
def validacao(aula, horario, sala, atribuicao):

    prof = aula["prof"]
    disciplinaAula = aula["disciplina"]

    if horario not in disponibilidade_prof[prof]:
        return False;

    if aula["tipo"] == "Laboratorio" and salas[sala] != "Laboratorio":
        return False;

    if horario in bloqueios_salas.get(sala, []):
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

def distribuir_aulas(indice, atribuicao):
    if indice == len(lista_aulas):
        return True

    aula = lista_aulas[indice]

    for horario in horarios_possiveis:
        for sala in salas_possiveis:
            if validacao(aula, horario, sala, atribuicao):
                atribuicao.append({
                    "disciplina": aula["disciplina"],
                    "id_aula": aula["id_aula"],
                    "prof": aula["prof"],
                    "tipo": aula["tipo"],
                    "horario": horario,
                    "sala": sala
                })

                if distribuir_aulas(indice + 1, atribuicao):
                    return True

