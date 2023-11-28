# Install dependencies and run the script
export PYTHON_VERSION=3.11.6
pyenv install $PYTHON_VERSION
pyenv virtualenv $PYTHON_VERSION fuel-price-finder-simulator-$PYTHON_VERSION
pyenv local fuel-price-finder-simulator-$PYTHON_VERSION

# Shell
poetry shell
poetry install --no-root
