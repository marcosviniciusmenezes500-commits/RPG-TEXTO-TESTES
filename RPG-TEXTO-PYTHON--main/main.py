from jogador import Jogador
from equipamento import Equipamento
from combate import Combate
from partida import Partida
from loja import Loja
from masmorra import Masmorra
from utils import ler_inteiro
from random import choice
from time import sleep

print("\n" + "="*50)
print("⚔️ BEM-VINDO À FENDA DE ÉBANO ⚔️")
print("="*50 + "\n")

# 1. Configurações Iniciais
while True:
    qj = ler_inteiro("Quantos jogadores teremos na partida? ")
    if qj >= 2:
        break
    print("Erro: O jogo necessita de, pelo menos, 2 jogadores para iniciar.")

# Regista os jogadores com 20 de HP base
jogadores = Partida.registrar_jogadores(qj=qj, hp=20)
partida = Partida(jogadores)

# 2. Configuração da Loja (O Mercador Errante)
loja_jogo = Loja()
loja_jogo.adicionar_item(Equipamento("Espada de Fogo 🔥", dano=15, valor=30, agilidade=0, tipo="arma"))
loja_jogo.adicionar_item(Equipamento("Adaga Venenosa 🐍", dano=8, valor=25, agilidade=5, tipo="arma"))
loja_jogo.adicionar_item(Equipamento("Anel do Vento 🌪️", dano=0, valor=25, agilidade=15, tipo="anel"))
loja_jogo.adicionar_item(Equipamento("Anel do Titã 🪨", dano=10, valor=40, agilidade=0, tipo="anel"))
loja_jogo.adicionar_item(Equipamento("Túnica de Couro 🧥", dano=0, valor=20, agilidade=2, defesa=3, tipo="armadura"))
loja_jogo.adicionar_item(Equipamento("Armadura de Ferro 🛡️", dano=0, valor=50, agilidade=-2, defesa=8, tipo="armadura"))
loja_jogo.adicionar_item(Equipamento("Armadura com Espinhos 🦔", dano=2, valor=40, agilidade=0, defesa=5, tipo="armadura"))

# 3. Inicia a Masmorra
masmorra = Masmorra(jogadores)
jogatual = 0

