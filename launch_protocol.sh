#!/bin/bash

# launch_protocol.sh
# Automated setup and launch protocol for the Phi-Chain project.
# Designed to ensure a consistent and powerful launch environment.

# --- Configuration ---
PYTHON_VERSION="3.11"
VENV_DIR=".venv"
LOG_FILE="launch_protocol.log"

# --- Utility Functions ---

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a $LOG_FILE
}

check_prerequisites() {
    log "Checking prerequisites..."
    if ! command -v python3 &> /dev/null
    then
        log "Error: Python 3 is not installed. Please install Python $PYTHON_VERSION or higher."
        exit 1
    fi
    if ! command -v pip3 &> /dev/null
    then
        log "Error: pip3 is not installed. Please install it."
        exit 1
    fi
    log "Prerequisites check passed."
}

setup_environment() {
    log "Setting up virtual environment..."
    if [ ! -d "$VENV_DIR" ]; then
        python3 -m venv $VENV_DIR
        log "Virtual environment created at $VENV_DIR."
    else
        log "Virtual environment already exists."
    fi
    
    source $VENV_DIR/bin/activate
    log "Virtual environment activated."
    
    log "Installing Python dependencies..."
    if [ -f "core/requirements.txt" ]; then
        pip install -r core/requirements.txt >> $LOG_FILE 2>&1
    elif [ -f "requirements.txt" ]; then
        pip install -r requirements.txt >> $LOG_FILE 2>&1
    else
        log "Warning: requirements.txt not found. Skipping Python dependency installation."
    fi
    
    log "Environment setup complete."
}

run_tests() {
    log "Running core mathematical tests..."
    # Assuming a test script exists, e.g., in the tests directory
    if [ -f "tests/test_phi_chain.py" ]; then
        python tests/test_phi_chain.py >> $LOG_FILE 2>&1
        if [ $? -eq 0 ]; then
            log "Core tests passed successfully."
        else
            log "Error: Core tests failed. Check $LOG_FILE for details."
            exit 1
        fi
    else
        log "Warning: Core test script not found. Skipping tests."
    fi
}

start_core_components() {
    log "Starting Phi-Chain core components..."
    
    # 1. Start the Reversible Core (if applicable)
    if [ -f "reversible_phi_core.py" ]; then
        log "Starting Reversible Core in background..."
        python reversible_phi_core.py &
        REVERSIBLE_PID=$!
        log "Reversible Core PID: $REVERSIBLE_PID"
    fi
    
    # 2. Start the main prototype/simulator
    if [ -f "phi_chain_prototype.py" ]; then
        log "Starting Phi-Chain Prototype..."
        python phi_chain_prototype.py &
        PROTOTYPE_PID=$!
        log "Prototype PID: $PROTOTYPE_PID"
    fi
    
    log "Core components started."
}

# --- Main Execution ---

log "--- Phi-Chain Launch Protocol Initiated ---"

check_prerequisites
setup_environment
run_tests
start_core_components

log "Launch sequence complete. Core components are running in the background."
log "To stop the components, use 'kill $REVERSIBLE_PID $PROTOTYPE_PID' (PIDs are in the log)."
log "To access the web interface, open index.html or wallet.html in your browser."
log "--- Phi-Chain Launch Protocol Finished ---"

# Ensure the script is executable
chmod +x launch_protocol.sh
