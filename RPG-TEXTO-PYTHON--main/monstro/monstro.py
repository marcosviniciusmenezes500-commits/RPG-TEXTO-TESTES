from random import randint
from time import sleep
from equipamento import Equipamento

class Monstro:
    def __init__(self, nome, nivel=1):
        self.nome = nome
        self.nivel = nivel
        
        self.hp_max = 10 + (nivel * 8) + randint(1, 10)
        self.hp = self.hp_max
        self.dano_base = 3 + (nivel * 2)
        self.agilidade_base = nivel

    def d20(self):
        print(f"O {self.nome} prepara-se para atacar...")
        sleep(1)
        rolagem = randint(1, 20)
        total = rolagem + self.agilidade_base
        print(f"▶ {self.nome} rolou [{rolagem}] (Total: {total})")
        return total

    def d10(self):
        return randint(1, 10)

    def calcular_dano(self, d20_resultado):
        dano_rolagem = self.d10()
        dano_total = self.dano_base + dano_rolagem
        
        if d20_resultado >= 20:
            print(f"💥 CRÍTICO! {self.nome} foi devastador!")
            sleep(0.5)
            dano_total *= 2
            
        return dano_total

    def gerar_exp(self):
        rolagem = randint(1, 20)
        exp_total = (self.nivel * 15) + rolagem
        return exp_total

    def mostrar_status(self):
        print(f"[{self.nome} Nv.{self.nivel}] ❤️ HP: {self.hp}/{self.hp_max} | ⚔️ ATQ: {self.dano_base}")

    def dropar_loot(self):
        rolagem = randint(1, 20)

        if rolagem >= 12:
            nome_base = self.nome.split(" [")[0]
            valor_nucleo = self.nivel * 12
            
            return Equipamento(f"Núcleo de {nome_base} 🔮", dano=0, valor=valor_nucleo, agilidade=0, tipo="nucleo")

        return None