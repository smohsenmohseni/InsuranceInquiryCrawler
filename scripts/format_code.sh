#!/bin/bash

THERE_IS_NO_CONFIGURATION_FILE='There is no configuration file.'


if [ ! -f ./pyproject.toml ] || [ ! -f ./.isort.cfg ] || [ ! -f ./mypy.ini ] || [ ! -f ./.flake8 ]
then
  echo -e "\n\033[31m${THERE_IS_NO_CONFIGURATION_FILE}\033[0m\n"
else
  isort . && echo -e \\n; black . && echo -e \\n; mypy . && echo -e \\n; flake8 .
fi
