def Read_File(file_path):
    labels = {}
    counter = 0
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.endswith(":"):
                label_name = line[:-1]
                labels[label_name] = counter
            elif line:
                counter += 4
    counter = 0
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.endswith(":"):
                continue
            elif line:
                try:
                    machine_code = Assembler(line, labels, counter)
                    print(f"Instruction: {line} -> Machine Code: {machine_code}")
                except ValueError as e:
                    print(f"Error in instruction '{line}': {e}")
                except IndexError as e:
                    print(f"Error in instruction '{line}': Invalid format. Expected more parts.")
                counter += 4

# Register mapping
registers = {
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011", "tp": "00100",
    "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "s1": "01001",
    "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101", "a4": "01110",
    "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011",
    "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000",
    "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100", "t4": "11101",
    "t5": "11110", "t6": "11111"
}

# Opcode mapping
opcode = {
    "add": "0110011", "sub": "0110011", "slt": "0110011", "or": "0110011",
    "and": "0110011", "lw": "0000011", "sw": "0100011", "beq": "1100011",
    "bne": "1100011", "jal": "1101111", "jalr": "1100111", "addi": "0010011",
    "blt": "1100011", "srl": "0110011"
}

# Funct3 mapping
funct3 = {
    "add": "000", "sub": "000", "slt": "010", "or": "110", "and": "111",
    "lw": "010", "sw": "010", "beq": "000", "bne": "001", "jalr": "000", 
    "addi": "000", "blt": "100", "srl": "101"
}

# Funct7 mapping
funct7 = {
    "add": "0000000", "sub": "0100000", "slt": "0000000", "or": "0000000", 
    "and": "0000000", "srl": "0000000"
}

def Bin_Converter_Pos(imm_val, bits):
    imm_val = int(imm_val)
    if imm_val < -2**(bits-1) or imm_val > 2**(bits-1)-1:
        raise ValueError("OUT OF RANGE IMMEDIATE VALUE")
    if imm_val < 0:
        imm_val = (2**bits) + imm_val
    bin_dig = []
    if imm_val == 0:
        bin_dig = ["0"] * bits
    else:
        while imm_val > 0:
            rem = imm_val % 2
            bin_dig.insert(0, str(rem))
            imm_val = imm_val // 2
    while len(bin_dig) < bits:
        bin_dig.insert(0, "0")
    bin_str = "".join(bin_dig)
    return bin_str

def Bin_Converter_Neg(imm_val, bits):
    imm_val = int(imm_val)
    power = 2**bits
    imm_val = power + imm_val
    bin_dig = []
    for i in range(bits):
        rem = imm_val % 2
        bin_dig.insert(0, str(rem))
        imm_val = imm_val // 2
    bin_str = "".join(bin_dig)
    return bin_str

def Assembler(instruction, labels, counter):
    instr_parts = instruction.replace(" ", ",").split(",")
    instr = instr_parts[0]
    # R-type instructions
    if instr in ["add", "sub", "and", "or", "slt", "srl"]:
        if len(instr_parts) < 4:
            raise ValueError(f"Invalid format for {instr}. Expected 4 parts, got {len(instr_parts)}")
        rd, rs1, rs2 = instr_parts[1], instr_parts[2], instr_parts[3]
        if rd not in registers or rs1 not in registers or rs2 not in registers:
            raise ValueError("INVALID REGISTER NAME")
        return funct7[instr] + registers[rs2] + registers[rs1] + funct3[instr] + registers[rd] + opcode[instr]
    else:
        raise ValueError(f"UNSUPPORTED INSTRUCTION: {instr}")


file_path = "fueh.txt"
Read_File(file_path)
