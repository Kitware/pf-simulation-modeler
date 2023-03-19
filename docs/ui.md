# `ui/`

## `ui.py`

Main UI class initialized by `../main.py`.

Creates basic trame `SinglePageLayout` and initializes the `Simput` root component.

Controls display of the current page based on the `state`'s `current_view` variable.

Initializes the following pages:

- `file_db.py` - 'File Database'
- `simulation_type.py` - 'Simulation Type'
- `domain.py` - 'Domain'
- `timing.py` - 'Timing'
- `boundary_conditions.py` - 'Boundary Conditions'
- `pressure.py` - 'Pressure'
- `subsurface_props.py` - 'Subsurface Properties'
- `solver.py` - 'Solver'
- `code_gen.py` - 'Code Generation'

---

### `file_db.py`

File database class used to store and retrieve files from the local filesystem. Uses custom vue component `FileDatabase`.

### `simulation_type.py`

Used to select broad parameters of the simulation. Uses custom vue component `SimulationType` and `vuetify` elements.

### `domain.py`

Parameters for the domain of the simulation. Select relevant files including: Indicator, Slope X, Slope Y, and Elevation.

Selecting an Indicator file will automatically calculate the default **computational grid** and **box domain**.

Default patches for the domain are also editable in the **Patches** section.

Selecting a Slope X, Slope Y, and Indicator will allow users to view a Paraview rendered preview of the domain. *(Not yet implemented)*

### `timing.py`

Define general timing parameters and create timing Cycles.

### `boundary_conditions.py`

Define boundary conditions for the domain patches. Assign a boundary type and a timing cycle to each patch.

### `pressure.py`

Select a pressure file and the associated domain patch.

### `subsurface_props.py`

Fill in subsurface properties for each soil type in the property matrix. The `domain` row parameters will act as default values for soils with unset properties.

### `solver.py`

Specify solver parameters.

### `code_gen.py`

Display the generated code for the simulation.

At this point the user can use the **Save** button to export the project to the directory specified in the `--datastore` cli argument.

---

## Other Components

### `save_project.py`

Dialogue popup for saving the project. There are three steps:

- Output Directory
  - Select project name and the directory to save the project to.
- Project Files
  - Ensure required project files are selected.
- Project Code
  - Select project code and save to the project directory.

### `snippet.py`

Used to display code snippets on various pages.
