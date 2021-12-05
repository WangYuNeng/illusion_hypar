import kahypar as kahypar

class Vertex:

    def __init__(self, id, weight=1):
        self.id = id
        self.weight = weight
        self.connections = []

    def add_connection(self, edges):
        self.connections += edges

    def get_edges(self):
        return self.edges
    
    def get_edges_id(self):
        return [e.id for e in self.edges]

class Edge:

    def __init__(self, id, weight=1):
        self.id = id
        self.weight = weight
        self.terminals = []

    def add_terminal(self, vertices):
        self.terminals += vertices
    
    def get_termials(self):
        return self.terminals
    
    def get_terminals_id(self):
        return [t.id for t in self.terminals]


class Hypergraph:
    '''
    Vertices and edges sorted by id
    '''

    def __init__(self, weighted_vertex=False, weighted_edge=False):
        self.vertices = []
        self.edges = []
        self.weighted_vertex = weighted_vertex
        self.weighted_edge = weighted_edge
    
    def create_vertices(self, n_vertices=1, weights=None):
        if weights is None:
            self.vertices += [Vertex(i + len(self.vertices)) for i in range(n_vertices)]
        else:
            assert len(weights) == n_vertices
            assert self.weighted_vertex == True
            self.vertices += [Vertex(i + len(self.vertices), w) for i, w in weights]

    def create_edges(self, n_edges=1, weights=None):
        if weights is None:
            self.edges += [Edge(i + len(self.edges)) for i in range(n_edges)]
        else:
            assert len(weights) == n_edges
            assert self.weighted_edge == True
            self.edges += [Edge(i + len(self.edges), w) for i, w in weights]

    def connect(self, edge, terminals):
        if isinstance(edge, int):
            edge = self.edges[edge]
        for i, vertex in enumerate(terminals):
            if isinstance(vertex, int):
                terminals[i] = self.vertices[vertex]
            terminals[i].add_connection([edge])
        edge.add_terminal(terminals)

    def solve(self, n_partition, epsilon, config, solver="kahypar"):
        if solver != "kahypar":
            raise NotImplementedError
        n_vertices = len(self.vertices)
        n_edges = len(self.edges)
        edge_indices = []
        edge_vertices = []

        for edge in self.edges:
            edge_indices.append(len(edge_vertices))
            edge_vertices += edge.get_terminals_id()

        edge_indices.append(len(edge_vertices))

        if self.weighted_vertex:
            vertex_weights = [v.weight for v in self.vertices]
        else:
            vertex_weights = []
        
        if self.weighted_edge:
            edge_weights = [e.weight for e in self.edges]
        else:
            edge_weights = []

        hypergraph = kahypar.Hypergraph(n_vertices, n_edges, edge_indices, edge_vertices, n_partition, edge_weights, vertex_weights)

        context = kahypar.Context()
        context.loadINIconfiguration(config)

        context.setK(n_partition)
        context.setEpsilon(epsilon)

        kahypar.partition(hypergraph, context)


    def dump_hMetis(self, file_name):
        with open(file_name, "w") as file:
            n_vertices = len(self.vertices)
            n_edges = len(self.edges)
            fmt = self._fmt()
            file.write("{} {} {}\n".format(n_edges, n_vertices, fmt))
            for edge in self.edges:
                if self.weighted_edge:
                    file.write("{} ".format(edge.weight))
                file.write(" ".join([str(eid + 1) for eid in edge.get_terminals_id()])) # hMetis starts from 1
                file.write("\n")
            if self.weighted_vertex:
                for vertex in self.vertices:
                    file.write("{}\n".format(vertex.weight))
    
    def _fmt(self):
        if self.weighted_edge and self.weighted_vertex:
            return "11"
        elif self.weighted_edge:
            return "1"
        elif self.weighted_vertex:
            return "10"
        return ""
