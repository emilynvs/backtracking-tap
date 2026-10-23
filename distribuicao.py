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

    # cria uma forma de chamar todas as variáveis da validação
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
                # passa por meio de recursividade a próxima aula
                if distribuir_aulas(indice + 1, atribuicao):
                    return True

                # parte do backtracking que ocorre caso não passe na validacao
                atribuicao.pop()

    return False


def mostrar_grade(atribuicao):

    for horario in horarios_possiveis:
        # aqui é uma forma de fazer mini listas criadas por horário, entao mostra as aulas que tem por horário
        # se ta no h1 mostra as aulas que tem no h1
        aulas_horario = [
            aula for aula in atribuicao
            if aula["horario"] == horario
        ]

        if aulas_horario:
            print(f"\n{horario.upper()}:")

            # Organiza as aulas pelo nome da sala
            aulas_horario.sort(key=lambda aula: aula["sala"])

            for aula in aulas_horario:
                print(
                    f"  Sala: {aula['sala']:<6} | "
                    f"Disciplina: {aula['disciplina']:<25} | "
                    f"Professor: {aula['prof']} | "
                    f"Aula {aula['id_aula']}"
                )

    print("\nTotal de aulas alocadas:", len(atribuicao))

atribuicao = []
resultado = distribuir_aulas(0, atribuicao)

if resultado:
    mostrar_grade(atribuicao)
else:
    print('Não consegui encontrar uma solução')
