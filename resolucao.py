#############################
# PROJETO CLASSIFICATORIO PARA O PROCESSO SELETIVO ROCKY TI
# AUTOR: GUILHERME MILANI DE OLIVEIRA
#############################

import json

#funcao que converte um arquivo json em um dicionario no python
def json2py(filename):
    try:
        with open(filename, "r") as file:
            data = json.loads(file.read())

    except FileNotFoundError:
        print("Error while opening file, check the filename passed as argument.")
        data = -1

    finally:
        return data

#convertendo os dados inseridos para um arquivo json com indentacao similar ao "broken-database"
def py2json(data):
    data = json.dumps(data, indent=2, ensure_ascii=False) #ensure_ascii necessario para salvar acentuacao
    with open("saida.json", "w") as newfile:
        newfile.write(data)

#funcao para corrigir os nomes corrompidos no banco de dados
def fix_name(data):
    for entry in data: #para cada entrada no banco

        index = 0
        for character in entry["name"]: #verificar cada caracter do campo destinado ao nome

            if ord(character) == 230: #se houver uma ligadura 'ae' no lugar de onde deveria ter um 'a'
                entry["name"] = change_char_at(index, entry["name"], 'a')

            if ord(character) == 162: #se houver um simobolo de cents no lugar de 'c'
                entry["name"] = change_char_at(index, entry["name"], 'c')

            if ord(character) == 248: #se houver um 'o' cortado no lugar de um 'o' comum
                entry["name"] = change_char_at(index, entry["name"], 'o')

            if ord(character) == 223: #se houver um beta no lugar de 'b'
                entry["name"] = change_char_at(index, entry["name"], 'b')

            index += 1

#funcao utilizada para substituir um caracter especifico numa string
def change_char_at(index, old_string, new_char):
    new_string = list(old_string) #transformamos a string passada em uma lista de char
    new_string[index] = new_char #modificamos o char na posicao selecionada para o novo caracter desejado
    new_string = "".join(new_string) #juntamos a lista numa string com o metodo join usando um separador vazio
    return new_string

#repara os precos transformados em string
def fix_price(data):
    for entry in data:
        if isinstance(entry["price"], str): #se o valor contido no campo price for do tipo string
            entry["price"] = float(entry["price"])

#repara as entradas sem o campo quantidade
def fix_quantity(data):
    for entry in data: 
        if entry.get("quantity", 1) == 1: #o metodo get ira retornar 1 caso nao houver o campo quantity
            entry["quantity"] = 0

#funcao para ordenar o db conforme ordem especificada e imprimir os nomes nessa nova ordem
def sort(data):
    data.sort(key= lambda key_value : key_value["id"]) #funcao lambda para utilizar o valor "id" na ordenacao 
    data.sort(key= lambda key_value : key_value["category"]) #a ultima ordenacao realizada eh a que recebe a preferencia
    for i in data:
        print(i["name"])

#soma do valor total em estoque por categoria
def sum_by_category(data):
    total_sum = {} #criando um dicionario para adicionar a quantidade total em cada categoria
    for entry in data:
        if(not total_sum.get(entry["category"])): #outra maneira de verificar se uma determinada key existe num dicionario
            total_sum[entry["category"]] = 0  #criando o campo para a categoria

        for x in range(entry["quantity"]): #usando um for para somar todos os produtos em estoque
            total_sum[entry["category"]] += entry["price"] #mas uma multiplicacao funcionaria da mesma maneira

    for entry in total_sum: #arredondando todos os valores
        total_sum[entry] = round(total_sum[entry], 2)
    
    return total_sum

def main():
    data = json2py("broken-database.json")
    
    if data == -1: #encerrar o programa caso o banco de dados nao seja lido corretamente
        return

    fix_name(data)
    fix_price(data)
    fix_quantity(data)

    py2json(data) #salvar o banco corrigido

    sort(data) #ordenar e imprimir

    inventory_valuation = sum_by_category(data)
    
    print()
    print(inventory_valuation) #imprimir a avaliacao de estoque

#caso o codigo seja importado em outro modulo a main devera ser chamada explicitamente
if __name__ == "__main__":
    main()