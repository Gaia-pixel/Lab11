import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.bestCammino = []
        self.graph = None
        self.idmap = {}

    def get_colors(self):
        return DAO.get_colors()

    def buildGraph(self, anno, colore):
        self.graph = nx.Graph()
        allNodes = DAO.getAllNodes(colore)
        self.graph.add_nodes_from(allNodes)
        for n in allNodes:
            self.idmap[n.Product_number] = n
        self.getAllArchi2(colore, anno)

    def getAllNodes(self):
        return self.graph.nodes()

    def getArchiMaggiori(self):
        lista = self.graph.edges(data = True) # per avere anche il peso
        archi = []
        for l in lista:
            archi.append((l[0], l[1], l[2]['weight']))
        archi.sort(key=lambda x:x[2], reverse = True)
        return archi

    def getAllArchi1(self, colore, anno):
        allArchi = DAO.getAllArchi(colore, anno)
        for p1,p2,peso in allArchi:
            self.graph.add_edge(self.idmap[p1],self.idmap[p2], weight = peso)

    def getAllArchi2(self, colore, anno):
        lista = DAO.getAllArchi2(anno, colore)
        insieme = set()
        for p1, r1, d1 in lista:
            for p2, r2, d2 in lista:
                if p1 > p2 and r1 == r2 and d1 == d2:
                    insieme.add((p1,p2,d1))
        for p1,p2,d1 in insieme:
            if self.graph.has_edge(self.idmap[p1],self.idmap[p2]):
                self.graph[self.idmap[p1]][self.idmap[p2]]['weight'] = self.graph[self.idmap[p1]][self.idmap[p2]]['weight'] + 1
            else:
                self.graph.add_edge(self.idmap[p1], self.idmap[p2], weight = 1)


    def getGraphDetails(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()

    def getMaxCamminoArchi(self, prodotto):
        self.ricorsione([prodotto])
        return len(self.bestCammino)-1

    def ricorsione(self, parziale):
        if len(parziale) > 1 and len(parziale)-1 > len(self.bestCammino)-1:
            self.bestCammino = copy.deepcopy(parziale)

        else:
            for v in nx.neighbors(self.graph, parziale[-1]):
                if self.condizione(parziale, v):
                    parziale.append(v)
                    self.ricorsione(parziale)
                    parziale.pop()

    def condizione(self, parziale, v):
        if len(parziale)==1:
            return True
        nodo1 = parziale[-1]
        nodo2 = parziale[len(parziale)-2]
        if self.graph[nodo1][v]['weight'] > self.graph[nodo1][nodo2]['weight']:
            return True
        return False