#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# !!! IMPORTANT: Set this to the absolute path of your Git repository on the HOST machine !!!
# Example: HOST_REPO_PATH="/home/user/my_project_repo"
HOST_REPO_PATH="/data/data/agent_test_codebase/GitTaskBench" # MODIFY THIS

# Directory containing the .md problem statement files
PROMPT_DIR="/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/prompt"

# Path to the Python batch script
PYTHON_SCRIPT="/data/code/agent_new/SWE-agent/batch_sweagent_run.py"

# --- SWE-agent Parameters (Modify as needed) ---
MODEL_NAME="claude-3-5-sonnet-20241022"
# Find your image ID using 'docker images | grep sweagent'
# Example: DOCKER_IMAGE="sweagent/swe-agent:latest" or "3eb72bc4a848"
DOCKER_IMAGE="3eb72bc4a848" # MODIFY THIS if necessary
REPO_PATH_IN_CONTAINER="/data/data/agent_test_codebase/GitTaskBench" # Path inside the container
CONFIG_FILE="/data/code/agent_new/SWE-agent/config/default.yaml"

# --- Batch Script Parameters ---
# Set to 1 for sequential post-task actions (recommended for Docker/Git safety)
NUM_WORKERS=1
# Sleep duration in seconds after each task's cleanup
SLEEP_DURATION=5
# Set to "true" to skip docker prune, leave empty or comment out to enable prune
# SKIP_DOCKER_PRUNE="true"
# Set to "true" to skip git commit, leave empty or comment out to enable commit
# SKIP_GIT_COMMIT="true"
# Logging level for the script (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL="INFO"
# --- New Parameters for Skipping --- #
# Base directory where SWE-agent outputs are stored
OUTPUT_BASE_DIR="trajectories" # Default: trajectories
# Username used in the output path structure
USER_NAME="batch_user" # Default: batch_user

# --- Argument Construction ---
ARGS=(
    "--prompt-dir" "$PROMPT_DIR"
    "--host-repo-path" "$HOST_REPO_PATH"
    "--workers" "$NUM_WORKERS"
    "--sleep-duration" "$SLEEP_DURATION"
    "--log-level" "$LOG_LEVEL"
    # SWE-agent specific args
    "--model-name" "$MODEL_NAME"
    "--image" "$DOCKER_IMAGE"
    "--repo-path" "$REPO_PATH_IN_CONTAINER"
    "--config-path" "$CONFIG_FILE"
    # New args for skipping
    "--output-base-dir" "$OUTPUT_BASE_DIR"
    "--user-name" "$USER_NAME"
)

# Add optional flags if set
if [[ -n "$SKIP_DOCKER_PRUNE" && "$SKIP_DOCKER_PRUNE" == "true" ]]; then
    ARGS+=("--skip-docker-prune")
fi

if [[ -n "$SKIP_GIT_COMMIT" && "$SKIP_GIT_COMMIT" == "true" ]]; then
    ARGS+=("--skip-git-commit")
fi


# --- Execution ---
echo "Starting SWE-agent batch run..."
echo "Python Script: $PYTHON_SCRIPT"
echo "Host Repo Path (for Git): $HOST_REPO_PATH"
echo "Prompt Directory: $PROMPT_DIR"
echo "Workers: $NUM_WORKERS"
echo "Sleep Duration: $SLEEP_DURATION"
echo "Log Level: $LOG_LEVEL"
echo "SWE-agent Model: $MODEL_NAME"
echo "SWE-agent Image: $DOCKER_IMAGE"
echo "SWE-agent Repo Path (Container): $REPO_PATH_IN_CONTAINER"
echo "SWE-agent Config: $CONFIG_FILE"
[[ -n "$SKIP_DOCKER_PRUNE" && "$SKIP_DOCKER_PRUNE" == "true" ]] && echo "Docker Prune: SKIPPED"
[[ -n "$SKIP_GIT_COMMIT" && "$SKIP_GIT_COMMIT" == "true" ]] && echo "Git Commit: SKIPPED"
echo "Output Base Dir (for checking): $OUTPUT_BASE_DIR"
echo "Username (for checking): $USER_NAME"
echo "---"


# Ensure the script is executable (optional, but good practice)
# chmod +x $PYTHON_SCRIPT

# Execute the Python script with all arguments
python3 "$PYTHON_SCRIPT" "${ARGS[@]}"

echo "---"
echo "Batch run script finished."
