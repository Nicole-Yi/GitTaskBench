#!/usr/bin/env python3
import argparse
import os
import subprocess
import logging
import time # Added for sleep
import shlex # Added for command splitting
# No need for platform module anymore, removed platform import
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

# Configure logging for the script itself
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(threadName)s - [BatchScript] %(message)s' # Added prefix
)
logger = logging.getLogger(__name__)

def run_subprocess_cmd(command: List[str], task_name: str, step_name: str) -> bool:
    """
    Runs a command as a subprocess and logs its output/errors.

    Args:
        command: The command to run as a list of strings.
        task_name: The name of the parent task for logging context.
        step_name: The name of the specific step being executed (e.g., "Docker Prune").

    Returns:
        True if the command executed successfully (return code 0), False otherwise.
    """
    try:
        # For commands involving shell expansion like $(docker ps -aq), use shell=True
        # and pass the command as a string. Be cautious with shell=True.
        is_shell_cmd = isinstance(command, str) or any("$" in str(arg) or "*" in str(arg) for arg in command)
        cmd_str = ' '.join(command) if not isinstance(command, str) else command
        logger.info(f"[{task_name}] Running {step_name}: {cmd_str}")

        result = subprocess.run(
            cmd_str if is_shell_cmd else command,
            capture_output=True,
            text=True,
            check=False,
            shell=is_shell_cmd # Enable shell if needed (e.g., for $(...))
        )

        if result.stdout:
            stdout_msg = f"[{task_name}] {step_name} stdout:\n{result.stdout.strip()}"
            logger.info(stdout_msg)
        if result.stderr:
            stderr_msg = f"[{task_name}] {step_name} stderr:\n{result.stderr.strip()}"
            logger.warning(stderr_msg)

        if result.returncode == 0:
            logger.info(f"[{task_name}] {step_name} completed successfully.")
            return True
        else:
            logger.error(f"[{task_name}] {step_name} failed (RC: {result.returncode}).")
            return False
    except FileNotFoundError:
        cmd_name = command[0] if isinstance(command, list) and command else str(command)
        logger.error(f"[{task_name}] {step_name} failed: Command not found ('{cmd_name}'). Ensure it's in PATH.")
        return False
    except Exception as e:
        logger.error(f"[{task_name}] {step_name} failed due to script exception: {e}")
        return False


def run_sweagent_task(
    base_cmd: List[str],
    problem_statement_path: str,
    task_name: str
) -> Tuple[str, bool, str]:
    """
    Runs a single SWE-agent task, letting its output go directly to the terminal.

    Args:
        base_cmd: The base list of command arguments for sweagent run.
        problem_statement_path: The path to the specific .md problem statement.
        task_name: A descriptive name for the task (e.g., the .md filename).

    Returns:
        A tuple containing:
        - task_name (str): The name of the task.
        - success (bool): True if the command executed successfully (return code 0), False otherwise.
        - output (str): An empty string, as output is not captured directly here.
    """
    full_cmd = base_cmd + ['--problem_statement.path', problem_statement_path]
    logger.info(f"Starting task: {task_name} | Command: {' '.join(full_cmd)}")
    logger.info(f"--- Output for {task_name} will appear below (interleaved if workers > 1) ---")
    try:
        # Let the subprocess inherit stdout/stderr from the parent for live output
        process = subprocess.Popen(full_cmd)
        returncode = process.wait()
        output = "" # Output is inherited, not captured

        if returncode == 0:
            logger.info(f"--- Task {task_name} completed successfully (RC: {returncode}) ---")
            return task_name, True, output
        else:
            logger.error(f"--- Task {task_name} failed (RC: {returncode}) ---")
            return task_name, False, output

    except Exception as e:
        logger.error(f"--- Task {task_name} failed to run due to script exception: {e} ---")
        rc = -1
        return task_name, False, f"Exception: {str(e)}\nReturn Code: {rc}"

