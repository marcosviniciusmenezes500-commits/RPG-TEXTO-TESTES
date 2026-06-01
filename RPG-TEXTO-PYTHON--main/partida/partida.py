from jogador import Jogador
from utils import ler_texto

class Partida :
    def __init__(self,jogadores:Jogador):
        self.jogadores = jogadores
        self.mortos:list[Jogador] = []

    @classmethod
    def registrar_jogadores(cls,qj,hp):
        jogadores = []
        for i in range(qj):
            # Presumindo que já implementou a função ler_texto no passo anterior
            nome = ler_texto(f"Introduza o nome do Jogador {i + 1}: ")
            
            # Cria o jogador
            novo_jogador = Jogador(nome, hp)
            
            # Rola o dado do destino para gerar os status aleatórios visualmente
            novo_jogador.rolar_atributos_iniciais()
            
            jogadores.append(novo_jogador)
        return jogadores

    def verificar_mortos (self) :
        for jogador in self.jogadores :
            if jogador.hp <= 0 and jogador not in self.mortos:
                print(f"{jogador.nome} morreu")
                self.mortos.append(jogador)
                

    def lista_mortos(self): #testando
        print("Vivos :")
        for jog in self.jogadores :
            print(jog.nome)
        if self.mortos :
            print("Lista de mortos :")
            for morto in self.mortos :
                print(morto.nome)

    def fim_partida (self):
        # Cria uma lista apenas com os jogadores que ainda têm HP
        vivos = [j for j in self.jogadores if j.hp > 0]
        
        if len(vivos) == 1:
            campeao:Jogador = vivos[0]
            print(f"{campeao.nome} Venceu a partida!")
            return True
            
        elif len(vivos) == 0:
            print("Todo mundo morreu")
            return True

        return False



