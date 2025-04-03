memory = {}
registers = [0]*32
registers[2] = 380
import sys
input_file, output_file = sys.argv[1], sys.argv[2]
with open(output_file,"w+") as output:
    pass

def print_registers(pc):
    with open(output_file,"a+") as output:
        lines = f"0b{format(pc & 0xFFFFFFFF, '032b')} " + "0b" + " 0b".join( format(reg & 0xFFFFFFFF, '032b') for reg in registers)
        output.writelines(lines)
        output.write("\n")
    
def print_memory(memory: dict):
    with open(output_file,"a+") as output:
        base_address = 0x00010000
        
        for i in range(32):  # print 32 memory locations
            key = decimal_to_hex(base_address + (i * 4))
            line = f"0x{decimal_to_hex(base_address + (i * 4))}:" + "0b" + format(memory.get(str(key), 0) & 0xFFFFFFFF, '032b')
            output.writelines(line)
            output.write("\n")
    
def decimal_to_hex(decimal_number):
    return format(decimal_number & 0xFFFFFFFF, '08X')  #8-digit hex output


def bin_to_decimal(binary_str):
    sign_bit = binary_str[0]

    if sign_bit == "0":  
        return int(binary_str, 2)  
    else:
        inverted_bin = ''.join('1' if b == '0' else '0' for b in binary_str)  
        decimal_value = int(inverted_bin, 2) + 1  
        return -decimal_value

def bin_to_decimal_u(binary_str):
    return int(binary_str, 2)

def imm_extend(binary_str):   #extends immediate and converts to decimal value 
    x = len(binary_str) 
    if x > 32:
        raise ValueError("Input binary string exceeds 32 bits")

    sign_bit = binary_str[0]  
    extended_bits = sign_bit * (32 - x)  
    return bin_to_decimal(extended_bits + binary_str)

# R-type Instruction Class
class Rtype:
    def __init__(self, instruction):
        self.instr = instruction
        self.parts = {
            "opcode": self.instr[25:32],
            "rd": bin_to_decimal_u(self.instr[20:25]),
            "funct3": self.instr[17:20],
            "rs1": bin_to_decimal_u(self.instr[12:17]),
            "rs2": bin_to_decimal_u(self.instr[7:12]),
            "funct7": self.instr[0:7]
        }
        
    def add(self):
        registers[self.parts["rd"]] = registers[self.parts["rs1"]] + registers[self.parts["rs2"]]
    
    def sub(self):
        registers[self.parts["rd"]] = registers[self.parts["rs1"]] - registers[self.parts["rs2"]]
    
    def slt(self):
        if registers[self.parts["rs1"]] < registers[self.parts["rs2"]]:
            registers[self.parts["rd"]] = 1
    
    def srl(self):
        shift = registers[self.parts["rs2"]] & 0x1F
        registers[self.parts["rd"]] = registers[self.parts["rs1"]] >> shift
    
    def or_operation(self):
        registers[self.parts["rd"]] = registers[self.parts["rs1"]] | registers[self.parts["rs2"]]
    def and_operation(self):
        registers[self.parts["rd"]] = registers[self.parts["rs1"]] & registers[self.parts["rs2"]]

# I-type Instruction Class
class Itype:
    def __init__(self, instruction):
        self.instr = instruction
        self.parts = {
            "opcode": self.instr[25:32],
            "rd": bin_to_decimal_u(self.instr[20:25]),
            "funct3": self.instr[17:20],
            "rs1": bin_to_decimal_u(self.instr[12:17]),
            "imm": self.instr[0:12]
        }
        
    def addi(self):
        registers[self.parts["rd"]] = registers[self.parts["rs1"]] + imm_extend(self.parts["imm"])
    
    def jalr(self, pc):
        registers[self.parts["rd"]] = pc + 4
        if self.parts["rs1"]!=0:
            new_pc = registers[self.parts["rs1"]] + imm_extend(self.parts["imm"])
        else:
            new_pc = imm_extend(self.parts["imm"])
        return new_pc & ~1  # Ensures even jump
    
    def lw(self):
        address = decimal_to_hex(registers[self.parts["rs1"]] + imm_extend(self.parts["imm"]))
        registers[self.parts["rd"]] = memory.get(address, 0)

# S-type Instruction Class
class Stype:
    def __init__(self, instruction):
        self.instr = instruction
        self.parts = {
            "opcode": self.instr[25:32],
            "funct3": self.instr[17:20],
            "rs1": bin_to_decimal_u(self.instr[12:17]),
            "rs2": bin_to_decimal_u(self.instr[7:12]),
            "imm": self.instr[0:7] + self.instr[20:25]      
        }
        
    def sw(self):
        address = decimal_to_hex(registers[self.parts["rs1"]] + imm_extend(self.parts["imm"]))
        memory[address] = registers[self.parts["rs2"]]
