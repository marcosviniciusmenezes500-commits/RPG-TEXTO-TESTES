from utils import ler_inteiro
from random import randint, choices
from time import sleep
from equipamento import Equipamento

class Jogador:
    def __init__(self, nome, hp):
        self.nome = nome
        self.hp = hp
        self.hp_max = hp
        self.ouro = 50
        self.danobase = 10
        self.agilidadebase = 0
        self.defesabase = 0
        self.armadura = None
        self.inventario = []

        self.nivel = 1
        self.exp = 0
        self.exp_max = 100
        self.pontos_status = 0

        self.arma = None
        self.anel = None

        self.habilidade_usada_andar = False
        self.buff_dano = 0
        self.buff_agilidade = 0
        self.buff_defesa = 0

    def d20(self):
        print("Rolando dado de agilidade...")
        sleep(0.5)
        rolagem = randint(10, 20)
        
        bonus_agilidade = self.agilidadebase + self.buff_agilidade
        
        if self.arma:
            bonus_agilidade += self.arma.agilidade
        if self.anel:
            bonus_agilidade += self.anel.agilidade
            
        total = rolagem + bonus_agilidade
        print(f"Dado: {rolagem} | Bônus: +{bonus_agilidade} | Total: {total}")
        return total

    def d10(self):
        print("Rolando dado de ataque...")
        sleep(0.5)
        d10 = randint(1, 10)
        print(d10)
        return d10

    def danotot(self, d10, d20):
        danotot = d10
        if self.danobase > 0:
            print(f"+ {self.danobase} (Força Base)")
            danotot += self.danobase
            
        if self.arma and self.arma.dano > 0:
            danotot += self.arma.dano
            print(f"+ {self.arma.dano} ({self.arma.nome})")
            
        if self.anel and self.anel.dano > 0:
            danotot += self.anel.dano
            print(f"+ {self.anel.dano} ({self.anel.nome})")

        if self.buff_dano > 0:
            danotot += self.buff_dano
            print(f"+ {self.buff_dano} (Buff)")
            
        if d20 >= 20:
            print("⭐ CRÍTICO! Dano DOBRADO!")
            sleep(0.3)
            danotot *= 2
            
        return danotot

    def adicionar_item_inventario(self, item):
        print(f"{item.nome} foi adicionado no inventário")
        self.inventario.append(item)

    def mostrar_inventario(self):
        if not self.inventario:
            print("Inventário vazio")
            return
        opc = 0
        fim = len(self.inventario)
        while opc != fim:
            for i, item in enumerate(self.inventario):
                print(f"-[{i}] {item.nome} | Dano: {item.dano} | AGI: {item.agilidade} | DEF: {item.defesa} | Tipo: {item.tipo}")
            print(f"-[{fim}] Saída")
            
            if self.arma:
                print(f"Arma equipada: {self.arma.nome}")
            if self.anel:
                print(f"Anel equipado: {self.anel.nome}")
            if self.armadura:
                print(f"Armadura equipada: {self.armadura.nome}")
                
            opc = ler_inteiro("> ")
            if opc == fim:
                return
            if opc < 0 or opc > fim:
                print("❌ Opção inválida!")
                continue
                
            if self.inventario[opc].tipo in ("arma", "anel", "armadura"):
                self.equipar(self.inventario[opc])
    
    def mostrar_status(self):
        dano_extra = 0
        agil_extra = 0
        defesa_extra = 0
        
        for equipamento in [self.arma, self.anel, self.armadura]:
            if equipamento:
                dano_extra += equipamento.dano
                agil_extra += equipamento.agilidade
                defesa_extra += equipamento.defesa

        dano_total = self.danobase + dano_extra
        agil_total = self.agilidadebase + agil_extra
        defesa_total = self.defesabase + defesa_extra

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
            print(f"⭐ PONTOS LIVRES: {self.pontos_status}")
        
        print("\n━━━━━━━━━━━━━━━━━━")
        print("ATRIBUTOS BASE")
        print("━━━━━━━━━━━━━━━━━━")
        print(f"Força Base: {self.danobase}")
        print(f"Agilidade Base: {self.agilidadebase}")
        print(f"Defesa Base: {self.defesabase}")

        print("\nBônus de Equipamentos:")
        if not self.arma and not self.anel and not self.armadura:
            print("Nenhum equipamento.")
        else:
            def formatar_bonus(item):
                bonus = []
                if item.dano != 0: 
                    bonus.append(f"{item.dano:+d} Força")
                if item.agilidade != 0: 
                    bonus.append(f"{item.agilidade:+d} AGI")
                if item.defesa != 0: 
                    bonus.append(f"{item.defesa:+d} DEF")
                return ", ".join(bonus) if bonus else "+0"

            if self.arma:
                print(f"⚔️ {formatar_bonus(self.arma)} ({self.arma.nome})")
                
            if self.anel:
                print(f"💍 {formatar_bonus(self.anel)} ({self.anel.nome})")

            if self.armadura:
                print(f"👕 {formatar_bonus(self.armadura)} ({self.armadura.nome})")

        print("\n━━━━━━━━━━━━━━━━━━")
        print("TOTAL")
        print("━━━━━━━━━━━━━━━━━━")
        print(f"Força Total: {dano_total}")
        print(f"Agilidade Total: {agil_total}")
        print(f"Defesa Total: {defesa_total}")

        print("\n━━━━━━━━━━━━━━━━━━")
        print(f"💰 Ouro: {self.ouro}")
        print("="*40 + "\n")


    def equipar(self, item):
        if item not in self.inventario:
            print(f"❌ {item.nome} não está no inventário")
            return
            
        if item.tipo == 'arma':
            if self.arma:
                print(f"Desequipando {self.arma.nome}")
            self.arma = item
            
        elif item.tipo == "anel":
            if self.anel:
                print(f"Desequipando {self.anel.nome}")
            self.anel = item
            
        elif item.tipo == "armadura":
            if self.armadura:
                print(f"Desequipando {self.armadura.nome}")
            self.armadura = item
            
        print(f"✅ {self.nome} equipou {item.nome}")
        
    
    def rolar_atributos_iniciais(self):
        print(f"\n{'='*40}")
        print(f"🎲 Definindo o destino de {self.nome}...")
        print("Rolando D20...")
        sleep(1.5)
        
        rolagem = randint(1, 20)
        print(f"▶ Resultado: [{rolagem}]\n")
        sleep(0.5)
        
        hp_orig, ouro_orig, dano_orig, agil_orig = self.hp, self.ouro, self.danobase, self.agilidadebase
        
        if rolagem == 1:
            print("💀 DESASTRE! Você começou ferido e endividado.")
            self.hp -= 5
            self.ouro -= 20
            self.danobase -= 2
            
        elif 2 <= rolagem <= 7:
            print("🌧️ AZAR! As coisas não começaram bem.")
            self.hp -= 2
            self.ouro -= 10
            self.danobase -= 1
            
        elif 8 <= rolagem <= 13:
            print("⚖️ COMUM. Um aventureiro padrão.")
            
        elif 14 <= rolagem <= 19:
            print("🍀 SORTE! Você começou com bons recursos.")
            self.hp += 5
            self.ouro += 15
            self.danobase += 2
            self.agilidadebase += 2
            
        elif rolagem == 20:
            print("🌟 LENDÁRIO! Os deuses o abençoaram!")
            self.hp += 10
            self.ouro += 50
            self.danobase += 5
            self.agilidadebase += 5

        self.hp = max(1, self.hp)
        self.ouro = max(0, self.ouro)
        self.danobase = max(1, self.danobase)
        self.hp_max = self.hp
        
        print("[Status Alterados]")
        
        def formatar_mudanca(antigo, novo):
            if novo > antigo: 
                return f"→ {novo} (+{novo-antigo})"
            elif novo < antigo: 
                return f"→ {novo} ({novo-antigo})"
            return f"→ {novo}"

        print(f"❤️ HP:        {hp_orig:2}  {formatar_mudanca(hp_orig, self.hp)}")
        print(f"💰 Ouro:      {ouro_orig:2}  {formatar_mudanca(ouro_orig, self.ouro)}")
        print(f"⚔️ Força:     {dano_orig:2}  {formatar_mudanca(dano_orig, self.danobase)}")
        print(f"💨 Agilidade: {agil_orig:2}  {formatar_mudanca(agil_orig, self.agilidadebase)}")
        print(f"{'='*40}")
        sleep(2)
    
    def ganhar_exp(self, quantidade):
        self.exp += quantidade
        print(f"🌟 {self.nome} recebeu {quantidade} EXP!")
        
        while self.exp >= self.exp_max:
            self.exp -= self.exp_max
            self.nivel += 1
            self.pontos_status += 3
            
            self.exp_max = int(self.exp_max * 1.5)
            
            print(f"\n🎉 {self.nome} SUBIU PARA O NÍVEL {self.nivel}!")
            print("⭐ Você ganhou +3 Pontos de Status!")
            
            classe_nome = getattr(self, 'classe', '')
            
            if "Bárbaro" in classe_nome:
                self.danobase += 1
                print("🪓 +1 Força Base!")
            elif "Guardião" in classe_nome:
                self.defesabase += 1
                print("🛡️ +1 Defesa Base!")
            elif "Duelista" in classe_nome:
                self.agilidadebase += 1
                print("🗡️ +1 Agilidade Base!")
            elif "Vanguarda" in classe_nome:
                self.hp_max += 3
                print("⚔️ +3 HP Máximo!")
            elif "Herói" in classe_nome:
                self.hp_max += 2
                self.danobase += 1
                self.defesabase += 1
                self.agilidadebase += 1
                print("🌟 +2 HP, +1 Força, +1 Defesa, +1 AGI!")
            
            self.hp = self.hp_max
            print("💚 HP restaurado!")
            print(f"📈 Próximo nível: {self.exp_max} EXP")
            print("="*40 + "\n")
            
    def subir_nivel(self):
        self.nivel += 1
        self.exp -= self.exp_max
        self.exp_max = int(self.exp_max * 1.5)
        self.pontos_status += 3
        
        self.hp = self.hp_max
        
        print("\n" + "🌟"*20)
        print(f"🎉 LEVEL UP! {self.nome} alcançou o Nível {self.nivel}!")
        print(f"Você ganhou 3 Pontos de Status! (Total: {self.pontos_status})")
        print("🌟"*20 + "\n")
        sleep(1.5)

    def distribuir_pontos(self):
        if self.pontos_status <= 0:
            print("❌ Você não tem pontos disponíveis.")
            return
            
        while self.pontos_status > 0:
            print(f"\n--- DISTRIBUIR PONTOS ({self.pontos_status} disponíveis) ---")
            print("[1] +5 HP Máximo")
            print("[2] +1 Força")
            print("[3] +1 Agilidade")
            print("[4] +1 Defesa")
            print("[0] Guardar para depois")
            
            opc = ler_inteiro("Onde quer investir? ")
            
            if opc == 1:
                self.hp_max += 5
                self.hp += 5
                self.pontos_status -= 1
                print("❤️ HP Máximo +5!")
            elif opc == 2:
                self.danobase += 1
                self.pontos_status -= 1
                print("⚔️ Força +1!")
            elif opc == 3:
                self.agilidadebase += 1
                self.pontos_status -= 1
                print("💨 Agilidade +1!")
            elif opc == 4:
                self.defesabase += 1
                self.pontos_status -= 1
                print("🛡️ Defesa +1!")
            elif opc == 0:
                print("Pontos guardados!")
                break
            else:
                print("❌ Opção inválida.")
    
    def receber_dano(self, dano_bruto):
        defesa_total = self.defesabase + self.buff_defesa
        
        if self.arma:
            defesa_total += self.arma.defesa
        if self.anel:
            defesa_total += self.anel.defesa
        if self.armadura:
            defesa_total += self.armadura.defesa
        
        dano_final = max(1, dano_bruto - defesa_total)
        self.hp -= dano_final
        return dano_final

    def sortear_origem(self):
        origens = [
            "Mendigo Amaldiçoado", "Desertor Covarde",
            "Camponês Comum", "Guarda Noturno",
            "Mercenário Veterano", "Assassino das Sombras",
            "O Herói Escolhido"
        ]
        
        pesos = [25, 25, 15, 15, 8, 8, 4]
        
        escolha = choices(origens, weights=pesos, k=1)[0]
        self.origem = escolha
        
        print("\n" + "="*50)
        print(f"🎲 Sorteando o passado de {self.nome}...")
        sleep(2)
        print(f"✨ Você é: {escolha.upper()}")
        
        if escolha == "Mendigo Amaldiçoado":
            print("📖 Você viveu nas ruas, amaldiçoado.")
            print("📉 -5 HP, -2 Força, -1 Agilidade")
            self.hp_max -= 5
            self.danobase -= 2
            self.agilidadebase -= 1
            
        elif escolha == "Desertor Covarde":
            print("📖 Você fugiu da guerra, ganhando velocidade mas perdendo força.")
            print("📉 +2 Agilidade, -3 Força, -2 HP")
            self.hp_max -= 2
            self.danobase -= 3
            self.agilidadebase += 2
            
        elif escolha == "Camponês Comum":
            print("📖 Você trabalhou a vida toda, ganhou resistência.")
            print("📈 +5 HP")
            self.hp_max += 5
            
        elif escolha == "Guarda Noturno":
            print("📖 Você era guarda, ganhou experiência mas perdeu reflexos.")
            print("📈 +1 Força, +1 Defesa, -1 Agilidade")
            self.danobase += 1
            self.defesabase += 1
            self.agilidadebase -= 1
            
        elif escolha == "Mercenário Veterano":
            print("📖 Você é um guerreiro experiente e muito hábil.")
            print("📈 +10 HP, +3 Força, +2 Defesa")
            self.hp_max += 10
            self.danobase += 3
            self.defesabase += 2
            
        elif escolha == "Assassino das Sombras":
            print("📖 Você foi treinado como um assassino silencioso.")
            print("📈 +4 Agilidade, +2 Força, +1 Defesa")
            self.agilidadebase += 4
            self.danobase += 2
            self.defesabase += 1
            
        elif escolha == "O Herói Escolhido":
            print("📖 Você é o escolhido pelo destino para purificar a Fenda!")
            print("🌟 +15 HP, +5 Força, +3 AGI, +3 DEF")
            self.hp_max += 15
            self.danobase += 5
            self.agilidadebase += 3
            self.defesabase += 3
            
            espada_heroi = Equipamento("Espada do Herói ⚔️🌟", dano=12, valor=100, agilidade=2, defesa=0, tipo="arma")
            self.inventario.append(espada_heroi)
            self.equipar(espada_heroi)
            print("🎁 Você começa com a Espada do Herói!")

        self.hp_max = max(1, self.hp_max)
        self.danobase = max(1, self.danobase)
        
        self.hp = self.hp_max
        print("="*50 + "\n")
        sleep(2)
    
    def escolher_classe(self):
        print(f"\n{'='*50}")
        print(f"🛡️  SEU CAMINHO MARCIAL  🛡️")
        print("Escolha o seu estilo de combate:\n")

        print("[1] Bárbaro 🪓")
        print("    Foco: Dano brutal. Ignora segurança.")
        print("    Inicial: +10 HP, +3 Força, -2 Defesa")
        print("    Por Nível: +1 Força")
        print("    Habilidade: FÚRIA BERSERKER (Dobra Força)\n")

        print("[2] Guardião 🛡️")
        print("    Foco: Resistência pura. Muralha viva.")
        print("    Inicial: +5 HP, +4 Defesa, -2 AGI")
        print("    Por Nível: +1 Defesa")
        print("    Habilidade: MURALHA ABSOLUTA (Dobra Defesa)\n")

        print("[3] Duelista 🗡️")
        print("    Foco: Reflexos perfeitos. Frágil mas rápido.")
        print("    Inicial: +4 AGI, +1 Força, -5 HP")
        print("    Por Nível: +1 AGI")
        print("    Habilidade: DANÇA DAS LÂMINAS (Boost AGI)\n")

        print("[4] Vanguarda ⚔️")
        print("    Foco: Equilibrado e resistente.")
        print("    Inicial: +2 Força, +1 Defesa, +1 AGI")
        print("    Por Nível: +3 HP (ganho alto)")
        print("    Habilidade: GRITO DE GUERRA (Cura aliados)\n")

        if getattr(self, 'origem', '') == "O Herói Escolhido":
            print("[5] Herói 🌟 (DESBLOQUEADO!)")
            print("    Foco: Equilíbrio perfeito e milagres.")
            print("    Inicial: +5 HP, +2 Força, +2 Defesa, +2 AGI")
            print("    Por Nível: +2 HP, +1 a cada atributo")
            print("    Habilidade: LUZ DA ESPERANÇA (Cura total)\n")

        while True:
            opc = ler_inteiro("Qual será a sua Classe? ")
            
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
            elif opc == 5 and getattr(self, 'origem', '') == "O Herói Escolhido":
                self.classe = "Herói 🌟"
                self.hp_max += 5
                self.danobase += 2
                self.defesabase += 2
                self.agilidadebase += 2
                break
            elif opc == 5:
                print("❌ Apenas o Herói Escolhido pode trilhar este caminho.")
            else:
                print("❌ Opção inválida!")

        self.defesabase = max(0, self.defesabase)
        self.agilidadebase = max(0, self.agilidadebase)
        self.danobase = max(1, self.danobase)
        self.hp_max = max(1, self.hp_max)
        
        self.hp = self.hp_max
        
        print(f"\n✨ {self.nome} é agora um {self.classe}!")
        sleep(2)
    
    def usar_habilidade(self, jogadores_vivos):
        if self.habilidade_usada_andar:
            print(f"❌ {self.nome} já usou a habilidade neste andar!")
            sleep(2)
            return False
            
        classe_nome = getattr(self, 'classe', '')
        if not classe_nome:
            print("❌ Você não possui uma classe.")
            return False

        self.habilidade_usada_andar = True
        
        dano_total_atual = self.danobase + (self.arma.dano if self.arma else 0) + (self.anel.dano if self.anel else 0)
        defesa_total_atual = self.defesabase + (self.armadura.defesa if self.armadura else 0) + (self.anel.defesa if self.anel else 0) + (self.arma.defesa if self.arma else 0)
        agil_total_atual = self.agilidadebase + (self.arma.agilidade if self.arma else 0) + (self.anel.agilidade if self.anel else 0)

        print("\n" + "✨"*20)
        if "Bárbaro" in classe_nome:
            print(f"😡 FÚRIA BERSERKER!")
            print(f"📈 Força DOBRADA (+{dano_total_atual})!")
            self.buff_dano = dano_total_atual
            
        elif "Guardião" in classe_nome:
            print(f"🛡️ MURALHA ABSOLUTA!")
            print(f"📈 Defesa DOBRADA (+{defesa_total_atual})!")
            self.buff_defesa = defesa_total_atual
            
        elif "Duelista" in classe_nome:
            print(f"🗡️ DANÇA DAS LÂMINAS!")
            buff = max(5, agil_total_atual)
            print(f"📈 Agilidade massivamente aumentada (+{buff})!")
            self.buff_agilidade = buff
            
        elif "Vanguarda" in classe_nome:
            print(f"🎺 GRITO DE GUERRA!")
            for j in jogadores_vivos:
                cura = j.hp_max // 2
                j.hp = min(j.hp_max, j.hp + cura)
                print(f"💚 {j.nome} recuperou {cura} HP!")
                
        elif "Herói" in classe_nome:
            print(f"🌟 LUZ DA ESPERANÇA!")
            
            cura_heroi = self.hp_max // 2
            self.hp = min(self.hp_max, self.hp + cura_heroi)
            print(f"💚 {self.nome} curou-se em {cura_heroi} HP!")
            
            for j in jogadores_vivos:
                if j != self:
                    cura_aliado = j.hp_max // 4
                    j.hp = min(j.hp_max, j.hp + cura_aliado)
                    print(f"✨ {j.nome} foi curado em {cura_aliado} HP!")
        print("✨"*20 + "\n")
        
        sleep(2)
        return True

    def remover_buffs(self):
        self.buff_dano = 0
        self.buff_agilidade = 0
        self.buff_defesa = 0

    