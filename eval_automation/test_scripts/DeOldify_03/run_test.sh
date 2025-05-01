#!/bin/bash

# --- 定义全局路径变量 ---
########################################################################################################
# 需要修改
# --- 定义仓库名称（将此变量替换为实际仓库名）---
REPO_NAME="DeOldify_03"  # ⚠️ 修改此行！！！
DEFAULT_EVALING_DIR="/mnt/nfs_200T/home/nzy/GitTaskBench/eval_automation"
GIT_ROOT_DIR="/mnt/nfs_200T/home/nzy/"


GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output"
SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results"


# --- 自动创建缺失目录 ---
mkdir -p "${GT_DIR}/${REPO_NAME}"
mkdir -p "${OUTPUT_DIR}/${REPO_NAME}"
mkdir -p "${SCRIPT_DIR}/${REPO_NAME}"
mkdir -p "${RESULT_DIR}/${REPO_NAME}"


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

# --- 执行核心命令 ---
echo "=== 开始处理仓库 ${REPO_NAME} ==="
# 在 output/ 下，查找名为 output 后跟任意后缀的文件
file=$(find "$OUTPUT_SUB_DIR" -maxdepth 1 -type f -name 'output.*' | head -n1)
if [[ -n "$file" ]]; then
    python "${TEST_SCRIPT}" \
        --output "${file}" \
        --threshold 10.0  \
        --result "${RESULT_JSON}"
else
    echo "No matching file found"
fi


# --- 检查执行结果 ---
if [ $? -eq 0 ]; then
    echo "[成功] 输出文件: ${RESULT_JSON}"
else
    echo "[失败] 请检查以上错误信息！"
    exit 1
fi