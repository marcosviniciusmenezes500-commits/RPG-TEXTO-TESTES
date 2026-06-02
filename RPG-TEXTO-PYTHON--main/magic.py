from enum import Enum
from random import randint
from time import sleep


class TipoMagia(Enum):
    """Tipos de magias disponíveis."""
    AOE = "Área de Efeito"
    ALVO_UNICO = "Alvo Único"
    CURA = "Cura"
    BUFF = "Buff"
    DEBUFF = "Debuff"


class ElementoMagia(Enum):
    """Elementos de magia."""
    FOGO = "Fogo"
    GELO = "Gelo"
    RAIO = "Raio"
    LUZ = "Luz"
    SOMBRAS = "Sombras"


class Magia:
    """Representa um feitiço/magia do jogo."""
    
    def __init__(self, nome, custo_mana, dano, tipo, elemento, descricao, nivel_requisito=1):
        """
        Cria uma nova magia.
        
        Args:
            nome (str): Nome da magia
            custo_mana (int): Mana necessária para lançar
            dano (int): Dano causado (ou cura)
            tipo (TipoMagia): Tipo de magia
            elemento (ElementoMagia): Elemento da magia
            descricao (str): Descrição do efeito
            nivel_requisito (int): Nível mínimo para aprender
        """
        self.nome = nome
        self.custo_mana = custo_mana
        self.dano = dano
        self.tipo = tipo
        self.elemento = elemento
        self.descricao = descricao
        self.nivel_requisito = nivel_requisito
        self.tempo_recarga = 0  # Turnos até poder usar novamente
    
    def obter_emoji(self):
        """Retorna emoji baseado no elemento."""
        emojis = {
            ElementoMagia.FOGO: "🔥",
            ElementoMagia.GELO: "❄️",
            ElementoMagia.RAIO: "⚡",
            ElementoMagia.LUZ: "✨",
            ElementoMagia.SOMBRAS: "🌑"
        }
        return emojis.get(self.elemento, "🪄")
    
    def __repr__(self):
        return f"{self.obter_emoji()} {self.nome} (Mana: {self.custo_mana})"


class SistemaInteligencia:
    """Gerencia o atributo inteligência e mana de um personagem."""
    
    def __init__(self, inteligencia=0, mana_base=20):
        """
        Inicializa o sistema de inteligência.
        
        Args:
            inteligencia (int): Valor base de inteligência
            mana_base (int): Mana máxima base
        """
        self.inteligencia = inteligencia
        self.mana_max = mana_base
        self.mana = mana_base
        self.magias_aprendidas = {}  # {id: Magia}
        self.magia_equipada = None
    
    def recuperar_mana(self, quantidade):
        """Recupera mana do personagem."""
        mana_anterior = self.mana
        self.mana = min(self.mana + quantidade, self.mana_max)
        return self.mana - mana_anterior
    
    def gastar_mana(self, quantidade):
        """Gasta mana, retorna True se teve mana suficiente."""
        if self.mana >= quantidade:
            self.mana -= quantidade
            return True
        return False
    
    def aprender_magia(self, magia):
        """Aprende uma nova magia."""
        self.magias_aprendidas[magia.nome] = magia
    
    def obter_dano_magia_modificado(self, magia):
        """Calcula o dano de uma magia com bônus de inteligência."""
        bonus = int(self.inteligencia * 0.5)
        return magia.dano + bonus


# Catálogo de Magias
MAGIAS_CATALOGO = {
    # Magias de Fogo (Dano)
    "bola_fogo": Magia(
        "Bola de Fogo",
        custo_mana=20,
        dano=25,
        tipo=TipoMagia.AOE,
        elemento=ElementoMagia.FOGO,
        descricao="Lança uma bola de fogo que atinge uma área.",
        nivel_requisito=3
    ),
    
    "chama_ardente": Magia(
        "Chama Ardente",
        custo_mana=15,
        dano=15,
        tipo=TipoMagia.ALVO_UNICO,
        elemento=ElementoMagia.FOGO,
        descricao="Atira uma chama que queima o alvo.",
        nivel_requisito=1
    ),
    
    # Magias de Gelo (Controle)
    "chuva_gelo": Magia(
        "Chuva de Gelo",
        custo_mana=25,
        dano=20,
        tipo=TipoMagia.AOE,
        elemento=ElementoMagia.GELO,
        descricao="Congela os inimigos em uma área.",
        nivel_requisito=5
    ),
    
    "espinho_gelo": Magia(
        "Espinho de Gelo",
        custo_mana=12,
        dano=12,
        tipo=TipoMagia.ALVO_UNICO,
        elemento=ElementoMagia.GELO,
        descricao="Congela o alvo, reduzindo sua velocidade.",
        nivel_requisito=2
    ),
    
    # Magias de Raio (Ofensiva)
    "relampago": Magia(
        "Relâmpago",
        custo_mana=18,
        dano=30,
        tipo=TipoMagia.ALVO_UNICO,
        elemento=ElementoMagia.RAIO,
        descricao="Dispara um raio contra o alvo.",
        nivel_requisito=4
    ),
    
    "tempestade_raios": Magia(
        "Tempestade de Raios",
        custo_mana=35,
        dano=35,
        tipo=TipoMagia.AOE,
        elemento=ElementoMagia.RAIO,
        descricao="Cria uma tempestade que atinge todos.",
        nivel_requisito=7
    ),
    
    # Magias de Luz (Cura/Buff)
    "cura_luz": Magia(
        "Cura de Luz",
        custo_mana=20,
        dano=0,  # Cura, não dano
        tipo=TipoMagia.CURA,
        elemento=ElementoMagia.LUZ,
        descricao="Cura um aliado (restaura 30 HP).",
        nivel_requisito=1
    ),
    
    "bencao_divina": Magia(
        "Bênção Divina",
        custo_mana=25,
        dano=0,
        tipo=TipoMagia.BUFF,
        elemento=ElementoMagia.LUZ,
        descricao="Aumenta a defesa de um aliado.",
        nivel_requisito=5
    ),
    
    # Magias de Sombra (Debuff/Controle)
    "maldição_sombra": Magia(
        "Maldição Sombra",
        custo_mana=20,
        dano=15,
        tipo=TipoMagia.DEBUFF,
        elemento=ElementoMagia.SOMBRAS,
        descricao="Enfraquece o alvo com uma maldição.",
        nivel_requisito=3
    ),
    
    "prisão_sombra": Magia(
        "Prisão de Sombra",
        custo_mana=25,
        dano=0,
        tipo=TipoMagia.DEBUFF,
        elemento=ElementoMagia.SOMBRAS,
        descricao="Immobiliza o inimigo com sombras.",
        nivel_requisito=6
    ),
}


