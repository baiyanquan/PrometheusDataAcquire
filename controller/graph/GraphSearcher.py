class GraphSearcher:

    def __init__(self):
        pass

    @staticmethod
    def traverse(graph, start_point, qtype=set()):
        S,Q = set(), qtype()
        Q.add(start_point)
        print(Q)
        while Q:
            u = Q.pop()
            print(u)
            if u in S: continue
            S.add(u)
            if u in graph.keys():
                for v in graph[u].keys():
                    Q.add(v)
            yield u

    @staticmethod
    def search_source(graph, start_point):
        search_result = SearchResult(start_point)

        GraphSearcher._search_source(graph, start_point, search_result)

        #search_result.print()

        path_list = []
        initial_path = [search_result.node]
        path_list.append(initial_path)

        GraphSearcher._build_path(search_result, initial_path, path_list)

        return path_list, search_result

    @staticmethod
    def _search_source(graph, node, search_result):
        sub_sources = []
        splice_links = []

        if node not in graph.keys():
            return

        links = sorted(graph[node].items(), key = lambda x: abs(x[1]), reverse= True)
        #print(links)

        sub_graph = graph.copy()
        sub_graph.pop(node)

        for link, weight in links:
            child_result = SearchResult(link)
            search_result.children.append(child_result)
            GraphSearcher._search_source(sub_graph, link, child_result)


    @staticmethod
    def _build_path(search_result, current_path, path_list):
        if not search_result.children:
            return

        path_list.remove(current_path)

        for child in search_result.children:
            new_path = current_path.copy()
            #print(new_path)
            if child.node in new_path:
                continue
            new_path.append(child.node)
            path_list.append(new_path)
            GraphSearcher._build_path(child, new_path, path_list)

    @staticmethod
    def path_to_stirng(path, graph, with_weight=False):
        from_node = path.pop()

        if from_node in path:
            from_node = path.pop()

        path_string = from_node
        while path:
            to_node = path.pop()
            weight = graph[to_node][from_node]
            if with_weight:
                path_string = "%s -(%f)" % (path_string, weight)
            path_string = path_string + "->" + to_node
            from_node = to_node

        return path_string



class stack(list):
    add=list.append

class SearchResult():

    def __init__(self, node_name):
        self.node = node_name
        self.children = []

    def print(self):
        print("node name: %s" % self.node)

        for child in self.children:
            print("child: %s" % child.node)
            child.print()

