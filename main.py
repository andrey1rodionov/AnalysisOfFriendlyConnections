import networkx as nx
import vk
import graph

user_id = 0  # id пользователя, для которого необходимо построить граф (0 - текущий пользователь)
depth = 1

# определение перекрёстных связей с визуализацией популярности
# maximum = vk.Parser.mutual_friends_with_colors(user_id)

# поиск в глубину
vk.Parser.deep_friends(user_id, depth)

# чтение графа из файла
G = nx.read_edgelist(path="friends.list", delimiter=":")

# отрисовка графа в .png изображение
Graph = graph.Drawer()
Graph.graph = G
Graph.draw_deep_graph()
