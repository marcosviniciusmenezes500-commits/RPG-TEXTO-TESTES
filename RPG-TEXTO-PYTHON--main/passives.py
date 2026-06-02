from enum import Enum


class Passiva:
    """Representa uma passiva/talento que um jogador pode aprender."""
    
    def __init__(self, id_passiva, nome, descricao, requisito_nivel, categoria):
        """
        Cria uma nova passiva.
        
        Args:
            id_passiva (str): ID único da passiva
            nome (str): Nome da passiva
            descricao (str): Descrição do efeito
            requisito_nivel (int): Nível mínimo para aprender
            categoria (str): Categoria (Combate, Defesa, Utilidade)
        """
        self.id = id_passiva
        self.nome = nome
        self.descricao = descricao
        self.requisito_nivel = requisito_nivel
        self.categoria = categoria
        self.ativa = False
    
    def aplicar_efeito(self, jogador):
        """Aplica o efeito da passiva ao jogador."""
        pass
    
    def remover_efeito(self, jogador):
        """Remove o efeito da passiva do jogador."""
        pass
    
    def __repr__(self):
        return f"{self.nome} (Nv.{self.requisito_nivel})"


class PassivaAumento:
    """Passiva que aumenta um atributo."""
    
    def __init__(self, id_passiva, nome, descricao, requisito_nivel, atributo, valor_aumento):
        self.id = id_passiva
        self.nome = nome
        self.descricao = descricao
        self.requisito_nivel = requisito_nivel
        self.categoria = "Combate"
        self.ativa = False
        self.atributo = atributo
        self.valor_aumento = valor_aumento
    
    def aplicar_efeito(self, jogador):
        """Aplica o aumento de atributo."""
        if self.atributo == "dano":
            jogador.danobase += self.valor_aumento
        elif self.atributo == "agilidade":
            jogador.agilidadebase += self.valor_aumento
        elif self.atributo == "defesa":
            jogador.defesabase += self.valor_aumento
        elif self.atributo == "hp":
            jogador.hp_max += self.valor_aumento
            jogador.hp = jogador.hp_max
        
        self.ativa = True
    
    def remover_efeito(self, jogador):
        """Remove o aumento de atributo."""
        if self.atributo == "dano":
            jogador.danobase -= self.valor_aumento
        elif self.atributo == "agilidade":
            jogador.agilidadebase -= self.valor_aumento
        elif self.atributo == "defesa":
            jogador.defesabase -= self.valor_aumento
        elif self.atributo == "hp":
            jogador.hp_max -= self.valor_aumento
        
        self.ativa = False
    
    def __repr__(self):
        return f"{self.nome} (Nv.{self.requisito_nivel})"


# Catálogo de Passivas Disponíveis
PASSIVAS_CATALOGO = {
    # Nível 3 - Passivas Básicas
    "sede_sangue": PassivaAumento(
        "sede_sangue",
        "Sede de Sangue 🩸",
        "Recupera 2 HP ao eliminar um inimigo.",
        3,
        "hp",
        2
    ),
    
    "pele_ferro": PassivaAumento(
        "pele_ferro",
        "Pele de Ferro 🪨",
        "+2 Defesa permanente.",
        3,
        "defesa",
        2
    ),
    
    "aprendiz_arcano": PassivaAumento(
        "aprendiz_arcano",
        "Aprendiz Arcano 📚",
        "+10 Mana Máxima (futuro).",
        3,
        "inteligencia",
        1
    ),
    
    # Nível 5 - Passivas Intermediárias
    "golpe_certeiro": PassivaAumento(
        "golpe_certeiro",
        "Golpe Certeiro ⚔️",
        "+3 Dano adicional.",
        5,
        "dano",
        3
    ),
    
    "reflexos_agucos": PassivaAumento(
        "reflexos_agucos",
        "Reflexos Aguços 💨",
        "+2 Agilidade permanente.",
        5,
        "agilidade",
        2
    ),
    
    "resistencia_forja": PassivaAumento(
        "resistencia_forja",
        "Resistência da Forja 🛡️",
        "+3 Defesa permanente.",
        5,
        "defesa",
        3
    ),
    
    # Nível 10 - Passivas Avançadas
    "lâmina_mestre": PassivaAumento(
        "lâmina_mestre",
        "Lâmina Mestre ⚡",
        "+5 Dano permanente.",
        10,
        "dano",
        5
    ),
    
    "veterano_combate": PassivaAumento(
        "veterano_combate",
        "Veterano de Combate 🏆",
        "+20 HP máximo.",
        10,
        "hp",
        20
    ),
    
    "escudo_inquebravel": PassivaAumento(
        "escudo_inquebravel",
        "Escudo Inquebrantável 🔒",
        "+5 Defesa permanente.",
        10,
        "defesa",
        5
    ),
}


