# Parflow Simulation Modeler

Port of pf-simulation-modeler to trame 2

- Free software: Apache Software License

## Installing

Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Build and install the Vue components

```bash
cd vue-components
npm i
npm run build
cd -
```

Install the application

```bash
pip install -e .
```

Run the application

```bash
pf_sim_2
```

### Or use the build script

```bash
./build.sh   # for development (will not rebuild vue components)
./build.sh b # for full rebuild (hot reloads will not work)
```

*Note: only use `build.sh` after initial setup install.*

## File Structure

```bash
- pf_sim_2/
    - app/
        - engine/
            - model/    # Simput model/UI definitions
            - snippets/ # Logic for page code snippets
            - engine.py # Main logic handler
            - ...       # Logic components (generally specific to pages)

        - ui/
            - ui.py # Main UI handler
            - ...   # UI components (pages)

        - main.py # Entry point

    - module/  # Serves the compiled Vue components
    - widgets/ # Python wrapper around the Vue components

- vue-components/src/components/ # Custom Vue components
    - FileDatabase/ # FileDatabase Vue component
        - index.vue     # Vue component
        - script.js     # JS logic
        - template.html # HTML template

    - ... # Other Vue components

- data/ # Data files (used for cli args)
    - database/ # FileDatabase data
    - output/   # Project Output data
    - share/    # Shared data
```

## Features

- TODO
