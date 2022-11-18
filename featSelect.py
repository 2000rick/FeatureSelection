# Load data
data = []
dataFile = open('CS170_Small_Data__96.txt', 'r')
for y in dataFile:
    entry = [float(num) for num in y.split()] #one row of data
    data.append(entry)
dataFile.close()

for element in data:
    print(element)

print(f'Number of rows: {len(data)}')
print(f'Number of features: {len(data[0])-1}')
