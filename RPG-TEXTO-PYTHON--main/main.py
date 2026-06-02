from jogador import Jogador
from equipamento import Equipamento
from combate import Combate
from partida import Partida
from loja import Loja
from masmorra import Masmorra
from utils import ler_inteiro
from random import choice
from time import sleep

print("\n" + "="*60)
print("  ⚔️  BEM-VINDO À FENDA DE ÉBANO  ⚔️")
print("  RPG de Texto - Aventura Multijogador")
print("="*60 + "\n")

while True:
    qj = ler_inteiro("Quantos jogadores teremos na partida? ")
    if qj >= 1:
        break
    print("❌ Erro: O jogo necessita de, pelo menos, 1 jogador para iniciar.")

jogadores = Partida.registrar_jogadores(qj=qj, hp=20)
partida = Partida(jogadores)

for j in jogadores:
    j.sortear_origem()
    j.escolher_classe()

loja_jogo = Loja()
loja_jogo.adicionar_item(Equipamento("Espada de Fogo 🔥", dano=15, valor=30, agilidade=0, tipo="arma"))
loja_jogo.adicionar_item(Equipamento("Adaga Venenosa 🐍", dano=8, valor=25, agilidade=5, tipo="arma"))
loja_jogo.adicionar_item(Equipamento("Anel do Vento 🌪️", dano=0, valor=25, agilidade=15, tipo="anel"))
loja_jogo.adicionar_item(Equipamento("Anel do Titã 🪨", dano=10, valor=40, agilidade=0, tipo="anel"))
loja_jogo.adicionar_item(Equipamento("Túnica de Couro 🧥", dano=0, valor=20, agilidade=2, defesa=3, tipo="armadura"))
loja_jogo.adicionar_item(Equipamento("Armadura de Ferro 🛡️", dano=0, valor=50, agilidade=-2, defesa=8, tipo="armadura"))
loja_jogo.adicionar_item(Equipamento("Armadura com Espinhos 🦔", dano=2, valor=40, agilidade=0, defesa=5, tipo="armadura"))

masmorra = Masmorra(jogadores)
jogatual = 0

while True:
    partida.verificar_mortos()
    vivos = [j for j in jogadores if j.hp > 0]
    
    if len(vivos) == 0:
        print("\n💀 GAME OVER! A Fenda de Ébano consumiu as vossas almas.")
        break

    if jogatual >= len(jogadores):
        jogatual = 0
        if masmorra.monstros_atuais:
            print("\n" + "="*50)
            print("👹 TURNO DOS INIMIGOS!")
            print("="*50)
            sleep(1)
            for m in masmorra.monstros_atuais:
                if m.hp > 0:
                    alvo = choice(vivos)
                    print(f"\n{m.nome} avança furiosamente contra {alvo.nome}!")
                    sleep(0.8)
                    d20_m = m.d20()
                    if d20_m > 10:
                        dano_bruto = m.calcular_dano(d20_m)
                        dano_real = alvo.receber_dano(dano_bruto)
                        print(f"🩸 {alvo.nome} sofreu {dano_real} de dano!")
                    else:
                        print(f"💨 {alvo.nome} conseguiu esquivar-se!")
                    sleep(0.8)
            print("\n" + "="*50 + "\n")
            continue

    jogador_turno = jogadores[jogatual]

    if jogador_turno.hp <= 0:
        jogatual += 1
        continue

    if masmorra.monstros_atuais:
        print(f"\n🗡️ Turno de Combate: {jogador_turno.nome} | HP: {jogador_turno.hp}/{jogador_turno.hp_max}")
        print("\n[1] Atacar            [2] Inventário")
        print("[3] Status            [4] Habilidade Especial")
        
        opc = ler_inteiro("A sua ação: ")
        
        if opc == 1:
            combate = Combate(jogador_turno, jogadores, masmorra.monstros_atuais)
            combate.ataque_jogador()
            
            monstros_vivos = []
            for m in masmorra.monstros_atuais:
                if m.hp <= 0:
                    exp_ganha = m.gerar_exp()
                    print(f"✨ O grupo recebe {exp_ganha} EXP pelo abate de {m.nome}!")
                    
                    loot = m.dropar_loot()
                    if loot:
                        print(f"🎁 {m.nome} deixou cair: {loot.nome}!")
                        jogador_turno.inventario.append(loot)
                    
                    vivos_atuais = [j for j in jogadores if j.hp > 0]
                    for j in vivos_atuais:
                        j.ganhar_exp(exp_ganha)
                else:
                    monstros_vivos.append(m)
                    
            masmorra.monstros_atuais = monstros_vivos
            jogatual += 1
            
        elif opc == 2:
            jogador_turno.mostrar_inventario()
        elif opc == 3:
            jogador_turno.mostrar_status()
        elif opc == 4:
            jogador_turno.usar_habilidade([j for j in jogadores if j.hp > 0])
            continue
        if not masmorra.monstros_atuais:
            for j in jogadores:
                j.remover_buffs()
    else:
        print(f"\n🗺️ Turno de Exploração: {jogador_turno.nome} | HP: {jogador_turno.hp}/{jogador_turno.hp_max}")
        print("\n[1] Avançar para próxima sala   [2] Loja do Mercador")
        print("[3] Inventário                  [4] Status")
        print("[5] Distribuir Pontos           [6] Passar a vez")
        
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
            outros_vivos = [j for j in jogadores if j.hp > 0 and j != jogador_turno]
            
            if not outros_vivos:
                print("❌ Você é o único sobrevivente!")
            else:
                print("\n--- Escolha o próximo jogador ---")
                for i, j in enumerate(jogadores):
                    if j.hp > 0 and j != jogador_turno:
                        print(f"[{i}] {j.nome}")
                
                while True:
                    escolha = ler_inteiro("Digite o número: ")
                    if 0 <= escolha < len(jogadores) and jogadores[escolha].hp > 0 and jogadores[escolha] != jogador_turno:
                        jogatual = escolha
                        print(f"\n🔄 Turno passado para {jogadores[escolha].nome}!")
                        break
                    print("❌ Opção inválida!")