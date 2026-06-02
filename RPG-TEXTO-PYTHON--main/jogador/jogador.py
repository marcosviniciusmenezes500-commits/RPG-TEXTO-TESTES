from utils import ler_inteiro
from random import randint
from time import sleep
from equipamento import Equipamento
class Jogador :
    def __init__(self,nome,hp):
        self.nome = nome
        self.hp = hp
        self.hp_max = hp
        self.ouro = 50
        self.danobase = 10
        self.agilidadebase = 0
        self.defesabase = 0
        self.armadura = None
        self.inventario = []

        # --- SISTEMA DE NÍVEL ---
        self.nivel = 1
        self.exp = 0
        self.exp_max = 100  # EXP necessária para o nível 2
        self.pontos_status = 0

        #slots
        self.arma:Equipamento = None
        self.anel = None


    def d20 (self) :
        print("Rolando dado de agilidade🎲 . . .")
        sleep(0.5)
        rolagem = randint(10,20)
        
        # Calcula o total de agilidade (base + equipamentos)
        bonus_agilidade = self.agilidadebase
        if self.arma:
            bonus_agilidade += self.arma.agilidade
        if self.anel:
            bonus_agilidade += self.anel.agilidade
            
        total = rolagem + bonus_agilidade
        print(f"Dado: {rolagem} | Bónus de Agilidade: +{bonus_agilidade} | Total: {total}")
        return total
    def d10 (self) :
        print("Rolando dado de ataque🎲 . . .")
        sleep(0.5)
        d10 = randint(1,10)
        print(d10)
        return d10

    def danotot (self,d10,d20) :
        danotot = d10
        if self.danobase >0 :
            print(f"+ {self.danobase} de bônus")
            danotot += self.danobase
            
        if self.arma and self.arma.dano > 0 :
            danotot += self.arma.dano
            print(f"+ {self.arma.dano} ⚔️ (Arma)")
            
        # NOVA ADIÇÃO: Soma o dano do anel, se estiver equipado
        if self.anel and self.anel.dano > 0 :
            danotot += self.anel.dano
            print(f"+ {self.anel.dano} 💍 (Anel)")
            
        if d20 >= 20 :
            print("ESPECIAL ATIVADO!!!")
            sleep(0.3)
            danotot *= 2
            
        return danotot
    def adicionar_item_inventario(self,item) :
        print (f"{item.nome} foi adicionado no inventário")
        self.inventario.append(item)

    def mostrar_inventario(self):
        if not self.inventario :
            print("Inventário vazio")
            return
        opc = 0
        fim = len(self.inventario)
        while opc != fim :
            for i, item in enumerate(self.inventario) :
                # ADICIONADO: Exibição do status de defesa do item
                print(f"-[{i}] {item.nome}  dano:{item.dano}  agilidade:{item.agilidade}  defesa:{item.defesa}  tipo:{item.tipo}")
            print(f"-[{fim}] Saída")
            
            if self.arma :
                print(f"Arma equipada : {self.arma.nome}")
            if self.anel :
                print(f"Anel equipado : {self.anel.nome}")
            # ADICIONADO: Exibição da armadura equipada
            if self.armadura :
                print(f"Armadura equipada : {self.armadura.nome}")
                
            opc = ler_inteiro("> ")
            if opc == fim :
                return
            if opc < 0 or opc > fim:
                print("Erro: Opção inválida. Escolha um item válido do inventário.")
                continue
                
            # ADICIONADO: Permite que itens do tipo "armadura" sejam enviados para o método equipar()
            if self.inventario[opc].tipo == "arma" or self.inventario[opc].tipo == "anel" or self.inventario[opc].tipo == "armadura":
                self.equipar(self.inventario[opc])
    
    def mostrar_status(self):
        # Cálculos de bónus dos equipamentos para mostrar no total
        dano_extra = 0
        agil_extra = 0
        defesa_extra = 0
        
        # Soma os bónus de todos os equipamentos equipados
        for equipamento in [self.arma, self.anel, self.armadura]:
            if equipamento:
                dano_extra += equipamento.dano
                agil_extra += equipamento.agilidade
                defesa_extra += equipamento.defesa

        dano_total = self.danobase + dano_extra
        agil_total = self.agilidadebase + agil_extra
        defesa_total = self.defesabase + defesa_extra

        # Exibição Visual
        print("\n╔══════════════════════════╗")
        print("║      STATUS DO HERÓI     ║")
        print("╚══════════════════════════╝\n")
        
        origem_personagem = getattr(self, 'origem', 'Desconhecida')
        classe_personagem = getattr(self, 'classe', 'Aventureiro')
        print(f"Nome: {self.nome} | Nível: {self.nivel}")
        print(f"Classe: {classe_personagem} | Origem: {origem_personagem}")
        
        print(f"EXP: {self.exp} / {self.exp_max}")
        print(f"HP (Vida): {self.hp} / {self.hp_max}")
        if self.pontos_status > 0:
            print(f"⭐ PONTOS DE STATUS LIVRES: {self.pontos_status} (Use o menu para distribuir)")
        
        print("\n━━━━━━━━━━━━━━━━━━")
        print("ATRIBUTOS BASE")
        print("━━━━━━━━━━━━━━━━━━")
        print(f"Força Base: {self.danobase}")
        print(f"Agilidade Base: {self.agilidadebase}")
        print(f"Defesa Base: {self.defesabase}")

        print("\nBônus de Equipamentos:")
        if not self.arma and not self.anel and not self.armadura:
            print("Nenhum bônus de equipamento.")
        else:
            # Função auxiliar para formatar os bónus (+5 ou -2)
            def formatar_bonus(item):
                bonus = []
                if item.dano != 0: bonus.append(f"{item.dano:+d} Força")
                if item.agilidade != 0: bonus.append(f"{item.agilidade:+d} Agilidade")
                if item.defesa != 0: bonus.append(f"{item.defesa:+d} Defesa")
                return ", ".join(bonus) if bonus else "+0 Atributos"

            if getattr(self, 'arma', None):
                print(f"⚔️ {formatar_bonus(self.arma)} ({self.arma.nome})")
                
            if getattr(self, 'anel', None):
                print(f"💍 {formatar_bonus(self.anel)} ({self.anel.nome})")

            if getattr(self, 'armadura', None):
                print(f"👕 {formatar_bonus(self.armadura)} ({self.armadura.nome})")

        print("\n━━━━━━━━━━━━━━━━━━")
        print("TOTAL")
        print("━━━━━━━━━━━━━━━━━━")
        print(f"Força Total: {dano_total}")
        print(f"Agilidade Total: {agil_total}")
        print(f"Defesa Total: {defesa_total}")

        print("\n━━━━━━━━━━━━━━━━━━")
        print("MOCHILA")
        print("━━━━━━━━━━━━━━━━━━")
        print(f"💰 Ouro: {self.ouro}")
        print("\n" + "="*40 + "\n")


    def equipar(self, item):
        if item not in self.inventario :
            print(f"{item.nome} Não está no inventário")
            return
            
        if item.tipo == 'arma' :
            if self.arma :
                print(f"Desequipando {self.arma.nome}")
            self.arma = item
            
        elif item.tipo == "anel" :
            if self.anel :
                print(f"Desequipando {self.anel.nome}")
            self.anel = item
            
        # O BLOCO QUE FALTAVA PARA GUARDAR A ARMADURA
        elif item.tipo == "armadura" :
            if getattr(self, 'armadura', None): # Verifica com segurança se já tem armadura
                print(f"Desequipando {self.armadura.nome}")
            self.armadura = item
            
        print(f"{self.nome} Equipou {item.nome}")
        
    
    def rolar_atributos_iniciais(self):
        print(f"\n{'='*40}")
        print(f"🎲 Definindo o destino de {self.nome}...")
        print("Rolando D20 . . .")
        sleep(1.5)
        
        rolagem = randint(1, 20)
        print(f"▶ Resultado: [ {rolagem} ]\n")
        sleep(0.5)
        
        # Guarda os valores originais para mostrar a diferença visualmente
        hp_orig, ouro_orig, dano_orig, agil_orig = self.hp, self.ouro, self.danobase, self.agilidadebase
        
        if rolagem == 1:
            print("💀 DESASTRE! Você começou a aventura com ferimentos e dívidas.")
            self.hp -= 5
            self.ouro -= 20
            self.danobase -= 2
            
        elif 2 <= rolagem <= 7:
            print("🌧️ AZAR! As coisas não começaram muito bem para si.")
            self.hp -= 2
            self.ouro -= 10
            self.danobase -= 1
            
        elif 8 <= rolagem <= 13:
            print("⚖️ COMUM. O seu treino foi mediano, um aventureiro padrão.")
            # Status mantêm-se iguais
            
        elif 14 <= rolagem <= 19:
            print("🍀 SORTE! Você começou com recursos extras e um bom talento.")
            self.hp += 5
            self.ouro += 15
            self.danobase += 2
            self.agilidadebase += 2
            
        elif rolagem == 20:
            print("🌟 LENDÁRIO! Os deuses abençoaram a sua jornada desde o nascimento!")
            self.hp += 10
            self.ouro += 50
            self.danobase += 5
            self.agilidadebase += 5

        # Travas de segurança para impedir atributos negativos
        self.hp = max(1, self.hp)
        self.ouro = max(0, self.ouro)
        self.danobase = max(1, self.danobase)
        self.hp_max = self.hp
        # Apresentação visual das alterações
        print("[Status Iniciais Alterados]")
        
        def formatar_mudanca(antigo, novo):
            if novo > antigo: return f"-> {novo} (+{novo-antigo})"
            elif novo < antigo: return f"-> {novo} ({novo-antigo})"
            return f"-> {novo} (Manteve)"

        print(f"❤️ HP:         {hp_orig:2}  {formatar_mudanca(hp_orig, self.hp)}")
        print(f"💰 Ouro:       {ouro_orig:2}  {formatar_mudanca(ouro_orig, self.ouro)}")
        print(f"⚔️ Dano Base:  {dano_orig:2}  {formatar_mudanca(dano_orig, self.danobase)}")
        print(f"💨 Agilidade:  {agil_orig:2}  {formatar_mudanca(agil_orig, self.agilidadebase)}")
        print(f"{'='*40}")
        sleep(2)
    
    def ganhar_exp(self, quantidade):
        self.exp += quantidade
        print(f"🌟 {self.nome} recebeu {quantidade} de EXP!")
        
        # Sistema de Nível
        while self.exp >= self.exp_max:
            self.exp -= self.exp_max
            self.nivel += 1
            self.pontos_status += 3  # Mantém os 3 pontos livres
            
            print(f"\n🎉 {self.nome} SUBIU PARA O NÍVEL {self.nivel}!")
            print("⭐ Você ganhou +3 Pontos de Status livres!")
            
            # --- NOVO: Bónus Fixo da Classe ---
            classe_nome = getattr(self, 'classe', '')
            
            if "Bárbaro" in classe_nome:
                self.danobase += 1
                print("🪓 Bónus de Bárbaro: +1 Força Base!")
            elif "Guardião" in classe_nome:
                self.defesabase += 1
                print("🛡️ Bónus de Guardião: +1 Defesa Base!")
            elif "Duelista" in classe_nome:
                self.agilidadebase += 1
                print("🗡️ Bónus de Duelista: +1 Agilidade Base!")
            elif "Vanguarda" in classe_nome:
                self.hp_max += 3
                print("⚔️ Bónus de Vanguarda: +3 HP Máximo!")
            
            # Restaura o HP ao subir de nível
            self.hp = self.hp_max 
            print("💚 HP totalmente restaurado!")
            print("="*40 + "\n")
            
    def subir_nivel(self):
        from time import sleep
        self.nivel += 1
        self.exp -= self.exp_max
        self.exp_max = int(self.exp_max * 1.5) # O próximo nível será 50% mais difícil
        self.pontos_status += 3 # Ganha 3 pontos livres
        
        # Cura o jogador como bónus
        self.hp = self.hp_max 
        
        print("\n" + "🌟"*20)
        print(f"🎉 LEVEL UP! {self.nome} alcançou o Nível {self.nivel}!")
        print(f"Você ganhou 3 Pontos de Status! (Total: {self.pontos_status})")
        print("🌟"*20 + "\n")
        sleep(1.5)

    def distribuir_pontos(self):
        from utils import ler_inteiro
        if self.pontos_status <= 0:
            print("Você não tem pontos de status para distribuir.")
            return
            
        while self.pontos_status > 0:
            print(f"\n--- DISTRIBUIR PONTOS ({self.pontos_status} disponíveis) ---")
            print("[1] +5 HP Máximo")
            print("[2] +1 Força (Dano Base)")
            print("[3] +1 Agilidade Base")
            print("[4] +1 Defesa Base")
            print("[0] Guardar pontos para depois")
            
            opc = ler_inteiro("Onde quer investir? ")
            
            if opc == 1:
                self.hp_max += 5
                self.hp += 5 # Cura a vida adicionada
                self.pontos_status -= 1
                print("❤️ HP Máximo aumentado em 5!")
            elif opc == 2:
                self.danobase += 1
                self.pontos_status -= 1
                print("⚔️ Força aumentada em 1!")
            elif opc == 3:
                self.agilidadebase += 1
                self.pontos_status -= 1
                print("💨 Agilidade aumentada em 1!")
            elif opc == 4:
                self.defesabase += 1
                self.pontos_status -= 1
                print("🛡️ Defesa aumentada em 1!")
            elif opc == 0:
                print("Pontos guardados com sucesso.")
                break
            else:
                print("Opção inválida.")
    
    def receber_dano(self, dano_bruto):
        """Calcula o dano final após aplicar a redução da Defesa Total."""
        defesa_total = self.defesabase
        if self.arma: defesa_total += self.arma.defesa
        if self.anel: defesa_total += self.anel.defesa
        if self.armadura: defesa_total += self.armadura.defesa
        
        # O dano final é o ataque menos a defesa, mas nunca menos que 1
        dano_final = max(1, dano_bruto - defesa_total)
        self.hp -= dano_final
        return dano_final

    def sortear_origem(self):
        from random import choices
        from time import sleep
        from equipamento import Equipamento

        origens = [
            "Mendigo Amaldiçoado", "Desertor Covarde",  # 2 Ruins (25% cada)
            "Camponês Comum", "Guarda Noturno",         # 2 Normais (15% cada)
            "Mercenário Veterano", "Assassino das Sombras", # 2 Boas (8% cada)
            "O Herói Escolhido"                         # 1 Lendária (4%)
        ]
        
        # Pesos em percentagem exata
        pesos = [25, 25, 15, 15, 8, 8, 4]
        
        # choices retorna uma lista, pegamos o primeiro elemento [0]
        escolha = choices(origens, weights=pesos, k=1)[0]
        self.origem = escolha
        
        print("\n" + "="*50)
        print(f"🎲 Sorteando o passado de {self.nome}...")
        sleep(2)
        print(f"✨ A Roda do Destino parou em: ** {escolha.upper()} **!")
        
        if escolha == "Mendigo Amaldiçoado":
            print("📖 História: Você viveu nas ruas e sobreviveu de restos. Uma bruxa o amaldiçoou, enfraquecendo o seu corpo e alma. A Fenda de Ébano é a sua última chance de redenção na vida.")
            print("📉 Modificadores: -5 HP Máximo, -2 Força Base, -1 Agilidade.")
            self.hp_max -= 5
            self.danobase -= 2
            self.agilidadebase -= 1
            
        elif escolha == "Desertor Covarde":
            print("📖 História: Quando a guerra estourou, você fugiu na calada da noite e escondeu-se em cavernas. O medo constante tornou-o muito rápido, mas os anos de fuga minaram a sua força.")
            print("📉 Modificadores: +2 Agilidade, -3 Força Base, -2 HP Máximo.")
            self.hp_max -= 2
            self.danobase -= 3
            self.agilidadebase += 2
            
        elif escolha == "Camponês Comum":
            print("📖 História: Uma vida inteira a arar campos pacíficos. Você não tem nenhum treino militar ou habilidades especiais, mas o trabalho duro debaixo de sol deu-lhe um corpo bastante resistente.")
            print("⚖️ Modificadores: +5 HP Máximo.")
            self.hp_max += 5
            
        elif escolha == "Guarda Noturno":
            print("📖 História: Você patrulhava as muralhas de uma vila pequena. Sabe segurar uma arma e defender-se, embora as noites mal dormidas a vigiar portões o tenham deixado com reflexos lentos.")
            print("⚖️ Modificadores: +1 Força Base, +1 Defesa Base, -1 Agilidade.")
            self.danobase += 1
            self.defesabase += 1
            self.agilidadebase -= 1
            
        elif escolha == "Mercenário Veterano":
            print("📖 História: O seu passado está manchado de sangue em troca de moedas de ouro. A experiência em inúmeras batalhas pelo continente forjou um guerreiro letal, resistente e implacável.")
            print("📈 Modificadores: +10 HP Máximo, +3 Força Base, +2 Defesa Base.")
            self.hp_max += 10
            self.danobase += 3
            self.defesabase += 2
            
        elif escolha == "Assassino das Sombras":
            print("📖 História: Treinado desde criança por um culto secreto de assassinos, você aprendeu a matar em absoluto silêncio. Os seus reflexos são invejáveis e os seus golpes atingem pontos vitais.")
            print("📈 Modificadores: +4 Agilidade, +2 Força Base, +1 Defesa Base.")
            self.agilidadebase += 4
            self.danobase += 2
            self.defesabase += 1
            
        elif escolha == "O Herói Escolhido":
            print("📖 História: Marcado pelo destino no momento em que nasceu. As estrelas alinharam-se e as profecias antigas cantam o seu nome. Você é o portador da luz, destinado a purificar a Fenda de Ébano e realizar grandes feitos que ecoarão pela eternidade!")
            print("🌟 Modificadores: +15 HP Máximo, +5 Força Base, +3 Agilidade, +3 Defesa Base.")
            self.hp_max += 15
            self.danobase += 5
            self.agilidadebase += 3
            self.defesabase += 3
            
            # Equipamento Lendário Exclusivo
            espada_heroi = Equipamento("Espada do Herói ⚔️🌟", dano=12, valor=100, agilidade=2, defesa=0, tipo="arma")
            self.inventario.append(espada_heroi)
            self.equipar(espada_heroi)
            print("🎁 O destino intercedeu: Você começa com a 'Espada do Herói'! (Pode ser substituída ou aprimorada no futuro).")

        # 1. Garante que atributos base não quebram o jogo (mínimo de 1)
        self.hp_max = max(1, self.hp_max)
        self.danobase = max(1, self.danobase)
        
        # 2. Cura o jogador para o seu novo HP Máximo real após os cálculos
        self.hp = self.hp_max
        print("="*50 + "\n")
        sleep(2)
    
    def escolher_classe(self):
        from utils import ler_inteiro
        from time import sleep
        
        print(f"\n{'='*50}")
        print(f"🛡️ O CAMINHO MARCIAL DE {self.nome.upper()} 🛡️")
        print("Chegou o momento de escolher o seu estilo de combate.")
        print("Esta escolha definirá os seus atributos iniciais e o seu crescimento a cada nível!\n")

        print("[1] Bárbaro 🪓")
        print("    Foco: Dano brutal e vida alta. Ignora a própria segurança.")
        print("    Inicial: +10 HP Máximo, +3 Força Base, -2 Defesa Base.")
        print("    Por Nível: +1 Força Base.\n")

        print("[2] Guardião 🛡️")
        print("    Foco: Resistência pura. Uma verdadeira muralha viva.")
        print("    Inicial: +5 HP Máximo, +4 Defesa Base, -2 Agilidade Base.")
        print("    Por Nível: +1 Defesa Base.\n")

        print("[3] Duelista 🗡️")
        print("    Foco: Reflexos perfeitos. Frágil, mas quase intocável.")
        print("    Inicial: +4 Agilidade Base, +1 Força Base, -5 HP Máximo.")
        print("    Por Nível: +1 Agilidade Base.\n")

        print("[4] Vanguarda ⚔️")
        print("    Foco: O soldado perfeito e equilibrado.")
        print("    Inicial: +2 Força Base, +1 Defesa Base, +1 Agilidade Base.")
        print("    Por Nível: +3 HP Máximo (ganha mais vida natural por nível).\n")

        while True:
            opc = ler_inteiro("Qual será a sua Classe? (1 a 4): ")
            
            if opc == 1:
                self.classe = "Bárbaro 🪓"
                self.hp_max += 10
                self.danobase += 3
                self.defesabase -= 2
                break
            elif opc == 2:
                self.classe = "Guardião 🛡️"
                self.hp_max += 5
                self.defesabase += 4
                self.agilidadebase -= 2
                break
            elif opc == 3:
                self.classe = "Duelista 🗡️"
                self.agilidadebase += 4
                self.danobase += 1
                self.hp_max -= 5
                break
            elif opc == 4:
                self.classe = "Vanguarda ⚔️"
                self.danobase += 2
                self.defesabase += 1
                self.agilidadebase += 1
                break
            else:
                print("❌ Opção inválida! Escolha uma classe de 1 a 4.")

        # Travas de segurança para os atributos não ficarem negativos (mínimo de 0 ou 1)
        self.defesabase = max(0, self.defesabase)
        self.agilidadebase = max(0, self.agilidadebase)
        self.danobase = max(1, self.danobase)
        self.hp_max = max(1, self.hp_max)
        
        # Cura totalmente após definir a classe
        self.hp = self.hp_max
        
        print(f"\n✨ O destino está selado! {self.nome} agora é um {self.classe}!")
        sleep(2)