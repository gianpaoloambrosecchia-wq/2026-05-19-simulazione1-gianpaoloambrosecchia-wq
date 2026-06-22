import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapA = {}
        self._bestSol = []
        self._bestCosto = 0

    def getPath(self, source):
        self._bestSol = []
        self._bestCosto = 0
        parziale = [source]
        self._ricorsione(parziale, float('-inf'))



    def _ricorsione(self, parziale, peso_arco_precedente):
        #1) Condizione di ottimalità
        if self._calcolaCosto(parziale) > self._bestCosto:
            self._bestSol = copy.deepcopy(parziale)
            self._bestCosto = self._calcolaCosto(parziale)

        for v in self._graph.neighbors(parziale[-1]):

            peso_arco_corrente = self._graph[parziale[-1]][v]["weight"]

            if peso_arco_corrente >= peso_arco_precedente and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale, peso_arco_corrente)
                parziale.pop()


    def _calcolaCosto(self, parziale):
        costo = 0
        for i in range(len(parziale)-1):
            costo += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return costo




    def buildGraph(self, genreId):
        self._graph.clear()
        self._idMapA = {}
        nodes = DAO.getArtists(genreId)
        self._graph.add_nodes_from(nodes)
        for n in nodes:
            self._idMapA[n.ArtistId] = n
        self._addEdges(genreId)

    def _addEdges(self, genreId):
        archi = DAO.getEdges(genreId, self._idMapA)
        # Cioè avendo i vari collegamneti, in base all popolarita costruisco l'arco
        for a in archi:
            if a[0].pop > a[1].pop:
                self._graph.add_edge(a[0], a[1], weight = a[0].pop + a[1].pop)
                a[0].pesoArchiUscenti += a[0].pop + a[1].pop
                a[1].pesoArchiEntranti += a[0].pop + a[1].pop
            elif a[0].pop < a[1].pop:
                self._graph.add_edge(a[1], a[0], weight = a[0].pop + a[1].pop)
                a[1].pesoArchiUscenti += a[0].pop + a[1].pop
                a[0].pesoArchiEntranti += a[0].pop + a[1].pop
            else:
                self._graph.add_edge(a[0], a[1], weight = a[0].pop + a[1].pop)
                self._graph.add_edge(a[1], a[0], weight=a[0].pop + a[1].pop)
                a[0].pesoArchiUscenti += a[0].pop + a[1].pop
                a[1].pesoArchiEntranti += a[0].pop + a[1].pop
                a[1].pesoArchiUscenti += a[0].pop + a[1].pop
                a[0].pesoArchiEntranti += a[0].pop + a[1].pop

    def getAllGenres(self):
        genres = DAO.getAllGenres()
        return genres

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getInfluenza(self):

        #topArtista = max(self._graph.nodes, key = lambda x: x.pesoArchiUscenti-x.pesoArchiEntranti)
        #influenza = topArtista.pesoArchiUscenti - topArtista.pesoArchiEntranti
        #return topArtista, influenza

        # METODO PER CALCOLARE LA DIFFERENZA TRA IL PESO DEGLI ARCHI USCENTI E QUELLO DEGLI ARCHI ENTRANTI
        # DI UN NODO (USANDO nx)
        influenza = {}
        for node in self._graph.nodes:
            peso_uscenti = sum(data["weight"] for _, _, data in self._graph.out_edges(node, data=True))
            peso_entranti = sum(data["weight"] for _, _, data in self._graph.in_edges(node, data=True))
            influenza[node] = peso_uscenti - peso_entranti

        artistaPiuInfluente = max(influenza, key=lambda x: influenza[x])
        return artistaPiuInfluente, influenza[artistaPiuInfluente]

    def getTopArchi(self):
        if (len(self._graph.edges)) < 5:
            return self._graph.edges
        # RICORDA!!!! data=True altrimenti non puoi considerare il peso
        topArchi = sorted(self._graph.edges(data=True), key=lambda edge: edge[2]["weight"], reverse=True)
        return topArchi[0:5]
