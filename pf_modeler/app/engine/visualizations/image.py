import vtk
from paraview import simple
from .elevation import ElevationFilter


class SourceImage:
    def __init__(self, grid, terrainFile):
        self.zSpacing = 1
        self.eScale = 0

        self.proxiesToDelete = []

        # Build up image grid
        self.image = vtk.vtkImageData()
        self.image.SetOrigin(grid.Origin[0], grid.Origin[1], grid.Origin[2])
        self.image.SetSpacing(grid.Spacing[0], grid.Spacing[1], grid.Spacing[2])
        self.image.SetDimensions(grid.Size[0] + 1, grid.Size[1] + 1, grid.Size[2] + 1)  # Point maxes

        # Attach grid to paraview source
        self.paraviewProducer = simple.TrivialProducer()
        vtkProducer = self.paraviewProducer.GetClientSideObject()
        vtkProducer.SetOutput(self.image)

        self.elevationFilter = ElevationFilter(grid, terrainFile)
        self.addPointArray(self.elevationFilter.getArray())
        self.elevatedSource = self.elevationFilter.getFilter(self.paraviewProducer)

        self.proxiesToDelete = [self.elevatedSource, self.paraviewProducer]

    def addCellArray(self, data):
        self.image.GetCellData().AddArray(data)
        self.elevatedSource.MarkModified(self.elevatedSource)

    def addPointArray(self, data):
        self.image.GetPointData().AddArray(data)

    def getSource(self):
        return self.elevatedSource

    def setZSpace(self, space):
        self.zSpacing = space
        currSpacing = self.image.GetSpacing()
        self.image.SetSpacing(currSpacing[0], currSpacing[1], currSpacing[2] * self.zSpacing)

        self.elevatedSource.MarkModified(self.elevatedSource)
        return self.zSpacing

    def setElevationScale(self, eScale):
        self.eScale = eScale
        self.elevationFilter.setScale(eScale)
        self.elevatedSource.MarkModified(self.elevatedSource)
        return self.eScale

    def minElevation(self):
        return self.elevationFilter.getMin()

    def __del__(self):
        for proxy in self.proxiesToDelete:
            simple.Delete(proxy)
