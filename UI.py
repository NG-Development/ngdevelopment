import sys
import vtk
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class UI(QtGui.QMainWindow):

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

##        filename = "F117_.stl"

##        reader = vtk.vtkSTLReader()
##        reader.SetFileName(filename)

        mapper = vtk.vtkPolyDataMapper()
##        if vtk.VTK_MAJOR_VERSION <= 5:
##            mapper.SetInput(reader.GetOutput())
##        else:
##            mapper.SetInputConnection(reader.GetOutputPort())
##
##        #Reads .obj file and renders into window
##        filename1 = "millenium.obj"
##
##        reader = vtk.vtkOBJReader()
##        reader.SetFileName(filename1)
##
##        mapper = vtk.vtkPolyDataMapper()
##        if vtk.VTK_MAJOR_VERSION <= 5:
##            mapper.SetInput(reader.GetOutput())
##        else:
##            mapper.SetInputConnection(reader.GetOutputPort())

        # Create an actor
        #global actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.render.AddActor(actor)

        self.render.ResetCamera()

        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)

        self.show()
        self.interactor.Initialize()

        #Import button
        self.planes = QtGui.QPushButton('Import Plane Model', self)
        self.layout.addWidget(self.planes)
        self.planes.clicked.connect(self.readfiles)

        #Wireframe button
        self.wireframe = QtGui.QPushButton('Toggle Wireframe Mode', self)
        self.layout.addWidget(self.wireframe)
        self.wireframe.clicked.connect(self.handleButton)

        
       

    def handleButton(self):
        if self.solid == 1:
            self.actor.GetProperty().SetRepresentationToWireframe()
            self.interactor.Render()
            self.solid = 0
        else:
            self.actor.GetProperty().SetRepresentationToSurface()
            self.interactor.Render()
            self.solid = 1

    #importing OBJ currently
    def readfiles(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Import Models")
        #print filename
        file = open(filename, "r")
        #self.render.RemoveActor(actor)
        
        with file:
            
            reader = vtk.vtkOBJReader()
            reader.SetFileName(str(filename))

            mapper = vtk.vtkPolyDataMapper()
            if vtk.VTK_MAJOR_VERSION <= 5:
                mapper.SetInput(reader.GetOutput())
            else:
                mapper.SetInputConnection(reader.GetOutputPort())

            self.actor.SetMapper(mapper)
            self.render.AddActor(self.actor)
            self.render.ResetCamera()
            self.interactor.Render()

                


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    window = UI()

    sys.exit(app.exec_()) 
