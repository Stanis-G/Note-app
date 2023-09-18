import os
import sys
import inspect
from itertools import product

import graphviz
from modules.note import Note
from modules.lecture import Lecture
from modules.utils import Writable


class CommonGraph:

    def __init__(self):
        self.graph = graphviz.Digraph('round-table', comment='The Round Table')

    def find_nodes(self):
        """Find names of all classes in the "modules" directory"""
        self.classes = []
        # Find all modules names in "modules" directory
        modules = [f[:-3] for f in os.listdir('modules') if f.endswith('.py')]
        for module in modules:
            # Find all classes in each module
            for cls_name, cls_obj in inspect.getmembers(sys.modules[f'modules.{module}']):
                if inspect.isclass(cls_obj) and cls_obj.__module__ == f'modules.{module}':
                    self.classes.append(cls_obj)
        # Some classes are returned from several modules
        self.classes = list(set(self.classes))
        return self.classes

    def build_nodes(self):
        """Create node for each class"""
        for class_ in self.classes:
            node_name = class_.__name__
            self.graph.node(node_name, node_name)

    def build_edges(self):
        """Build edges between every pair of nodes"""
        for class_1, class_2 in product(self.classes, self.classes):
            if class_1 in class_2.__bases__:
                self.graph.edge(
                    class_1.__name__,
                    class_2.__name__,
                    constraint='True',
                )
        
                 
    def build_hierarchy(self):
        pass




