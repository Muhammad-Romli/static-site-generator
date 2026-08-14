class HTMLNode():
    def __init__(self, tag: str|None=None, value: str|None=None, children: list[HTMLNode]|list[LeafNode]|None=None, props: dict|None=None):
        self.tag = tag #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value #A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children #  A list of HTMLNode objects representing the children of this node
        self.props = props #A dictionary key-value pairs representing the attributes of the HTML. 
                           #For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        attributes = []
        if self.props is None or self.props == [] or self.props == [""]:
            return ""
        for key, value in self.props.items():
            attributes.append(f'{key}="{value}"')
        return " ".join(attributes)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str|None, value: str, props: dict|None=None):
        super().__init__(tag=tag, value=value, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("value is missing")
        if self.tag is None:
            return self.value #if it just raw text
        
        props_str = self.props_to_html() if self.props else "" # The only time when the format slightly different is when the tag different

        if props_str:
            props_str = f" {props_str}" # Adding space in the start so the format correct
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>" # Try understand it and it will make sense

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode] | list[LeafNode], props: dict|None=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is missing")
        if self.children is None:
            raise ValueError("children is missing.... What?")
        
        props_str = self.props_to_html() if self.props else "" # The only time when the format slightly different is when the tag different
        if props_str:
            props_str = f" {props_str}" # Adding space in the start so the format correct

        all_children = "".join(list_of_child.to_html() for list_of_child in self.children)
        return f"<{self.tag}{props_str}>{all_children}</{self.tag}>"
    