class ClasseMagia:
    """Define uma classe que usa magia."""
    
    def __init__(self, nome, magias_iniciais, bonus_inteligencia=0, bonus_mana=0):
        """
        Cria uma nova classe de magia.
        
        Args:
            nome (str): Nome da classe
            magias_iniciais (list): Nomes das magias iniciais (IDs do catálogo)
            bonus_inteligencia (int): Bônus de inteligência
            bonus_mana (int): Bônus de mana máxima
        """
        self.nome = nome
        self.magias_iniciais = magias_iniciais
        self.bonus_inteligencia = bonus_inteligencia
        self.bonus_mana = bonus_mana
        self.descricao = ""
    
    def aplicar_bonos(self, jogador):
        """Aplica os bônus da classe ao jogador."""
        jogador.inteligencia = getattr(jogador, 'inteligencia', 0) + self.bonus_inteligencia
        if hasattr(jogador, 'magia'):
            jogador.magia.mana_max += self.bonus_mana
            jogador.magia.mana = jogador.magia.mana_max
            
            # Ensinar magias iniciais
            for magia_id in self.magias_iniciais:
                if magia_id in MAGIAS_CATALOGO:
                    jogador.magia.aprender_magia(MAGIAS_CATALOGO[magia_id])


# Definição de Classes de Magia
CLASSES_MAGIA = {
    "mago": ClasseMagia(
        "Mago",
        ["chama_ardente", "espinho_gelo", "relampago"],
        bonus_inteligencia=5,
        bonus_mana=30
    ),
    "clerigo": ClasseMagia(
        "Clérigo",
        ["cura_luz", "chama_ardente"],
        bonus_inteligencia=3,
        bonus_mana=25
    ),
    "feiticeiro": ClasseMagia(
        "Feiticeiro",
        ["maldição_sombra", "chama_ardente", "cura_luz"],
        bonus_inteligencia=4,
        bonus_mana=20
    ),
}


def lancar_magia(lancador, alvo, magia):
    """
    Lança uma magia contra um alvo.
    
    Args:
        lancador: Personagem lançando a magia
        alvo: Alvo da magia
        magia: A magia a ser lançada
    
    Returns:
        dict: Informações sobre o resultado do lançamento
    """
    print(f"\n{'='*50}")
    print(f"🪄 {lancador.nome} lança {magia}!")
    sleep(1)
    
    # Verificar mana
    if not hasattr(lancador, 'magia'):
        return {"sucesso": False, "mensagem": "Você não consegue lançar magias!"}
    
    if lancador.magia.mana < magia.custo_mana:
        return {
            "sucesso": False,
            "mensagem": f"Mana insuficiente! Você tem {lancador.magia.mana}/{magia.custo_mana}"
        }
    
    # Gastar mana
    lancador.magia.gastar_mana(magia.custo_mana)
    
    # Calcular dano/efeito
    if magia.tipo == TipoMagia.ALVO_UNICO or magia.tipo == TipoMagia.AOE:
        dano = lancador.magia.obter_dano_magia_modificado(magia)
        # Variação de dano
        dano_final = dano + randint(-3, 5)
        alvo.hp -= dano_final
        
        mensagem = f"💥 {magia.nome} atinge {alvo.nome}! Dano: {dano_final}"
    
    elif magia.tipo == TipoMagia.CURA:
        cura = magia.dano + (lancador.magia.inteligencia // 2)
        alvo.hp = min(alvo.hp + cura, alvo.hp_max)
        mensagem = f"✨ {magia.nome} cura {alvo.nome}! Recuperou {cura} HP"
    
    elif magia.tipo == TipoMagia.BUFF:
        # Aplicar buff de defesa
        from status_effects import aplicar_buff_defesa
        aplicar_buff_defesa(alvo, potencia=2, duracao=3)
        mensagem = f"🛡️ {magia.nome} fortalece {alvo.nome}!"
    
    elif magia.tipo == TipoMagia.DEBUFF:
        # Aplicar debuff baseado no elemento
        from status_effects import aplicar_congelamento, aplicar_maldição
        if magia.elemento == ElementoMagia.GELO:
            aplicar_congelamento(alvo, potencia=2, duracao=2)
        elif magia.elemento == ElementoMagia.SOMBRAS:
            # Aplicar efeito de maldição (reduzi dano)
            alvo.buff_dano -= 2
        mensagem = f"⚠️ {magia.nome} afeta {alvo.nome}!"
    
    print(mensagem)
    print(f"{'='*50}\n")
    
    return {"sucesso": True, "mensagem": mensagem}
