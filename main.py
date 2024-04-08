from neo4j import GraphDatabase

class GrafoFamilia:
    def __init__(self, uri, usuario, senha):
        self.driver = GraphDatabase.driver(uri, auth=(usuario, senha))

    def fechar(self):
        self.driver.close()

    def encontrar_engenheiros(self):
        with self.driver.session() as sessao:
            resultado = sessao.run("MATCH (p:Pessoa:Engenheiro) RETURN p.nome AS nome")
            print("Engenheiros na família:")
            for registro in resultado:
                print(registro["nome"])

    def encontrar_filhos_de(self, nome_pai):
        with self.driver.session() as sessao:
            resultado = sessao.run(
                "MATCH (p:Pessoa)-[:PAI_DE]->(filho) WHERE p.nome = $nome_pai RETURN filho.nome AS nome",
                nome_pai=nome_pai)
            print(f"Filhos de {nome_pai}:")
            for registro in resultado:
                print(registro["nome"])

    def encontrar_parceiro_desde_quando(self, nome_pessoa):
        with self.driver.session() as sessao:
            resultado = sessao.run(
                "MATCH (p:Pessoa)-[r:CASADO_COM]->(parceiro) WHERE p.nome = $nome_pessoa RETURN parceiro.nome AS nome, r.desde AS desde",
                nome_pessoa=nome_pessoa)
            for registro in resultado:
                print(f"{nome_pessoa} casado com {registro['nome']} desde {registro['desde']}.")


uri = "bolt://localhost:7687"
usuario = "neo4j"
senha = "neo4j"

grafo = GrafoFamilia(uri, usuario, senha)


grafo.encontrar_engenheiros()
grafo.encontrar_filhos_de("Carlos")
grafo.encontrar_parceiro_desde_quando("Valéria")

grafo.fechar()
