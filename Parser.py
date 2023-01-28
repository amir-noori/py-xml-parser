
class XmlParser:

    class Tree:

        def __init__(self, root=None):
            self.root = root

    class Node:

        def __init__(self, name, content, parent=None, children=[], location=None):
            self.name = name
            self.content = content
            self.parent = parent
            self.children = children
            self.location = location

        def __str__(self):
            return f"{self.name}, child count: {len(self.children)}"

        def show(self, level=0, include_self=True):
            if include_self:
                print(f"{level*' '} {self.name}")
                level = level + 1
            if self.children == None or len(self.children) == 0:
                print(f"{level*' '} -")

            for child in self.children:
                print(f"{level*' '} {child.name}")
                child.show(level + 1, False)

    class Location:

        def __init__(self, tag_name, position, type, depth=[]):
            self.tag_name = tag_name
            self.position = position
            self.type = type
            self.depth = depth

        def __str__(self):
            return f"{self.tag_name}, {self.position}, {self.type}, {self.depth}"


    def __init__(self, input = ""):
        self.input = input

    def parse_xml(self):
        tag_begin = False
        tag_end_begin = False
        current_tag = ""
        current_end_tag = ""
        tag_stack = []
        position = 0

        for ch in self.input:

            if tag_begin and ch == ">":
                tag_begin = False
                tag_stack.append(XmlParser.Location(str(current_tag), position, "start"))
                current_tag = ""

            if tag_end_begin and ch == ">":
                tag_end_begin = False
                tag_stack.append(XmlParser.Location(str(current_end_tag), position, "end"))
                current_end_tag = ""

            if tag_begin:
                current_tag = current_tag + ch

            if tag_end_begin:
                current_end_tag = current_end_tag + ch

            if ch == "<" and self.input[position + 1] != "/":
                tag_begin = True
                tag_end_begin = False
            elif ch == "<" and self.input[position + 1] == "/":
                tag_begin = False
                tag_end_begin = True

            position = position + 1

        return tag_stack


    def set_depth_level(self, stack):
        root_node = None
        depth_stack = []
        current_no = 0

        for i in range(0, len(stack)):
            node = stack[i]
            if root_node == None:
                root_node = node
                depth_stack.append(current_no)
                root_node.depth = depth_stack.copy()
            elif node.type == "start":
                depth_stack.append(current_no)
                node.depth = depth_stack.copy()
                current_no = 0
            elif node.type == "end":
                depth_stack.pop()
                current_no = current_no + 1


    def find_children(self, node, all_nodes):
        children = []
        for item in all_nodes:
            if len(node.location.depth) + 1 == len(item.location.depth) and self.starts_with(item.location.depth, node.location.depth):
                children.append(item)
        return children


    def starts_with(self, arr1, arr2):
        for i in range(0, len(arr2)):
            if arr2[i] != arr1[i]:
                return False
        return True


    def setup_xml_tree(self, all_nodes_locations):
        root_node = None
        current_node = None

        all_ndoes = []

        for node_location in all_nodes_locations:
            if node_location.type == "start":
                current_node = XmlParser.Node(node_location.tag_name, "",
                                    None, location=node_location)
                if root_node == None:
                    root_node = current_node

                all_ndoes.append(current_node)

        for node in all_ndoes:
            node.children = self.find_children(node, all_ndoes)

        return root_node

    def parse(self):
        result = self.parse_xml()
        self.set_depth_level(result)
        return self.setup_xml_tree(result)



