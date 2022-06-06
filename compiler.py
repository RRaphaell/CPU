import argparse
from typing import List

instructions = {
    "Add": "00000000",
    "Sub": "00000001",
    "Mult": "00000010",
    "Div": "00000011",
    "Or": "00000100",
    "Xor": "00000101",
    "And": "00000110",
    "Not": "00000111",
    "Equal": "00001000",
    "Rem": "00001001",
    "Write": "00001010",
    "Jump": "0001011",
    "Jump1": "00001100",
    "Jump0": "00001101"
}

registers = {
    "A": "00000000",
    "B": "00000001",
    "C": "00000010",
    "D": "00000011",
    "E": "00000100",
    "RV": "00000101",
    "SP": "00000110",
    "PC": "00000111",
    "DDR": "00001000",
    "PORT": "00001001",
    "INPUT": "00001010",
    "UPDATE": "00001011",
    "PRESCALER2": "00001100",
    "PRESCALER1": "00001101",
    "MASK": "00001110"
}

operands = {
    "number": "0000",
    "#": "0001",
    "?": "0001",
    "!": "0010",
    "/": "0011"
}


def encode_instruction(splitted: List[str]) -> str:
    res = instructions[splitted[0]]
    just_check = False

    for i in range(1, len(splitted)):
        if splitted[0] == "Write" and i == 2:
            operands["#"] = "0000"
            just_check = True
        if splitted[i][0].isnumeric():
            res += operands["number"]
        else:
            res += operands[splitted[i][0]]
        if splitted[i][0] == "#" or splitted[i][0] == "?" or splitted[i][0] == "/":
            res += registers[splitted[i][1:]]
        else:
            if splitted[i][0] == "!":
                temp = (str(bin(int(splitted[i][1:]))).split("b"))[1]
            else:
                temp = (str(bin(int(splitted[i]))).split("b"))[1]
            if len(temp) < 8:
                padding = [0] * (8 - len(temp))
                res += ''.join([str(elem) for elem in padding])
            res += temp
        if just_check:
            operands["#"] = "0001"
            just_check = False
    return res


def convert(input_file_name: str, output_file_name: str) -> None:
    file = open(output_file_name, "w")
    file.write("v3.0 hex words addressed\n")

    with open(input_file_name, 'r') as reader:
        for inputStr in reader:
            splitted = inputStr.split()
            binary_instruction = ""
            try:
                binary_instruction = encode_instruction(splitted)
                if splitted[0] == "Jump" or splitted[0] == "Jump1" or splitted[0] == "Jump0":
                    padding = [0] * 12
                    res = ''.join([str(elem) for elem in padding])
                    binary_instruction += res
            except:
                print("There are no similar instructions")

            file.write(str(hex(int(binary_instruction, 2))).split("x")[1] + " ")

    file.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("InputFile", help="name of the input file")
    parser.add_argument("OutputFile", help="name of the output file", nargs='?', default="instructions.txt")
    args = parser.parse_args()

    convert(args.InputFile, args.OutputFile)


if __name__ == "__main__":
    main()
