# modelos.py
from abc import ABC, abstractmethod
from datetime import datetime

# 1. Classe Local
class Local:
    def __init__(self, id: int, nome: str, endereco: str, capacidade: int):
        self._id = id
        self._nome = nome
        self._endereco = endereco
        self._capacidade = capacidade
    
    @property
    def nome(self) -> str: return self._nome
    
    @property
    def endereco(self) -> str: return self._endereco

    def __str__(self):
        return f"Local: {self.nome} ({self.endereco})"

# 2. Classe Base Abstrata
class Usuario(ABC):
    def __init__(self, id: int, nome: str, email: str, senha: str):
        self._id = id
        self._nome = nome
        self._email = email
        self._senha = senha
    
    @property
    def id(self) -> int: return self._id
    
    @property
    def nome(self) -> str: return self._nome
    
    @property
    def email(self) -> str: return self._email

    @abstractmethod
    def autenticar(self, senha: str) -> bool:
        pass

    def __str__(self):
        return f"[{self.__class__.__name__}] {self.nome} ({self.email})"

# 3. Classes de Domínio
class Relatorio:
    def __init__(self, id: int, conteudo: str):
        self._id = id
        self._dataGeracao = datetime.now()
        self._conteudo = conteudo
    
    @property
    def conteudo(self) -> str: return self._conteudo

    def gerarResumo(self) -> str:
        return (f"Relatório ID {self._id} (Gerado em: {self._dataGeracao.strftime('%Y-%m-%d')})\n"
                + "="*20 + f"\n{self.conteudo}")

class Ingresso:
    def __init__(self, id: int, tipo: str, preco: float, participante: 'Participante', evento: 'Evento'):
        self._id = id
        self._tipo = tipo
        self._preco = preco
        self._status = "Vendido"
        self._participante = participante
        self._evento = evento
    
    @property
    def id(self) -> int: return self._id
    
    @property
    def status(self) -> str: return self._status
    
    @property
    def participante(self) -> 'Participante': return self._participante
    
    @property
    def evento(self) -> 'Evento': return self._evento

    def validar(self) -> bool:
        print(f"Ingresso {self.id} validado para {self.participante.nome}.")
        self._status = "Utilizado"
        return True

    def cancelar(self):
        print(f"Ingresso {self.id} cancelado.")
        self._status = "Cancelado"

    def __str__(self):
        return f"Ingresso {self.id} ({self._tipo}) - {self.status}"

class Evento:
    def __init__(self, id: int, nome: str, descricao: str, dataInicio: datetime, dataFim: datetime, capacidade: int, local_info: dict):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._dataInicio = dataInicio
        self._dataFim = dataFim
        self._capacidade = capacidade
        self._status = "Planejado"
        
        self._local = Local(
            id=local_info['id'],
            nome=local_info['nome'],
            endereco=local_info['endereco'],
            capacidade=local_info['capacidade']
        )
        
        self._ingressos: list[Ingresso] = []

    @property
    def nome(self) -> str: return self._nome
    
    @property
    def local(self) -> Local: return self._local
    
    @property
    def ingressos(self) -> list[Ingresso]: return self._ingressos
    
    @property
    def capacidade(self) -> int: return self._capacidade

    def validarCapacidade(self) -> bool:
        vagas_ocupadas = len([ing for ing in self._ingressos if ing.status == "Vendido"])
        if vagas_ocupadas < self._capacidade:
            return True
        print(f"**REGRA DE NEGÓCIO (FALHA)**: Capacidade máxima do evento '{self.nome}' atingida ({self._capacidade}).")
        return False

    def adicionarIngresso(self, ingresso: Ingresso):
        if self.validarCapacidade():
            self._ingressos.append(ingresso)
            vagas_restantes = self.capacidade - len([ing for ing in self.ingressos if ing.status == "Vendido"])
            print(f"Ingresso adicionado ao evento '{self.nome}'. Vagas restantes: {vagas_restantes}")
        else:
            raise ValueError("Não foi possível adicionar ingresso, capacidade esgotada.")

    def __str__(self):
        vagas_ocupadas = len([ing for ing in self.ingressos if ing.status == "Vendido"])
        return (f"Evento: {self.nome} (Status: {self._status})\n"
                f"   Local: {self.local.nome}\n"
                f"   Vagas: {vagas_ocupadas}/{self.capacidade}")

