import vtk
from paraview import simple
from .elevation import ElevationFilter


class SourceImage:
    def __init__(self, parflowConfig, terrainFile):
        self.parflowConfig = parflowConfig

        self.zSpacing = 1
        self.eScale = 0

        self.proxiesToDelete = []

        # Build up image grid
        self.image = vtk.vtkImageData()
        cg = self.parflowConfig.ComputationalGrid
        self.image.SetOrigin(cg.Lower.X, cg.Lower.Y, cg.Lower.Z)
        self.image.SetSpacing(cg.DX, cg.DY, cg.DZ)
        self.image.SetDimensions(cg.NX + 1, cg.NY + 1, cg.NZ + 1)  # Point maxes

        # Attach grid to paraview source
        self.paraviewProducer = simple.TrivialProducer()
        vtkProducer = self.paraviewProducer.GetClientSideObject()
        vtkProducer.SetOutput(self.image)

        self.elevationFilter = ElevationFilter(self.parflowConfig, terrainFile)
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
        cg = self.parflowConfig.ComputationalGrid
        self.zSpacing = space
        self.image.SetSpacing(cg.DX, cg.DY, cg.DZ * self.zSpacing)

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
