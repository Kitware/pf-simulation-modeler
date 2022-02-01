import vtk
import numpy as np
from paraview import simple

from parflowio.pyParflowio import PFData

from .base import AbstractVisualization
from .colors import black


class SoilVisualization(AbstractVisualization):
    def __init__(self, view, parflowImage):
        super().__init__(view, parflowImage)
        self.parflowImage = self.parflowImage

        # Viz variables
        self.indicatorFilename = ""
        self.fieldName = "soilId"
        self.allSoilsRep = None
        self.selectedSoilRep = None
        self.zSpaceFactor = 1

    # -------------------------------------------------------------------------
    # Needed by all viz
    # -------------------------------------------------------------------------

    def getState(self):
        """Set of properties that are specific to this viz"""
        return {}

    # -------------------------------------------------------------------------
    # Viz setup
    # -------------------------------------------------------------------------

    def _load(self):
        # Load indicator file that contains soil ids
        try:
            a = PFData(self.indicatorFilename)
        except:
            print(f"Could not find pfb {self.indicatorFilename}")
            raise

        a.loadHeader()
        a.loadData()
        indicator = a.moveDataArray()

        # Add soil value on cells
        indicator.reshape(indicator.size)
        soilId = vtk.vtkIntArray()
        soilId.SetName(self.fieldName)
        soilId.SetNumberOfComponents(1)
        soilId.SetNumberOfTuples(indicator.size)
        for index, value in enumerate(np.nditer(indicator)):
            soilId.SetTuple1(index, value)
        self.parflowImage.addCellArray(soilId)

        self.source = self.parflowImage.getSource()

        # Threshold for showing just selected soil
        self.selectedSoil = simple.Threshold(Input=self.source)
        self.selectedSoil.Scalars = [
            "CELLS",
            self.fieldName,
        ]
        self.selectedSoil.LowerThreshold = 1.0
        self.selectedSoil.UpperThreshold = 1.0
        self.selectedSoil.ThresholdMethod = vtk.vtkThreshold.THRESHOLD_BETWEEN

        # show data in view
        self.allSoilsRep = simple.Show(self.source, self.view, "GeometryRepresentation")
        self.selectedSoilRep = simple.Show(
            self.selectedSoil, self.view, "UnstructuredGridRepresentation"
        )

        # Color and display visualization
        self.allSoilsRep.SetRepresentationType("Surface")
        self.selectedSoilRep.SetRepresentationType("Surface")
        simple.ColorBy(self.allSoilsRep, ("CELLS", self.fieldName))
        simple.ColorBy(self.selectedSoilRep, ("CELLS", self.fieldName))

        # Color axes info
        self.allSoilsRep.DataAxesGrid.XTitle = ""
        self.allSoilsRep.DataAxesGrid.YTitle = ""
        self.allSoilsRep.DataAxesGrid.XLabelColor = black
        self.allSoilsRep.DataAxesGrid.YLabelColor = black
        self.allSoilsRep.DataAxesGrid.ZLabelColor = black
        self.allSoilsRep.DataAxesGrid.GridColor = black
        self.allSoilsRep.DataAxesGrid.FacesToRender = 36

        # update the self.view to ensure updated data information
        self.setSoilVisualizationMode("all")
        simple.Render(self.view)

        self.loaded = True

        # Register components for services
        self.allRepresentations.append(self.allSoilsRep)
        self.allRepresentations.append(self.selectedSoilRep)
        self.edgeRepresentations.append(self.allSoilsRep)
        self.edgeRepresentations.append(self.selectedSoilRep)
        self.scaleRepresentations.append(self.allSoilsRep)
        self.scaleRepresentations.append(self.selectedSoilRep)

        self.proxyToDelete.append(self.allSoilsRep)
        self.proxyToDelete.append(self.selectedSoilRep)
        self.proxyToDelete.append(self.selectedSoil)

    # -------------------------------------------------------------------------
    # Viz API
    # -------------------------------------------------------------------------

    def activateSoil(self, soil_value):
        self.selectedSoil.LowerThreshold = soil_value
        self.selectedSoil.UpperThreshold = soil_value
        self.selectedSoil.ThresholdMethod = vtk.vtkThreshold.THRESHOLD_BETWEEN
        self.selectedSoil.UpdatePipeline()
        return self.selectedSoil.GetDataInformation().DataInformation.GetNumberOfCells()

    def setSoilVisualizationMode(self, mode):
        if mode == "selection":
            simple.ColorBy(self.allSoilsRep, None)
            self.allSoilsRep.SetRepresentationType("Outline")
        else:
            self.allSoilsRep.SetRepresentationType("Surface")
            simple.ColorBy(self.allSoilsRep, ("CELLS", self.fieldName))

        self.setEdgeVisibility(self.edgeVisibility)

    def setSoilColors(self, valueToFloatRGBMap):
        lut = simple.GetColorTransferFunction(self.fieldName)
        lut.InterpretValuesAsCategories = 1
        lut.AnnotationsInitialized = 1

        indexedOpacities = []
        annotations = []
        indexedColors = []

        for (soil_value, rgb) in valueToFloatRGBMap.items():
            annotations.append(soil_value)  # Value
            annotations.append(soil_value)  # Label

            indexedColors.extend(rgb)
            indexedOpacities.append(1.0)

        lut.IndexedOpacities = indexedOpacities
        lut.Annotations = annotations
        lut.IndexedColors = indexedColors
