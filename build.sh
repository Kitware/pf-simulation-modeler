#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"

export NODE_OPTIONS=--openssl-legacy-provider
source "$parent_path/.venv/bin/activate"

ARGS="--server --port 1234 -D data/database/ -S data/share/ -O data/output/"

vue () {
    cd "$parent_path/vue-components"
    npm i
    npm run build
}

python_build () {
    cd "$parent_path"
    pip install .
    pf_sim_2 $ARGS
}

python_dev () {
    cd "$parent_path"
    pip install .
    python ./pf_sim_2/app/main.py --hot-reload $ARGS
}

if [[ -z $1 ]]; then # if no argument is passed
    python_dev
else
    vue && python_build
fi
