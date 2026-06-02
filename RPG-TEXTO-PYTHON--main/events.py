from random import randint, choice
from time import sleep
from utils import ler_inteiro


class EnigmaSala:
    """Representa um enigma em uma sala."""
    
    ENIGMAS = [
        {
            "pergunta": "Tenho cidades, mas nenhuma casa. Tenho montanhas, mas nenhuma árvore. O que sou?",
            "respostas": ["mapa", "um mapa"],
            "recompensa_ouro": 50,
            "recompensa_descricao": "Um mapa antigo com marcações de tesouro!"
        },
        {
            "pergunta": "Quanto mais você tira, mais deixa para trás. O que sou?",
            "respostas": ["pegadas", "pegada", "footsteps"],
            "recompensa_ouro": 40,
            "recompensa_descricao": "Um artefato misterioso!"
        },
        {
            "pergunta": "Sou leve como uma pena, mas o homem mais forte não consegue me segurar por mais de um minuto. O que sou?",
            "respostas": ["respiracao", "hálito", "ar", "breath"],
            "recompensa_ouro": 60,
            "recompensa_descricao": "Uma poção rara!"
        },
        {
            "pergunta": "Falo sem boca e ouço sem ouvidos. Tenho ninguém, mas vivo no vento. O que sou?",
            "respostas": ["eco", "echos"],
            "recompensa_ouro": 45,
            "recompensa_descricao": "Um cristal brilhante!"
        },
    ]
    
    @staticmethod
    def gerar_enigma():
        """Gera um enigma aleatório."""
        return choice(EnigmaSala.ENIGMAS)
    
    @staticmethod
    def resolver_enigma(enigma, resposta_jogador):
        """Verifica se a resposta está correta."""
        resposta_normalizada = resposta_jogador.lower().strip()
        return resposta_normalizada in enigma["respostas"]


class NPCPerdido:
    """Representa um NPC perdido encontrado em uma sala."""
    
    NPCS = [
        {
            "nome": "Mercenário Ferido",
            "descricao": "Um guerreiro machucado que pede ajuda.",
            "opcoes": [
                {"texto": "Ajudar", "recompensa": 100, "resultado": "O mercenário agradece e oferece ouro!"},
                {"texto": "Ignorar", "recompensa": 0, "resultado": "Você segue em frente."},
                {"texto": "Explorar seus pertences", "recompensa": 200, "resultado": "Você encontra ouro escondido!"}
            ]
        },
        {
            "nome": "Comerciante Perdido",
            "descricao": "Um mercador que se viu preso na masmorra.",
            "opcoes": [
                {"texto": "Ajudar", "recompensa": 80, "resultado": "O comerciante oferece um desconto em suas compras!"},
                {"texto": "Roubar", "recompensa": 150, "resultado": "Você rouba parte de seu ouro!"},
                {"texto": "Ignorar", "recompensa": 0, "resultado": "Você segue em frente."}
            ]
        },
        {
            "nome": "Prisioneiro",
            "descricao": "Um homem acorrentado que implora por libertação.",
            "opcoes": [
                {"texto": "Libertar", "recompensa": 120, "resultado": "O prisioneiro se oferece para ajudá-lo!"},
                {"texto": "Deixar preso", "recompensa": 50, "resultado": "Você toma o ouro dele e segue."},
                {"texto": "Ignorar", "recompensa": 0, "resultado": "Você segue em frente."}
            ]
        },
        {
            "nome": "Mago Errante",
            "descricao": "Um mago perdido que tenta encontrar o caminho de volta.",
            "opcoes": [
                {"texto": "Ajudar", "recompensa": 200, "resultado": "O mago oferece um feitiço raro!"},
                {"texto": "Desafiar", "recompensa": 100, "resultado": "Vocês trocam feitiços!"},
                {"texto": "Ignorar", "recompensa": 0, "resultado": "Você segue em frente."}
            ]
        },
    ]
    
    @staticmethod
    def gerar_npc():
        """Gera um NPC aleatório."""
        return choice(NPCPerdido.NPCS)


class SalaSecreta:
    """Representa uma sala secreta encontrada através de detecção."""
    
    SALAS = [
        {
            "nome": "Câmara do Tesouro",
            "descricao": "Uma sala brilhante repleta de ouro e jóias!",
            "ouro": randint(200, 500),
            "nucleos": randint(5, 10)
        },
        {
            "nome": "Biblioteca Antiga",
            "descricao": "Milhares de livros antigos com conhecimento perdido.",
            "ouro": randint(100, 300),
            "nucleos": randint(2, 5)
        },
        {
            "nome": "Câmara de Cristal",
            "descricao": "Uma câmara toda feita de cristal que brilha com poder mágico.",
            "ouro": randint(150, 400),
            "nucleos": randint(3, 8)
        },
        {
            "nome": "Cripta de Heróis",
            "descricao": "Túmulos de guerreiros antigos com relíquias valiosas.",
            "ouro": randint(180, 450),
            "nucleos": randint(4, 9)
        },
    ]
    
    @staticmethod
    def gerar_sala_secreta():
        """Gera uma sala secreta aleatória."""
        return choice(SalaSecreta.SALAS)


