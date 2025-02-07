import sys
location = sys.argv[1]
min_val = int(sys.argv[2])
max_val = int(sys.argv[3])
step = int(sys.argv[4])
if location[-1] != '/':
    location = location + '/'
with open(location + '/../collatz.tree', 'r', encoding = 'utf-8') as input_file:
    input_string = input_file.read()
    for val in range(min_val, max_val + 1, step):
        with open(location + 'collatz_' + str(val) + '.tree', 'w', encoding = 'utf-8') as output_file:
            output_file.write(input_string.replace('REPLACE_ME', str(val)))
