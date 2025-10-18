
data = open("xy.txt").read()

x_collector = 0
y_collector = 0

for index, line in enumerate(data.splitlines()):    
    chunks = line.split("y")
    
    y_index = index + 1
    x_index = 0
    
    print(index, line)
    
    for chunk in chunks:
        x_index += len(chunk)
        # print(chunk, x_index, y_index)
        
        y_collector += y_index
    
    y_collector -= y_index

print(y_collector)

for index, line in enumerate(data.splitlines()):
    # print(index, line)
    
    y_index = index + 1
    x_index = 0
    x_indexs = 0
    
    while "x" in line:
        index_x = line.index("x")
        
        x_index = index_x + 1
        print(line, x_index, x_indexs)
        line = line[x_index:]
        
        x_collector += x_index + x_indexs
        x_indexs += index_x + 1
        
        //

print(x_collector)

print(x_collector + y_collector)
