import sys
import vtk
import csv
# import xlrd
from PyQt4 import QtCore, QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class UI(QtGui.QMainWindow):
    solid = 1
    # Used to toggle between wireframe and solid mode
    showANT = 0
    # Used to show an hide antennas
    assemblyMade = False

    # denotes if the assembly has been made yet

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # Holds all active antennas with keys being a tuple of an antenna's coordinates
        self.antennas = {}

        # Create Gui Frame
        self.frame = QtGui.QFrame()

        # Create and add VTK render window to QT for display of VTK objects
        self.layout = QtGui.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.layout.addWidget(self.vtkWidget)

        # Create renderer to render actor
        self.render = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.render)
        self.interactor = self.vtkWidget.GetRenderWindow().GetInteractor()

        # Create mapper to draw actors
        self.mapper = vtk.vtkPolyDataMapper()

        # Create an actor
        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)

        # Add the actor to the renderer and reset camera so it is centered on the actor
        self.render.AddActor(self.actor)
        self.render.ResetCamera()

        self.frame.setLayout(self.layout)
        self.setCentralWidget(self.frame)

        self.show()
        self.interactor.Initialize()

        # Import button, used to import plane models from various 3D filetypes
        self.planes = QtGui.QPushButton('Import Plane Model', self)
        self.layout.addWidget(self.planes)
        self.planes.clicked.connect(self.readfiles)

        # Wireframe button, used to toggle between solid and wireframe mode
        self.wireframe = QtGui.QPushButton('Toggle Wireframe Mode', self)
        self.layout.addWidget(self.wireframe)
        self.wireframe.clicked.connect(self.toggleWireframe)

        # Import Antennas, used to import antennas from a csv
        self.antennaImport = QtGui.QPushButton('Import Antennas From CSV', self)
        self.layout.addWidget(self.antennaImport)
        self.antennaImport.clicked.connect(self.importCSV)

        # Toggle Antennas, used to Show/Hide antennas, not currently implemented
        self.antenna = QtGui.QPushButton('Toggle Antennas', self)
        self.layout.addWidget(self.antenna)
        self.antenna.clicked.connect(self.showAntenna)

    # Currently using CSV in place of XLS
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
        if (not self.assemblyMade):
            self.assembly = vtk.vtkAssembly()
            self.assemblyMade = True
        for antenna in antennaLocs:
            self.convertDimensions(antenna[0], antenna[1], antenna[2], antenna[3])

    # import CSV files for antenna coordinates
    def importCSV(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Import CSV files")
        file = open(filename, 'r')
        self.readCSV(filename)

    # adds models to the renderer
    def addModel(self, reader):
        self.maper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            self.mapper.SetInput(reader.GetOutput())
        else:
            self.mapper.SetInputConnection(reader.GetOutputPort())
        # Check if assembly has been made yet
        if (not self.assemblyMade):
            self.assembly = vtk.vtkAssembly()
            self.assemblyMade = True
        self.assembly = vtk.vtkAssembly()
        # Add the main actor(plane model) to the assembly then call render and reset the camera
        self.assembly.AddPart(self.actor)
        self.render.AddActor(self.assembly)
        self.render.ResetCamera()
        self.interactor.Render()

    def convertDimensions(self, ngx, ngy, ngz, ngo):
        '''It's important to note that NG uses different x,y, and z coordinates than VTK.  NG's x
        plane start at 0 at the tip of the nose and extends to the back of the plane.  VTK's x
        starts at the tip of the plane's right and extends to the tip of the plane's left wing.

        NG's y starts at 0 in the center of the plane and extends to each wing tip.  Extending to
        the plane's right wing increases the value of y while exntending to the plane's left wing
        decreases the value of y. VTK's y start at the bottom-most point of the plane and extends
        to the top-most point.  The bottom-most point is 0 and increases as you extend towards
        the top-most point.

        NG's z start just on top of the nose of the plane and extends to the bottom-most and
        top-most points of the plane.  It increases as you move towards the bottom-most point
        and decreases as you move towards the top-most point.  VTK's z begins at the tip of the
        nose of the plane and extends to the tip of the back of the plane.  The tip of the nose
        is 0 and increases as you extend towards the back.

        Orientation is not currently implemented and thus ngo is not used.
        '''

        xmid = 226.6690063476525 / 2
        # Finds the middle of the plane in terms of VTK's x plane, used in conjunction with NG's y
        # to determine antennas placement on VTK's x plane.  Currently hardcoded until support for
        # more models is added

        ymid = 100.79100036621094 / 2
        # Finds the middle of the plane in terms of VTK's y plane, used in conjunction with NG's z
        # to determine antennas placement on VTK's y plane.  Currently hardcoded until support for
        # more models is added

        mod = 20.80
        # Used to convert meters to VTK units.  This is specific to each plane model, but since MVP only
        # deals with the F16, this will remain hardcoded until more models are supported

        # Outdated, we have decided to stick with one conversion unit as the slight variations are likely
        # due to addition parts on the model not accounted for by the specs found on wikipedia.
        # xmod = 22.7579323642
        # ymod = 20.6538935177
        # zmod = 20.957569867

        x = xmid + (ngy * mod)
        # Since NG's y is our x and starts in the middle of the plane, we find the middle and apply
        # NG's y with the unit conversion factor

        y = ymid - 13 + (-ngz * mod)
        # Since NG's z is VTK's y, is inverted, and starts in the middle of the plane, we find the
        # middle and apply the inverted value of NG's z with the unit conversion factor

        if -9.0 < ngx < -6.5:
            z = (ngx + 13.8) * mod
        else:
            z = (ngx + 15.09) * mod
        # Since NG's x is VTK's z and starts from on top of the nose rather than the center of the plane,
        # we apply an offset to NG's x before converting it with the unit conversion factor.  The different
        # offsets are a result of botched coordinates supplied to us by NG for the antennas located on
        # the wings.  In the future, there will be one offset for every point

        # Check if the assembly already exists
        if (not self.assemblyMade):
            self.assembly = vtk.vtkAssembly()
        # Add the main actor(the plane) to the assembly
        self.assembly.AddPart(self.actor)

        # Create a sphere of radius 3 and assign it an actor and mapper
        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(3)
        sphereMapper = vtk.vtkPolyDataMapper()
        sphereMapper.SetInputConnection(sphere.GetOutputPort())
        sphereActor = vtk.vtkActor()
        sphereActor.SetMapper(sphereMapper)

        # Set the sphere to the location calculated by the method and set its color to red before
        # adding it to the assembly
        sphereActor.SetPosition(x, y, z)
        sphereActor.GetProperty().SetColor(255, 0, 0)
        self.assembly.AddPart(sphereActor)
        self.antennas[(ngx, ngy, ngz)] = sphereActor
        # Tolerance will have to be changed, currently you need to exact location, the the decimal
        # in order to locate an antenna

    # Show Antenna on model, currently not implemented
    def showAntenna(self):
        if self.showANT == 1:
            # antennas should be shown, add all from dictionary to assembly
            for antenna in self.antennas:
                self.assembly.AddPart(self.antennas[antenna])
            self.render.ResetCamera()
            self.interactor.Render()
            self.showANT = 0
        else:
            # antennas should be hidden, remove all in dictionary from assembly
            for antenna in self.antennas:
                self.assembly.RemovePart(self.antennas[antenna])
            self.render.ResetCamera()
            self.interactor.Render()
            self.showANT = 1

    # wireframe function
    def toggleWireframe(self):
        if self.solid == 1:
            self.actor.GetProperty().SetRepresentationToWireframe()
            self.interactor.Render()
            self.solid = 0
        else:
            self.actor.GetProperty().SetRepresentationToSurface()
            self.interactor.Render()
            self.solid = 1

    # importing OBJ/STL/PLY currently
    def readfiles(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, "Import Models")
        file = open(filename, "r")
        extension = QtCore.QFileInfo(filename).suffix()

        # create an obj, stl, ply reader based on the extension of the filename selected
        # we add the selected 3D model to our renderer
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

        if extension == 'ply':
            with file:
                reader = vtk.vtkPLYReader()
                reader.SetFileName(str(filename))
                self.addModel(reader)


# this creates the window and all the renderers
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = UI()
    window.setWindowTitle('CEESIM Visualizer')
    sys.exit(app.exec_())
