#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

########################################################################################################
# === 修改项：仓库名 ===
REPO_NAME="Eparse_03"  # ⚠️ 修改为你当前测试的子目录名称
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

########################################################################################################
# === 路径配置 ===
GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth/${REPO_NAME}"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output/${REPO_NAME}"
SCRIPT_PATH="${DEFAULT_EVALING_DIR}/test_scripts/${REPO_NAME}/test_script.py"
RESULT_PATH="${DEFAULT_EVALING_DIR}/test_results/${REPO_NAME}/results.jsonl"

PRED_FILE="${OUTPUT_DIR}/output.json"
GT_FILE="${GT_DIR}/gt.json"

########################################################################################################
# === 创建必要目录 ===
mkdir -p "${GT_DIR}" "${OUTPUT_DIR}"
mkdir -p "$(dirname "${SCRIPT_PATH}")"
mkdir -p "$(dirname "${RESULT_PATH}")"

########################################################################################################
# === 检查文件存在性 ===
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[❌ 错误] 文件不存在: $1"
    fi
}

check_file_exists "${SCRIPT_PATH}"
check_file_exists "${PRED_FILE}"
check_file_exists "${GT_FILE}"

########################################################################################################
# === 执行测试 ===
echo "=== 开始评测：${REPO_NAME} ==="
python "${SCRIPT_PATH}" \
    --pred "${PRED_FILE}" \
    --gt "${GT_FILE}" \
    --result "${RESULT_PATH}"

# === 状态判断 ===
if [ $? -eq 0 ]; then
    echo "[✅ 成功] 测试完成，结果写入：${RESULT_PATH}"
else
    echo "[❌ 失败] 脚本执行出错，请查看日志"
fi
