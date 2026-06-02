from jogador import Jogador
from utils import ler_texto

class Partida:
    def __init__(self, jogadores):
        self.jogadores = jogadores
        self.mortos = []

    @classmethod
    def registrar_jogadores(cls, qj, hp):
        jogadores = []
        for i in range(qj):
            nome = ler_texto(f"Nome do Jogador {i + 1}: ")
            novo_jogador = Jogador(nome, hp)
            novo_jogador.rolar_atributos_iniciais()
            jogadores.append(novo_jogador)
        return jogadores

    def verificar_mortos(self):
        for jogador in self.jogadores:
            if jogador.hp <= 0 and jogador not in self.mortos:
                print(f"💀 {jogador.nome} morreu!")
                self.mortos.append(jogador)

    def fim_partida(self):
        vivos = [j for j in self.jogadores if j.hp > 0]
        
        if len(vivos) == 1:
            campeao = vivos[0]
            print(f"\n🏆 {campeao.nome} VENCEU A PARTIDA!")
            return True
            
        elif len(vivos) == 0:
            print("\n💀 Todos foram derrotados!")
            return True

        return False



