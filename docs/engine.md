# `engine/`

## `engine.py`

Main engine class initialized by `../main.py`.

Initializes `state` variables and `Simput` UI/models.

Initializes the following engine components:

- `files.py`
- `domain.py`
- `timing.py`
- `boundary_conditions.py`
- `pressure.py`
- `solver.py`
- `cli.py`
- `save_project.py`
- `snippets/`

---

## Pages

### `files.py`

Contains classes `FileDatabase` and `FileLogic` for the internal database and external `File Database` page respectively.

`FileDatabase` is an API that manages files on the server's filesystem.

`FileLogic` exposes the `FileDatabase` API to the `FileDatabase` vue component and handles UI specific logic.

### `domain.py`

`DomainLogic` class handles backend logic for the `Domain` page. Creates `state` variables for page state, file selection, simput UI elements, and domain parameters.

Majority of logic concerns tracking active files, file names, and the data contained within them.

### `timing.py`

`TimingLogic` class handles backend logic for the `Timing` page. Creates `state` variables `cycle_ids` and `sub_cycle_ids` to track creation of Cycle/SubCycle simput items.

### `boundary_conditions.py`

`BCLogic` class handles backend logic for the `Boundary Conditions` page.

Tracks active patches & patch names defined on the `Domain` page.

Tracks active Cycles & SubCycles defined on the `Timing` page and dynamically update simput model definitions based on their current state.

### `pressure.py`

`PressureLogic` class handles selection of pressure files.

### `solver.py`

`SolverLogic` class handles creation of Solver simput items.

---

## Misc Components

### `cli.py`

`ArgumentsValidator` class handles command line arguments and validates them with the `FileDatabase`.

### `save_project.py`

Handles the export of the current project and associated files. Creates project directory in `data/output` and copies all files to the project directory.

### `snippets/`

Module that contains handlers for pages' code snippets. Also handles the generation of all code at the `Code Generation` step.

**See [Snippets](snippets.md) for more.**
