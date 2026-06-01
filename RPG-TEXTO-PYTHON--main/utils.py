def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("Erro: Entrada inválida. Por favor, digite um número inteiro.")

def ler_texto(mensagem):
    while True:
        entrada = input(mensagem).strip()
        if entrada:  # Garante que a string não está vazia
            return entrada
        print("Erro: O campo não pode estar vazio. Por favor, introduza um nome válido.")