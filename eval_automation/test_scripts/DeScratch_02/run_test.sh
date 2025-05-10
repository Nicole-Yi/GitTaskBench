#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# --- 定义全局路径变量 ---
########################################################################################################
# 需要修改
# --- 定义仓库名称（将此变量替换为实际仓库名）---
REPO_NAME="DeScratch_02"  # ⚠️ 修改此行！！！
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output"
SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results"


# --- 自动创建缺失目录 ---
mkdir -p "${GT_DIR}/${REPO_NAME}"
mkdir -p "${OUTPUT_DIR}/${REPO_NAME}"
mkdir -p "${SCRIPT_DIR}/${REPO_NAME}"
mkdir -p "${RESULT_DIR}/${REPO_NAME}"

# --- 检查文件或目录是否存在 ---
check_dir_exists() {
    if [ ! -d "$1" ]; then  # 检查目录是否存在
        echo "[错误] 目录不存在: $1"
        return 1
    fi
}

check_file_exists() {
    if [ ! -f "$1" ]; then  # 检查文件是否存在
        echo "[错误] 文件不存在: $1"
        return 1
    fi
}

# 验证测试脚本和输入文件
OUTPUT_SUB_DIR="${OUTPUT_DIR}/${REPO_NAME}"
RESULT_JSON="${RESULT_DIR}/${REPO_NAME}/results.jsonl"
########################################################################################################
# 需要修改，是否涉及01 02，格式 
TEST_SCRIPT="${SCRIPT_DIR}/${REPO_NAME}/test_script.py"

echo "检查文件路径：${TEST_SCRIPT}"  # 输出调试信息，检查路径
check_file_exists "${TEST_SCRIPT}"

# --- 检查预测和真实掩码文件夹是否存在 ---
echo "GT路径：${GT_DIR}/${REPO_NAME}/gt"  # 输出调试信息，检查路径
echo "预测路径：${OUTPUT_SUB_DIR}"     # 输出调试信息，检查路径

check_dir_exists "${GT_DIR}/${REPO_NAME}/gt"  # 检查GT目录是否存在
check_dir_exists "${OUTPUT_SUB_DIR}"          # 检查预测结果目录是否存在

# --- 执行核心命令 ---
echo "=== 开始处理仓库 ${REPO_NAME} ==="
# 执行测试脚本并传递预测掩码和真实掩码路径，以及结果保存路径
python "${TEST_SCRIPT}" \
    --pred_dir "${OUTPUT_SUB_DIR}" \
    --gt_dir "${GT_DIR}/${REPO_NAME}/gt" \
    --result "${RESULT_JSON}"

# --- 检查执行结果 ---
if [ $? -eq 0 ]; then
    echo "[成功] 输出文件: ${RESULT_JSON}"
else
    echo "[失败] 请检查以上错误信息！"
fi