def post_task_actions(
    task_name: str,
    host_repo_path: str,
    sleep_duration: int,
    skip_docker_prune: bool,
    skip_git_commit: bool
) -> None:
    """
    Performs cleanup and Git operations after a task finishes.
    Args are the same as before.
    """
    logger.info(f"--- Starting post-task actions for {task_name} ---")

    if not skip_docker_prune:
        logger.info(f"[{task_name}] Cleaning up Docker containers...")
        # Use shell=True for command substitution $()
        stop_cmd = "docker stop $(docker ps -aq)"
        rm_cmd = "docker rm $(docker ps -aq)"
        run_subprocess_cmd(stop_cmd, task_name, "Docker Stop")
        run_subprocess_cmd(rm_cmd, task_name, "Docker Remove")
        logger.info(f"[{task_name}] Docker cleanup finished.")
    else:
        logger.info(f"[{task_name}] Skipping Docker prune step.")

    if sleep_duration > 0:
        logger.info(f"[{task_name}] Sleeping for {sleep_duration} seconds...")
        time.sleep(sleep_duration)
        logger.info(f"[{task_name}] Sleep finished.")

    if not skip_git_commit:
        if not os.path.isdir(host_repo_path):
            logger.error(f"[{task_name}] Git repo path not found or not a directory: {host_repo_path}. Skipping Git actions.")
            return

        logger.info(f"[{task_name}] Performing Git actions in {host_repo_path}...")
        add_cmd = ['git', '-C', host_repo_path, 'add', '.']
        run_subprocess_cmd(add_cmd, task_name, "Git Add")

        commit_msg = f"SWE-agent task {task_name}: Post-run commit"
        commit_cmd = ['git', '-C', host_repo_path, 'commit', '--allow-empty', '--no-verify', '-m', commit_msg]
        run_subprocess_cmd(commit_cmd, task_name, "Git Commit")
    else:
         logger.info(f"[{task_name}] Skipping Git commit step.")

    logger.info(f"--- Finished post-task actions for {task_name} ---")


