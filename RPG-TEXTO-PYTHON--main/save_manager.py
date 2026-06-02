import json
import os
from datetime import datetime
from pathlib import Path


class SaveManager:
    """Gerenciador de persistência do jogo usando JSON."""
    
    SAVE_DIR = Path("./saves")
    
    def __init__(self):
        """Inicializa o gerenciador de saves."""
        self.SAVE_DIR.mkdir(exist_ok=True)
    
    def salvar_partida(self, partida, nome_save=None):
        """
        Salva a partida atual em um arquivo JSON.
        
        Args:
            partida: Objeto Partida a ser salvo
            nome_save (str): Nome do save (default: timestamp)
        
        Returns:
            str: Caminho do arquivo salvo
        """
        if not nome_save:
            nome_save = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        caminho_save = self.SAVE_DIR / f"{nome_save}.json"
        
        dados_partida = {
            "data_salvo": datetime.now().isoformat(),
            "jogadores": [],
            "andar_atual": 0,
            "sala_atual": 0,
        }
        
        # Salvar dados dos jogadores
        for jogador in partida.jogadores:
            dados_jogador = self._serializar_jogador(jogador)
            dados_partida["jogadores"].append(dados_jogador)
        
        # Salvar dados da masmorra se existir
        if hasattr(partida, 'masmorra') and partida.masmorra:
            dados_partida["andar_atual"] = partida.masmorra.andar_atual
            dados_partida["sala_atual"] = partida.masmorra.sala_atual
        
        # Escrever JSON
        with open(caminho_save, 'w', encoding='utf-8') as f:
            json.dump(dados_partida, f, indent=4, ensure_ascii=False)
        
        print(f"\n✅ Partida salva em: {caminho_save}")
        return str(caminho_save)
    
    def carregar_partida(self, nome_save):
        """
        Carrega uma partida salva.
        
        Args:
            nome_save (str): Nome do save (sem extensão .json)
        
        Returns:
            dict: Dados da partida
        """
        caminho_save = self.SAVE_DIR / f"{nome_save}.json"
        
        if not caminho_save.exists():
            print(f"❌ Arquivo de save '{nome_save}' não encontrado!")
            return None
        
        try:
            with open(caminho_save, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            print(f"✅ Partida carregada de: {caminho_save}")
            return dados
        except json.JSONDecodeError:
            print(f"❌ Erro ao ler arquivo de save!")
            return None
    
    def listar_saves(self):
        """Lista todos os arquivos de save disponíveis."""
        saves = []
        
        if not self.SAVE_DIR.exists():
            return saves
        
        for arquivo in self.SAVE_DIR.glob("*.json"):
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                    saves.append({
                        "nome": arquivo.stem,
                        "data": dados.get("data_salvo", "Desconhecida"),
                        "jogadores": len(dados.get("jogadores", [])),
                        "andar": dados.get("andar_atual", 0)
                    })
            except:
                pass
        
        return sorted(saves, key=lambda x: x["data"], reverse=True)
    
    def deletar_save(self, nome_save):
        """Deleta um arquivo de save."""
        caminho_save = self.SAVE_DIR / f"{nome_save}.json"
        
        if caminho_save.exists():
            caminho_save.unlink()
            print(f"✅ Save '{nome_save}' deletado!")
            return True
        else:
            print(f"❌ Save '{nome_save}' não encontrado!")
            return False
    
    def _serializar_jogador(self, jogador):
        """Converte um jogador em dicionário JSON."""
        dados = {
            "nome": jogador.nome,
            "hp": jogador.hp,
            "hp_max": jogador.hp_max,
            "ouro": jogador.ouro,
            "nucleos_monstro": jogador.nucleos_monstro,
            "danobase": jogador.danobase,
            "agilidadebase": jogador.agilidadebase,
            "defesabase": jogador.defesabase,
            "nivel": jogador.nivel,
            "exp": jogador.exp,
            "exp_max": jogador.exp_max,
            "pontos_status": jogador.pontos_status,
            "habilidade_usada_andar": jogador.habilidade_usada_andar,
            "buff_dano": jogador.buff_dano,
            "buff_agilidade": jogador.buff_agilidade,
            "buff_defesa": jogador.buff_defesa,
            
            # Equipamentos
            "arma": self._serializar_equipamento(jogador.arma) if jogador.arma else None,
            "armadura": self._serializar_equipamento(jogador.armadura) if jogador.armadura else None,
            "anel": self._serializar_equipamento(jogador.anel) if jogador.anel else None,
            
            # Inventário e consumíveis
            "inventario": [self._serializar_equipamento(item) for item in jogador.inventario],
            "consumiveis": [self._serializar_consumivel(c) for c in jogador.consumiveis],
        }
        return dados
    
    def _serializar_equipamento(self, equipamento):
        """Converte um equipamento em dicionário."""
        if not equipamento:
            return None
        
        return {
            "nome": equipamento.nome,
            "dano": equipamento.dano,
            "valor": equipamento.valor,
            "agilidade": equipamento.agilidade,
            "defesa": equipamento.defesa,
            "tipo": equipamento.tipo,
            "nivel_upgrade": getattr(equipamento, 'nivel_upgrade', 0)
        }
    
    def _serializar_consumivel(self, consumivel):
        """Converte um consumível em dicionário."""
        dados = {
            "nome": consumivel.nome,
            "valor": consumivel.valor,
            "tipo": consumivel.__class__.__name__,
        }
        
        # Dados específicos por tipo de consumível
        if hasattr(consumivel, 'cura'):
            dados["cura"] = consumivel.cura
        if hasattr(consumivel, 'mana'):
            dados["mana"] = consumivel.mana
        
        return dados
    
    def desserializar_jogador(self, dados_jogador, Jogador):
        """Reconstrói um jogador a partir de dados JSON."""
        from equipamento import Equipamento
        from itens import Poção, PocaoMana
        
        jogador = Jogador(dados_jogador["nome"], dados_jogador["hp_max"])
        
        # Restaurar atributos básicos
        jogador.hp = dados_jogador["hp"]
        jogador.ouro = dados_jogador["ouro"]
        jogador.nucleos_monstro = dados_jogador.get("nucleos_monstro", 0)
        jogador.danobase = dados_jogador["danobase"]
        jogador.agilidadebase = dados_jogador["agilidadebase"]
        jogador.defesabase = dados_jogador["defesabase"]
        jogador.nivel = dados_jogador["nivel"]
        jogador.exp = dados_jogador["exp"]
        jogador.exp_max = dados_jogador["exp_max"]
        jogador.pontos_status = dados_jogador["pontos_status"]
        jogador.habilidade_usada_andar = dados_jogador["habilidade_usada_andar"]
        jogador.buff_dano = dados_jogador["buff_dano"]
        jogador.buff_agilidade = dados_jogador["buff_agilidade"]
        jogador.buff_defesa = dados_jogador["buff_defesa"]
        
        # Restaurar equipamentos
        if dados_jogador.get("arma"):
            jogador.arma = self._desserializar_equipamento(dados_jogador["arma"])
        if dados_jogador.get("armadura"):
            jogador.armadura = self._desserializar_equipamento(dados_jogador["armadura"])
        if dados_jogador.get("anel"):
            jogador.anel = self._desserializar_equipamento(dados_jogador["anel"])
        
        # Restaurar inventário
        jogador.inventario = [
            self._desserializar_equipamento(item)
            for item in dados_jogador.get("inventario", [])
        ]
        
        # Restaurar consumíveis
        jogador.consumiveis = [
            self._desserializar_consumivel(c)
            for c in dados_jogador.get("consumiveis", [])
        ]
        
        return jogador
    
    def _desserializar_equipamento(self, dados):
        """Reconstrói um equipamento a partir de dados JSON."""
        from equipamento import Equipamento
        
        equip = Equipamento(
            nome=dados["nome"],
            dano=dados["dano"],
            valor=dados["valor"],
            agilidade=dados["agilidade"],
            defesa=dados["defesa"],
            tipo=dados["tipo"]
        )
        equip.nivel_upgrade = dados.get("nivel_upgrade", 0)
        return equip
    
    def _desserializar_consumivel(self, dados):
        """Reconstrói um consumível a partir de dados JSON."""
        from itens import Poção, PocaoMana
        
        tipo = dados["tipo"]
        
        if tipo == "Poção":
            return Poção(
                nome=dados["nome"],
                cura=dados.get("cura", 30),
                valor=dados["valor"]
            )
        elif tipo == "PocaoMana":
            return PocaoMana(
                nome=dados["nome"],
                mana=dados.get("mana", 20),
                valor=dados["valor"]
            )
        
        return None


def menu_saves():
    """Menu interativo para gerenciar saves."""
    from utils import ler_inteiro
    
    manager = SaveManager()
    
    while True:
        saves = manager.listar_saves()
        
        print(f"\n{'='*60}")
        print("  GERENCIADOR DE SAVES")
        print(f"{'='*60}")
        
        if saves:
            print("\nSaves disponíveis:")
            for i, save in enumerate(saves, 1):
                print(f"[{i}] {save['nome']} - Andar {save['andar']} - {save['data']}")
        else:
            print("\nNenhum save disponível.")
        
        print("\n[1] Carregar Save")
        print("[2] Deletar Save")
        print("[3] Voltar")
        
        opcao = ler_inteiro("Escolha uma opção: ")
        
        if opcao == 1:
            if saves:
                num = ler_inteiro("Digite o número do save: ")
                if 1 <= num <= len(saves):
                    return saves[num - 1]["nome"]
        elif opcao == 2:
            if saves:
                num = ler_inteiro("Digite o número do save a deletar: ")
                if 1 <= num <= len(saves):
                    manager.deletar_save(saves[num - 1]["nome"])
        elif opcao == 3:
            return None
