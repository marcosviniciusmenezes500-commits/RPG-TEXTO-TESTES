from enum import Enum
from time import sleep


class TipoEfeito(Enum):
    """Tipos de efeitos de status no jogo."""
    VENENO = "Veneno"
    SANGRAMENTO = "Sangramento"
    ATORDOAMENTO = "Atordoamento"
    QUEIMADURA = "Queimadura"
    CONGELAMENTO = "Congelamento"
    BUFF_DANO = "Buff de Dano"
    BUFF_DEFESA = "Buff de Defesa"


class EfeitoStatus:
    """Classe para representar um efeito de status aplicado a um personagem."""
    
    def __init__(self, tipo, duracao, potencia=1):
        """
        Cria um novo efeito de status.
        
        Args:
            tipo (TipoEfeito): Tipo do efeito
            duracao (int): Quantos turnos o efeito dura
            potencia (int): Intensidade do efeito (1-5)
        """
        self.tipo = tipo
        self.duracao = duracao
        self.duracao_max = duracao
        self.potencia = min(potencia, 5)  # Máximo 5
    
    def aplicar_efeito(self, alvo):
        """
        Aplica o efeito ao alvo no início do turno.
        
        Args:
            alvo: Personagem afetado (Jogador ou Monstro)
        """
        if self.tipo == TipoEfeito.VENENO:
            dano = 3 * self.potencia
            alvo.hp -= dano
            print(f"☠️  {alvo.nome} sofre {dano} de dano por veneno!")
        
        elif self.tipo == TipoEfeito.SANGRAMENTO:
            dano = 2 * self.potencia
            alvo.hp -= dano
            print(f"🩸 {alvo.nome} sangra e perde {dano} de HP!")
        
        elif self.tipo == TipoEfeito.QUEIMADURA:
            dano = 4 * self.potencia
            alvo.hp -= dano
            print(f"🔥 {alvo.nome} queima e sofre {dano} de dano!")
        
        elif self.tipo == TipoEfeito.ATORDOAMENTO:
            # Atordoamento não faz dano, mas afeta a capacidade de agir
            print(f"😵 {alvo.nome} está atordoado!")
        
        elif self.tipo == TipoEfeito.CONGELAMENTO:
            reducao = 5 * self.potencia
            print(f"❄️  {alvo.nome} está congelado! Agilidade reduzida em {reducao}%")
        
        elif self.tipo == TipoEfeito.BUFF_DANO:
            print(f"⚔️  {alvo.nome} está em fúria! Dano aumentado!")
        
        elif self.tipo == TipoEfeito.BUFF_DEFESA:
            print(f"🛡️  {alvo.nome} está protegido! Defesa aumentada!")
    
    def obter_modificador_ataque(self):
        """Retorna modificador de ataque baseado no efeito."""
        if self.tipo == TipoEfeito.ATORDOAMENTO:
            return 0.5  # Atordoamento reduz chance de acerto em 50%
        elif self.tipo == TipoEfeito.CONGELAMENTO:
            return 0.7  # Congelamento reduz chance em 30%
        return 1.0
    
    def obter_modificador_defesa(self):
        """Retorna modificador de defesa baseado no efeito."""
        if self.tipo == TipoEfeito.BUFF_DEFESA:
            return 1 + (0.2 * self.potencia)  # +20% a +100% de defesa
        return 1.0
    
    def obter_modificador_dano(self):
        """Retorna modificador de dano baseado no efeito."""
        if self.tipo == TipoEfeito.BUFF_DANO:
            return 1 + (0.15 * self.potencia)  # +15% a +75% de dano
        return 1.0
    
    def decrementar_duracao(self):
        """Reduz a duração do efeito em 1 turno."""
        self.duracao -= 1
        return self.duracao > 0
    
    def __repr__(self):
        return f"{self.tipo.value} (Duracao: {self.duracao} | Potencia: {self.potencia}⭐)"


