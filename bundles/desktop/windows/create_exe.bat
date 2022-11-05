pyinstaller ^
  --hidden-import vtkmodules.all ^
  --collect-data pywebvue ^
  --onefile ^
  --windowed ^
  --icon pf_sim_2.ico ^
  .\run.py
