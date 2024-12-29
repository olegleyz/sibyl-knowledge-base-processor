import textwrap

# Function to wrap long strings in the dictionary
def print_json_pretty(d, width=150):
    if type(d) != dict:
        print(textwrap.fill(f"{d}", width=width))
        return
    for key in d:
        print()
        print(f"{key}:")
        if type(d[key]) != dict:
            print(textwrap.fill(f"{d[key]}", width=width))
            print()
        else:
            for k in d[key]:
                print(textwrap.fill(f"{k}: {d[key][k]}", width=width))
                print()

def save_dict_to_file(dict_to_save, filename):
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(dict_to_save, json_file, ensure_ascii=False, indent=4)