class SistemaAcampamento:
    """Sistema de acampamento para descanso e recuperação."""
    
    @staticmethod
    def dormir(jogador):
        """Jogador dorme e recupera muito HP."""
        print("\n🏕️ Você se acomoda para dormir...")
        sleep(1)
        
        # Grande recuperação de HP
        cura = int(jogador.hp_max * 0.8)
        jogador.hp = min(jogador.hp + cura, jogador.hp_max)
        
        # Pequena recuperação de Mana
        if hasattr(jogador, 'magia'):
            jogador.magia.recuperar_mana(int(jogador.magia.mana_max * 0.5))
        
        print(f"😴 Você dorme profundamente e recupera {cura} HP!")
        
        # Chance de emboscada
        if randint(1, 100) <= 20:  # 20% de chance
            print("⚠️ EMBOSCADA! Monstros o atacaram enquanto dormia!")
            dano = randint(5, 15)
            jogador.hp -= dano
            print(f"🩸 Você sofre {dano} de dano!")
            return "emboscada"
        else:
            print("✅ Você dorme sem ser incomodado.")
            return "seguro"
    
    @staticmethod
    def vigiar(jogador):
        """Jogador fica de vigília sem recuperação."""
        print("\n🔥 Você fica acordado de vigília...")
        sleep(1)
        
        # Recuperação pequena de Mana
        if hasattr(jogador, 'magia'):
            recuperado = jogador.magia.recuperar_mana(int(jogador.magia.mana_max * 0.3))
            print(f"✨ Você recupera {recuperado} de Mana!")
        
        # Reduz chance de emboscada
        if randint(1, 100) <= 5:  # 5% de chance (vs 20% dormindo)
            print("⚠️ Monstros tentam atacar, mas você estava preparado!")
            dano = randint(2, 5)
            jogador.hp -= dano
            print(f"🩸 Você sofre {dano} de dano (reduzido por estar vigia)!")
            return "ataque_detectado"
        else:
            print("✅ Noite tranquila. Ninguém o atacou.")
            return "seguro"


class GerenciadorEventos:
    """Gerencia eventos de exploração na masmorra."""
    
    def __init__(self):
        pass
    
    def evento_enigma(self, jogador):
        """Evento de sala de enigmas."""
        print("\n" + "="*60)
        print("  🧩 SALA DE ENIGMAS")
        print("="*60)
        
        enigma = EnigmaSala.gerar_enigma()
        print(f"\n{enigma['pergunta']}\n")
        
        resposta = input("Sua resposta: ")
        
        if EnigmaSala.resolver_enigma(enigma, resposta):
            print(f"\n✅ CORRETO! {enigma['recompensa_descricao']}")
            jogador.ouro += enigma['recompensa_ouro']
            print(f"💰 Você recebeu {enigma['recompensa_ouro']} de ouro!")
            return True
        else:
            print("\n❌ INCORRETO! A sala se enche de perigo!")
            dano = randint(10, 20)
            jogador.hp -= dano
            print(f"🩸 Você sofre {dano} de dano ao tentar escapar!")
            return False
    
    def evento_npc_perdido(self, jogador):
        """Evento de encontro com NPC perdido."""
        print("\n" + "="*60)
        print("  👤 ENCONTRO COM VIAJANTE")
        print("="*60)
        
        npc = NPCPerdido.gerar_npc()
        print(f"\nVocê encontra: {npc['nome']}")
        print(f"Descrição: {npc['descricao']}\n")
        
        # Mostrar opções
        for i, opcao in enumerate(npc['opcoes'], 1):
            print(f"[{i}] {opcao['texto']}")
        
        escolha = ler_inteiro("O que fazer? ")
        
        if 1 <= escolha <= len(npc['opcoes']):
            opcao_selecionada = npc['opcoes'][escolha - 1]
            print(f"\n{opcao_selecionada['resultado']}")
            
            if opcao_selecionada['recompensa'] > 0:
                jogador.ouro += opcao_selecionada['recompensa']
                print(f"💰 Você recebeu {opcao_selecionada['recompensa']} de ouro!")
            
            return True
        else:
            print("❌ Ação inválida!")
            return False
    
    def evento_sala_secreta(self, jogador):
        """Evento de descoberta de sala secreta."""
        print("\n" + "="*60)
        print("  🔓 SALA SECRETA DESCOBERTA!")
        print("="*60)
        
        sala = SalaSecreta.gerar_sala_secreta()
        print(f"\nVocê descobre: {sala['nome']}")
        print(f"Descrição: {sala['descricao']}\n")
        
        print(f"💰 Você encontra {sala['ouro']} de ouro!")
        print(f"🧿 Você encontra {sala['nucleos']} Núcleo(s) de Monstro!")
        
        jogador.ouro += sala['ouro']
        jogador.nucleos_monstro += sala['nucleos']
        
        return True
    
    def evento_acampamento(self, jogador):
        """Evento de acampamento para descanso."""
        print("\n" + "="*60)
        print("  🏕️ SALA SEGURA - ACAMPAMENTO")
        print("="*60)
        print(f"\nHP Atual: {jogador.hp}/{jogador.hp_max}")
        if hasattr(jogador, 'magia'):
            print(f"Mana Atual: {jogador.magia.mana}/{jogador.magia.mana_max}")
        
        print("\n[1] Dormir (Grande recuperação, risco de emboscada)")
        print("[2] Vigiar (Pequena recuperação, menos emboscada)")
        print("[3] Sair")
        
        opc = ler_inteiro("O que fazer? ")
        
        if opc == 1:
            resultado = SistemaAcampamento.dormir(jogador)
        elif opc == 2:
            resultado = SistemaAcampamento.vigiar(jogador)
        elif opc == 3:
            print("Você deixa o acampamento.")
            return False
        else:
            print("❌ Opção inválida!")
            return False
        
        return True


def verificar_sala_secreta(jogador):
    """Verifica se o jogador encontra uma sala secreta baseado em agilidade."""
    percepcao = jogador.agilidadebase + jogador.agilidade_modificadores if hasattr(jogador, 'agilidade_modificadores') else jogador.agilidadebase
    resultado = randint(1, 20) + percepcao
    
    # Dificuldade: 15
    return resultado >= 15
