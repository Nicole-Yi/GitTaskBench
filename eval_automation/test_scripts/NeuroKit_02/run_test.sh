#!/bin/bash

# run_test.sh: Evaluate RSP signal analysis results for NeuroKit2

# Get directory paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# --- 定义全局路径变量 ---
########################################################################################################
# 需要修改
# === 基本变量配置 ===
REPO_NAME="NeuroKit_02"
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output"
SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results"

# --- 自动创建缺失目录 ---
mkdir -p "${OUTPUT_DIR}/${REPO_NAME}"
mkdir -p "${RESULT_DIR}/${REPO_NAME}"
mkdir -p "${SCRIPT_DIR}/${REPO_NAME}"
mkdir -p "${GT_DIR}/${REPO_NAME}"

# --- 检查关键文件是否存在 ---
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[错误] 文件不存在: $1"
    fi
}

# 验证测试脚本和输入文件
OUTPUT_SUB_DIR="${OUTPUT_DIR}/${REPO_NAME}"
RESULT_JSON="${RESULT_DIR}/${REPO_NAME}/results.jsonl"
########################################################################################################
# 需要修改
TEST_SCRIPT_EVAL="${SCRIPT_DIR}/${REPO_NAME}/test_script.py"
INPUT_CSV="${OUTPUT_SUB_DIR}/output.csv"
GROUND_TRUTH_CSV="${GT_DIR}/${REPO_NAME}/gt.csv"

check_file_exists "${TEST_SCRIPT_EVAL}"
check_file_exists "${INPUT_CSV}"
check_file_exists "${GROUND_TRUTH_CSV}"



# --- 执行核心命令 ---
echo "=== 开始处理仓库 ${REPO_NAME} ==="

# 运行评估
echo "[信息] 运行 test_script.py ..."
python "${TEST_SCRIPT_EVAL}" \
    --output "${INPUT_CSV}" \
    --gt "${GROUND_TRUTH_CSV}" \
    --result "${RESULT_JSON}"

# 检查评估是否成功
if [ $? -eq 0 ]; then
    echo "[成功] 评估结果: ${RESULT_JSON}"
else
    echo "[失败] 执行失败，请检查错误信息！"
fi

