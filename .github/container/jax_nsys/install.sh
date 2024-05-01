#!/bin/bash
#
# Usage: ./install.sh [optional arguments to virtualenv]
#
# If it doesn't already exist, this creates a virtual environment named
# `nsys_jax_env` in the current directory and installs Jupyter Lab and the
# dependencies of the Analysis.ipynb notebook that is shipped alongside this
# script inside the output archives of the `nsys-jax` wrapper.
#
# The expectation is that those archives will be copied and extracted on a
# laptop or workstation, and this installation script will be run there, while
# the `nsys-jax` wrapper is executed on a remote GPU cluster.
SCRIPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
VIRTUALENV="${SCRIPT_DIR}/nsys_jax_venv"
if [[ ! -d "${VIRTUALENV}" ]]; then
  # Let `virtualenv` find/choose a Python
  virtualenv "$@" "${VIRTUALENV}"
  . "${VIRTUALENV}/bin/activate"
  python -m pip install -U pip
  "${SCRIPT_DIR}/nsys-jax-ensure-protobuf"
  python -m pip install jupyterlab
  python -m pip install -e "${SCRIPT_DIR}/python/jax_nsys"
  curl -o "${VIRTUALENV}/bin/flamegraph.pl" https://raw.githubusercontent.com/brendangregg/FlameGraph/master/flamegraph.pl
  chmod 755 "${VIRTUALENV}/bin/flamegraph.pl"
else
  echo "Virtual environment already exists, not installing anything..."
fi
echo "Launching: cd ${SCRIPT_DIR} && ${VIRTUALENV}/bin/python -m jupyterlab Analysis.ipynb"
cd "${SCRIPT_DIR}" && "${VIRTUALENV}/bin/python" -m jupyterlab Analysis.ipynb