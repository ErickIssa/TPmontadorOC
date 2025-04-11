def registrador_para_bin(reg):
    """Converte x0 até x31 para binário de 5 bits."""
    if reg.startswith("x") and reg[1:].isdigit():
        num = int(reg[1:])
        if 0 <= num <= 31:
            return format(num, "05b")
    return "00000"  # valor default caso inválido

def IMM_registrador_para_bin(reg):
        num = int(reg[0:])
        if 0 <= num <= 50:
            return format(num, "012b")
    # valor default caso inválido

def substituir_instrucaoR(linha, instrucao):
    palavras = linha.replace(",", "").split()

    if palavras and palavras[0] == instrucao:
        if len(palavras) == 4:
            rd = registrador_para_bin(palavras[1])
            rs1 = registrador_para_bin(palavras[2])
            rs2 = registrador_para_bin(palavras[3])

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
                return linha  # instrução não suportada

            binario = f"{funct7} {rs2} {rs1} {funct3} {rd} {opcode}"
            return binario
        else:
            return linha  # formato inesperado
    else:
        return linha  # instrução não corresponde

def substituir_instrucaoI(linha, instrucao):
    palavras = linha.replace(",", "").split()

    if palavras and palavras[0] == instrucao:
        if len(palavras) == 4:
            rd = registrador_para_bin(palavras[1])
            rs1 = registrador_para_bin(palavras[2])
            imm = IMM_registrador_para_bin(palavras[3])

            if instrucao == "addi":
                funct3 = "000"
                opcode = "0010011"
            else:
                return linha  # instrução não suportada

            binario = f"{imm} {rs1} {funct3} {rd} {opcode}"
            return binario
        else:
            return linha  # formato inesperado
    else:
        return linha  # instrução não corresponde


nome_arquivo = "programa.asm"

try:
    with open(nome_arquivo, "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()

            # Apenas substitui 'add' por binário
            linha = substituir_instrucaoR(linha, "add")
            linha = substituir_instrucaoR(linha, "sll")
            linha = substituir_instrucaoR(linha, "xor")
            linha = substituir_instrucaoI(linha, "addi")
            print(linha)

except FileNotFoundError:
    print(f"Arquivo '{nome_arquivo}' não encontrado.")
