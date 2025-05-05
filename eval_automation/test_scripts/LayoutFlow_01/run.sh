#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# --- 定义全局路径变量 ---
########################################################################################################
# 需要修改
# --- 定义仓库名称（将此变量替换为实际仓库名）---
REPO_NAME="LayoutFlow_01"  # ⚠️ 已修改为LayoutFlow_01
DEFAULT_EVALING_DIR="${EVAL_AUTOMATION_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output"
SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results"

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

# 验证测试脚本和输入文件
OUTPUT_SUB_DIR="${OUTPUT_DIR}/${REPO_NAME}"
RESULT_JSON="${RESULT_DIR}/${REPO_NAME}/results.jsonl"
########################################################################################################
# 针对LayoutFlow_01的配置
TEST_SCRIPT="${SCRIPT_DIR}/${REPO_NAME}/test_script.py"
OUTPUT_JSON="${OUTPUT_SUB_DIR}/output.json"

check_file_exists "${TEST_SCRIPT}"
check_file_exists "${OUTPUT_JSON}"

# --- 执行核心命令 ---
echo "=== 开始评估布局质量 ${REPO_NAME} ==="
python3 "${TEST_SCRIPT}" \
    --input "${OUTPUT_JSON}" \
    --result "${RESULT_JSON}"

# --- 检查执行结果 ---
if [ $? -eq 0 ]; then
    echo "[成功] 评估完成，结果已写入: ${RESULT_JSON}"
else
    echo "[失败] 请检查以上错误信息！"
    exit 1
fi 