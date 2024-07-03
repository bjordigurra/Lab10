import networkx as nx
from database.DAO import DAO


class Model:

    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._countries = DAO.getAllCountries()
        for country in self._countries:
            self._idMap[country.CCode] = country

    def creaGrafo(self, anno):
        self._grafo.clear()
        stati = set()
        confini_tutti = DAO.getAllEdges(anno, self._idMap)
        for confine in confini_tutti:
            stati.add(confine.state1)
            stati.add(confine.state2)

        self._grafo.add_nodes_from(stati) # nodi aggiunti

        confini_terra = DAO.getEdges(anno, self._idMap)
        for confine in confini_terra:
            self._grafo.add_edge(confine.state1, confine.state2)
            # confini aggiunti

    def getConnessioni(self, nodo):
        if nx.degree(self._grafo, nodo) == 0:
            return []

        successors = nx.dfs_successors(self._grafo, nodo)
        print(f"Metodo 2 (pred): {len(successors.values())}")
        return successors


    def numNodes(self):
        return len(self._grafo.nodes)

    def numEdges(self):
        return len(self._grafo.edges)

    def getGrado(self, nodo): # ritorna grado del nodo; se il nodo non è presente, ritorna 0
        if nodo in self._grafo.nodes:
            d = nx.degree(self._grafo, nodo)
            return d
        else:
            return 0

    @property
    def grafo(self):
        return self._grafo

    @property
    def countries(self):
        return self._countries

    def componenteConnessa(self):
        return nx.number_connected_components(self._grafo)

