#!/bin/bash

# === 基本变量配置 ===
REPO_NAME="eparse_01"  # 替换为你的仓库名称
BASE_DIR="/root/autodl-tmp/GitTaskBench/eval_automation"
GIT_ROOT="/root/autodl-tmp"

SCRIPT_DIR="${BASE_DIR}/test_scripts/${REPO_NAME}"
GT_DIR="${BASE_DIR}/groundtruth/${REPO_NAME}"
OUT_DIR="${BASE_DIR}/output/${REPO_NAME}"
RESULT_DIR="${BASE_DIR}/test_results/${REPO_NAME}"

TEST_SCRIPT="${SCRIPT_DIR}/test_script.py"
PRED_FILE="${OUT_DIR}/output.txt"
GT_FILE="${GT_DIR}/gt.txt"
RESULT_JSON="${RESULT_DIR}/results.jsonl"

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
check_file_exists "${PRED_FILE}"
check_file_exists "${GT_FILE}"

# === 执行测试脚本 ===
echo "=== [$(date)] 测试开始: ${REPO_NAME} ==="

python "${TEST_SCRIPT}" \
    --pred "${PRED_FILE}" \
    --gt "${GT_FILE}" \
    --result "${RESULT_JSON}"

# === 结果状态判断 ===
if [ $? -eq 0 ]; then
    echo "[✅ 成功] 测试完成，结果写入: ${RESULT_JSON}"
else
    echo "[❌ 失败] 脚本执行出错"
    exit 1
fi
