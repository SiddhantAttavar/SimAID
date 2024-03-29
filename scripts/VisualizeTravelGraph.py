# Import networkx and matplotlib
import networkx as nx
from matplotlib import pyplot as plt

def generateNewTravelProbabilities(cellSize):
    newTravelProbabilities = [[[] for _ in range(cellSize)] for _ in range(cellSize)]
    for i in range(cellSize):
        for j in range(cellSize):
            for k in range(cellSize * cellSize):
                newTravelProbabilities[i][j].append(random())
            newTravelProbabilities[i][j][i * cellSize + j] = 0
            for k in range(1, cellSize * cellSize):
                newTravelProbabilities[i][j][k] += newTravelProbabilities[i][j][k - 1]
            for k in range(cellSize * cellSize):
                newTravelProbabilities[i][j][k] /= newTravelProbabilities[i][j][-1]
    return newTravelProbabilities

# Create graph and initialize travel_probabilities
travelProbabilites = [[[0.0, 0.04396231995215526, 0.118947362397652, 0.170234327709524, 0.2643587237609316, 0.3226040565555893, 0.5749266268895028, 0.6535730150423884, 1.0], [0.03418172516668257, 0.03418172516668257, 0.08660310320430087, 0.1469408204911173, 0.2986155439728465, 0.5255306182933132, 0.8020272630957871, 0.8200673012854994, 1.0], [0.01698411792118938, 0.04270328391332469, 0.04270328391332469, 0.1253461893637136, 0.233224623056334, 0.4213638824327444, 0.463038380926035, 0.6533267320592453, 1.0]], [[0.05598035836625424, 0.1402626998757745, 0.1563461464000263, 0.1563461464000263, 0.1939104804279467, 0.443736972016149, 0.6026116707191296, 0.6585267917089894, 1.0], [0.02535851662535585, 0.1066688859267162, 0.1851966119688711, 0.2362613437950255, 0.2362613437950255, 0.481260773937209, 0.8848860131585504, 0.9006352503913205, 1.0], [0.03780372913763752, 0.05991451823452915, 0.1692118930385932, 0.1860506907466037, 0.281948850487111, 0.281948850487111, 0.397116149309498, 0.6427570745260207, 1.0]], [[0.03204387339068245, 0.08213029282771483, 0.1744781269650978, 0.2607086434694548, 0.4384891552999818, 0.6229591947962619, 0.6229591947962619, 0.7953470933484079, 1.0], [0.008972876428018981, 0.0242185006515865, 0.02890932243701686, 0.1309421908643885, 0.1448395631873683, 0.3489561630190827, 0.608899260381654, 0.608899260381654, 1.0], [0.02009007496692813, 0.07142161068466324, 0.2295667735753836, 0.3652197953585677, 0.3906046389693166, 0.50945797548272, 0.8271615544895533, 1.0, 1.0]]]
graph = nx.DiGraph()
cellSize = len(travelProbabilites)

for i in range(cellSize):
    for j in range(cellSize):
        for k in range(cellSize * cellSize - 1, 0, -1):
            travelProbabilites[i][j][k] -= travelProbabilites[i][j][k - 1]

# Create nodes
for i in range(cellSize):
    for j in range(cellSize):
        # Add node
        cellNum = i * cellSize + j
        graph.add_node(cellNum, pos = (i, j))

# Add edges
for i in range(cellSize):
    for j in range(cellSize):
        cellNum = i * cellSize + j
        for k in range(cellSize * cellSize):
            if cellNum != k:
                graph.add_weighted_edges_from([(cellNum, k, f'{travelProbabilites[i][j][k] * 100:.2f}%')])

# Display the graph
positions = nx.get_node_attributes(graph, 'pos')
edge_labels = nx.get_edge_attributes(graph, 'weight')
nx.draw(graph, positions, node_color = 'black', node_size = 400)
nx.draw_networkx_edge_labels(graph, positions, edge_labels = edge_labels, font_size = 16)
# plt.show()

# Save the graph
figure = plt.gcf()
figure.set_size_inches(10, 10)
figure.savefig('travel-graph.png', dpi = 100, transparent=True)
