#!/bin/bash
set -uo pipefail
set +e

FAILURE=false

echo "safety (failure is tolerated)"
FILE=requirements/prod.txt
if [ -f "$FILE" ]; then
    # We're in the main repo
    safety check -r requirements/prod.txt -r requirements/dev.txt
fi

printf "\npylint\n\n"
pylint modules libs app || FAILURE=true

printf "\npycodestyle\n\n"
pycodestyle modules libs app || FAILURE=true

printf "\npydocstyle\n\n"
pydocstyle modules libs app || FAILURE=true

printf "\nmypy\n\n"
mypy modules libs app || FAILURE=true

printf "\nbandit\n\n"
bandit -ll -r {modules,libs,app} || FAILURE=true

printf "\n\n"
if [ "$FAILURE" = true ]; then
  echo "Linting failed"
  exit 1
fi
echo "Linting passed"
exit 0
