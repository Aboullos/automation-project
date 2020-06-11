

class HtmlElement:
    __not_finishing_tags = ["br", "hr"]

    def __init__(self, tag: str, attributes: str = "", content: str = ""):
        self.tag: str = tag
        self.attributes: str = attributes
        self.content: str = content
        self.parent = None  # HtmlElement WARNING: python doesn't like "variable: Any = None"
        self.children: list = []

    @staticmethod
    def create_table_row(n_columns: int) -> 'HtmlElement':
        table_row = HtmlElement("tr")

        for i in range(n_columns):
            table_row.create_child("th")

        return table_row

    @staticmethod
    def create_table(n_rows: int, n_columns: int) -> 'HtmlElement':
        table_body = HtmlElement("tbody")

        for i in range(n_rows):
            table_body.add_child(HtmlElement.create_table_row(n_columns))

        return HtmlElement("table").add_child(table_body)

    def get_level(self) -> int:
        return 0 if self.parent is None else self.parent.get_level() + 1

    def add_attr(self, attribute: str, value: str) -> 'HtmlElement':
        self.attributes += (" " if self.attributes else "") + attribute + "=\"" + value + "\""

        return self

    def add_style(self, value: str) -> 'HtmlElement':
        style = "style=\""

        # if self.attributes.find(style) > 0 and self.attributes.find(value) < 0:
        if self.attributes.find(value) < 0 < self.attributes.find(style):
            for i in range(len(self.attributes)):
                if i - len(style) >= 0 and self.attributes[i - len(style): i] == style:
                    style_content = self.attributes[i:]
                    style_content = style_content[0: style_content.index('"')]

                    self.attributes = self.attributes.replace(style_content, style_content + " " + value)
        elif self.attributes.find(style) < 0 and not self.attributes.find(value) < 0:
            self.add_attr("style", value)

        return self

    def set_attributes(self, attributes: str) -> 'HtmlElement':
        self.attributes = attributes

        return self

    def set_content(self, content: str) -> 'HtmlElement':
        self.content = content

        return self

    def get_child(self, index: int) -> 'HtmlElement':
        result: HtmlElement = self.children[index]
        return result

    def get_child_by_tag(self, tag: str, index: int = 0) -> 'HtmlElement':
        current_index = 0
        child = None

        for i in range(len(self.children)):
            if self.children[i].tag == tag:
                if current_index == index:
                    child = self.children[i]
                    break

                current_index += 1

        return child

    def create_child(self, tag: str, attribute: str="", content: str="") -> 'HtmlElement':
        element = HtmlElement(tag, attribute, content)

        self.children.append(element)
        element.parent = self

        return self

    def add_child(self, child: 'HtmlElement') -> 'HtmlElement':
        self.children.append(child)
        child.parent = self

        return self

    def add_child_at(self, child: 'HtmlElement', index: int) -> 'HtmlElement':
        self.children.insert(index, child)
        child.parent = self

        return self

    def remove_child(self, child: 'HtmlElement') -> 'HtmlElement':
        self.children.remove(child)

        return self

    def remove_child_at(self, index: int) -> 'HtmlElement':
        self.children.pop(index)

        return self

    def clone_node(self) -> 'HtmlElement':
        cloned_node = HtmlElement(self.tag, self.attributes, self.content)

        for i in range(len(self.children)):
            cloned_node.add_child(self.children[i].clone_node())

        return cloned_node

    def to_string(self) -> str:
        html_text = ""
        tab = ""

        for i in range(self.get_level()):
            tab += "\t"

        if not self.tag:
            html_text += str(self.content)
        else:
            html_text += (tab + "<" + self.tag + ("" if not self.attributes else " " + self.attributes)
                          + ">" + ("" if not str(self.content) else "\n\t" + tab + str(self.content)))

        for i in range(len(self.children)):
            html_text += "\n" + self.children[i].to_string()

        if self.tag and self.tag not in self.__not_finishing_tags:
            html_text += (("\n" + tab if str(self.content) or len(self.children) > 0 else "")
                          + "</" + self.tag + ">")

        return html_text