def main():
    """
    Main function restored.
    """
    parser = argparse.ArgumentParser(
        description='Batch run SWE-agent tasks with post-task actions.'
    )
    # Add all arguments back (prompt-dir, workers, model-name, image, repo-path, config-path, host-repo-path, sleep-duration, skip-docker-prune, skip-git-commit, log-level)
    parser.add_argument(
        '--prompt-dir',
        type=str,
        required=True,
        help='Directory containing the .md problem statement files.'
    )
    parser.add_argument(
        '--workers',
        type=int,
        default=1,
        help='Number of concurrent workers. Set to 1 for sequential post-task actions.'
    )
    parser.add_argument(
        '--model-name', type=str, required=True, help='Agent model name.'
    )
    parser.add_argument(
        '--image', type=str, required=True, help='Docker image.'
    )
    parser.add_argument(
        '--repo-path', type=str, required=True, help='Repo path inside container.'
    )
    parser.add_argument(
        '--config-path', type=str, required=True, help='SWE-agent config file.'
    )
    parser.add_argument(
        '--host-repo-path', type=str, required=True, help='Host repo path for Git.'
    )
    parser.add_argument(
        '--sleep-duration', type=int, default=5, help='Sleep duration after task.'
    )
    parser.add_argument(
        '--skip-docker-prune', action='store_true', help='Skip Docker cleanup.'
    )
    parser.add_argument(
        '--skip-git-commit', action='store_true', help='Skip Git commit.'
    )
    parser.add_argument(
        '--log-level', type=str, default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Logging level.'
    )
    # Add arguments for checking existing output
    parser.add_argument(
        '--output-base-dir',
        type=str,
        default='trajectories', # Default SWE-agent output base dir
        help='Base directory where SWE-agent saves task outputs.'
    )
    parser.add_argument(
        '--user-name',
        type=str,
        default='batch_user', # Default user for trajectory path
        help='Username used in the SWE-agent output trajectory path.'
    )

    args = parser.parse_args()

    # Argument Validation (Workers and Git path)
    if args.workers > 1:
        logger.warning(
            f"Running with {args.workers} workers. Post-task actions (Docker/Git) might interleave. Set --workers 1 for sequential execution."
        )
    if not args.skip_git_commit and not os.path.isdir(args.host_repo_path):
         logger.warning(
             f"Host Git repository path '{args.host_repo_path}' not found. Git actions will be skipped."
         )

    # Set logging level
    log_level_upper = args.log_level.upper()
    try:
        log_level_int = getattr(logging, log_level_upper)
        # Reconfigure logger level based on args
        logging.getLogger().setLevel(log_level_int)
        for handler in logging.getLogger().handlers:
            handler.setLevel(log_level_int)
        logger.info(f"Logging level set to {log_level_upper}")
    except AttributeError:
        logger.error(f"Invalid log level: {args.log_level}. Using INFO.")
        # Keep default INFO level from basicConfig

    # Validate prompt directory
    if not os.path.isdir(args.prompt_dir):
        logger.error(f"Prompt directory not found: {args.prompt_dir}")
        return

    all_md_files = [f for f in os.listdir(args.prompt_dir) if f.endswith('.md') and os.path.isfile(os.path.join(args.prompt_dir, f))]
    if not all_md_files:
        logger.warning(f"No .md files found in {args.prompt_dir}")
        return

    logger.info(f"Found {len(all_md_files)} total .md files in {args.prompt_dir}")

    # Filter out tasks with existing output directories
    md_files_to_run = []
    skipped_count = 0
    for md_file in all_md_files:
        task_name_without_ext = os.path.splitext(md_file)[0]
        # Construct the expected output path based on SWE-agent conventions
        expected_output_dir = os.path.join(
            args.output_base_dir,
            args.user_name,
            f"{args.model_name}-{task_name_without_ext}"
        )

        if os.path.isdir(expected_output_dir):
            logger.info(f"Skipping task '{md_file}': Output directory already exists at '{expected_output_dir}'")
            skipped_count += 1
        else:
            md_files_to_run.append(md_file)

    if skipped_count > 0:
        logger.info(f"Skipped {skipped_count} tasks because their output directories already exist.")

    if not md_files_to_run:
        logger.warning(f"No tasks left to run after checking for existing outputs.")
        return

    logger.info(f"Preparing to run {len(md_files_to_run)} tasks.")
    # Log settings
    logger.info(f"Workers: {args.workers}")
    logger.info(f"Docker Prune Skipped: {args.skip_docker_prune}")
    logger.info(f"Git Commit Skipped: {args.skip_git_commit}")
    logger.info(f"Sleep Duration: {args.sleep_duration}")
    logger.info(f"Host Git Repo: {args.host_repo_path if not args.skip_git_commit else 'N/A'}")

    base_cmd = [
        'sweagent', 'run',
        '--config', args.config_path,
        '--agent.model.name', args.model_name,
        '--env.repo.path', args.repo_path,
        '--env.deployment.image', args.image,
    ]

    results = {}
    with ThreadPoolExecutor(max_workers=args.workers, thread_name_prefix='SWEAgentWorker') as executor:
        futures = {
            executor.submit(
                run_sweagent_task,
                base_cmd,
                os.path.join(args.prompt_dir, md_file),
                md_file
            ): md_file
            for md_file in md_files_to_run
        }

        for future in as_completed(futures):
            task_name = futures[future]
            try:
                name, success, output_str = future.result()
                results[name] = {'success': success, 'output': output_str}
            except Exception as exc:
                logger.error(f'{task_name} generated an exception during future processing: {exc}')
                results[task_name] = {'success': False, 'output': f"Exception: {str(exc)}"}

            # Perform post-task actions
            post_task_actions(
                task_name=task_name,
                host_repo_path=args.host_repo_path,
                sleep_duration=args.sleep_duration,
                skip_docker_prune=args.skip_docker_prune,
                skip_git_commit=args.skip_git_commit
            )

    # Reporting
    successful_tasks = sum(1 for r in results.values() if r['success'])
    failed_tasks = len(results) - successful_tasks
    logger.info("\n--- Batch Run Summary ---")
    logger.info(f"Total tasks processed: {len(results)}")
    logger.info(f"Successful SWE-agent runs: {successful_tasks}")
    logger.info(f"Failed SWE-agent runs: {failed_tasks}")
    if failed_tasks > 0:
        logger.warning("Failed SWE-agent runs list:")
        for name, result in results.items():
            if not result['success']:
                 failure_reason = result.get('output', 'Unknown error').splitlines()[0]
                 logger.warning(f"- {name} (Reason: {failure_reason})")

# Add the main execution block back
if __name__ == "__main__":
    main() 