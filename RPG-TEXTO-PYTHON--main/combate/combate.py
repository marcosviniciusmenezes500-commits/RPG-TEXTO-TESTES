from time import sleep
from utils import ler_inteiro

class Combate:
    def __init__(self, jogador_atual, jogadores, monstros):
        self.jogador = jogador_atual
        self.jogadores = jogadores
        self.monstros = monstros
        self.alvo = None

    def escolher_alvo(self):
        print("\n--- ESCOLHA O SEU ALVO ---")
        alvos_disponiveis = []
        indice_opcao = 0

        # 1. Listar Monstros Vivos
        print("Monstros:")
        for m in self.monstros:
            if m.hp > 0:
                print(f"[{indice_opcao}] 👹 {m.nome} (HP: {m.hp}/{m.hp_max})")
                alvos_disponiveis.append(m)
                indice_opcao += 1

        # 2. Listar Jogadores Vivos (Fogo Amigo habilitado)
        print("\nJogadores:")
        for j in self.jogadores:
            if j.hp > 0 and j != self.jogador:
                print(f"[{indice_opcao}] 👤 {j.nome} (HP: {j.hp}/{j.hp_max})")
                alvos_disponiveis.append(j)
                indice_opcao += 1

        while True:
            escolha = ler_inteiro("Digite o número do alvo: ")
            if 0 <= escolha < len(alvos_disponiveis):
                self.alvo = alvos_disponiveis[escolha]
                break
            print("❌ Alvo inválido. Escolha um número da lista.")

    def ataque_jogador(self):
        # 1. Jogador escolhe quem vai atacar
        self.escolher_alvo()
        
        print(f"\n{'='*40}")
        print(f"⚔️ {self.jogador.nome} avança para atacar {self.alvo.nome}!")
        sleep(1)

        # 2. Resolução do Ataque do Jogador
        d20_ataque = self.jogador.d20()

        if d20_ataque > 10:
            d10 = self.jogador.d10()
            dano = self.jogador.danotot(d10, d20_ataque)
            self.alvo.hp -= dano
            print(f"💥 SUCESSO! {self.alvo.nome} sofreu {dano} de dano!")
        else:
            print("❌ FALHA! O ataque não atingiu o alvo!")

        sleep(1)

        # 3. Resolução da Reação/Iniciativa do Alvo (se sobreviver)
        if self.alvo.hp > 0:
            self.testar_reacao_alvo()
        else:
            print(f"\n💀 {self.alvo.nome} foi derrotado!")
            
        print(f"{'='*40}\n")

    def testar_reacao_alvo(self):
        """Mecânica de interrupção de turno: O alvo testa a sorte para contra-atacar imediatamente."""
        print(f"\n⚡ {self.alvo.nome} tenta reagir rapidamente ao ataque!")
        sleep(1)
        
        # O alvo rola o seu D20 (funciona tanto para a classe Monstro quanto para Jogador)
        iniciativa = self.alvo.d20()
        
        # Dificuldade 15 para conseguir roubar o turno e contra-atacar
        if iniciativa >= 15: 
            print(f"\n⚠️ REFLEXO PERFEITO! {self.alvo.nome} roubou a iniciativa e contra-ataca!")
            sleep(1)
            
            # Verifica se o alvo é um Monstro ou um Jogador para aplicar o cálculo de dano correto
            if self.alvo.__class__.__name__ == "Monstro":
                dano_reacao = self.alvo.calcular_dano(iniciativa)
            else:
                # É um jogador (Fogo Amigo retribuído)
                d10 = self.alvo.d10()
                dano_reacao = self.alvo.danotot(d10, iniciativa)
                
            # O alvo contra-atacou o jogador
            dano_real = self.jogador.receber_dano(dano_reacao)
            print(f"🩸 {self.jogador.nome} sofreu {dano_real} de dano do contra-ataque de {self.alvo.nome}!")
            print(f"🩸 {self.jogador.nome} sofreu {dano_reacao} de dano do contra-ataque de {self.alvo.nome}!")
        else:
            print(f"💨 {self.alvo.nome} não foi rápido o suficiente para contra-atacar agora.")