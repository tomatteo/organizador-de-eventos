# main.py
from modelos import Administrador, Organizador, Participante
from servicos import ServicoSistema
from datetime import datetime

def main():
    print("--- Iniciando Demonstração do Sistema de Eventos ---")

    # 1. Configurar o Sistema
    sistema = ServicoSistema()
    print("\n" + "---" * 10 + "\n")

    # 2. Inserir usuários de teste
    print("--- 2. Cadastrando Atores ---")
    admin = Administrador(id=1, nome="Admin Geral", email="admin@sistema.com", senha="123")
    org_verificado = Organizador(id=2, nome="IFC Eventos", email="contato@ifc.com", senha="abc", verificado=True)
    org_nao_verificado = Organizador(id=3, nome="João da Silva", email="joao@gmail.com", senha="xyz", verificado=False)
    part_ana = Participante(id=4, nome="Ana Souza", email="ana@mail.com", senha="456", cpf="111.222.333-44")
    part_bruno = Participante(id=5, nome="Bruno Costa", email="bruno@mail.com", senha="789", cpf="555.666.777-88")

    sistema.cadastrar_usuario(admin)
    sistema.cadastrar_usuario(org_verificado)
    sistema.cadastrar_usuario(org_nao_verificado)
    sistema.cadastrar_usuario(part_ana)
    sistema.cadastrar_usuario(part_bruno)

    print("\n" + "---" * 10 + "\n")

    # 3. Testar autenticação
    print("--- 3. Testando Autenticação (Polimorfismo) ---")
    admin.autenticar("123")
    org_verificado.autenticar("abc")
    org_nao_verificado.autenticar("xyz")
    part_ana.autenticar("senha_errada")
    
    print("\n" + "---" * 10 + "\n")

    # 4. Testar criação de eventos
    print("--- 4. Testando Criação de Eventos (Composição) ---")
    
    print("\nTentativa 1 (Organizador Não Verificado):")
    sistema.servico_criar_evento(
        organizador=org_nao_verificado,
        nome="Evento Fantasma", desc="...", dt_inicio=datetime.now(), dt_fim=datetime.now(), cap=100,
        local_info={"id": 100, "nome": "Nenhum", "endereco": "N/A", "capacidade": 0}
    )

    print("\nTentativa 2 (Organizador Verificado):")
    local_info_palestra = {
        "id": 101, "nome": "Auditório IFC", 
        "endereco": "Rod. SC-150, Km 125", "capacidade": 200
    }
    evento_poo = sistema.servico_criar_evento(
        organizador=org_verificado,
        nome="Palestra de POO",
        desc="Discussão sobre UML e Python",
        dt_inicio=datetime(2025, 11, 20, 19, 0),
        dt_fim=datetime(2025, 11, 20, 22, 0),
        cap=2, # Capacidade baixa para testar a regra
        local_info=local_info_palestra
    )
    
    if evento_poo:
        print(f"\nDetalhes do Evento Criado (demonstra Composição):\n{evento_poo}")

    print("\n" + "---" * 10 + "\n")

    # 5. Testar inscrições e regra de capacidade
    print("--- 5. Testando Inscrições (Agregação e Regra de Negócio) ---")
    
    print("\nInscrição 1 (Ana):")
    ing_ana = sistema.servico_inscrever_evento(
        participante=part_ana,
        evento=evento_poo,
        tipo="Estudante",
        preco=10.0
    )
    
    print("\nInscrição 2 (Bruno):")
    ing_bruno = sistema.servico_inscrever_evento(
        participante=part_bruno,
        evento=evento_poo,
        tipo="Geral",
        preco=20.0
    )
    
    print("\nInscrição 3 (Carlos - Deve falhar):")
    part_extra = Participante(id=6, nome="Carlos", email="carlos@mail.com", senha="000", cpf="999...")
    sistema.cadastrar_usuario(part_extra)
    
    ing_carlos = sistema.servico_inscrever_evento(
        participante=part_extra,
        evento=evento_poo,
        tipo="Geral",
        preco=20.0
    )
    
    print(f"\nEstado final do evento (demonstra Agregação):\n{evento_poo}")

    print("\n" + "---" * 10 + "\n")

    # 6. Testar cancelamento
    print("--- 6. Testando Cancelamento (Agregação) ---")
    if ing_ana:
        part_ana.cancelarInscricao(ing_ana)
    
    print(f"\nIngressos da Ana (pós-cancelamento): {part_ana.ingressos}")
    print("\nIngressos no Evento (deve incluir o cancelado, provando vida independente):")
    for ing in evento_poo.ingressos:
        print(f"- Ingresso {ing.id} (Participante: {ing.participante.nome}): {ing.status}")

    print("\n" + "---" * 10 + "\n")

    # 7. Testar geração de relatório
    print("--- 7. Testando Geração de Relatório (Admin) ---")
    relatorio_final = sistema.servico_gerar_relatorio(admin)
    
    print("\n--- RELATÓRIO GERADO ---")
    print(relatorio_final.gerarResumo())
    print("--- FIM DA DEMONSTRAÇÃO ---")


if __name__ == "__main__":
    main()