class GerenciadorEfeitos:
    """Gerencia os efeitos de status aplicados a um personagem."""
    
    def __init__(self):
        self.efeitos_ativos = []
    
    def adicionar_efeito(self, efeito):
        """Adiciona um novo efeito de status."""
        # Verificar se há efeito do mesmo tipo
        for e in self.efeitos_ativos:
            if e.tipo == efeito.tipo:
                print(f"⚠️  {efeito.tipo.value} está sendo reforçado!")
                e.potencia = min(e.potencia + efeito.potencia, 5)
                e.duracao = max(e.duracao, efeito.duracao)
                return
        
        # Adicionar novo efeito
        self.efeitos_ativos.append(efeito)
        print(f"⚠️  Novo efeito aplicado: {efeito.tipo.value}!")
    
    def aplicar_efeitos_inicio_turno(self, alvo):
        """Aplica todos os efeitos ativos no início do turno."""
        for efeito in self.efeitos_ativos[:]:
            efeito.aplicar_efeito(alvo)
            
            if not efeito.decrementar_duracao():
                self.efeitos_ativos.remove(efeito)
                print(f"✅ {efeito.tipo.value} desapareceu!")
    
    def obter_modificadores(self):
        """Retorna os modificadores cumulativos de todos os efeitos."""
        modificador_ataque = 1.0
        modificador_defesa = 1.0
        modificador_dano = 1.0
        
        for efeito in self.efeitos_ativos:
            modificador_ataque *= efeito.obter_modificador_ataque()
            modificador_defesa *= efeito.obter_modificador_defesa()
            modificador_dano *= efeito.obter_modificador_dano()
        
        return {
            "ataque": modificador_ataque,
            "defesa": modificador_defesa,
            "dano": modificador_dano
        }
    
    def esta_atordoado(self):
        """Verifica se o personagem está atordoado."""
        return any(e.tipo == TipoEfeito.ATORDOAMENTO for e in self.efeitos_ativos)
    
    def listar_efeitos(self):
        """Lista todos os efeitos ativos."""
        if not self.efeitos_ativos:
            return "Nenhum efeito ativo"
        return ", ".join(str(e) for e in self.efeitos_ativos)
    
    def limpar_efeitos(self):
        """Remove todos os efeitos (usado em cura ou reset)."""
        self.efeitos_ativos.clear()


def aplicar_veneno(alvo, potencia=1, duracao=3):
    """Aplica veneno ao alvo."""
    efeito = EfeitoStatus(TipoEfeito.VENENO, duracao, potencia)
    alvo.efeitos.adicionar_efeito(efeito)


def aplicar_sangramento(alvo, potencia=1, duracao=2):
    """Aplica sangramento ao alvo."""
    efeito = EfeitoStatus(TipoEfeito.SANGRAMENTO, duracao, potencia)
    alvo.efeitos.adicionar_efeito(efeito)


def aplicar_queimadura(alvo, potencia=1, duracao=3):
    """Aplica queimadura ao alvo."""
    efeito = EfeitoStatus(TipoEfeito.QUEIMADURA, duracao, potencia)
    alvo.efeitos.adicionar_efeito(efeito)


def aplicar_atordoamento(alvo, potencia=1, duracao=1):
    """Aplica atordoamento ao alvo."""
    efeito = EfeitoStatus(TipoEfeito.ATORDOAMENTO, duracao, potencia)
    alvo.efeitos.adicionar_efeito(efeito)


def aplicar_congelamento(alvo, potencia=1, duracao=2):
    """Aplica congelamento ao alvo."""
    efeito = EfeitoStatus(TipoEfeito.CONGELAMENTO, duracao, potencia)
    alvo.efeitos.adicionar_efeito(efeito)


def aplicar_buff_dano(alvo, potencia=2, duracao=3):
    """Aplica buff de dano ao alvo."""
    efeito = EfeitoStatus(TipoEfeito.BUFF_DANO, duracao, potencia)
    alvo.efeitos.adicionar_efeito(efeito)


def aplicar_buff_defesa(alvo, potencia=2, duracao=3):
    """Aplica buff de defesa ao alvo."""
    efeito = EfeitoStatus(TipoEfeito.BUFF_DEFESA, duracao, potencia)
    alvo.efeitos.adicionar_efeito(efeito)
