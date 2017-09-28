import sys
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class MainWindow(QtGui.QMainWindow):

    solid = 1

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.frame = QtGui.QFrame()

        self.layout = QtGui.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.layout.addWidget(self.vtkWidget)

        self.render = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.render)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        filename = "F117_.stl"

        reader = vtk.vtkSTLReader()
        reader.SetFileName(filename)

        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(reader.GetOutput())
        else:
            mapper.SetInputConnection(reader.GetOutputPort())

        # Create an actor
        global actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.render.AddActor(actor)

        self.render.ResetCamera()

        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)

        self.show()
        self.interactor.Initialize()

        self.planes = QtGui.QPushButton('Import Plane Model', self)
        self.layout.addWidget(self.planes)

        self.wireframe = QtGui.QPushButton('Toggle Wireframe Mode', self)
        self.layout.addWidget(self.wireframe)
        self.wireframe.clicked.connect(self.handleButton)

    def handleButton(self):
        if self.solid == 1:
            actor.GetProperty().SetRepresentationToWireframe()
            self.solid = 0
        else:
            actor.GetProperty().SetRepresentationToSurface()
            self.solid = 1


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    window = MainWindow()

    sys.exit(app.exec_())