from model.model import Model

myModel = Model()

myModel.creaGrafo(2000)
print(f"Nodi: {myModel.numNodes()}")
print(f"Archi: {myModel.numEdges()}")
