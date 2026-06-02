from time import sleep
from utils import ler_inteiro

class Combate:
    def __init__(self, jogador_atual, jogadores, monstros):
        self.jogador = jogador_atual
        self.jogadores = jogadores
        self.monstros = monstros
        self.alvo = None

    def aplicar_efeitos_inicio_turno(self):
        """Aplica efeitos de status ao jogador no início do turno."""
        print(f"\n--- Efeitos de Status em {self.jogador.nome} ---")
        self.jogador.efeitos.aplicar_efeitos_inicio_turno(self.jogador)
        
        # Verificar se está morto após efeitos
        if self.jogador.hp <= 0:
            print(f"\n💀 {self.jogador.nome} sucumbiu aos efeitos de status!")
            return False
        return True

    def escolher_alvo(self):
        print("\n--- ESCOLHA SEU ALVO ---")
        alvos_disponiveis = []
        indice_opcao = 0

        print("Monstros:")
        for m in self.monstros:
            if m.hp > 0:
                print(f"[{indice_opcao}] 👹 {m.nome} (HP: {m.hp}/{m.hp_max})")
                alvos_disponiveis.append(m)
                indice_opcao += 1

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
            print("❌ Alvo inválido!")

    def ataque_jogador(self):
        # Aplicar efeitos de status no início do turno
        if not self.aplicar_efeitos_inicio_turno():
            return  # Jogador morreu por efeitos
        
        # Verificar se está atordoado
        if self.jogador.efeitos.esta_atordoado():
            print(f"\n😵 {self.jogador.nome} está atordoado e não consegue agir!")
            sleep(1)
            return
        
        self.escolher_alvo()
        
        print(f"\n{'='*40}")
        print(f"⚔️ {self.jogador.nome} avança para atacar {self.alvo.nome}!")
        sleep(1)

        d20_ataque = self.jogador.d20()
        
        # Aplicar modificador de ataque por efeitos
        modificadores = self.jogador.efeitos.obter_modificadores()
        d20_ataque_modificado = int(d20_ataque * modificadores["ataque"])

        if d20_ataque_modificado > 10:
            d10 = self.jogador.d10()
            dano = self.jogador.danotot(d10, d20_ataque_modificado)
            
            # Aplicar modificador de dano por efeitos
            dano_final = int(dano * modificadores["dano"])
            
            self.alvo.hp -= dano_final
            print(f"💥 SUCESSO! {self.alvo.nome} sofreu {dano_final} de dano!")
        else:
            print("❌ FALHA! O ataque não atingiu!")

        sleep(1)

        if self.alvo.hp > 0:
            self.testar_reacao_alvo()
        else:
            print(f"\n💀 {self.alvo.nome} foi derrotado!")
            
        print(f"{'='*40}\n")

    def testar_reacao_alvo(self):
        print(f"\n⚡ {self.alvo.nome} tenta reagir!")
        sleep(1)
        
        iniciativa = self.alvo.d20()
        
        if iniciativa >= 15:
            print(f"\n⚠️ REFLEXO PERFEITO! {self.alvo.nome} contra-ataca!")
            sleep(1)
            
            if self.alvo.__class__.__name__ == "Monstro":
                dano_reacao = self.alvo.calcular_dano(iniciativa)
            else:
                d10 = self.alvo.d10()
                dano_reacao = self.alvo.danotot(d10, iniciativa)
                
            dano_real = self.jogador.receber_dano(dano_reacao)
            print(f"🩸 {self.jogador.nome} sofreu {dano_real} de dano!")
        else:
            print(f"💨 {self.alvo.nome} não foi rápido o suficiente.")