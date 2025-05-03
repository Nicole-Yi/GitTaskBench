#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# --- 定义全局路径变量 ---
REPO_NAME="PDFPlumber_03"  # ⚠️ 修改此行！！！
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

# 定义各目录
GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output"
SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results"

# 创建目录
mkdir -p "${OUTPUT_DIR}/${REPO_NAME}"
mkdir -p "${RESULT_DIR}/${REPO_NAME}"
mkdir -p "${SCRIPT_DIR}/${REPO_NAME}"
mkdir -p "${GT_DIR}/${REPO_NAME}"

# --- 检查关键文件是否存在 ---
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[❌ 错误] 文件不存在: $1"
        exit 1
    fi
}

# 需要修改为对应的文件路径
PRED_FILE="${OUTPUT_DIR}/${REPO_NAME}/output.txt"
GT_FILE="${GT_DIR}/${REPO_NAME}/gt.txt"
RESULT_JSON="${RESULT_DIR}/${REPO_NAME}/results.jsonl"

# 验证输入文件是否存在
check_file_exists "${PRED_FILE}"
check_file_exists "${GT_FILE}"

# --- 执行测试脚本 ---
echo "=== [$(date)] 开始评估 ${REPO_NAME} ==="

# 运行评估脚本并将结果追加到 JSONL 文件
python "${SCRIPT_DIR}/${REPO_NAME}/test_script.py" \
    --pred_file "${PRED_FILE}" \
    --truth_file "${GT_FILE}" \
    --result "${RESULT_JSON}"

# 检查执行结果
if [ $? -eq 0 ]; then
    echo "[✅ 成功] 测试完成，结果写入: ${RESULT_JSON}"
else
    echo "[❌ 失败] 脚本执行出错"
    exit 1
fi
