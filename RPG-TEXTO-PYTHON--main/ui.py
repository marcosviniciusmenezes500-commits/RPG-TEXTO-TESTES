import os
import sys


class Cores:
    """Definição de cores para terminal usando escape codes ANSI."""
    
    # Cores básicas
    VERMELHO = '\033[91m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIANO = '\033[96m'
    BRANCO = '\033[97m'
    CINZA = '\033[90m'
    
    # Cores de fundo
    BG_VERMELHO = '\033[41m'
    BG_VERDE = '\033[42m'
    BG_AMARELO = '\033[43m'
    BG_AZUL = '\033[44m'
    
    # Estilos
    NEGRITO = '\033[1m'
    DIM = '\033[2m'
    ITALICO = '\033[3m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    @staticmethod
    def texto(cor, mensagem):
        """Retorna texto colorido."""
        return f"{cor}{mensagem}{Cores.RESET}"
    
    @staticmethod
    def texto_com_estilo(cor, mensagem, estilo=""):
        """Retorna texto com cor e estilo."""
        return f"{estilo}{cor}{mensagem}{Cores.RESET}"


class BarraHP:
    """Cria uma barra visual de HP."""
    
    @staticmethod
    def criar_barra(hp_atual, hp_max, tamanho=20):
        """
        Cria uma barra de HP visual.
        
        Args:
            hp_atual (int): HP atual
            hp_max (int): HP máximo
            tamanho (int): Tamanho da barra
        
        Returns:
            str: Barra de HP colorida
        """
        percentual = hp_atual / hp_max if hp_max > 0 else 0
        preenchido = int(tamanho * percentual)
        vazio = tamanho - preenchido
        
        # Escolher cor baseado no percentual
        if percentual > 0.6:
            cor = Cores.VERDE
        elif percentual > 0.3:
            cor = Cores.AMARELO
        else:
            cor = Cores.VERMELHO
        
        barra = f"{cor}{'█' * preenchido}{Cores.CINZA}{'░' * vazio}{Cores.RESET}"
        percentual_text = f"{int(percentual * 100):3d}%"
        
        return f"{barra} {percentual_text} ({hp_atual}/{hp_max})"
    
    @staticmethod
    def criar_barra_mana(mana_atual, mana_max, tamanho=20):
        """Cria uma barra de Mana visual."""
        percentual = mana_atual / mana_max if mana_max > 0 else 0
        preenchido = int(tamanho * percentual)
        vazio = tamanho - preenchido
        
        barra = f"{Cores.AZUL}{'█' * preenchido}{Cores.CINZA}{'░' * vazio}{Cores.RESET}"
        percentual_text = f"{int(percentual * 100):3d}%"
        
        return f"{barra} {percentual_text} ({mana_atual}/{mana_max})"


class UIJogo:
    """Interface visual do jogo com cores."""
    
    @staticmethod
    def limpar_tela():
        """Limpa a tela do terminal."""
        if sys.platform == "win32":
            os.system("cls")
        else:
            os.system("clear")
    
    @staticmethod
    def titulo_secao(titulo):
        """Exibe um título de seção formatado."""
        print(f"\n{Cores.NEGRITO}{Cores.CIANO}")
        print("=" * 60)
        print(f"  {titulo}")
        print("=" * 60)
        print(f"{Cores.RESET}\n")
    
    @staticmethod
    def mostrar_hp_jogo(jogador):
        """Exibe o HP do jogador com cores."""
        barra = BarraHP.criar_barra(jogador.hp, jogador.hp_max)
        print(f"{Cores.NEGRITO}❤️  HP:{Cores.RESET} {barra}")
    
    @staticmethod
    def mostrar_mana_jogo(jogador):
        """Exibe a Mana do jogador com cores."""
        if hasattr(jogador, 'magia'):
            barra = BarraHP.criar_barra_mana(
                jogador.magia.mana,
                jogador.magia.mana_max
            )
            print(f"{Cores.NEGRITO}💙 Mana:{Cores.RESET} {barra}")
    
    @staticmethod
    def ouro_colorido(quantidade):
        """Exibe ouro com cor."""
        return Cores.texto(Cores.AMARELO, f"💰 {quantidade}")
    
    @staticmethod
    def dano_colorido(quantidade):
        """Exibe dano com cor."""
        return Cores.texto(Cores.VERMELHO, f"⚔️  +{quantidade}")
    
    @staticmethod
    def item_lendario(nome):
        """Exibe item lendário com cor."""
        return Cores.texto(Cores.MAGENTA, f"✨ {nome} ✨")
    
    @staticmethod
    def item_raro(nome):
        """Exibe item raro com cor."""
        return Cores.texto(Cores.CIANO, f"💎 {nome}")
    
    @staticmethod
    def sistema_mensagem(mensagem):
        """Exibe mensagem do sistema em ciano."""
        print(f"{Cores.CIANO}➤ {mensagem}{Cores.RESET}")
    
    @staticmethod
    def mensagem_sucesso(mensagem):
        """Exibe mensagem de sucesso em verde."""
        print(f"{Cores.VERDE}✅ {mensagem}{Cores.RESET}")
    
    @staticmethod
    def mensagem_erro(mensagem):
        """Exibe mensagem de erro em vermelho."""
        print(f"{Cores.VERMELHO}❌ {mensagem}{Cores.RESET}")
    
    @staticmethod
    def mensagem_atencao(mensagem):
        """Exibe mensagem de atenção em amarelo."""
        print(f"{Cores.AMARELO}⚠️  {mensagem}{Cores.RESET}")
    
    @staticmethod
    def mostrar_status_combate(jogadores, monstros):
        """Exibe o status de combate com cores."""
        print(f"\n{Cores.NEGRITO}{'='*60}{Cores.RESET}")
        print(f"{Cores.NEGRITO}{Cores.BRANCO}  ESTADO DO COMBATE{Cores.RESET}")
        print(f"{Cores.NEGRITO}{'='*60}{Cores.RESET}\n")
        
        print(f"{Cores.NEGRITO}Jogadores:{Cores.RESET}")
        for j in jogadores:
            if j.hp > 0:
                status = "✅ Vivo"
                print(f"  {j.nome}: {BarraHP.criar_barra(j.hp, j.hp_max)}")
            else:
                print(f"  {Cores.VERMELHO}{j.nome}: MORTO{Cores.RESET}")
        
        print(f"\n{Cores.NEGRITO}Monstros:{Cores.RESET}")
        for m in monstros:
            if m.hp > 0:
                print(f"  {m.nome}: {BarraHP.criar_barra(m.hp, m.hp_max)}")
            else:
                print(f"  {Cores.VERMELHO}{m.nome}: DERROTADO{Cores.RESET}")
        
        print(f"\n{Cores.NEGRITO}{'='*60}{Cores.RESET}\n")
    
    @staticmethod
    def mostrar_status_detalhado(jogador):
        """Exibe status detalhado do jogador com cores."""
        print(f"\n{Cores.NEGRITO}{Cores.CIANO}")
        print("╔══════════════════════════╗")
        print("║      STATUS DO HERÓI     ║")
        print("╚══════════════════════════╝")
        print(f"{Cores.RESET}")
        
        origem = getattr(jogador, 'origem', 'Desconhecida')
        classe = getattr(jogador, 'classe', 'Aventureiro')
        
        print(f"Nome: {Cores.NEGRITO}{jogador.nome}{Cores.RESET} | Nível: {Cores.AMARELO}{jogador.nivel}{Cores.RESET}")
        print(f"Classe: {Cores.CIANO}{classe}{Cores.RESET} | Origem: {Cores.MAGENTA}{origem}{Cores.RESET}")
        
        print(f"\nEXP: {Cores.VERDE}{jogador.exp}/{jogador.exp_max}{Cores.RESET}")
        
        # HP com barra
        barra_hp = BarraHP.criar_barra(jogador.hp, jogador.hp_max)
        print(f"HP (Vida): {barra_hp}")
        
        # Mana com barra (se houver)
        if hasattr(jogador, 'magia'):
            barra_mana = BarraHP.criar_barra_mana(jogador.magia.mana, jogador.magia.mana_max)
            print(f"Mana: {barra_mana}")
        
        if jogador.pontos_status > 0:
            print(f"\n{Cores.AMARELO}⭐ PONTOS LIVRES: {jogador.pontos_status}{Cores.RESET}")
        
        print(f"\n{Cores.NEGRITO}{'━'*30}{Cores.RESET}")
        print(f"{Cores.NEGRITO}ATRIBUTOS BASE{Cores.RESET}")
        print(f"{Cores.NEGRITO}{'━'*30}{Cores.RESET}")
        
        print(f"Força Base: {Cores.VERMELHO}{jogador.danobase}{Cores.RESET}")
        print(f"Agilidade Base: {Cores.VERDE}{jogador.agilidadebase}{Cores.RESET}")
        print(f"Defesa Base: {Cores.AZUL}{jogador.defesabase}{Cores.RESET}")
        
        if hasattr(jogador, 'inteligencia'):
            print(f"Inteligência: {Cores.MAGENTA}{jogador.inteligencia}{Cores.RESET}")
        
        print(f"\n{Cores.NEGRITO}{'━'*30}{Cores.RESET}")
        print(f"Ouro: {Cores.AMARELO}{jogador.ouro}💰{Cores.RESET}")
        if hasattr(jogador, 'nucleos_monstro'):
            print(f"Núcleos de Monstro: {Cores.MAGENTA}{jogador.nucleos_monstro}🧿{Cores.RESET}")
        print(f"{Cores.NEGRITO}{'='*30}{Cores.RESET}\n")


def colorama_fallback():
    """Tenta fazer fallback para colorama se disponível."""
    try:
        from colorama import init
        init(autoreset=True)
        return True
    except ImportError:
        return False
