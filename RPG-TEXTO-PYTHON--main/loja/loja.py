from utils import ler_inteiro

class Loja:
    def __init__(self):
        self.itens_venda = []

    def adicionar_item(self, item):
        self.itens_venda.append(item)

    def abrir_loja(self, jogador):
        print(f"\n--- 🏪 LOJA DO MERCADOR ERRANTE ---")
        
        while True:
            print(f"\n💰 Ouro: {jogador.ouro} moedas")
            print("[1] Comprar")
            print("[2] Vender")
            print("[3] Sair")
            
            opc_menu = ler_inteiro("O que deseja? ")
            
            if opc_menu == 1:
                self.menu_comprar(jogador)
            elif opc_menu == 2:
                self.menu_vender(jogador)
            elif opc_menu == 3:
                print("O Mercador acena a cabeça. Saindo...")
                break
            else:
                print("❌ Opção inválida!")

    def menu_comprar(self, jogador):
        if not self.itens_venda:
            print("A loja está vazia.")
            return

        print("\n--- COMPRAR ---")
        for i, item in enumerate(self.itens_venda):
            print(f"[{i}] {item.nome} | DMG: {item.dano} | AGI: {item.agilidade} | DEF: {item.defesa} | {item.valor}💰")
        
        opc_sair = len(self.itens_venda)
        print(f"[{opc_sair}] Voltar")

        opc = ler_inteiro("\nO que deseja comprar? ")

        if opc == opc_sair:
            return
        
        if 0 <= opc < opc_sair:
            item_escolhido = self.itens_venda[opc]
            
            if jogador.ouro >= item_escolhido.valor:
                jogador.ouro -= item_escolhido.valor
                jogador.inventario.append(item_escolhido)
                print(f"✅ Você comprou {item_escolhido.nome}! Ouro: {jogador.ouro}")
            else:
                print("❌ Ouro insuficiente!")
        else:
            print("❌ Opção inválida!")

    def menu_vender(self, jogador):
        print("\n--- VENDER ---")
        if not jogador.inventario:
            print("Seu inventário está vazio.")
            return

        for i, item in enumerate(jogador.inventario):
            print(f"[{i}] {item.nome} | {item.valor}💰")
            
        opc_sair = len(jogador.inventario)
        print(f"[{opc_sair}] Voltar")
        
        opc = ler_inteiro("\nO que deseja vender? ")
        
        if opc == opc_sair:
            return
            
        if 0 <= opc < opc_sair:
            item_venda = jogador.inventario[opc]
            
            if item_venda == jogador.arma or item_venda == jogador.anel or item_venda == jogador.armadura:
                print(f"❌ O item '{item_venda.nome}' está equipado!")
            else:
                jogador.ouro += item_venda.valor
                jogador.inventario.pop(opc)
                print(f"✅ O Mercador pagou {item_venda.valor}💰 pelo {item_venda.nome}!")
        else:
            print("❌ Opção inválida!")