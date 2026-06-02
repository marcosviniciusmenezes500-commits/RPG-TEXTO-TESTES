from time import sleep
from utils import ler_inteiro
from random import randint


class Ferreiro:
    """NPC responsável por upgrades de equipamentos."""
    
    # Custo base de upgrade (aumenta com cada nível)
    CUSTOS_UPGRADE = {
        1: {"ouro": 50, "nucleos": 1},
        2: {"ouro": 100, "nucleos": 2},
        3: {"ouro": 200, "nucleos": 3},
        4: {"ouro": 350, "nucleos": 5},
        5: {"ouro": 500, "nucleos": 8},
    }
    
    # Multiplicador de dano/bônus por nível
    BONUS_POR_NIVEL = 0.15  # +15% de bônus a cada upgrade
    
    def __init__(self):
        self.nome = "Ferreiro Ancestral 🔨"
        self.nucleos_disponiveis = 0
    
    def abrir_ferraria(self, jogador):
        """Interface principal da ferraria."""
        print(f"\n{'='*60}")
        print(f"  {self.nome}")
        print(f"  'Venha melhorar seus equipamentos, aventureiro!'")
        print(f"{'='*60}")
        
        while True:
            print(f"\n💰 Ouro: {jogador.ouro}")
            print(f"🧿 Núcleos de Monstros: {jogador.nucleos_monstro}")
            print("\n[1] Upgradear Arma")
            print("[2] Upgradear Armadura")
            print("[3] Upgradear Anel")
            print("[4] Ver Detalhes dos Upgrades")
            print("[5] Sair da Ferraria")
            
            opc = ler_inteiro("O que deseja? ")
            
            if opc == 1:
                self._menu_upgrade_arma(jogador)
            elif opc == 2:
                self._menu_upgrade_armadura(jogador)
            elif opc == 3:
                self._menu_upgrade_anel(jogador)
            elif opc == 4:
                self._exibir_detalhes_upgrades()
            elif opc == 5:
                print(f"\n{self.nome} acena. Até logo, aventureiro!")
                break
            else:
                print("❌ Opção inválida!")
    
    def _menu_upgrade_arma(self, jogador):
        """Menu de upgrade da arma equipada."""
        if not jogador.arma:
            print("\n❌ Você não possui uma arma equipada!")
            return
        
        self._processar_upgrade(jogador, jogador.arma, "arma")
    
    def _menu_upgrade_armadura(self, jogador):
        """Menu de upgrade da armadura equipada."""
        if not jogador.armadura:
            print("\n❌ Você não possui uma armadura equipada!")
            return
        
        self._processar_upgrade(jogador, jogador.armadura, "armadura")
    
    def _menu_upgrade_anel(self, jogador):
        """Menu de upgrade do anel equipado."""
        if not jogador.anel:
            print("\n❌ Você não possui um anel equipado!")
            return
        
        self._processar_upgrade(jogador, jogador.anel, "anel")
    
    def _processar_upgrade(self, jogador, equipamento, tipo_equip):
        """Processa o upgrade de um equipamento."""
        nivel_atual = getattr(equipamento, 'nivel_upgrade', 0)
        
        print(f"\n{'='*50}")
        print(f"  UPGRADE: {equipamento.nome}")
        print(f"  Nível Atual: +{nivel_atual}")
        print(f"{'='*50}")
        
        # Verificar se pode fazer upgrade
        if nivel_atual >= 5:
            print("\n❌ Este equipamento já atingiu o máximo (Nível +5)!")
            return
        
        proximo_nivel = nivel_atual + 1
        
        # Exibir custo
        if proximo_nivel not in self.CUSTOS_UPGRADE:
            print("\n❌ Nível de upgrade inválido!")
            return
        
        custo = self.CUSTOS_UPGRADE[proximo_nivel]
        print(f"\n📊 Custo para +{proximo_nivel}:")
        print(f"   💰 {custo['ouro']} Ouro")
        print(f"   🧿 {custo['nucleos']} Núcleo(s) de Monstro")
        
        # Calcular novos bônus
        dano_base = getattr(equipamento, 'dano', 0)
        novo_dano = self._calcular_bonus_upgrade(dano_base, proximo_nivel)
        aumento_dano = novo_dano - dano_base
        
        if aumento_dano > 0:
            print(f"\n   ⚔️ Dano: +{aumento_dano} (Total: {novo_dano})")
        
        # Verificar recursos
        if jogador.ouro < custo['ouro']:
            print(f"\n❌ Ouro insuficiente! Você tem {jogador.ouro}, precisa de {custo['ouro']}")
            return
        
        if jogador.nucleos_monstro < custo['nucleos']:
            print(f"\n❌ Núcleos insuficientes! Você tem {jogador.nucleos_monstro}, precisa de {custo['nucleos']}")
            return
        
        # Confirmar upgrade
        print("\n" + "="*50)
        confirmar = input("Deseja prosseguir com o upgrade? (S/N): ").upper()
        
        if confirmar != 'S':
            print("Upgrade cancelado.")
            return
        
        # Aplicar upgrade
        self._aplicar_upgrade(jogador, equipamento, proximo_nivel, novo_dano, custo)
    
    def _calcular_bonus_upgrade(self, valor_base, nivel):
        """Calcula o novo valor com bônus de upgrade."""
        if valor_base == 0:
            return valor_base
        return int(valor_base * (1 + self.BONUS_POR_NIVEL * nivel))
    
    def _aplicar_upgrade(self, jogador, equipamento, novo_nivel, novo_dano, custo):
        """Aplica o upgrade ao equipamento."""
        # Deduzir recursos
        jogador.ouro -= custo['ouro']
        jogador.nucleos_monstro -= custo['nucleos']
        
        # Atualizar equipamento
        equipamento.nivel_upgrade = novo_nivel
        equipamento.dano = novo_dano
        
        # Aumentar valor do equipamento
        equipamento.valor = int(equipamento.valor * 1.5)
        
        # Atualizar nome
        nome_base = equipamento.nome.split(" +")[0].strip()
        equipamento.nome = f"{nome_base} +{novo_nivel}"
        
        # Efeito visual
        print("\n" + "🔥" * 30)
        sleep(0.5)
        print(f"✨ O Ferreiro trabalha incansavelmente...")
        sleep(1)
        print(f"💥 {equipamento.nome} foi aprimorado com sucesso!")
        print(f"   ⚔️ Novo dano: {novo_dano}")
        print(f"   💰 Ouro restante: {jogador.ouro}")
        print(f"   🧿 Núcleos restantes: {jogador.nucleos_monstro}")
        print("🔥" * 30 + "\n")
        sleep(1)
    
    def _exibir_detalhes_upgrades(self):
        """Exibe tabela de custos e bônus de upgrade."""
        print(f"\n{'='*70}")
        print(f"  TABELA DE UPGRADES")
        print(f"{'='*70}")
        print(f"{'Nível':<8} {'Ouro':<12} {'Núcleos':<12} {'Bônus Dano':<15}")
        print("-" * 70)
        
        for nivel, custo in self.CUSTOS_UPGRADE.items():
            bonus = f"+{int(self.BONUS_POR_NIVEL * nivel * 100)}%"
            print(f"+{nivel:<7} {custo['ouro']:<12} {custo['nucleos']:<12} {bonus:<15}")
        
        print("=" * 70 + "\n")


def adicionar_nucleos_jogador(jogador, quantidade=1):
    """Adiciona núcleos de monstros ao jogador."""
    if not hasattr(jogador, 'nucleos_monstro'):
        jogador.nucleos_monstro = 0
    jogador.nucleos_monstro += quantidade
