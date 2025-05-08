import json
import logging
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
import os # Import os for listdir
import re # Import re for log parsing

# Try importing rich, provide instructions if not found
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
except ImportError:
    print("Error: 'rich' library not found. Please install it using: pip install rich")
    sys.exit(1)

# 配置日志 (optional, rich handles its own formatting well)
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[logging.StreamHandler(sys.stdout)],
# )

# 使用 Rich Console
console = Console()


def parse_execution_log(log_file_path: Path) -> Dict[str, Dict[str, Any]]:
    """Parses the all_tests.log file to extract execution status of each test.

    Args:
        log_file_path: Path to the all_tests.log file.

    Returns:
        A dictionary mapping test names to their execution status.
        Example: {'TestName_01': {'status': 'success', 'exit_code': 0},
                  'TestName_02': {'status': 'failed', 'exit_code': 1}}
    """
    execution_statuses: Dict[str, Dict[str, Any]] = {}
    try:
        with log_file_path.open("r", encoding="utf-8") as f:
            current_test_name: Optional[str] = None
            for line in f:
                line = line.strip()
                # Regex to find the start of a test execution
                start_match = re.search(r"Executing test for: (\S+)", line)
                if start_match:
                    current_test_name = start_match.group(1)
                    if current_test_name not in execution_statuses: # Initialize if not seen
                        execution_statuses[current_test_name] = {"status": "unknown", "exit_code": None}
                    continue

                if current_test_name:
                    # Regex to find successful execution
                    success_match = re.search(r"Execution successful for: {}".format(re.escape(current_test_name)), line)
                    if success_match:
                        execution_statuses[current_test_name] = {"status": "success", "exit_code": 0}
                        current_test_name = None # Reset for next test block
                        continue

                    # Regex to find failed execution and capture exit code
                    fail_match = re.search(r"Execution FAILED for: {} \(Exit Code: (\d+)\)".format(re.escape(current_test_name)), line)
                    if fail_match:
                        exit_code = int(fail_match.group(1))
                        execution_statuses[current_test_name] = {"status": "failed", "exit_code": exit_code}
                        current_test_name = None # Reset for next test block
                        continue
    except FileNotFoundError:
        console.print(f":x: [bold red]Execution log file not found:[/bold red] {log_file_path}")
    except Exception as e:
        console.print(f":x: [bold red]Error reading execution log {log_file_path}:[/bold red] {e}")
    return execution_statuses


def find_latest_result(file_path: Path) -> Dict[str, Any] | None:
    """Reads a JSON Lines file and returns the last valid JSON object.

    Args:
        file_path: Path to the results.jsonl file.

    Returns:
        The last parsed JSON object as a dictionary, or None if the file
        is empty, not found, or contains no valid JSON.
    """
    last_result: Dict[str, Any] | None = None
    try:
        with file_path.open("r", encoding="utf-8") as f:
            # Read all lines and process the last one
            lines = f.readlines()
            if not lines:
                return None
            last_line = lines[-1].strip()
            if last_line:
                try:
                    line_data = json.loads(last_line)
                    if isinstance(line_data, dict):
                        last_result = line_data
                except json.JSONDecodeError:
                    # Use console.print for rich error messages
                    console.print(
                        f"[yellow]Skipping invalid JSON line in {file_path}:[/] {last_line}"
                    )
    except FileNotFoundError:
        console.print(f":x: [bold red]Result file not found:[/bold red] {file_path}")
    except Exception as e:
        console.print(f":x: [bold red]Error reading {file_path}:[/bold red] {e}")
    return last_result


