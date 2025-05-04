import json
import logging
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple
import os # Import os for listdir

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


def generate_summary(results_dir: Path, summary_file: Path) -> None:
    """Generates a summary report from all results.jsonl files.

    Args:
        results_dir: Path to the directory containing test result subdirectories.
        summary_file: Path to save the summary report.
    """
    # --- Calculate Expected Tests ---
    test_scripts_dir = results_dir.parent / "test_scripts"
    expected_tests_count = 0
    if test_scripts_dir.is_dir():
        # Count directories directly under test_scripts_dir
        expected_tests_count = sum(1 for item in test_scripts_dir.iterdir() if item.is_dir())
    else:
        console.print(f":warning: [yellow]Could not find test scripts directory:[/yellow] {test_scripts_dir}")


    # --- Process Found Results ---
    found_results_count = 0
    successful_tests = 0
    failed_tests = 0
    processed_but_failed = 0
    not_processed = 0
    failures: List[Tuple[str, str]] = [] # (test_name, comments)
    successes: List[str] = [] # test_name

    result_files = sorted(list(results_dir.rglob("**/results.jsonl"))) # Sort for consistent order
    found_results_count = len(result_files)

    plain_summary_lines = [] # For the text file

    if not result_files and expected_tests_count == 0:
         warning_message = f"No 'results.jsonl' files found in {results_dir} and no test script directories found in {test_scripts_dir}"
         console.print(f":warning: [yellow]{warning_message}[/]")
         plain_summary_lines.append(warning_message)
         summary_content = "No result files or test directories found."
    elif not result_files and expected_tests_count > 0:
        warning_message = f"Expected {expected_tests_count} tests based on directories, but found no 'results.jsonl' files in {results_dir}"
        console.print(f":warning: [yellow]{warning_message}[/]")
        plain_summary_lines.append(warning_message)
        summary_content = f"Expected {expected_tests_count} tests, found 0 result files."
        # Still generate the summary table structure but show 0 for found/success/fail
        total_tests = 0 # Use 0 for calculations if no results found
    else:
        console.print(f":information_source: [cyan]Expected Tests (based on dirs): {expected_tests_count}[/]")
        console.print(f":information_source: [cyan]Found {found_results_count} result files.[/]")
        total_tests = found_results_count # Use found count for processing loop
        for result_file in result_files:
            test_name = result_file.parent.name # Get the directory name (e.g., DeOldify_02)
            # console.print(f"Processing {test_name} from {result_file}...") # Reduced verbosity
            # total_tests += 1 # Now counted above based on found files

            latest_result = find_latest_result(result_file)

            if latest_result:
                process_status = latest_result.get("Process", False)
                result_status = latest_result.get("Result", False)
                comments = latest_result.get("comments", "No comments available.")

                if process_status and result_status:
                    successful_tests += 1
                    successes.append(test_name)
                    # console.print(f"  -> [green]Success[/]") # Reduced verbosity
                elif process_status and not result_status:
                    failed_tests += 1
                    processed_but_failed += 1
                    failures.append((test_name, comments))
                    console.print(f"  :warning: [yellow]{test_name}: Processed but Failed.[/] Reason: {comments}")
                elif not process_status:
                    failed_tests += 1
                    not_processed += 1
                    failures.append((test_name, f"Processing failed. {comments}"))
                    console.print(f"  :x: [red]{test_name}: Processing Failed.[/] Reason: {comments}")
                else:
                    failed_tests += 1
                    failures.append((test_name, f"Unknown status: Process={process_status}, Result={result_status}. {comments}"))
                    console.print(f"  :question: [magenta]{test_name}: Unknown Status.[/] Reason: {comments}")
            else:
                failed_tests += 1
                # Consider if this should be 'not_processed' or a separate category like 'parsing_failed'
                # Sticking with 'not_processed' for now as it implies the result wasn't usable
                not_processed += 1
                failures.append((test_name, "Could not read or parse result file."))
                console.print(f"  :x: [red]{test_name}: Failed (Could not read/parse result file)[/]")

        # --- Generate Plain Text Summary ---
        plain_summary_lines = [
            "==================== Test Summary ====================",
            f"Expected Tests (Directories): {expected_tests_count}",
            f"Found Result Files: {found_results_count}",
            f"Successful Tests (from found files): {successful_tests}",
            f"Failed Tests (from found files): {failed_tests}",
            f"  - Processed but Result Failed: {processed_but_failed}",
            f"  - Processing Not Completed/Failed or Unparseable: {not_processed}", # Updated category name slightly
            "-------------------- Failures --------------------",
        ]
        if failures:
            for name, reason in failures:
                plain_summary_lines.append(f"- {name}: {reason}")
        else:
            plain_summary_lines.append("No failures reported among found results.")
        plain_summary_lines.append("====================================================")
        summary_content = "\n".join(plain_summary_lines)

        # --- Generate Rich Console Summary ---
        summary_table = Table(title="Test Execution Summary", show_header=True, header_style="bold magenta")
        summary_table.add_column("Metric", style="dim", width=45) # Increased width slightly
        summary_table.add_column("Value", style="bold")

        summary_table.add_row(":clipboard: Expected Tests (Directories)", str(expected_tests_count))
        summary_table.add_row(":file_folder: Found Result Files", str(found_results_count))
        summary_table.add_row(":white_check_mark: Successful Tests (from found)", f"[green]{successful_tests}[/]")
        summary_table.add_row(":x: Failed Tests (from found)", f"[red]{failed_tests}[/]")
        summary_table.add_row("  :warning: Processed but Result Failed", str(processed_but_failed))
        summary_table.add_row("  :no_entry: Processing Not Completed/Failed or Unparseable", str(not_processed)) # Updated category name slightly

        console.print("\n")
        console.print(summary_table)

        if failures:
            failures_table = Table(title="Failure Details", show_header=True, header_style="bold red")
            failures_table.add_column("Test Name", style="yellow", width=30)
            failures_table.add_column("Reason", style="default")

            for name, reason in failures:
                failures_table.add_row(name, reason)
            console.print(failures_table)
        else:
            console.print(Panel("[green]:tada: All tests passed successfully! :tada:[/]"))

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
    results_base_dir = script_dir.parent / "test_results"
    summary_report_file = script_dir.parent / "summary_report.txt"

    # Check if running in a terminal that supports rich features
    if not console.is_terminal:
        console.print("[yellow]Warning: Not running in a TTY. Rich features might not render correctly.[/]")

    generate_summary(results_base_dir, summary_report_file) 