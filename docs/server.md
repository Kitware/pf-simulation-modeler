# State Variables

Here is a list of `state` variables/`ctrl` functions and a general location of where they are set.

---

## `state`

```python
# General | engine.py
current_view: str # current page
views: list[str]  # list of pages
sim_name: str     # name of simulation

# File Database | engine/files.py
db_files: dict              # dictionary of files in file database
file_categories: list[str]  # list of file categories
upload_error: str           # error message for file upload
db_selected_file: str       # selected file in file database

# Domain | engine/domain.py
domain_view: str # "grid" or "viz", determines which view is displayed
indicator_file: str     # indicator FileDatabase string
slope_x_file: str       # slope X FileDatabase string
slope_y_file: str       # slope Y FileDatabase string
elevation_file: str     # elevation FileDatabase string
indicator_filename: str # indicator filename
slope_x_filename: str   # slope X filename
slope_y_filename: str   # slope Y filename
elevation_filename: str # elevation filename
grid_id: int    # simput Grid proxy id
patches_id: int # simput Patches proxy id
x_bound: list[str] # x domain boundary
y_bound: list[str] # y domain boundary
z_bound: list[str] # z domain boundary
domain_geom_name: str    # name of domain geometry
indicator_geom_name: str # name of indicator geometry

# Timing | engine/timing.py
timing_id: int                 # simput Timing proxy id
cycle_ids: list[int]           # simput Cycle proxy ids
sub_cycle_ids: dict[int, list] # simput SubCycle proxy ids

# Boundary Conditions | engine/boundary_conditions.py
bc_pressure_ids: list[int]             # simput BCPressure proxy ids
bc_pressure_value_ids: dict[int, list] # simput BCPressureValue proxy ids
bc_patch_names: list[str] # list of patch names defined on Domain page
cycle_defs: dict[int, str]    # names of dynamically loaded cycles | engine.py
subcycle_defs: dict[int, str] # names of dynamically loaded subcycles | engine.py

# Pressure | engine/pressure.py
pressure_file: str     # pressure FileDatabase string
pressure_filename: str # pressure filename
pressure_patch: str    # pressure patch name

# Subsurface Properties | engine/domain.py
domain_id: int      # simput Domain proxy id
soil_ids: list[int] # simput Soil proxy ids

# Solver | engine/solver.py
solver_outputs: list[int] # array of selected solver outputs
solver_id: int            # simput Solver proxy id
solver_nonlinear_id: int  # simput SolverNonlinear proxy id
solver_linear_id: int     # simput SolverLinear proxy id

# Code Generation | engine/snippets/snippet_manager.py
generated_code: str   # generated code
display_snippet: bool # toggle display of snippets
active_snippet: str   # corresponds to current page
snippet_dirty: bool   # toggle display of save button

# Save Project | engine/save_project.py
save_dialog: bool      # toggle display of save dialog
save_page: int         # current page of save dialog
success_snackbar: bool # toggle display of success snackbar

# CLI | engine/cli.py
work_dir: str  # output directory
datastore: str # datastore directory
sharedir: str  # sharedir directory
warning: str   # warning message
```

---

## `ctrl`

```python
# General | engine.py
get_pxm()            # return the simput proxymanager
get_simput_manager() # return the simput manager

# Save Project | engine/save_project.py
save_project() # save project to file

# Timing | engine/timing.py
delete_cycle(id, owner_id=None) # delete a cycle proxy
create_cycle(proxy_type, owner_id=None) # create a proxy of type proxy_type
update_cycle_list() # recalculate state.cycle_ids and state.sub_cycle_ids

# Snippet Manager | engine/snippets/snippet_manager.py
toggle_snippet(snippet) # toggle state.display_snippet and regenerate snippet page's code
get_snippet(snippet)    # generate snippet page's code and set state.active_snippet
generate_code()         # generate code for all pages and set state.generated_code

# UI Simput | ui.py
simput_apply() # calls simput_widget.apply()
simput_reset() # calls simput_widget.reset()
simput_push(id)  # calls simput_widget.push(id)
```
