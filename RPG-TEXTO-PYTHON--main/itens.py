from enum import Enum
from time import sleep


class Raridade(Enum):
    """Enumeração das raridades possíveis de itens."""
    COMUM = "Comum"
    RARA = "Rara"
    EPICA = "Épica"
    LENDARIA = "Lendária"


class Item:
    """Classe base para todos os itens do jogo."""
    
    def __init__(self, nome, valor, raridade=Raridade.COMUM, descricao=""):
        self.nome = nome
        self.valor = valor
        self.raridade = raridade
        self.descricao = descricao
    
    def usar(self, jogador):
        """Método para usar o item. Deve ser sobrescrito pelas subclasses."""
        pass
    
    def __repr__(self):
        return f"{self.nome} ({self.raridade.value})"


class Poção(Item):
    """Poção consumível que recupera HP."""
    
    def __init__(self, nome="Poção de Cura Menor", cura=30, valor=15, raridade=Raridade.COMUM):
        self.cura = cura
        descricao = f"Recupera {cura} HP"
        super().__init__(nome, valor, raridade, descricao)
    
    def usar(self, jogador):
        """Usa a poção para recuperar HP do jogador."""
        hp_anterior = jogador.hp
        jogador.hp = min(jogador.hp + self.cura, jogador.hp_max)
        hp_recuperado = jogador.hp - hp_anterior
        
        print(f"\n✨ {jogador.nome} usou {self.nome}!")
        print(f"   ❤️  HP recuperado: +{hp_recuperado}")
        print(f"   HP agora: {jogador.hp}/{jogador.hp_max}")
        sleep(0.8)
        
        return True


class PocaoMana(Item):
    """Poção consumível que recupera Mana/Foco."""
    
    def __init__(self, nome="Poção de Foco Menor", mana=20, valor=20, raridade=Raridade.COMUM):
        self.mana = mana
        descricao = f"Recupera {mana} Mana/Foco"
        super().__init__(nome, valor, raridade, descricao)
    
    def usar(self, jogador):
        """Usa a poção para recuperar Mana/Foco do jogador."""
        if not hasattr(jogador, 'mana'):
            jogador.mana = 0
            jogador.mana_max = 100
        
        mana_anterior = jogador.mana
        jogador.mana = min(jogador.mana + self.mana, jogador.mana_max)
        mana_recuperado = jogador.mana - mana_anterior
        
        print(f"\n✨ {jogador.nome} usou {self.nome}!")
        print(f"   🔵 Mana recuperada: +{mana_recuperado}")
        print(f"   Mana agora: {jogador.mana}/{jogador.mana_max}")
        sleep(0.8)
        
        return True


class LagrFenix(Item):
    """Item raro que revive um aliado morto."""
    
    def __init__(self):
        super().__init__(
            nome="Lágrima da Fênix",
            valor=500,
            raridade=Raridade.LENDARIA,
            descricao="Revive um aliado com 50% do HP"
        )
        self.cura_ressurreicao = 50
    
    def usar(self, jogador):
        """Usa a lágrima para reviver o jogador."""
        if jogador.hp > 0:
            print(f"\n❌ {jogador.nome} já está vivo!")
            sleep(0.5)
            return False
        
        jogador.hp = max(1, int(jogador.hp_max * self.cura_ressurreicao / 100))
        
        print(f"\n🔥 {jogador.nome} foi revivido pela Lágrima da Fênix!")
        print(f"   ❤️  HP restaurado: {jogador.hp}/{jogador.hp_max}")
        sleep(1)
        
        return True


class Elixir(Item):
    """Elixir que aumenta todos os atributos temporariamente."""
    
    def __init__(self, nome="Elixir Menor", duracao_turnos=3, valor=50, raridade=Raridade.RARA):
        self.duracao_turnos = duracao_turnos
        self.buffs = {
            'buff_dano': 5,
            'buff_defesa': 3,
            'buff_agilidade': 2
        }
        descricao = f"Aumenta todos os atributos por {duracao_turnos} turnos"
        super().__init__(nome, valor, raridade, descricao)
    
    def usar(self, jogador):
        """Usa o elixir para buffar os atributos do jogador."""
        print(f"\n✨ {jogador.nome} usou {self.nome}!")
        
        for buff_nome, valor_buff in self.buffs.items():
            if hasattr(jogador, buff_nome):
                setattr(jogador, buff_nome, getattr(jogador, buff_nome) + valor_buff)
            else:
                setattr(jogador, buff_nome, valor_buff)
        
        print(f"   💪 Força +5 | 🛡️  Defesa +3 | ⚡ Agilidade +2")
        print(f"   Duração: {self.duracao_turnos} turnos")
        sleep(0.8)
        
        return True


class AntidotoVeneno(Item):
    """Poção que remove o debuff de veneno."""
    
    def __init__(self):
        super().__init__(
            nome="Antídoto de Veneno",
            valor=25,
            raridade=Raridade.COMUM,
            descricao="Remove o efeito de veneno"
        )
    
    def usar(self, jogador):
        """Remove o debuff de veneno do jogador."""
        if hasattr(jogador, 'envenenado') and jogador.envenenado:
            jogador.envenenado = False
            print(f"\n✨ {jogador.nome} usou {self.nome}!")
            print(f"   ✅ Veneno removido!")
            sleep(0.8)
            return True
        else:
            print(f"\n❌ {jogador.nome} não está envenenado!")
            sleep(0.5)
            return False


def criar_pocoes_loja():
    """Cria as poções disponíveis na loja."""
    pocoes = [
        Poção("Poção de Cura Menor", cura=30, valor=15, raridade=Raridade.COMUM),
        Poção("Poção de Cura", cura=60, valor=30, raridade=Raridade.RARA),
        Poção("Poção de Cura Superior", cura=100, valor=60, raridade=Raridade.EPICA),
        PocaoMana("Poção de Foco Menor", mana=20, valor=20, raridade=Raridade.COMUM),
        PocaoMana("Poção de Foco", mana=50, valor=40, raridade=Raridade.RARA),
        Elixir("Elixir Menor", duracao_turnos=3, valor=50, raridade=Raridade.RARA),
        Elixir("Elixir Maior", duracao_turnos=5, valor=100, raridade=Raridade.EPICA),
        AntidotoVeneno(),
    ]
    return pocoes
