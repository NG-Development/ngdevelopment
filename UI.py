import sys
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class UI(QtGui.QMainWindow):
    solid = 1
    global points
    points = {}

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.frame = QtGui.QFrame()

        self.layout = QtGui.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.layout.addWidget(self.vtkWidget)

        self.render = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.render)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        self.mapper = vtk.vtkPolyDataMapper()

        # Create an actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)

        self.render.AddActor(self.actor)

        self.render.ResetCamera()

        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)

        self.show()
        self.interactor.Initialize()

        # Import button
        self.planes = QtGui.QPushButton('Import Plane Model', self)
        self.layout.addWidget(self.planes)
        self.planes.clicked.connect(self.readfiles)

        # Wireframe button
        self.wireframe = QtGui.QPushButton('Toggle Wireframe Mode', self)
        self.layout.addWidget(self.wireframe)
        self.wireframe.clicked.connect(self.handleButton)

        # ids
        self.colorPlane = QtGui.QPushButton('Color Plane', self)
        self.layout.addWidget(self.colorPlane)
        self.colorPlane.clicked.connect(self.addColors)

        self.pd = vtk.vtkPolyData()

    def addColors(self):
        #Tuple at index (i) denotes the color of point(i)
        colors = vtk.vtkUnsignedCharArray()
        colors.SetNumberOfComponents(3)

        #Goes through each point in the polydata and assigns a color based on some criteria
        for i in range(1, self.pd.GetNumberOfPoints()+1):
            if i%3 == 0:
                colors.InsertNextTuple3(255,0,0)
            elif i%3 == 1:
                colors.InsertNextTuple3(0,255,0)
            else:
                colors.InsertNextTuple3(0,0,255)
            #sets up dict to track point ids by their coordinates
            points[self.pd.GetPoint(i)] = i

        #required to show colors on the actor
        self.pd.GetPointData().SetScalars(colors)
        self.mapper.SetColorModeToDefault()
        self.mapper.SetScalarModeToUsePointData()
        self.interactor.Render()

    def addModel(self, reader):

        self.mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.mapper.SetInput(reader.GetOutput())
        else:
            self.mapper.SetInputConnection(reader.GetOutputPort())

            self.actor.SetMapper(self.mapper)
            self.render.AddActor(self.actor)
            self.pd = self.mapper.GetInput()
            self.render.ResetCamera()
            self.interactor.Render()

    def handleButton(self):
        if self.solid == 1:
            self.actor.GetProperty().SetRepresentationToWireframe()
            self.interactor.Render()
            self.solid = 0
        else:
            self.actor.GetProperty().SetRepresentationToSurface()
            self.interactor.Render()
            self.solid = 1

    # importing OBJ/STL currently
    def readfiles(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Import Models")
        file = open(filename, "r")
        extension = QtCore.QFileInfo(filename).suffix()

        if extension == 'obj':
            with file:
                reader = vtk.vtkOBJReader()
                reader.SetFileName(str(filename))
                self.addModel(reader)

        if extension == 'stl':
            with file:
                reader = vtk.vtkSTLReader()
                reader.SetFileName(str(filename))
                self.addModel(reader)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    window = UI()
    window.setWindowTitle('CEESIM Visualizer')
    sys.exit(app.exec_())
