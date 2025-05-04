#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

REPO_NAME="Scrapy_02"
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts/${REPO_NAME}"
GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth/${REPO_NAME}"
OUT_DIR="${DEFAULT_EVALING_DIR}/output/${REPO_NAME}"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results/${REPO_NAME}"

PRED_FILE="${OUT_DIR}/output.csv"
GT_FILE="${GT_DIR}/gt.csv"
RESULT_FILE="${RESULT_DIR}/results.jsonl"
SCRIPT_FILE="${SCRIPT_DIR}/test_script.py"

mkdir -p "${SCRIPT_DIR}" "${GT_DIR}" "${OUT_DIR}" "${RESULT_DIR}"

# 检查文件存在
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "❌ 文件不存在: $1"
        exit 1
    fi
    if [ ! -s "$1" ]; then
        echo "❌ 文件为空: $1"
        exit 1
    fi
}

check_file_exists "${SCRIPT_FILE}"
check_file_exists "${PRED_FILE}"
check_file_exists "${GT_FILE}"

echo "=== [$(date)] 开始测试 ${REPO_NAME} ==="

python "${SCRIPT_FILE}" \
  --pred_file "${PRED_FILE}" \
  --gt_file "${GT_FILE}" \
  --result "${RESULT_FILE}"

if [ $? -eq 0 ]; then
    echo "✅ 测试成功，结果写入: ${RESULT_FILE}"
else
    echo "❌ 测试失败"
    exit 1
fi