# 4. Subclasses (Atores)
class Administrador(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha: str):
        super().__init__(id, nome, email, senha)

    def autenticar(self, senha: str) -> bool:
        is_valid = self._senha == senha
        print(f"Autenticação (Admin) para {self.nome}: {'Sucesso' if is_valid else 'Falha'}")
        return is_valid

    def gerarRelatorios(self, usuarios: list[Usuario], eventos: list[Evento]) -> Relatorio:
        print(f"ADM {self.nome} está gerando relatórios...")
        conteudo = "--- Relatório de Usuários ---\n"
        conteudo += f"Total de usuários: {len(usuarios)}\n"
        for user in usuarios:
            conteudo += f"- {user.nome} ({user.__class__.__name__})\n"
        
        conteudo += "\n--- Relatório de Eventos ---\n"
        conteudo += f"Total de eventos: {len(eventos)}\n"
        for evento in eventos:
            vagas_ocupadas = len([ing for ing in evento.ingressos if ing.status == "Vendido"])
            conteudo += f"- {evento.nome} ({vagas_ocupadas}/{evento.capacidade} ingressos)\n"

        return Relatorio(id=datetime.now().microsecond, conteudo=conteudo)

    def gerenciarUsuarios(self, usuario: Usuario, acao: str):
        print(f"ADM {self.nome} executou a ação '{acao}' no usuário '{usuario.nome}'.")

class Organizador(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha: str, verificado: bool = False):
        super().__init__(id, nome, email, senha)
        self._verificado = verificado

    @property
    def verificado(self) -> bool: return self._verificado

    def autenticar(self, senha: str) -> bool:
        is_valid = (self._senha == senha)
        if not self._verificado:
            print(f"Autenticação (Organizador) para {self.nome}: Falha (Conta não verificada)")
            return False
            
        print(f"Autenticação (Organizador) para {self.nome}: {'Sucesso' if is_valid else 'Falha'}")
        return is_valid
    
    def criarEvento(self, id: int, nome: str, desc: str, dt_inicio: datetime, dt_fim: datetime, cap: int, local_info: dict) -> Evento | None:
        if not self.verificado:
            print(f"Organizador {self.nome} não pode criar eventos (Não verificado).")
            return None
        
        print(f"Organizador {self.nome} criando evento '{nome}'...")
        novo_evento = Evento(
            id=id, nome=nome, descricao=desc, 
            dataInicio=dt_inicio, dataFim=dt_fim, 
            capacidade=cap, local_info=local_info
        )
        return novo_evento

    def editarEvento(self, evento: Evento, novo_nome: str):
        print(f"Organizador {self.nome} editando evento '{evento.nome}'.")
        evento._nome = novo_nome

    def cancelarEvento(self, evento: Evento):
        print(f"Organizador {self.nome} cancelando evento '{evento.nome}'.")
        evento._status = "Cancelado"
        for ingresso in evento.ingressos:
            if ingresso.status == "Vendido":
                ingresso.cancelar()

class Participante(Usuario):
    def __init__(self, id: int, nome: str, email: str, senha: str, cpf: str):
        super().__init__(id, nome, email, senha)
        self._cpf = cpf
        self._ingressos: list[Ingresso] = []
    
    @property
    def cpf(self) -> str: return self._cpf
    
    @property
    def ingressos(self) -> list[Ingresso]: return self._ingressos

    def autenticar(self, senha: str) -> bool:
        is_valid = self._senha == senha
        print(f"Autenticação (Participante) para {self.nome}: {'Sucesso' if is_valid else 'Falha'}")
        return is_valid

    def inscreverEvento(self, evento: Evento, id_ingresso: int, tipo: str, preco: float) -> Ingresso | None:
        print(f"Participante {self.nome} tentando se inscrever no evento '{evento.nome}'...")
        
        if not evento.validarCapacidade():
            return None

        novo_ingresso = Ingresso(id_ingresso, tipo, preco, self, evento)
        
        try:
            evento.adicionarIngresso(novo_ingresso)
        except ValueError as e:
            print(f"Falha ao adicionar ingresso: {e}")
            return None

        self._ingressos.append(novo_ingresso)
        
        print(f"Inscrição de {self.nome} no {evento.nome} bem-sucedida! (Ingresso {novo_ingresso.id})")
        return novo_ingresso

    def cancelarInscricao(self, ingresso: Ingresso):
        if ingresso in self._ingressos:
            print(f"Participante {self.nome} cancelando inscrição (Ingresso {ingresso.id}).")
            ingresso.cancelar()
            self._ingressos.remove(ingresso)
        else:
            print(f"Erro: {self.nome} não possui o ingresso {ingresso.id}.")