#!/bin/bash

# 获取脚本所在的目录
SCRIPT_DIR=/data/data/agent_test_codebase/GitTaskBench/eval_automation
TEST_SCRIPTS_DIR="${SCRIPT_DIR}/test_scripts"
TEST_RESULTS_DIR="${SCRIPT_DIR}/test_results"
LOG_FILE="${SCRIPT_DIR}/all_tests.log"
SUMMARY_SCRIPT="${SCRIPT_DIR}/test_scripts/summarize_results.py" # 稍后创建的 Python 摘要脚本

# 清空旧的日志文件
> "${LOG_FILE}"

echo "Starting batch execution of test scripts..." | tee -a "${LOG_FILE}"
echo "Log file: ${LOG_FILE}"

# 查找并执行所有 run_test.sh 脚本
find "${TEST_SCRIPTS_DIR}" -mindepth 2 -name 'run_test.sh' -type f | while IFS= read -r test_script_path; do
    test_dir=$(dirname "${test_script_path}")
    test_name=$(basename "${test_dir}")
    echo "--------------------------------------------------" | tee -a "${LOG_FILE}"
    echo "Executing test for: ${test_name}" | tee -a "${LOG_FILE}"
    echo "Script path: ${test_script_path}" | tee -a "${LOG_FILE}"
    echo "Working directory: ${test_dir}" | tee -a "${LOG_FILE}"

    # 进入脚本所在目录执行，输出直接打印到终端
    (cd "${test_dir}" && ./run_test.sh)

    # 检查上一个命令的退出状态
    exit_code=$?
    if [ ${exit_code} -eq 0 ]; then
        echo "Execution successful for: ${test_name}" | tee -a "${LOG_FILE}"
    else
        echo "Execution FAILED for: ${test_name} (Exit Code: ${exit_code})" | tee -a "${LOG_FILE}"
    fi
    echo "--------------------------------------------------" | tee -a "${LOG_FILE}"
    echo "" | tee -a "${LOG_FILE}" # 添加空行以提高可读性
done

echo "Batch execution finished." | tee -a "${LOG_FILE}"
echo "==================================================" | tee -a "${LOG_FILE}"
echo "Generating summary report..." | tee -a "${LOG_FILE}"

# 检查 Python 摘要脚本是否存在
if [ -f "${SUMMARY_SCRIPT}" ]; then
    # 执行 Python 脚本生成摘要，输出同样通过 tee 处理
    python3 "${SUMMARY_SCRIPT}" | tee -a "${LOG_FILE}"
else
    echo "[Warning] Summary script not found: ${SUMMARY_SCRIPT}" | tee -a "${LOG_FILE}"
    echo "Please create the summarize_results.py script to generate the summary." | tee -a "${LOG_FILE}"
fi

echo "Script finished." | tee -a "${LOG_FILE}" 