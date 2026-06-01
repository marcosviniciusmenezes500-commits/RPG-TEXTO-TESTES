from utils import ler_inteiro

class Loja:
    def __init__(self):
        self.itens_venda = []

    def adicionar_item(self, item):
        self.itens_venda.append(item)

    def abrir_loja(self, jogador):
        print(f"\n--- 🏪 BEM-VINDO À LOJA DO MERCADOR ERRANTE, {jogador.nome}! ---")
        
        while True:
            print(f"\n💰 Seu Ouro: {jogador.ouro} moedas")
            print("[1] Comprar Equipamentos")
            print("[2] Vender Núcleos e Itens")
            print("[3] Sair da Loja")
            
            opc_menu = ler_inteiro("O que deseja fazer? ")
            
            if opc_menu == 1:
                self.menu_comprar(jogador)
            elif opc_menu == 2:
                self.menu_vender(jogador)
            elif opc_menu == 3:
                print("O Mercador acena a cabeça. Saindo da loja...")
                break
            else:
                print("❌ Opção inválida!")

    def menu_comprar(self, jogador):
        if not self.itens_venda:
            print("A loja está vazia no momento.")
            return

        print("\n--- COMPRAR ITENS ---")
        for i, item in enumerate(self.itens_venda):
            print(f"[{i}] {item.nome} - Dano: {item.dano} | AGI: {item.agilidade} | DEF: {item.defesa} | Preço: {item.valor} moedas")
        
        opc_sair = len(self.itens_venda)
        print(f"[{opc_sair}] Voltar")

        opc = ler_inteiro("\nO que deseja comprar? ")

        if opc == opc_sair:
            return
        
        if 0 <= opc < opc_sair:
            item_escolhido = self.itens_venda[opc]
            
            if jogador.ouro >= item_escolhido.valor:
                jogador.ouro -= item_escolhido.valor
                jogador.inventario.append(item_escolhido) # Usa o append direto para guardar no inventário
                print(f"✅ Você comprou {item_escolhido.nome}! Ouro restante: {jogador.ouro}")
            else:
                print("❌ Ouro insuficiente para comprar este item!")
        else:
            print("❌ Opção inválida!")

    def menu_vender(self, jogador):
        print("\n--- VENDER ITENS ---")
        if not jogador.inventario:
            print("A sua mochila está vazia.")
            return

        for i, item in enumerate(jogador.inventario):
            print(f"[{i}] {item.nome} - Valor de Venda: {item.valor} moedas")
            
        opc_sair = len(jogador.inventario)
        print(f"[{opc_sair}] Voltar")
        
        opc = ler_inteiro("\nO que deseja vender ao Mercador? ")
        
        if opc == opc_sair:
            return
            
        if 0 <= opc < opc_sair:
            item_venda = jogador.inventario[opc]
            
            # Trava de segurança: Não deixar vender o que está equipado
            if item_venda == jogador.arma or item_venda == jogador.anel:
                print(f"❌ O item '{item_venda.nome}' está equipado! Vá ao seu inventário para o remover antes de vender.")
            else:
                jogador.ouro += item_venda.valor
                jogador.inventario.pop(opc) # Remove o item da mochila
                print(f"✅ O Mercador pagou {item_venda.valor} moedas pelo {item_venda.nome}!")
        else:
            print("❌ Opção inválida!")