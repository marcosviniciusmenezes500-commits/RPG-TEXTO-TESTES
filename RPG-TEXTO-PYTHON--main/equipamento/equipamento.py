class Equipamento:
    # O defesa=0 precisa estar aqui dentro dos parênteses!
    def __init__(self, nome, dano=0, valor=0, agilidade=0, defesa=0, tipo="arma"):
        self.nome = nome
        self.dano = dano
        self.valor = valor
        self.agilidade = agilidade
        self.defesa = defesa  # Para que esta linha funcione
        self.tipo = tipo
        self.nivel_upgrade = 0  # Sistema de upgrade do Ferreiro