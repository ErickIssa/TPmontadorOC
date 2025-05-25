def RegistradorBin(reg):
    if reg.startswith("x") and reg[1:].isdigit():
        num = int(reg[1:])
        if 0 <= num <= 31:
            return format(num, "05b")
    return "00000"

def IMMconversorBin(reg):
    num = int(reg[0:])
    if -2048 <= num <= 2047:
        return format(num & 0b111111111111, "012b")
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
                funct7 = "0000000"; funct3 = "000"; opcode = "0110011"
            elif instrucao == "sll":
                funct7 = "0000000"; funct3 = "001"; opcode = "0110011"
            elif instrucao == "xor":
                funct7 = "0000000"; funct3 = "100"; opcode = "0110011"
            elif instrucao == "sub":
                funct7 = "0100000"; funct3 = "000"; opcode = "0110011"
            elif instrucao == "and":
                funct7 = "0000000"; funct3 = "111"; opcode = "0110011"
            elif instrucao == "or":
                funct7 = "0000000"; funct3 = "110"; opcode = "0110011"
            elif instrucao == "srl":
                funct7 = "0000000"; funct3 = "101"; opcode = "0110011"
            else:
                return linha
            return f"{funct7}{rs2}{rs1}{funct3}{rd}{opcode}"
    return linha

def substituir_instrucaoI(linha, instrucao):
    palavras = linha.replace(",", "").split()
    if palavras and palavras[0] == instrucao and len(palavras) == 4:
        rd = RegistradorBin(palavras[1])
        rs1 = RegistradorBin(palavras[2])
        imm = IMMconversorBin(palavras[3])
        if instrucao == "addi":
            funct3 = "000"; opcode = "0010011"
        elif instrucao == "andi":
            funct3 = "111"; opcode = "0010011"
        elif instrucao == "ori":
            funct3 = "110"; opcode = "0010011"
        else:
            return linha
        return f"{imm}{rs1}{funct3}{rd}{opcode}"
    return linha

def substituir_instrucaoB(linha, instrucao):
    palavras = linha.replace(",", "").split()
    if palavras and palavras[0] == instrucao and len(palavras) == 4:
        rs1 = RegistradorBin(palavras[1])
        rs2 = RegistradorBin(palavras[2])
        imm = IMMconversorBin(palavras[3])
        if instrucao == "bne":
            funct3 = "001"; opcode = "1100011"
        elif instrucao == "beq":
            funct3 = "000"; opcode = "1100011"
        else:
            return linha
        return f"{imm[0]}{imm[2:8]}{rs2}{rs1}{funct3}{imm[8:12]}{imm[1]}{opcode}"
    return linha

def substituir_instrucaoW(linha, instrucao):
    palavras = linha.replace(",", "").replace("(", " ").replace(")", "").split()
    if palavras and palavras[0] == instrucao and len(palavras) == 4:
        rd = RegistradorBin(palavras[1])
        imm = IMMconversorBin(palavras[2])
        rs1 = RegistradorBin(palavras[3])
        if instrucao == "lw":
            funct3 = "010"; opcode = "0000011"
        elif instrucao == "lb":
            funct3 = "000"; opcode = "0000011"
        elif instrucao == "lh":
            funct3 = "001"; opcode = "0000011"
        else:
            return linha
        return f"{imm}{rs1}{funct3}{rd}{opcode}"
    return linha

def substituir_instrucaoS(linha, instrucao):
    palavras = linha.replace(",", "").replace("(", " ").replace(")", "").split()
    if palavras and palavras[0] == instrucao and len(palavras) == 4:
        rs2 = RegistradorBin(palavras[1])
        imm = IMMconversorBin(palavras[2])
        rs1 = RegistradorBin(palavras[3])
        if instrucao == "sw":
            funct3 = "010"; opcode = "0100011"
        elif instrucao == "sb":
            funct3 = "000"; opcode = "0100011"
        elif instrucao == "sh":
            funct3 = "001"; opcode = "0100011"
        else:
            return linha
        return f"{imm[0:7]}{rs2}{rs1}{funct3}{imm[7:12]}{opcode}"
    return linha

nome_arquivo = "programa.asm"
modo_saida = input("Digite o respectivo número para o tipo de saída desejado (1)Arquivo de texto / (2)saída no terminal: ").strip().lower()

saida_linhas = []

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
            linha = substituir_instrucaoR(linha, "sub")
            linha = substituir_instrucaoR(linha, "and")
            linha = substituir_instrucaoR(linha, "or")
            linha = substituir_instrucaoI(linha, "andi")
            linha = substituir_instrucaoI(linha, "ori")
            linha = substituir_instrucaoW(linha, "lb")
            linha = substituir_instrucaoW(linha, "lh")
            linha = substituir_instrucaoS(linha, "sb")
            linha = substituir_instrucaoS(linha, "sh")
            linha = substituir_instrucaoR(linha, "srl")
            linha = substituir_instrucaoB(linha, "beq")
            
            saida_linhas.append(linha)

    if modo_saida == "1":
        with open("saida.txt", "w") as arquivo_saida:
            for linha in saida_linhas:
                arquivo_saida.write(linha + "\n")
        print("Saída salva em 'saida.txt'")
    else: #se digitar errado ainda sai no terminal
        print("\n____Saída no Terminal____")
        for linha in saida_linhas:
            print(linha)

except FileNotFoundError:
    print(f"Arquivo '{nome_arquivo}' não encontrado.")
