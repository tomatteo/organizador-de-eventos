# servicos.py
from modelos import Administrador, Organizador, Participante, Evento, Ingresso, Relatorio, Usuario
from datetime import datetime

GLOBAL_EVENTO_ID = 1
GLOBAL_INGRESSO_ID = 100

class ServicoSistema:
    def __init__(self):
        self._usuarios: list[Usuario] = []
        self._eventos: list[Evento] = []
        print("Serviço do Sistema de Eventos iniciado.")

    def cadastrar_usuario(self, usuario: Usuario):
        self._usuarios.append(usuario)
        print(f"Usuário '{usuario.nome}' cadastrado no sistema.")

    def servico_criar_evento(self, organizador: Organizador, nome: str, desc: str, dt_inicio: datetime, dt_fim: datetime, cap: int, local_info: dict) -> Evento | None:
        global GLOBAL_EVENTO_ID
        
        novo_evento = organizador.criarEvento(
            id=GLOBAL_EVENTO_ID,
            nome=nome, desc=desc, dt_inicio=dt_inicio, dt_fim=dt_fim,
            cap=cap, local_info=local_info
        )
        
        if novo_evento:
            self._eventos.append(novo_evento)
            GLOBAL_EVENTO_ID += 1
            print(f"Evento '{novo_evento.nome}' adicionado ao sistema.")
            return novo_evento
        return None

    def servico_inscrever_evento(self, participante: Participante, evento: Evento, tipo: str, preco: float) -> Ingresso | None:
        global GLOBAL_INGRESSO_ID
        
        novo_ingresso = participante.inscreverEvento(
            evento=evento,
            id_ingresso=GLOBAL_INGRESSO_ID,
            tipo=tipo,
            preco=preco
        )
        if novo_ingresso:
            GLOBAL_INGRESSO_ID += 1
            return novo_ingresso
        return None

    def servico_gerar_relatorio(self, admin: Administrador) -> Relatorio:
        relatorio = admin.gerarRelatorios(self._usuarios, self._eventos)
        return relatorio

    def get_evento_por_nome(self, nome: str) -> Evento | None:
        for evento in self._eventos:
            if evento.nome == nome:
                return evento
        print(f"Sistema: Evento com nome '{nome}' não encontrado.")
        return None