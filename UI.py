import sys
import vtk
import csv
#import xlrd
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class UI(QtGui.QMainWindow):
    solid = 1
    #global antennas
    #antennas = []

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
        self.wireframe.clicked.connect(self.toggleWireframe)

        #Import Antennas
        self.antennaImport = QtGui.QPushButton('Import Antennas From CSV', self)
        self.layout.addWidget(self.antennaImport)
        self.antennaImport.clicked.connect(self.importCSV)

    # read sample XLS sent
    ##    def readXLS(self):
    ##        fileXLS = xlrd.open_workbook('F16.xls')
    ##        coordinates = fileXLS.sheet_by_index(0)
    ##
    ##        xyz = []
    ##        #xyz =[] #list of xyz in each row
    ##        coords = [] #list of all coordinates
    ##        for i in range(0, 9):
    ##            xyz.append([])
    ##            for j in range(0, 3):
    ##                xyz[i].append(coordinates.cell(i , j))
    ##        print "coordinate list: ", xyz

        # read and print CSV file
    def readCSV(self, antennas):
        xyz = []
        with open(antennas, 'rb') as csvfile:
            coordinates = csv.reader(csvfile, delimiter=',')
            for row in coordinates:
                # convert list of strings to float
                row = map(float, row)
                xyz.append(row)
        global antennaLocs
        antennaLocs = xyz
        print(antennas)

    # import CSV files for antenna coordinates
    def importCSV(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Import CSV files")
        file = open(filename, 'r')
        self.readCSV(filename)

    def addModel(self, reader):
        print(antennaLocs)
        self.maper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.mapper.SetInput(reader.GetOutput())
        else:
            self.mapper.SetInputConnection(reader.GetOutputPort())

            self.actor.SetMapper(self.mapper)
            self.assembly = vtk.vtkAssembly()
            self.assembly.AddPart(self.actor)
            self.render.AddActor(self.assembly)
            for antenna in antennaLocs:
                self.convertDimensions(antenna[0],antenna[1],antenna[2],antenna[3])
            self.render.ResetCamera()
            self.interactor.Render()


    def convertDimensions(self, ngx, ngy, ngz, ngo):
        xmid = 226.6690063476525 / 2
        ymid = 100.79100036621094 / 2
        xmod = 22.7579323642
        ymod = 20.6538935177
        zmod = 20.957569867
        x = xmid+(ngy*zmod)
        y = ymid-13+(-ngz*ymod)
        if -9.0 < ngx < -6.5:
            z = (ngx+13.8)*zmod
        else:
            z = (ngx+15.09)*zmod
        assembly = vtk.vtkAssembly()
        assembly.AddPart(self.actor)
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(3)
        sphereMapper = vtk.vtkPolyDataMapper()
        sphereMapper.SetInputConnection(sphere.GetOutputPort())
        sphereActor = vtk.vtkActor()
        sphereActor.SetMapper(sphereMapper)
        sphereActor.SetPosition(x,y,z)
        sphereActor.GetProperty().SetColor(255, 0, 0)
        self.assembly.AddPart(sphereActor)


    def toggleWireframe(self):
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
