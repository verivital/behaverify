

def make_trees():
    modes = (
        'float',
        'fixed',
        'fixed_direct'
    )
    values = {
        100 : ((10, 32), (7, 35)),
        # 128 : ((16, 32), (12, 48)),
        # 200 : ((16, 64), (32, 64)),
        512 : ((64, 128),)
    }
    networks = (
        # '0.98 acc/7_11_1__16_3.onnx',
        '1.0 acc/7_11_1__20_3.onnx',
        # '1.0 acc/7_11_1__24_3.onnx',
        # '1.0 acc/7_11_1__32_3.onnx',
        '1.0 acc/7_11_1__64_1.onnx',
    )
    with open('ANSRn_7_11_1.tree', 'r', encoding = 'utf-8') as input_file:
        template = input_file.read()
    for network in networks:
        for mode in modes:
            for total in values:
                for (int_part, float_part) in values[total]:
                    new_tree = template.replace('REPLACE_MODE', mode).replace('REPLACE_TOTAL', str(total)).replace('REPLACE_INT', str(int_part)).replace('REPLACE_FLOAT', str(float_part)).replace('REPLACE_SOURCE', '\'../' + network + '\'')
                    with open('./tree/network_' + mode + '__' + str(total) + '_' + str(int_part) + '_' + str(float_part) + '__' + network.replace(' ', '_').replace('/', '_').replace('.', '_', 1).replace('.onnx', '.tree'), 'w', encoding = 'utf-8') as output_file:
                        output_file.write(new_tree)
                    if mode == 'float':
                        break

if __name__ == '__main__':
    make_trees()
