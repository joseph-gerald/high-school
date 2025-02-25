from gulesider import get_suggestions
from concurrent.futures import ThreadPoolExecutor
import json

data = open("data.csv", "r", encoding="utf-8").read()

# tlf_number,first_name,middle_name,last_name,birth_of_date,address

def handle_line(index, line):
    parsed_data = []

    for data in line.split(","):
        parsed_data.append(data)

    parsed_data = {
        "tlf_number": parsed_data[0],
        "first_name": parsed_data[1],
        "middle_name": parsed_data[2],
        "last_name": parsed_data[3],
        "full_name": f"{parsed_data[1]} {parsed_data[2]} {parsed_data[3]}".strip(),
        "birth_of_date": parsed_data[4],
        "address": parsed_data[5]
    }

    if (parsed_data["address"] == ""):
        return

    parsed_data["recent"] = get_suggestions(parsed_data["full_name"])

    if (parsed_data["recent"] == []):
        return
    
    print(index)
    with open("output.txt", "a", encoding="utf-8") as f:
        f.write(json.dumps(parsed_data) + "\n")

max_workers = 100

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = []
    for index, line in enumerate(data.split("\n")):
        if index == 0:
            continue

        if index % 100 == 0:
            parsed_data = []
            print("ADDED", index)
            
            futures.append(executor.submit(handle_line, index, line))

    for future in futures:
        future.result()

