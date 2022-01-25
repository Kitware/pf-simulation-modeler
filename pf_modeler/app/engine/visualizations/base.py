import vtk
from paraview import simple
from parflowio.pyParflowio import PFData
from abc import ABC, abstractmethod


class AbstractVisualization(ABC):
    def __init__(self, view, parflowImage, parflowConfig):
        self.loaded = False
        self.view = view
        self.parflowImage = parflowImage
        self.parflowConfig = parflowConfig

        # Viz variables
        self.edgeVisibility = False
        self.allRepresentations = []
        self.edgeRepresentations = []
        self.scaleRepresentations = []
        self.proxyToDelete = []

    # Common to all visualizations
    def setEdgeVisibility(self, visible):
        self.edgeVisibility = visible

        repTypeSurface = "Surface With Edges" if self.edgeVisibility else "Surface"
        repTypeOutline = "Wireframe" if self.edgeVisibility else "Outline"

        for rep in self.edgeRepresentations:
            if "Surface" in str(rep.Representation):
                rep.SetRepresentationType(repTypeSurface)
            else:
                rep.SetRepresentationType(repTypeOutline)
            rep.AmbientColor = [0.2, 0.2, 0.2]
            rep.EdgeColor = [0.2, 0.2, 0.2]

        return self.edgeVisibility

    def setAxesInfoVisibility(self, visibility):
        for rep in self.allRepresentations:
            rep.DataAxesGrid.GridAxesVisibility = 1

    def activate(self, activate=True):
        if activate:
            if not self.loaded:
                self._load()
            self.setEdgeVisibility(self.edgeVisibility)

        visibility = 1 if activate else 0
        for rep in self.allRepresentations:
            rep.Visibility = visibility

    @abstractmethod
    def _load(self):
        pass

    def __del__(self):
        for proxy in self.proxyToDelete:
            simple.Delete(proxy)
