from random import randint, choice
from time import sleep
from monstro import Monstro

class Masmorra:
    def __init__(self, jogadores):
        self.jogadores = jogadores
        self.andar_atual = 1
        self.sala_atual = 0
        self.total_salas = 0
        self.monstros_atuais = []
        
        self.temas_andares = [
            "Cavernas Esquecidas",
            "Prisão de Ferro",
            "Jardins Venenosos",
            "Catacumbas Sombrias",
            "O Fosso de Lava",
            "O Trono do Abismo"
        ]
        self.gerar_andar()

    def gerar_andar(self):
        self.sala_atual = 0
        self.total_salas = randint(3, 5) + (self.andar_atual // 2)
        
        print(f"\n{'='*50}")
        print(f"🏰 ANDAR {self.andar_atual}: {self.temas_andares[self.andar_atual-1]}")
        print(f"Há {self.total_salas} salas à vossa frente...")
        print(f"{'='*50}\n")
        sleep(2)

    def avancar_sala(self):
        self.sala_atual += 1
        
        if self.sala_atual > self.total_salas:
            if self.andar_atual == 6:
                print("\n🏆 VOCÊS RESGATARAM A ORÁCULO CEGA! Parabéns!")
                return "VITORIA"
            else:
                print(f"\n🚪 Vocês encontraram as escadas para o {self.andar_atual + 1}º Andar!")
                self.andar_atual += 1
                
                for j in self.jogadores:
                    j.habilidade_usada_andar = False
                print("🌟 Habilidades recarregadas!")
                
                self.gerar_andar()
                return "PROXIMO_ANDAR"

        print(f"\n--- Sala {self.sala_atual}/{self.total_salas} ---")
        sleep(1.5)
        self.gerar_evento()
        return "SALA"

    def gerar_evento(self):
        rolagem = randint(1, 100)
        
        if rolagem <= 40:
            self.evento_combate()
        elif rolagem <= 65:
            self.evento_tesouro()
        elif rolagem <= 85:
            self.evento_armadilha()
        else:
            print("🕯️ Sala segura. Vocês descansam.")
            for j in self.jogadores:
                if j.hp > 0:
                    cura = randint(5, 15)
                    j.hp = min(j.hp_max, j.hp + cura)
            print("💚 Todos recuperaram HP.")

    def evento_combate(self):
        qtd_monstros = randint(1, 2) if self.andar_atual < 3 else randint(1, 3)
        print(f"⚠️ COMBATE! {qtd_monstros} inimigo(s)!")
        sleep(1)
        
        nomes_inimigos = ["Goblin Corrompido", "Esqueleto de Ferro", "Morcego Gigante", "Cultista Sombrio", "Demônio Menor"]
        self.monstros_atuais = []
        
        for i in range(qtd_monstros):
            nome = choice(nomes_inimigos)
            nivel_monstro = self.andar_atual + randint(0, 1)
            novo_monstro = Monstro(f"{nome} [{i+1}]", nivel=nivel_monstro)
            self.monstros_atuais.append(novo_monstro)
            
    def evento_tesouro(self):
        print("💎 Vocês encontraram um baú de tesouro!")
        ouro_encontrado = randint(10, 30) * self.andar_atual
        
        vivos = [j for j in self.jogadores if j.hp > 0]
        if vivos:
            fatia = ouro_encontrado // len(vivos)
            print(f"Cada um recebeu {fatia} moedas de ouro!")
            for j in vivos:
                j.ouro += fatia
                
    def evento_armadilha(self):
        print("🪤 ARMADILHA! Dardos voam das paredes!")
        sleep(1)
        
        for j in self.jogadores:
            if j.hp > 0:
                print(f"\n{j.nome} tenta desviar!")
                teste = j.d20() + j.agilidadebase
                
                if teste > 12:
                    print(f"💨 Sucesso! {j.nome} desviou!")
                else:
                    dano = randint(3, 8) + self.andar_atual
                    j.hp -= dano
                    print(f"🩸 Falha! {j.nome} perdeu {dano} HP!")