def generate_summary(results_dir: Path, summary_file: Path, execution_log_file: Path) -> None:
    """Generates a summary report from all results.jsonl files and execution log.

    Args:
        results_dir: Path to the directory containing test result subdirectories.
        summary_file: Path to save the summary report.
        execution_log_file: Path to the all_tests.log file.
    """
    # --- Parse Execution Log ---
    execution_statuses = parse_execution_log(execution_log_file)
    if not execution_statuses:
        console.print(":warning: [yellow]Could not parse any execution statuses from log.[/]")
        # Decide if to proceed or exit; for now, proceed but metrics will be affected

    # --- Calculate Expected Tests (from test_scripts directory) ---
    test_scripts_dir = results_dir.parent / "test_scripts"
    expected_tests_from_scripts_count = 0
    all_script_test_names: List[str] = []
    if test_scripts_dir.is_dir():
        all_script_test_names = sorted([item.name for item in test_scripts_dir.iterdir() if item.is_dir()])
        expected_tests_from_scripts_count = len(all_script_test_names)
    else:
        console.print(f":warning: [yellow]Could not find test scripts directory:[/yellow] {test_scripts_dir}")

    # --- Initialize Counters based on Execution Status ---
    total_attempted_scripts = expected_tests_from_scripts_count # Assuming all dirs in test_scripts were attempted
    scripts_execution_successful = 0
    scripts_execution_failed = 0

    content_validation_passed = 0  # For scripts that executed successfully
    content_validation_failed = 0  # For scripts that executed successfully
    
    execution_failure_details: List[Tuple[str, str]] = []  # (test_name, reason like "Exit Code: X")
    content_failure_details: List[Tuple[str, str]] = []    # (test_name, comments from jsonl or missing file)
    
    processed_jsonl_count = 0 # Count of successfully parsed results.jsonl files

    plain_summary_lines = []

    if not all_script_test_names:
        warning_message = f"No test script directories found in {test_scripts_dir}. Cannot determine attempted tests."
        console.print(f":warning: [yellow]{warning_message}[/]")
        plain_summary_lines.append(warning_message)
        summary_content = "No test script directories found."
    else:
        console.print(f":information_source: [cyan]Attempting to summarize based on {total_attempted_scripts} test scripts found in {test_scripts_dir}[/]")

        for test_name in all_script_test_names:
            exec_status_info = execution_statuses.get(test_name)

            if exec_status_info and exec_status_info["status"] == "success":
                scripts_execution_successful += 1
                # Now check content validation for successfully executed scripts
                result_file_path = results_dir / test_name / "results.jsonl"
                latest_result = find_latest_result(result_file_path)
                if latest_result:
                    processed_jsonl_count +=1
                    process_status_json = latest_result.get("Process", False)
                    result_status_json = latest_result.get("Result", False)
                    comments_json = latest_result.get("comments", "No comments available.")

                    if process_status_json and result_status_json:
                        content_validation_passed += 1
                    else: # Processed but content result failed, or not processed according to json
                        content_validation_failed += 1
                        reason = comments_json
                        if not process_status_json:
                            reason = f"JSON indicates not processed. {comments_json}"
                        content_failure_details.append((test_name, reason))
                else: # results.jsonl not found or unparseable for a successfully executed script
                    content_validation_failed += 1
                    content_failure_details.append((test_name, "results.jsonl missing or invalid after successful script execution."))
            
            elif exec_status_info and exec_status_info["status"] == "failed":
                scripts_execution_failed += 1
                exit_code = exec_status_info.get("exit_code", "N/A")
                execution_failure_details.append((test_name, f"Script execution failed (Exit Code: {exit_code})"))
            else: # Test name from script dir not found in execution_log or status unknown
                scripts_execution_failed += 1 # Count as failed if status is unknown or missing
                execution_failure_details.append((test_name, "Execution status not found in log or unknown."))

        # --- Generate Plain Text Summary ---
        plain_summary_lines = [
            "==================== Test Execution Summary (Based on Script Exit Codes) ====================",
            f"Total Test Scripts Attempted (from '{test_scripts_dir.name}' dir): {total_attempted_scripts}",
            f"  - Scripts Execution Successful (Exit Code 0): {scripts_execution_successful}",
            f"  - Scripts Execution Failed (Non-zero Exit Code or Unknown): {scripts_execution_failed}",
        ]
        if scripts_execution_successful > 0:
            plain_summary_lines.extend([
                f"Content Validation for {scripts_execution_successful} Successfully Executed Scripts (from 'results.jsonl'):",
                f"    - Content Validation Passed ('Process': true, 'Result': true): {content_validation_passed}",
                f"    - Content Validation Failed (or results.jsonl issues): {content_validation_failed}",
                f"    (Successfully parsed 'results.jsonl' files for executed scripts: {processed_jsonl_count})",
            ])
        
        plain_summary_lines.append("-------------------- Execution Failures (from all_tests.log) --------------------")
        if execution_failure_details:
            for name, reason in execution_failure_details:
                plain_summary_lines.append(f"- {name}: {reason}")
        else:
            plain_summary_lines.append("No script execution failures reported (or all tests attempted had status in log).")

        if content_failure_details:
            plain_summary_lines.append("-------------------- Content Validation Failures (for successfully executed scripts) --------------------")
            for name, reason in content_failure_details:
                plain_summary_lines.append(f"- {name}: {reason}")
        else:
             if scripts_execution_successful > 0:
                plain_summary_lines.append("No content validation failures for successfully executed scripts (or all passed).")
        
        plain_summary_lines.append("======================================================================================")
        summary_content = "\n".join(plain_summary_lines)

        # --- Generate Rich Console Summary ---
        summary_table = Table(title="Test Execution Summary (Based on Script Exit Codes)", show_header=True, header_style="bold magenta")
        summary_table.add_column("Metric", style="dim", width=60) # Increased width
        summary_table.add_column("Value", style="bold")

        summary_table.add_row(":rocket: Total Test Scripts Attempted", str(total_attempted_scripts))
        summary_table.add_row("  :white_check_mark: Scripts Execution Successful (Exit Code 0)", f"[green]{scripts_execution_successful}[/]")
        summary_table.add_row("  :x: Scripts Execution Failed (Non-zero Exit Code or Unknown)", f"[red]{scripts_execution_failed}[/]")
        
        if scripts_execution_successful > 0:
            summary_table.add_row("--- Content Validation (for successfully executed scripts) ---", "")
            summary_table.add_row("    :page_facing_up: Parsed 'results.jsonl' files", str(processed_jsonl_count))
            summary_table.add_row("    :white_check_mark: Content Validation Passed", f"[green]{content_validation_passed}[/]")
            summary_table.add_row("    :warning: Content Validation Failed (or issues with 'results.jsonl')", f"[yellow]{content_validation_failed}[/]")


        console.print("\n")
        console.print(summary_table)

        if execution_failure_details:
            exec_failures_table = Table(title="Script Execution Failure Details (from all_tests.log)", show_header=True, header_style="bold red")
            exec_failures_table.add_column("Test Name (from script dir)", style="yellow", width=30)
            exec_failures_table.add_column("Reason", style="default")
            for name, reason in execution_failure_details:
                exec_failures_table.add_row(name, reason)
            console.print(exec_failures_table)
        
        if content_failure_details:
            content_failures_table = Table(title="Content Validation Failure Details (for successfully executed scripts)", show_header=True, header_style="bold orange_red1")
            content_failures_table.add_column("Test Name", style="yellow", width=30)
            content_failures_table.add_column("Reason (from results.jsonl or file issue)", style="default")
            for name, reason in content_failure_details:
                content_failures_table.add_row(name, reason)
            console.print(content_failures_table)

        if not execution_failure_details and not content_failure_details and scripts_execution_successful == total_attempted_scripts and content_validation_passed == scripts_execution_successful :
             console.print(Panel("[green]:tada: All attempted scripts executed successfully AND passed content validation! :tada:[/]"))
        elif not execution_failure_details and scripts_execution_successful == total_attempted_scripts:
             console.print(Panel("[green]:tada: All attempted scripts executed successfully! (Check content validation details) :tada:[/]"))


    # Print to console (Rich output is already printed)
    # print("\n" + summary_content) # No longer needed for console

    # Write plain text to file
    try:
        with summary_file.open("w", encoding="utf-8") as f:
            f.write(summary_content)
        console.print(f":floppy_disk: [cyan]Plain text summary report saved to:[/cyan] {summary_file}")
    except Exception as e:
        console.print(f":x: [bold red]Failed to write summary report to {summary_file}:[/bold red] {e}")

if __name__ == "__main__":
    script_dir = Path(__file__).parent.resolve()
    # Go up one level from script_dir (test_scripts) to the parent (eval_automation)
    # Then find the 'test_results' and 'summary_report.txt' in the parent directory
    results_base_dir = script_dir.parent / "test_results" # This is 'output' in your context
    summary_report_file = script_dir.parent / "summary_report.txt"
    execution_log_main_file = script_dir.parent / "all_tests.log" # Path to the main log

    # Check if running in a terminal that supports rich features
    if not console.is_terminal:
        console.print("[yellow]Warning: Not running in a TTY. Rich features might not render correctly.[/]")

    generate_summary(results_base_dir, summary_report_file, execution_log_main_file) # Pass log file path 