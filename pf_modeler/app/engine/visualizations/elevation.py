import vtk
from paraview import simple
from parflowio.pyParflowio import PFData


class ElevationFilter:
    def __init__(self, grid, terrainFile):
        self.grid = grid
        self.demFilename = terrainFile

        self.loadedElevation = None
        self.fieldName = "_elevation"

    def getArray(self):
        if self.loadedElevation is not None:
            return self.loadedElevation

        if self.demFilename is None:
            raise Exception(".dem file not specified")

        # Read in elevation array
        elevationReader = PFData(self.demFilename)
        elevationReader.loadHeader()
        elevationReader.loadData()
        elevation = elevationReader.moveDataArray()
        self.minElevation = elevation.min()

        # Transfer elevations to lower-left points, copying last top and last right
        elevationArray = vtk.vtkFloatArray()
        elevationArray.SetName(self.fieldName)
        elevationArray.SetNumberOfComponents(1)
        (kPointMax, jPointMax, iPointMax) = (self.grid.Size[2] + 1, self.grid.Size[1] + 1, self.grid.Size[0] + 1)
        elevationArray.SetNumberOfTuples(iPointMax * jPointMax * kPointMax)

        for k in range(kPointMax):
            for j in range(jPointMax):
                for i in range(iPointMax):
                    idx = i + iPointMax * j + iPointMax * jPointMax * k
                    try:
                        value = elevation[0, j, i]
                    except IndexError:
                        # For the last row and column, copy values from previous row and column
                        (offsetI, offsetJ) = (i, j)
                        if i == elevation.shape[2]:
                            offsetI = elevation.shape[2] - 1
                        if j == elevation.shape[1]:
                            offsetJ = elevation.shape[1] - 1
                        value = elevation[0, offsetJ, offsetI]

                    elevationArray.SetTuple1(idx, value)

        self.loadedElevation = elevationArray
        return elevationArray

    def getFilter(self, source):
        self.filter = simple.WarpByScalar(Input=source)
        self.filter.Scalars = ["POINTS", self.fieldName]
        return self.filter

    def getMin(self):
        if self.loadedElevation:
            return self.minElevation
        return None

    def setScale(self, scale):
        self.filter.ScaleFactor = scale
