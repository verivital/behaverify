import argparse

def edit_constants(input_path, new_constants):
    with open(input_path, 'r',  encoding = 'utf-8') as input_file:
        contents = input_file.read()
    (preamble, postamble) = contents.split('constants {', 1)
    postamble = postamble.split('} end_constants', 1)[1]
    with open(input_path, 'w', encoding = 'utf-8') as output_file:
        output_file.write(preamble + new_constants + postamble)
    return


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('input_path')
    arg_parser.add_argument('new_constants')
    args = arg_parser.parse_args()
    edit_constants(args.input_path, args.new_constants)
