#Initializing the Graph Class
class Graph:
    def __init__(self, vertices):
        self.V = vertices   
        self.graph = []     
        self.nodes = []

    def add_edge(self, s, d, w):
        self.graph.append([s, d, w])
    
    def addNode(self,value):
        self.nodes.append(value)

    def print_solution(self, dist):
        print("Distance of Vertex from Source")
        for key, value in dist.items():
            print('  ' + key, ' :    ', value)

    #Implementing Bellman-Ford's Algorithm
    def bellman_ford(self, src):
        dist = {i : float("Inf") for i in self.nodes}
        dist[src] = 0

        for temp in range(self.V-1):
            for s, d, w in self.graph:
                if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                    dist[d] = dist[s] + w
            
        for s, d, w in self.graph:
            if dist[s] != float("Inf") and dist[s] + w < dist[d]:
                print("Graph contains negative cycle",s,d, w, dist[s])
                #return
            

        self.print_solution(dist)

g = Graph(5)
g.addNode("USD")
g.addNode("CAD")
g.addNode("EUR")

g.add_edge("USD", "EUR", 0.29)
g.add_edge("EUR", "CAD", -0.31)
g.add_edge("CAD", "USD", 0.005)

g.bellman_ford("CAD")