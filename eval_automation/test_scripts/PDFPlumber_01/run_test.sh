#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# === 基本变量配置 ===
REPO_NAME="PDFPlumber_01"
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts/${REPO_NAME}"
GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth/${REPO_NAME}"
OUT_DIR="${DEFAULT_EVALING_DIR}/output/${REPO_NAME}"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results/${REPO_NAME}"

TEST_SCRIPT="${SCRIPT_DIR}/test_script.py"
INPUT_TEXT="${GT_DIR}/gt.txt"         # 输入文本的真实文件路径
OUTPUT_TEXT="${OUT_DIR}/output.txt"   # 输出文本的预测文件路径
RESULT_JSON="${RESULT_DIR}/results.jsonl"  # 结果 JSONL 文件

# === 自动创建必要目录 ===
mkdir -p "${SCRIPT_DIR}" "${GT_DIR}" "${OUT_DIR}" "${RESULT_DIR}"

# === 检查必要文件 ===
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[❌ 错误] 文件不存在: $1"
        exit 1
    fi
}

check_file_exists "${TEST_SCRIPT}"
check_file_exists "${INPUT_TEXT}"
check_file_exists "${OUTPUT_TEXT}"

# === 执行测试脚本 ===
echo "=== [$(date)] 测试开始: ${REPO_NAME} ==="

python "${TEST_SCRIPT}" \
    --pred_file "${OUTPUT_TEXT}" \
    --truth_file "${INPUT_TEXT}" \
    --result "${RESULT_JSON}"

# === 结果状态判断 ===
if [ $? -eq 0 ]; then
    echo "[✅ 成功] 测试完成，结果写入: ${RESULT_JSON}"
else
    echo "[❌ 失败] 脚本执行出错"
    exit 1
fi
