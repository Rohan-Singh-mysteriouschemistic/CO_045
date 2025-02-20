registers = {
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011", "tp": "00100",
    "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "s1": "01001",
    "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101", "a4": "01110",
    "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011",
    "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000",
    "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100", "t4": "11101",
    "t5": "11110", "t6": "11111"
}

opcode = {
    "add": "0110011", "sub": "0110011", "slt": "0110011", "or": "0110011",
    "and": "0110011", "lw": "0000011", "sw": "0100011", "beq": "1100011",
    "bne": "1100011", "jal": "1101111", "jalr": "1100111", "addi": "0010011",
    "blt": "1100011", "srl": "0110011"
}

funct3 = {
    "add": "000", "sub": "000", "slt": "010", "or": "110", "and": "111",
    "lw": "010", "sw": "010", "beq": "000", "bne": "001", "jalr": "000", 
    "addi": "000", "blt": "100", "srl": "101"
}

funct7 = {
    "add": "0000000", "sub": "0100000", "slt": "0000000", "or": "0000000", 
    "and": "0000000", "srl": "0000000"
}

def immToBin(value, bits):
    value = int(value)
    if value < -2**(bits - 1) or value > 2**(bits - 1) - 1:
        raise ValueError(f"Value {value} out of range for {bits} bits")
    if value < 0:
        value = (2**bits) + value 
    return bin(value)[2:].zfill(bits) 

def assemble(instruction, labels, pc, output_file):
    parts = instruction.replace(",", " ").split()
    instr = parts[0]
    
    try: 

        if instr in ["add", "sub", "and", "or", "slt", "srl"]: # R-type
            if len(parts) != 4:
                raise ValueError(f"Instruction length error at pc = {pc}")
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            if rd not in registers or rs1 not in registers or rs2 not in registers:
                raise ValueError(f"Invalid register at pc = {pc}")
            return funct7[instr] + registers[rs2] + registers[rs1] + funct3[instr] + registers[rd] + opcode[instr]
            
        elif instr == "addi" or instr == "jalr": # I-type addi and jalr
            if len(parts) != 4:
                raise ValueError(f"Instruction length error at pc = {pc}")
            rd, rs1, imm = parts[1], parts[2], int(parts[3])
            if rd not in registers or rs1 not in registers:
                raise ValueError(f"Invalid register at pc = {pc}")
            return immToBin(imm, 12) + registers[rs1] + funct3[instr] + registers[rd] + opcode[instr]
        elif instr == "lw": #I-type lw
            parts = instruction.replace(",", " ").replace("(", " ").replace(")", "").split()
            if len(parts) != 4:
                raise ValueError(f"Instruction length error at pc = {pc}")
            rd, offset, rs1 = parts[1], int(parts[2]), parts[3]
            if rs1 not in registers or rd not in registers:
                raise ValueError(f"Invalid register at pc = {pc}")
            imm = immToBin(offset, 12)
            return imm + registers[rs1] + funct3[instr] + registers[rd] + opcode[instr]
        

        elif instr == "sw": # S-type
            parts = instruction.replace(",", " ").replace("(", " ").replace(")", "").split()
            if len(parts) != 4:
                raise ValueError(f"Instruction length error at pc = {pc}")
            rs2, offset, rs1 = parts[1], int(parts[2]), parts[3]
            if rs1 not in registers or rs2 not in registers:
                raise ValueError(f"Invalid register at pc = {pc}")
            imm = immToBin(offset, 12)
            return imm[:7] + registers[rs2] + registers[rs1] + funct3[instr] + imm[7:] + opcode[instr]
        elif instr in ["beq", "bne", "blt"]: # B-type
            if len(parts) != 4:
                raise ValueError(f"Instruction length error at pc = {pc}")
            rs1, rs2, label = parts[1], parts[2], parts[3]
            if rs1 not in registers or rs2 not in registers:
                raise ValueError(f"Invalid register at pc = {pc}")
            if label in labels:
                imm = (labels[label] - pc) 
            else:
                try:
                    imm = int(label) 
                except:
                  raise ValueError(f"Label not found at pc = {pc}")  
            imm_bin = immToBin(imm, 13)
            return imm_bin[0] + imm_bin[2:8] + registers[rs2] + registers[rs1] + funct3[instr] + imm_bin[8:12] + imm_bin[1] + opcode[instr]
        
        elif instr == "jal": # J-type
            if len(parts) != 3:
                raise ValueError(f"Instruction length error at pc = {pc}")
            rd, label = parts[1], parts[2]
            if rd not in registers:
                raise ValueError(f"Invalid register at pc = {pc}")
            if label in labels:
                imm = (labels[label] - pc) 
            else:
                raise ValueError(f"Label {label} not found at pc = {pc}")
            imm_bin = immToBin(imm, 21)
            return imm_bin[0] + imm_bin[1:9] + imm_bin[9] + imm_bin[10:20] + registers[rd] + opcode[instr]
        
        else:
            raise ValueError(f"Unsupported instruction at pc = {pc}")
    except ValueError as err:
        with open(output_file,"w") as file:
            return f"{err}"
        
