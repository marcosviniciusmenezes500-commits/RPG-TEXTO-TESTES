from random import randint, choice
from time import sleep
from monstro import Monstro

class Masmorra:
    def __init__(self, jogadores):
        self.jogadores = jogadores
        self.andar_atual = 1
        self.sala_atual = 0
        self.total_salas = 0
        self.monstros_atuais = []  # IMPORTANTE: Controla se estamos em combate ou exploração!
        
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
        """Prepara um novo andar com uma quantidade aleatória de salas."""
        self.sala_atual = 0
        # O número de salas escala com a profundidade do andar (ex: 3 a 7 salas)
        self.total_salas = randint(3, 5) + (self.andar_atual // 2)
        
        print(f"\n{'='*50}")
        print(f"🏰 DESCENDO PARA O {self.andar_atual}º ANDAR: {self.temas_andares[self.andar_atual-1]}")
        print(f"As trevas ocultam {self.total_salas} salas à vossa frente...")
        print(f"{'='*50}\n")
        sleep(2)

    def avancar_sala(self):
        """O grupo decide avançar. Rola eventos e verifica se encontrou as escadas."""
        self.sala_atual += 1
        
        # Se ultrapassámos o número de salas, encontramos as escadas!
        if self.sala_atual > self.total_salas:
            if self.andar_atual == 6:
                print("\n🎉 VOCÊS RESGATARAM A ORÁCULO CEGA! A Fenda de Ébano foi purificada!")
                return "VITORIA"
            else:
                print(f"\n🚪 Vocês encontraram as escadas para o {self.andar_atual + 1}º Andar!")
                self.andar_atual += 1
                self.gerar_andar()
                return "PROXIMO_ANDAR"

        print(f"\n--- 🚪 Explorando a Sala {self.sala_atual}/{self.total_salas} do {self.andar_atual}º Andar ---")
        sleep(1.5)
        self.gerar_evento()
        return "SALA"

    def gerar_evento(self):
        """Mecânica do D100 para decidir o que está dentro da sala."""
        rolagem = randint(1, 100)
        
        if rolagem <= 40:
            self.evento_combate()
        elif rolagem <= 65:
            self.evento_tesouro()
        elif rolagem <= 85:
            self.evento_armadilha()
        else:
            print("🕯️ A sala está vazia e segura. Vocês aproveitam para descansar.")
            for j in self.jogadores:
                if j.hp > 0:
                    cura = randint(5, 15)
                    j.hp = min(j.hp_max, j.hp + cura)
            print("💚 Todos os jogadores vivos recuperaram um pouco de HP.")

    def evento_combate(self):
        """Gera de 1 a 3 monstros consoante o nível e coloca-os na sala."""
        qtd_monstros = randint(1, 2) if self.andar_atual < 3 else randint(1, 3)
        print(f"⚠️ EMBOSCADA! {qtd_monstros} inimigo(s) bloquearam o caminho!")
        sleep(1)
        
        nomes_inimigos = ["Goblin Corrompido", "Esqueleto de Ferro", "Morcego Gigante", "Cultista Sombrio", "Demônio Menor"]
        self.monstros_atuais = []  # Reinicia a lista de inimigos da sala
        
        for i in range(qtd_monstros):
            nome = choice(nomes_inimigos)
            nivel_monstro = self.andar_atual + randint(0, 1) # O nível escala com o andar
            novo_monstro = Monstro(f"{nome} [{i+1}]", nivel=nivel_monstro)
            self.monstros_atuais.append(novo_monstro)
            
    def evento_tesouro(self):
        """Encontram um baú com Ouro que é dividido pela equipa."""
        print("💎 Vocês encontraram um baú de tesouro abandonado!")
        ouro_encontrado = randint(10, 30) * self.andar_atual
        
        vivos = [j for j in self.jogadores if j.hp > 0]
        if vivos:
            fatia = ouro_encontrado // len(vivos)
            print(f"O grupo dividiu as moedas! Cada jogador recebeu {fatia} de Ouro.")
            for j in vivos:
                j.ouro += fatia
                
    def evento_armadilha(self):
        """Todos os jogadores rolam a Agilidade para não perder vida."""
        print("🪤 TRRAK! Alguém pisou numa placa de pressão! Dardos voam das paredes!")
        sleep(1)
        
        for j in self.jogadores:
            if j.hp > 0:
                # Teste de agilidade para desviar
                print(f"\n{j.nome} tenta desviar-se!")
                teste = j.d20() + j.agilidadebase
                
                # Dificuldade da armadilha é 12
                if teste > 12:
                    print(f"💨 Sucesso! {j.nome} conseguiu esquivar-se!")
                else:
                    dano = randint(3, 8) + self.andar_atual
                    j.hp -= dano
                    print(f"🩸 Falha! {j.nome} foi atingido e perdeu {dano} de HP!")