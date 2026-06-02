from random import randint
from time import sleep
from equipamento import Equipamento
from status_effects import GerenciadorEfeitos

class Monstro:
    def __init__(self, nome, nivel=1):
        self.nome = nome
        self.nivel = nivel
        
        self.hp_max = 10 + (nivel * 8) + randint(1, 10)
        self.hp = self.hp_max
        self.dano_base = 3 + (nivel * 2)
        self.agilidade_base = nivel
        
        # Sistema de efeitos de status
        self.efeitos = GerenciadorEfeitos()

    def d20(self):
        print(f"O {self.nome} prepara-se para atacar...")
        sleep(1)
        rolagem = randint(1, 20)
        total = rolagem + self.agilidade_base
        print(f"▶ {self.nome} rolou [{rolagem}] (Total: {total})")
        return total

    def d10(self):
        return randint(1, 10)

    def calcular_dano(self, d20_resultado):
        dano_rolagem = self.d10()
        dano_total = self.dano_base + dano_rolagem
        
        if d20_resultado >= 20:
            print(f"💥 CRÍTICO! {self.nome} foi devastador!")
            sleep(0.5)
            dano_total *= 2
            
        return dano_total

    def gerar_exp(self):
        rolagem = randint(1, 20)
        exp_total = (self.nivel * 15) + rolagem
        return exp_total

    def mostrar_status(self):
        print(f"[{self.nome} Nv.{self.nivel}] ❤️ HP: {self.hp}/{self.hp_max} | ⚔️ ATQ: {self.dano_base}")

    def dropar_loot(self):
        rolagem = randint(1, 20)

        if rolagem >= 12:
            # Sempre dropam núcleos
            return {"nucleos": randint(1, 2), "tipo": "nucleo"}

        return None


class Boss(Monstro):
    """Classe especial para Bosses de Andar - versões muito mais fortes de monstros."""
    
    # Lista de Bosses por andar
    BOSSES_ANDAR = {
        1: "Golem Ancestral",
        2: "Arcano Sombrio",
        3: "Cavaleiro Espectral",
        4: "Dragão das Profundezas",
        5: "Rei Esqueleto",
        6: "O Abismo Encarnado"
    }
    
    DESCRICOES_BOSSES = {
        "Golem Ancestral": "Uma construção de pedra antiga que protege os segredos das cavernas.",
        "Arcano Sombrio": "Um ser de pura magia sombria, aprisionado há séculos.",
        "Cavaleiro Espectral": "Um guerreiro morto-vivo que ainda defende sua prisão de ferro.",
        "Dragão das Profundezas": "Uma criatura lendária com asas de fogo e escamas de ouro.",
        "Rei Esqueleto": "O monarca da morte que comanda os exércitos de não-mortos.",
        "O Abismo Encarnado": "A encarnação do próprio abismo - poder incomparável."
    }
    
    def __init__(self, andar):
        """Cria um Boss baseado no andar da masmorra."""
        nome_boss = self.BOSSES_ANDAR.get(andar, "Guardião Desconhecido")
        nivel = 5 + (andar * 3)  # Bosses são muito mais fortes
        
        super().__init__(nome_boss, nivel)
        
        self.andar = andar
        self.descricao = self.DESCRICOES_BOSSES.get(nome_boss, "Um inimigo formidável.")
        self.eh_boss = True
        
        # Bosses têm muito mais HP
        self.hp_max = int(self.hp_max * 3.5)
        self.hp = self.hp_max
        
        # Bosses fazem mais dano
        self.dano_base = int(self.dano_base * 2.5)
        
        # Bosses têm mais agilidade
        self.agilidade_base = int(self.agilidade_base * 1.5)
        
        # Defesa do boss
        self.defesa_boss = 3 + andar
    
    def d20(self):
        """O Boss rola dois d20 e pega o melhor (vantagem)."""
        print(f"🔥 {self.nome} se prepara para atacar com poder devastador!")
        sleep(1)
        
        rolagem1 = randint(1, 20)
        rolagem2 = randint(1, 20)
        melhor_rolagem = max(rolagem1, rolagem2)
        
        total = melhor_rolagem + self.agilidade_base
        print(f"🔥 {self.nome} rolou [{rolagem1}] e [{rolagem2}] → [{melhor_rolagem}] (Total: {total})")
        return total
    
    def calcular_dano(self, d20_resultado):
        """Bosses causam dano crítico com mais frequência."""
        dano_rolagem = self.d10()
        dano_total = self.dano_base + dano_rolagem
        
        # Crítico em 18+ ao invés de 20
        if d20_resultado >= 18:
            print(f"💥💥 CRÍTICO DO BOSS! {self.nome} causa destruição massiva!")
            sleep(0.5)
            dano_total = int(dano_total * 2.5)  # 2.5x ao invés de 2x
        
        return dano_total
    
    def dropar_loot(self):
        """Bosses sempre dropam mais núcleos e recompensas especiais."""
        return {
            "nucleos": randint(5, 10),
            "tipo": "nucleo",
            "bonus_ouro": 100 * self.andar,
            "raro": True
        }
    
    def mostrar_status(self):
        """Exibe status de um Boss com destaque especial."""
        print(f"\n{'🔥'*20}")
        print(f"🏆 BOSS: {self.nome} 🏆")
        print(f"Descrição: {self.descricao}")
        print(f"Nível: {self.nivel} | ❤️ HP: {self.hp}/{self.hp_max}")
        print(f"⚔️ Dano: {self.dano_base} | 🛡️ Defesa: {self.defesa_boss}")
        print(f"{'🔥'*20}\n")