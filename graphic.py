import sys

import pydot
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.uic import loadUi

from BTree import BTree


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        loadUi("graphic.ui", self)
        self.btree = BTree(self.grade_sb.value())

        self.le_data.returnPressed.connect(self.insert)
        self.btn_clear.clicked.connect(self.clear)
        self.bt_add.clicked.connect(self.insert)
        self.btn_remove.clicked.connect(self.remove)
        self.grade_sb.valueChanged.connect(self.grade_changed)

        img_add = QIcon('img/add')
        img_del = QIcon('img/del')
        img_clean = QIcon('img/clean') #TODO add img clear

        self.bt_add.setIcon(img_add)
        self.btn_remove.setIcon(img_del)
        self.btn_clear.setIcon(img_clean)

    def clear(self):
        self.tree_lb.clear()
        self.btree = BTree(self.grade_sb.value())
        self.lw_operations.clear()

    def grade_changed(self, grade):
        self.btree = BTree(grade)
        self.tree_modified()

    def insert(self):
        value = self.le_data.text()

        try:
            self.btree.insert(float(value))
            self.tree_modified()
            self.lw_operations.addItem('Insertado: %s' %value)
        except ValueError:
            QMessageBox.information(self, "Información", "El valor entrado no es correcto.")
        finally:
            self.le_data.clear()

    def remove(self):
        value = self.le_data.text()

        try:
            self.btree.delete(float(value))
            self.tree_modified()
            self.lw_operations.addItem('Eliminado: %s' % value)
        except ValueError:
            QMessageBox.information(self, "Información", "El valor entrado no es correcto.")
        finally:
            self.le_data.clear()
            self.le_data.setFocus()

    def tree_modified(self):
        graph = pydot.Dot(graph_type='digraph', ratio='fill')

        is_empty = self.btree.root is None or not self.btree.root.keys
        nodes = [] if is_empty else [self.btree.root]

        while nodes:
            parent = nodes.pop(0)
            value = '|'.join(map(self.to_str, parent.keys))

            dot_parent = pydot.Node(value, shape='square')
            graph.add_node(dot_parent)

            for child in [ch for ch in parent.sons if ch is not None]:
                nodes.append(child)
                value = '|'.join(map(self.to_str, child.keys))

                dot_node = pydot.Node(value, shape='square')
                graph.add_node(dot_node)

                graph.add_edge(pydot.Edge(dot_parent, dot_node))

        if is_empty:
            image = QPixmap()
        else:
            _bytes = graph.create(format='png')
            image = QPixmap()
            image.loadFromData(_bytes)

        self.tree_lb.setPixmap(image)

    @staticmethod
    def to_str(number):
        if number.is_integer():
            return str(int(number))
        return str(number)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()

    sys.exit(app.exec_())
