data = open("walk.txt", encoding="utf-8").read()

map_matrix = [list(line) for line in data.splitlines()]

start_char = "→"
start_char_pos = None

acceptance_map = {
    "→": (1, 0),
    "┘": {
        str((1, 0)): (0, -1),
        str((0, 1)): (-1, 0)
        },
    "└": {
        str((-1, 0)): (0, -1),
        str((0, 1)): (1, 0)
        },
    "┌": {
        str((-1, 0)): (0, 1),
        str((0, -1)): (1, 0)
        },
    "┐": {
        str((1, 0)): (0, 1),
        str((0, -1)): (-1, 0)
        },
    "─": None,
    "│": None
}

cur_pos = ()
counter = 0

for row_index, row in enumerate(map_matrix):
    for col_index, char in enumerate(row):
        if char == start_char:
            start_char_pos = (col_index, row_index)
            cur_pos = start_char_pos
            break
    if start_char_pos:
        break

def get_at(x, y):
    return map_matrix[y][x]

last_acceptance = None
step = 0

while True:
    step += 1
    cur_char = get_at(cur_pos[0], cur_pos[1])
    
    acceptance = acceptance_map[cur_char]
    
    if (acceptance is None):
        acceptance = last_acceptance

    if (type(acceptance) is dict):
        acceptance = acceptance[str(last_acceptance)]

    last_acceptance = acceptance

    new_pos = (cur_pos[0] + acceptance[0], cur_pos[1] + acceptance[1])
    new_char = get_at(new_pos[0], new_pos[1])

    print(cur_pos, "+", acceptance, "=", new_pos, ":", cur_char, " to ",new_char)

    cur_pos = new_pos
    
    if (new_char == start_char):
        print("Returned after", step, "steps")
        break
    
    if (step > 380000):
        break