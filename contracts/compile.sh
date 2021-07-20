#!/usr/bin/env bash

set -e -o pipefail

echo "----------------------------------------"
echo "Compiling contracts ... "
echo "----------------------------------------"

# Expected location of SmartPy CLI.
SMART_PY_CLI=~/smartpy-cli/SmartPy.sh

# Build artifact directory.
OUT_DIR=./.tmp_contract_build

# Array of SmartPy files to compile.
CONTRACTS_ARRAY=(demo)

# Exit if SmartPy is not installed. 
if [ ! -f "$SMART_PY_CLI" ]; then
    echo "Fatal: Please install SmartPy CLI at $SMART_PY_CLI" && exit
fi

function processContract {
    CONTRACT_NAME=$1
    OUT_DIR=$2
    CONTRACT_IN="${CONTRACT_NAME}.py"
    CONTRACT_OUT="${CONTRACT_NAME}.json"
    CONTRACT_COMPILED="${CONTRACT_NAME}/step_000_cont_0_contract.json"

    echo ">> Processing ${CONTRACT_NAME}"

    # Ensure file exists.
    if [ ! -f "$CONTRACT_IN" ]; then
        echo "Fatal: $CONTRACT_IN not found. Running from wrong dir?" && exit
    fi

    echo ">>> [1 / 3] Testing ${CONTRACT_NAME} ... "
    $SMART_PY_CLI test $CONTRACT_IN $OUT_DIR

    echo ">>> [2 / 3] Compiling ${CONTRACT_NAME} ..."
    $SMART_PY_CLI compile $CONTRACT_IN $OUT_DIR

    echo ">>> [3 / 3] Extracting Michelson contract ... "
    cp $OUT_DIR/$CONTRACT_COMPILED $CONTRACT_OUT
    echo ">>> Michelson contract written to ${CONTRACT_OUT}"
}

echo "> [1 / 2] Unit Testing and Compiling Contracts."
# Execute processContract on all files in CONTRACTS_ARRAY
for i in ${!CONTRACTS_ARRAY[@]}; do
    processContract ${CONTRACTS_ARRAY[$i]} $OUT_DIR
done

# Remove build artifacts.
echo "> [2 / 2] Cleaning up ..."
rm -rf $OUT_DIR
echo "> Removed artifacts."
echo ""

echo "----------------------------------------"
echo "Task complete."
echo "----------------------------------------"