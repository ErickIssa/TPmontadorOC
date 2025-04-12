def RegistradorBin(reg):
    """Converte x0 até x31 para binário de 5 bits."""
    if reg.startswith("x") and reg[1:].isdigit():
        num = int(reg[1:])
        if 0 <= num <= 31:
            return format(num, "05b")
    return "00000"  # valor deu errado

def IMMconversorBin(reg):
    num = int(reg[0:])
    if -2048 <= num <= 2047:
        return format(num & 0b111111111111, "012b")  # Aplica máscara de 12 bits
    else:
        raise ValueError("Número Inválido")

def substituir_instrucaoR(linha, instrucao):
    palavras = linha.replace(",", "").split()

    if palavras and palavras[0] == instrucao:
        if len(palavras) == 4:
            rd = RegistradorBin(palavras[1])
            rs1 = RegistradorBin(palavras[2])
            rs2 = RegistradorBin(palavras[3])

            if instrucao == "add":
                funct7 = "0000000"
                funct3 = "000"
                opcode = "0110011"
            elif instrucao == "sll":
                funct7 = "0000000"
                funct3 = "001"
                opcode = "0110011"
            elif instrucao == "xor":
                funct7 = "0000000"
                funct3 = "100"
                opcode = "0110011"
            else:
                return linha

            binario = f"{funct7} {rs2} {rs1} {funct3} {rd} {opcode}"
            return binario
        else:
            return linha  # return caso instru maior
    else:
        return linha

def substituir_instrucaoI(linha, instrucao):
    palavras = linha.replace(",", "").split()

    if palavras and palavras[0] == instrucao:
        if len(palavras) == 4:
            rd = RegistradorBin(palavras[1])
            rs1 = RegistradorBin(palavras[2])
            imm = IMMconversorBin(palavras[3])

            if instrucao == "addi":
                funct3 = "000"
                opcode = "0010011"
            elif instrucao == "lw":
                funct3 = "010"
                opcode = "0000011"
            else:
                return linha  

            binario = f"{imm} {rs1} {funct3} {rd} {opcode}"
            return binario
        else:
            return linha 
    else:
        return linha

def substituir_instrucaoB(linha, instrucao):
    palavras = linha.replace(",", "").split()

    if palavras and palavras[0] == instrucao:
        if len(palavras) == 4:
            rs1 = RegistradorBin(palavras[1])
            rs2 = RegistradorBin(palavras[2])
            imm = IMMconversorBin(palavras[3])

            if instrucao == "bne":
                funct3 = "001"
                opcode = "1100011"
            else:
                return linha  

            binario = f"{imm[0]} {imm[1:6]} {rs2} {rs1} {funct3} {imm[6:10]} {imm[11]} {opcode}"
            return binario
        else:
            return linha 
    else:
        return linha

def substituir_instrucaoW(linha, instrucao):
    palavras = linha.replace(",", "").replace("(", " ").replace(")", "").split()
    if palavras and palavras[0] == instrucao:
        if len(palavras) == 4:
            rd = RegistradorBin(palavras[1])
            imm = IMMconversorBin(palavras[2])
            rs1 = RegistradorBin(palavras[3])

            if instrucao == "lw":
                funct3 = "010"
                opcode = "0000011"
            else:
                return linha             
            
            binario = f"{imm} {rs1} {funct3} {rd} {opcode}"
            return binario
        else:
            return linha 
    else:
        return linha
    
def substituir_instrucaoS(linha, instrucao):
    palavras = linha.replace(",", "").replace("(", " ").replace(")", "").split()
    if palavras and palavras[0] == instrucao:
        if len(palavras) == 4:
            rs2 = RegistradorBin(palavras[1])
            imm = IMMconversorBin(palavras[2])
            rs1 = RegistradorBin(palavras[3])

            if instrucao == "sw":
                funct3 = "010"
                opcode = "0100011"
            else:
                return linha
            
            binario = f"{imm[0:7]} {rs2} {rs1} {funct3} {imm[7:12]} {opcode}"
            return binario
        else:
            return linha
    else:
        return linha

nome_arquivo = "programa.asm"

try:
    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            linha = substituir_instrucaoR(linha, "add")
            linha = substituir_instrucaoR(linha, "sll")
            linha = substituir_instrucaoR(linha, "xor")
            linha = substituir_instrucaoI(linha, "addi")
            linha = substituir_instrucaoB(linha, "bne")
            linha = substituir_instrucaoW(linha, "lw")
            linha = substituir_instrucaoS(linha, "sw")
            print(linha)

except FileNotFoundError:
    print(f"Arquivo '{nome_arquivo}' não encontrado.")
