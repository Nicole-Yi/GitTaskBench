#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# === 基础配置 ===
REPO_NAME="Faker_03"
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"

SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts/${REPO_NAME}"
DATA_DIR="${DEFAULT_EVALING_DIR}/output/${REPO_NAME}"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results/${REPO_NAME}"

TEST_SCRIPT="${SCRIPT_DIR}/test_script.py"
INPUT_FILE="${DEFAULT_EVALING_DIR}/groundtruth/${REPO_NAME}/gt.txt"  # 原始文本文件路径
OUTPUT_FILE="${DATA_DIR}/output.txt"  # 生成的假文本文件路径
RESULT_FILE="${RESULT_DIR}/results.jsonl"  # 结果保存的 jsonl 文件路径

# === 创建目录 ===
mkdir -p "${SCRIPT_DIR}" "${DATA_DIR}" "${RESULT_DIR}"

# === 检查文件是否存在 ===
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[❌ 错误] 缺失文件: $1"
        exit 1
    fi
}

check_file_exists "${TEST_SCRIPT}"
check_file_exists "${INPUT_FILE}"
check_file_exists "${OUTPUT_FILE}"

# === 执行测试 ===
echo "=== [$(date)] 开始测试: ${REPO_NAME} ==="

python "${TEST_SCRIPT}" \
  --input_file "${INPUT_FILE}" \
  --output_file "${OUTPUT_FILE}" \
  --result "${RESULT_FILE}"

# === 测试结束判断 ===
if [ $? -eq 0 ]; then
    echo "[✅ 成功] 测试完成，结果写入: ${RESULT_FILE}"
else
    echo "[❌ 失败] 测试脚本运行出错"
    exit 1
fi