class ArvorePassivas:
    """Gerencia a árvore de passivas de um jogador."""
    
    def __init__(self):
        """Inicializa a árvore de passivas."""
        self.passivas_disponíveis = dict(PASSIVAS_CATALOGO)
        self.passivas_aprendidas = set()
        self.passivas_ativas = []
    
    def obter_passivas_disponiveis(self, nivel_jogador):
        """Retorna passivas que o jogador pode aprender no seu nível atual."""
        return {
            id_p: passiva
            for id_p, passiva in self.passivas_disponíveis.items()
            if passiva.requisito_nivel <= nivel_jogador and id_p not in self.passivas_aprendidas
        }
    
    def aprender_passiva(self, id_passiva, jogador):
        """Aprende uma nova passiva."""
        if id_passiva in self.passivas_aprendidas:
            return False, "Você já aprendeu essa passiva!"
        
        if id_passiva not in self.passivas_disponíveis:
            return False, "Passiva não existe!"
        
        passiva = self.passivas_disponíveis[id_passiva]
        
        if passiva.requisito_nivel > jogador.nivel:
            return False, f"Você precisa estar no nível {passiva.requisito_nivel}!"
        
        # Aprender a passiva
        passiva.aplicar_efeito(jogador)
        self.passivas_aprendidas.add(id_passiva)
        self.passivas_ativas.append(id_passiva)
        
        return True, f"✨ Você aprendeu: {passiva.nome}! {passiva.descricao}"
    
    def ativar_passiva(self, id_passiva, jogador):
        """Ativa uma passiva já aprendida."""
        if id_passiva not in self.passivas_aprendidas:
            return False, "Você não aprendeu essa passiva!"
        
        passiva = self.passivas_disponíveis[id_passiva]
        
        if id_passiva not in self.passivas_ativas:
            passiva.aplicar_efeito(jogador)
            self.passivas_ativas.append(id_passiva)
            return True, f"✨ Passiva ativada: {passiva.nome}"
        
        return False, "Essa passiva já está ativa!"
    
    def desativar_passiva(self, id_passiva, jogador):
        """Desativa uma passiva."""
        if id_passiva not in self.passivas_ativas:
            return False, "Essa passiva não está ativa!"
        
        passiva = self.passivas_disponíveis[id_passiva]
        passiva.remover_efeito(jogador)
        self.passivas_ativas.remove(id_passiva)
        
        return True, f"Passiva desativada: {passiva.nome}"
    
    def listar_aprendidas(self):
        """Lista todas as passivas aprendidas."""
        resultado = []
        for id_p in self.passivas_aprendidas:
            passiva = self.passivas_disponíveis[id_p]
            ativa = "✅" if id_p in self.passivas_ativas else "❌"
            resultado.append(f"{ativa} {passiva}")
        return resultado
    
    def mostrar_menu_passivas(self, jogador):
        """Exibe menu interativo para aprender/gerenciar passivas."""
        from utils import ler_inteiro
        
        while True:
            print(f"\n{'='*60}")
            print(f"  ÁRVORE DE PASSIVAS - {jogador.nome} (Nv.{jogador.nivel})")
            print(f"{'='*60}")
            
            passivas_novas = self.obter_passivas_disponiveis(jogador.nivel)
            
            if passivas_novas:
                print("\n📚 NOVAS PASSIVAS DISPONÍVEIS:")
                opcoes = []
                indice = 1
                
                for id_p, passiva in passivas_novas.items():
                    print(f"[{indice}] {passiva.nome}")
                    print(f"    Descrição: {passiva.descricao}")
                    print(f"    Nível: {passiva.requisito_nivel}")
                    opcoes.append(id_p)
                    indice += 1
                
                escolha = ler_inteiro("\nEscolha uma passiva para aprender (0 para sair): ")
                
                if escolha == 0:
                    break
                
                if 1 <= escolha <= len(opcoes):
                    id_escolhida = opcoes[escolha - 1]
                    sucesso, mensagem = self.aprender_passiva(id_escolhida, jogador)
                    print(f"\n{mensagem}")
                else:
                    print("❌ Opção inválida!")
            else:
                print("\n📚 Nenhuma passiva nova disponível no seu nível!")
            
            # Mostrar passivas aprendidas
            aprendidas = self.listar_aprendidas()
            if aprendidas:
                print("\n🎖️ PASSIVAS APRENDIDAS:")
                for passiva_str in aprendidas:
                    print(f"   {passiva_str}")
            
            break  # Sair do menu após mostrar uma vez
