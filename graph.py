import matplotlib.pyplot as plt
import networkx as nx


class Drawer(object):
    def __init__(self, file_name='graph.png'):
        self.graph = nx.Graph()
        self.file_name = file_name

    def draw_deep_graph(self):
        options = {
            'node_color': '#FF0000',  # цвет узла
            'node_size': 50,  # размер узла
            'edge_color': '#000000',  # цвет соединений
            'font_size': 7,
            'font_color': '#4B0082',
            'with_labels': False
        }
        nx.draw(self.graph, pos=nx.spring_layout(self.graph), **options)

        plt.gcf().set_size_inches(30, 15)
        plt.savefig(self.file_name, dpi=550)

    def get_rgb(self, maximum, red=255, blue=0):
        green = int(self * (255 / maximum))
        return red, green, blue

    def draw_with_colors(self, maximum):
        color_map = []
        for node in self.graph:
            power = int(node.split('/')[-1])
            color_map.append('#%02x%02x%02x' % Drawer.get_rgb(power, maximum))
        options = {
            'node_color': color_map,  # цвет узла
            'node_size': 300,  # размер узла
            'edge_color': '#000000',  # цвет соединений
            'font_size': 7,
            'font_color': '#4B0082',
            'with_labels': False
        }
        nx.draw(self.graph, pos=nx.spring_layout(self.graph), **options)

        plt.gcf().set_size_inches(30, 15)
        plt.savefig(self.file_name, dpi=550)
