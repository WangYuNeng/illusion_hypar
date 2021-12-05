from illusion_hypar.hypergraph import Hypergraph

if __name__ == "__main__":
    hp = Hypergraph()
    hp.create_vertices(7)
    hp.create_edges(4)
    hp.connect(0, [0, 1])
    hp.connect(1, [0, 6, 4, 5])
    hp.connect(2, [4, 5, 3])
    hp.connect(3, [1, 2, 3])
    hp.dump_hMetis("test.hgr")
    hp.solve(2, 0.03, "config/km1_kKaHyPar_sea20.ini")