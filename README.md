# Parflow Simulation Modeler

## License

Free software: Apache Software License

## Installing

Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Build and install the Vue components

```bash
export NODE_OPTIONS=--openssl-legacy-provider
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
pf-simulation-modeler --help
pf-simulation-modeler --server --port 1234 -D data/database/ -S data/share/ -O data/output/
```

## Documentation

- [Engine](docs/engine.md) Structure
  - [Snippets](docs/snippets.md)
- [UI](docs/ui.md) Structure
- Server [`state` and `ctrl`](docs/server.md) variables

## File Structure

```bash
- pf_simulation_modeler/
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
