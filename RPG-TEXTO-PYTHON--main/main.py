from jogador import Jogador
from equipamento import Equipamento
from combate import Combate
from partida import Partida
from loja import Loja
from masmorra import Masmorra
from utils import ler_inteiro
from itens import criar_pocoes_loja
from save_manager import SaveManager
from random import choice
from time import sleep

print("\n" + "="*60)
print("  ⚔️  BEM-VINDO À FENDA DE ÉBANO  ⚔️")
print("  RPG de Texto - Aventura Multijogador")
print("="*60 + "\n")

# Menu inicial
save_manager = SaveManager()
saves_disponiveis = save_manager.listar_saves()

print("[1] Nova Partida")
if saves_disponiveis:
    print("[2] Carregar Partida")
    menu_opt = ler_inteiro("Escolha uma opção: ")
else:
    menu_opt = 1

carregar_partida = False
if menu_opt == 2 and saves_disponiveis:
    print("\nSaves disponíveis:")
    for i, save in enumerate(saves_disponiveis, 1):
        print(f"[{i}] {save['nome']} - Andar {save['andar']}")
    
    escolha = ler_inteiro("Escolha o save: ")
    if 1 <= escolha <= len(saves_disponiveis):
        nome_save = saves_disponiveis[escolha - 1]["nome"]
        dados_carregados = save_manager.carregar_partida(nome_save)
        if dados_carregados:
            # Carregar partida será implementado aqui
            print("⚠️  Funcionalidade de carregamento em desenvolvimento.")
            carregar_partida = False

if not carregar_partida:
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

for consumivel in criar_pocoes_loja():
    loja_jogo.adicionar_consumivel(consumivel)

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
        print("[5] Usar Consumível")
        
        opc = ler_inteiro("A sua ação: ")

        if opc == 1:
            combate = Combate(jogador_turno, jogadores, masmorra.monstros_atuais)
            combate.ataque_jogador()

            monstros_vivos = []
            for m in masmorra.monstros_atuais:
                if m.hp <= 0:
                    exp_ganha = m.gerar_exp()
                    
                    # Recompensa especial para Bosses
                    if hasattr(m, 'eh_boss') and m.eh_boss:
                        exp_ganha = int(exp_ganha * 3)  # 3x EXP
                        print(f"\n🏆 BOSS DERROTADO! 🏆")
                        print(f"✨ O grupo recebe {exp_ganha} EXP!")
                    else:
                        print(f"✨ O grupo recebe {exp_ganha} EXP pelo abate de {m.nome}!")

                    loot = m.dropar_loot()
                    if loot:
                        if loot.get("tipo") == "nucleo":
                            nucleos = loot.get("nucleos", 1)
                            vivos_atuais = [j for j in jogadores if j.hp > 0]
                            nucleos_por_jogador = nucleos // len(vivos_atuais) if vivos_atuais else nucleos
                            
                            for j in vivos_atuais:
                                j.nucleos_monstro += nucleos_por_jogador
                            
                            print(f"🧿 {m.nome} deixou cair {nucleos} Núcleo(s) de Monstro! (+{nucleos_por_jogador} cada)")
                            
                            # Bônus de ouro para bosses
                            if loot.get("raro"):
                                bonus_ouro = loot.get("bonus_ouro", 0)
                                ouro_por_jogador = bonus_ouro // len(vivos_atuais) if vivos_atuais else bonus_ouro
                                for j in vivos_atuais:
                                    j.ouro += ouro_por_jogador
                                print(f"💰 Bônus de ouro por derrotar o boss: +{ouro_por_jogador} cada!")
                        else:
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
        elif opc == 5:
            indice_consumivel = jogador_turno.mostrar_consumiveis()
            if indice_consumivel is not None:
                jogador_turno.usar_consumivel(indice_consumivel)
                jogatual += 1

        if not masmorra.monstros_atuais:
            for j in jogadores:
                j.remover_buffs()
    else:
        print(f"\n🗺️ Turno de Exploração: {jogador_turno.nome} | HP: {jogador_turno.hp}/{jogador_turno.hp_max}")
        print("\n[1] Avançar para próxima sala   [2] Loja do Mercador")
        print("[3] Inventário                  [4] Status")
        print("[5] Distribuir Pontos           [6] Usar Consumível")
        print("[7] Árvore de Passivas          [8] Salvar Partida")
        print("[9] Carregar Partida            [10] Passar a vez")

        opc = ler_inteiro("O que deseja fazer? ")

        if opc == 1:
            estado = masmorra.avancar_sala()
            if estado == "VITORIA":
                break
            jogatual += 1
        elif opc == 2:
            loja_jogo.abrir_loja(jogador_turno)
        elif opc == 3:
            jogador_turno.mostrar_inventario()
        elif opc == 4:
            jogador_turno.mostrar_status()
        elif opc == 5:
            jogador_turno.distribuir_pontos()
        elif opc == 6:
            indice_consumivel = jogador_turno.mostrar_consumiveis()
            if indice_consumivel is not None:
                jogador_turno.usar_consumivel(indice_consumivel)
                jogatual += 1
        elif opc == 7:
            # Acessar Árvore de Passivas
            jogador_turno.passivas.mostrar_menu_passivas(jogador_turno)
        elif opc == 8:
            # Salvar partida
            save_manager = SaveManager()
            partida.masmorra = masmorra
            nome_save = input("\nDigite o nome para o save (ou deixe em branco para automático): ").strip()
            save_manager.salvar_partida(partida, nome_save if nome_save else None)
        elif opc == 9:
            # Carregar partida (será implementado após reinicialização)
            print("⚠️  Para carregar uma partida, reinicie o jogo e escolha essa opção no menu inicial.")
        elif opc == 10:
            pass  # Passa a vez
        else:
            print("❌ Opção inválida!")

