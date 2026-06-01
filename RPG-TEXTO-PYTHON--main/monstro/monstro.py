from random import randint
from time import sleep
from equipamento import Equipamento

class Monstro:
    # Agora recebe o 'nivel' (por padrão é 1)
    def __init__(self, nome, nivel=1):
        self.nome = nome
        self.nivel = nivel
        
        # Os status base escalam com o nível do monstro!
        self.hp_max = 10 + (nivel * 8) + randint(1, 10)
        self.hp = self.hp_max
        self.dano_base = 3 + (nivel * 2)
        self.agilidade_base = nivel

    def d20(self):
        print(f"O {self.nome} prepara-se para atacar...")
        sleep(1)
        rolagem = randint(1, 20)
        total = rolagem + self.agilidade_base
        print(f"▶ {self.nome} rolou [ {rolagem} ] no D20 (Total: {total})")
        return total

    def d10(self):
        return randint(1, 10)

    def calcular_dano(self, d20_resultado):
        dano_rolagem = self.d10()
        dano_total = self.dano_base + dano_rolagem
        
        if d20_resultado >= 20:
            print(f"💥 CRÍTICO! O ataque de {self.nome} foi devastador!")
            sleep(0.5)
            dano_total *= 2
            
        return dano_total

    def gerar_exp(self):
        """Calcula a EXP que o monstro dá ao morrer."""
        rolagem = randint(1, 20)
        # EXP Base (Nível * 15) + a rolagem de sorte do dado
        exp_total = (self.nivel * 15) + rolagem 
        return exp_total

    def mostrar_status(self):
        # Agora exibe o nível do monstro
        print(f"[{self.nome} Nv.{self.nivel}] ❤️ HP: {self.hp}/{self.hp_max} | ⚔️ ATQ Base: {self.dano_base}")

    def dropar_loot(self):
     """Rola um D20 para decidir se o monstro dropa o seu núcleo."""
     rolagem = randint(1, 20)

     # Chance de drop: Tem de tirar 12 ou mais no D20 (45% de chance)
     if rolagem >= 12:
         # Limpa o nome (ex: tira o "[1]" de "Goblin Corrompido [1]")
         nome_base = self.nome.split(" [")[0]
         # O valor do núcleo escala com o nível do bicho
         valor_nucleo = self.nivel * 12 

         # Cria o núcleo como um "item" sem status, apenas com valor
         return Equipamento(f"Núcleo de {nome_base} 🔮", dano=0, valor=valor_nucleo, agilidade=0, tipo="nucleo")

     return None