# --- CICLO PRINCIPAL DO JOGO ---
while True:
    partida.verificar_mortos()
    vivos = [j for j in jogadores if j.hp > 0]
    
    # Condição de Derrota
    if len(vivos) == 0:
        print("\n💀 GAME OVER! A Fenda de Ébano consumiu as vossas almas.")
        break

    # Se a rodada dos jogadores acabou, é o TURNO DOS MONSTROS (se houver algum vivo)
    if jogatual >= len(jogadores):
        jogatual = 0
        if masmorra.monstros_atuais:
            print("\n" + "="*40)
            print("👹 TURNO DOS INIMIGOS!")
            sleep(1)
            for m in masmorra.monstros_atuais:
                if m.hp > 0:
                    alvo = choice(vivos) # Monstro escolhe um jogador vivo aleatório
                    print(f"\nO {m.nome} avança furiosamente contra {alvo.nome}!")
                    sleep(1)
                    d20_m = m.d20()
                    if d20_m > 10: # Dificuldade padrão para acerto
                        dano_bruto = m.calcular_dano(d20_m)
                        
                        # NOVA LÓGICA DE DEFESA
                        dano_real = alvo.receber_dano(dano_bruto) 
                        
                        print(f"🩸 {alvo.nome} sofreu {dano_real} de dano! (Ataque original: {dano_bruto})")
                    else:
                        print(f"💨 {alvo.nome} conseguiu esquivar-se do ataque de {m.nome}!")
                    sleep(1)
            print("="*40 + "\n")
            continue # Reinicia o ciclo para verificar se alguém morreu com os ataques

    jogador_turno = jogadores[jogatual]

    # Se o jogador estiver morto, passa a vez
    if jogador_turno.hp <= 0:
        jogatual += 1
        continue

    # ==========================================
    # ESTADO 1: MODO COMBATE (Há monstros na sala)
    # ==========================================
    if masmorra.monstros_atuais:
        print(f"\n🗡️ Turno de Combate: {jogador_turno.nome} (HP: {jogador_turno.hp}/{jogador_turno.hp_max})")
        print("[1] Atacar")
        print("[2] Ver Inventário")
        print("[3] Ver Status")
        
        opc = ler_inteiro("A sua ação: ")
        
        if opc == 1:
            combate = Combate(jogador_turno, jogadores, masmorra.monstros_atuais)
            combate.ataque_jogador()
            
            # Após o ataque, verificar mortes e distribuir EXP e Ouro
            monstros_vivos = []
            for m in masmorra.monstros_atuais:
                if m.hp <= 0:
                    exp_ganha = m.gerar_exp()
                    print(f"✨ O grupo recebe {exp_ganha} EXP pelo abate de {m.nome}!")
                    
                    # Sistema de Drop de Núcleos
                    loot = m.dropar_loot()
                    if loot:
                        print(f"🎁 {m.nome} deixou cair um item brilhante: {loot.nome}!")
                        # O loot vai para o jogador que deu o golpe final
                        jogador_turno.inventario.append(loot)
                        print(f"🎒 Guardado na mochila de {jogador_turno.nome}.")
                    else:
                        print(f"💨 O {m.nome} desintegrou-se e não deixou nenhum núcleo para trás.")
                    
                    # Distribuir EXP para todos os vivos
                    vivos_atuais = [j for j in jogadores if j.hp > 0]
                    for j in vivos_atuais:
                        j.ganhar_exp(exp_ganha)
                else:
                    monstros_vivos.append(m)
                    
            masmorra.monstros_atuais = monstros_vivos # Atualiza a lista da sala
            jogatual += 1 # Passa a vez
            
        elif opc == 2:
            jogador_turno.mostrar_inventario()
        elif opc == 3:
            jogador_turno.mostrar_status()

    # ==========================================
    # ESTADO 2: MODO EXPLORAÇÃO (Sala limpa)
    # ==========================================
    else:
        print(f"\n🗺️ Turno de Exploração: {jogador_turno.nome} (HP: {jogador_turno.hp}/{jogador_turno.hp_max})")
        print("[1] Avançar para a próxima sala")
        print("[2] Loja do Mercador Errante")
        print("[3] Ver Inventário")
        print("[4] Ver Status")
        print("[5] Distribuir Pontos de Status")
        print("[6] Passar a vez para outro jogador se preparar")
        
        opc = ler_inteiro("O que deseja fazer? ")
        
        if opc == 1:
            estado = masmorra.avancar_sala()
            if estado == "VITORIA":
                break
            jogatual += 1 # O turno avança depois de explorar
        elif opc == 2:
            loja_jogo.abrir_loja(jogador_turno)
        elif opc == 3:
            jogador_turno.mostrar_inventario()
        elif opc == 4:
            jogador_turno.mostrar_status()
        elif opc == 5:
            jogador_turno.distribuir_pontos()
        elif opc == 6:
            # Lista quem está vivo e não é o jogador atual
            outros_vivos = [j for j in jogadores if j.hp > 0 and j != jogador_turno]
            
            if not outros_vivos:
                print("❌ Você é o único sobrevivente! Não há para quem passar a vez.")
            else:
                print("\n--- ESCOLHA QUEM VAI SE PREPARAR ---")
                for i, j in enumerate(jogadores):
                    if j.hp > 0 and j != jogador_turno:
                        print(f"[{i}] 👤 {j.nome}")
                
                while True:
                    escolha = ler_inteiro("Digite o número do jogador: ")
                    # Valida se o índice existe, se o jogador está vivo e se não é ele mesmo
                    if 0 <= escolha < len(jogadores) and jogadores[escolha].hp > 0 and jogadores[escolha] != jogador_turno:
                        jogatual = escolha # Altera diretamente o dono do turno!
                        print(f"\n🔄 Iniciativa passada para {jogadores[escolha].nome}!")
                        break
                    print("❌ Escolha inválida. Digite o número de um aliado vivo.")