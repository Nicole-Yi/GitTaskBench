#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# --- 定义全局路径变量 ---
########################################################################################################
# 需要修改
# --- 定义仓库名称（将此变量替换为实际仓库名）---
REPO_NAME="DeOldify_01"  # ⚠️ 修改此行！！！
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."


GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output"
SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results"

INPUT_IMAGE="${GT_DIR}/${REPO_NAME}/gt.jpg"


# --- 检查关键文件是否存在 ---
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[错误] 文件不存在: $1"
        exit 1
    fi
}

# --- 自动创建缺失目录 ---
mkdir -p "${OUTPUT_DIR}/${REPO_NAME}"
mkdir -p "${RESULT_DIR}/${REPO_NAME}"
mkdir -p "${SCRIPT_DIR}/${REPO_NAME}"
mkdir -p "${GT_DIR}/${REPO_NAME}"

# --- 检查关键文件是否存在 ---
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[错误] 文件不存在: $1"
        exit 1
    fi
}

# 验证测试脚本和输入文件
OUTPUT_SUB_DIR="${OUTPUT_DIR}/${REPO_NAME}"
RESULT_JSON="${RESULT_DIR}/${REPO_NAME}/results.jsonl"
########################################################################################################
# 需要修改，是否涉及01 02，格式 
TEST_SCRIPT="${SCRIPT_DIR}/${REPO_NAME}/test_script.py"


check_file_exists "${TEST_SCRIPT}"


# 查找 output.*
file=$(find "$OUTPUT_SUB_DIR" -maxdepth 1 -type f -name 'output.*' | head -n1)

# --- 执行核心命令 ---
echo "=== 开始处理仓库 ${REPO_NAME} ==="
if [[ -n "$file" ]]; then
    python "${TEST_SCRIPT}" \
        --input "${INPUT_IMAGE}" \
        --output "${file}" \
        --ciede-thresh 2.0  \
        --niqe-thresh 7.0 \
        --result "${RESULT_JSON}"
    
    # --- 检查执行结果 ---
    if [ $? -eq 0 ]; then
        echo "[成功] 输出文件: ${OUTPUT_SUB_DIR}/output.png"
    else
        echo "[失败] 请检查以上错误信息！"
        exit 1
    fi
else
    echo "[错误] 文件不存在: ${OUTPUT_SUB_DIR}/output.*"
    exit 1
fi