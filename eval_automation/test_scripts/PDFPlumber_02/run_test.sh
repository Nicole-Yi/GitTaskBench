#!/bin/bash

# 获取脚本所在目录（test_scripts/REPO_NAME）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# === 定义仓库名 ===
REPO_NAME="PDFPlumber_02"  # ⚠️ 修改为实际仓库名（必须与子目录保持一致）
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

# === 路径定义 ===
GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth/${REPO_NAME}"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output/${REPO_NAME}"
SCRIPT_PATH="${DEFAULT_EVALING_DIR}/test_scripts/${REPO_NAME}/test_script.py"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results/${REPO_NAME}"
PRED_CSV="${OUTPUT_DIR}/output.csv"
GT_CSV="${GT_DIR}/gt.csv"
RESULT_JSONL="${RESULT_DIR}/results.jsonl"

# === 自动创建所需目录 ===
mkdir -p "${GT_DIR}" "${OUTPUT_DIR}" "${RESULT_DIR}"

# === 检查文件是否存在 ===
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[❌ 错误] 缺少文件: $1"
    fi
}

check_file_exists "${SCRIPT_PATH}"
check_file_exists "${PRED_CSV}"
check_file_exists "${GT_CSV}"

# === 执行评估脚本 ===
echo "=== [$(date)] 开始评估 ${REPO_NAME} ==="
python "${SCRIPT_PATH}" \
    --pred_file "${PRED_CSV}" \
    --truth_file "${GT_CSV}" \
    --result "${RESULT_JSONL}"

# === 判断是否成功 ===
if [ $? -eq 0 ]; then
    echo "[✅ 成功] 测试完成，结果记录在: ${RESULT_JSONL}"
else
    echo "[❌ 失败] 测试过程中发生错误"
fi
