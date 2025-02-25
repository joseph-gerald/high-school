import json

lines = open("output.txt", "r", encoding="utf-8").read().split("\n")
flyttet_counter = 0

for line in lines:
    data = json.loads(line)
    
    if (len(data["recent"]) > 1):
        continue

    flyttet = data["recent"][0]["geo"].split(",")[0] not in data["address"]
    flyttet_counter += flyttet

    if (flyttet and data["birth_of_date"] != ""):
        print(f"{data['full_name']} flyttet til {data['recent'][0]['geo']}")
        with open("flyttet.txt", "a", encoding="utf-8") as f:
            f.write(data["birth_of_date"] +","+ data["recent"][0]["geo"] + "\n")
            pass

print(f"Flyttet: {flyttet_counter}", f"Total: {len(lines)}")