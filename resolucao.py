import json

def json2py(filename):
    try:
        with open(filename, "r") as file:
            data = json.loads(file.read())

    except FileNotFoundError:
        print("Error while opening file, check the filename passed as argument.")
        data = -1

    finally:
        return data

def py2json(data):
    data = json.dumps(data, indent=2, ensure_ascii=False)
    with open("saida.json", "w") as newfile:
        newfile.write(data)

def fix_name(data):
    for i in data:
        index = 0

        for element in i["name"]:
            if ord(element) == 230:
                i["name"] = change_char_at(index, i["name"], 'a')
            if ord(element) == 162:
                i["name"] = change_char_at(index, i["name"], 'c')
            if ord(element) == 248:
                i["name"] = change_char_at(index, i["name"], 'o')
            if ord(element) == 223:
                i["name"] = change_char_at(index, i["name"], 'b')

            index += 1

def change_char_at(index, old_string, new_char):
    new_string = list(old_string)
    new_string[index] = new_char
    new_string = "".join(new_string)
    return new_string
    
def fix_price(data):
    for i in data:
        if isinstance(i["price"], str):
            i["price"] = float(i["price"])

def fix_quantity(data):
    for i in data:
        if i.get("quantity", 1) == 1:
            i["quantity"] = 0

def sort(data):
    data.sort(key= lambda key_value : key_value["id"])
    data.sort(key= lambda key_value : key_value["category"])
    for i in data:
        print(i["name"])

def sum_by_category(data):
    total_sum = {}
    for i in data:
        if(not total_sum.get(i["category"])):
            total_sum[i["category"]] = 0

        for x in range(i["quantity"]):
            total_sum[i["category"]] += i["price"]

    for i in total_sum:
        total_sum[i] = round(total_sum[i], 2)
    
    return total_sum

def main():
    data = json2py("broken-database.json")
    
    if data == -1:
        return

    fix_name(data)
    fix_price(data)
    fix_quantity(data)

    py2json(data)

    sort(data)

    inventory_valuation = sum_by_category(data)
    
    print()
    print(inventory_valuation)


if __name__ == "__main__":
    main()