#!/bin/bash

# 获取当前脚本所在目录（DeScratch_03 目录）
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 向上推导路径结构
# SCRIPT_DIR = …/eval_automation/test_scripts/DeScratch_03
# EVAL_AUTOMATION_DIR = …/eval_automation
EVAL_AUTOMATION_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# 修改此处仓库名称
REPO_NAME="DeScratch_03"

# 路径变量
GT_DIR="${EVAL_AUTOMATION_DIR}/groundtruth"
OUTPUT_DIR="${EVAL_AUTOMATION_DIR}/output"
SCRIPT_PATH="${EVAL_AUTOMATION_DIR}/test_scripts/DeScratch_03/test_script.py"  # 确保此路径正确指向脚本
RESULT_DIR="${EVAL_AUTOMATION_DIR}/test_results"

# 输出文件路径
GT_SUB_DIR="${EVAL_AUTOMATION_DIR}/groundtruth/${REPO_NAME}/gt"
OUTPUT_SUB_DIR="${EVAL_AUTOMATION_DIR}/output/${REPO_NAME}/output"
RESULT_JSON="${RESULT_DIR}/${REPO_NAME}/results.jsonl"

# 自动创建输出目录
mkdir -p "${RESULT_DIR}/${REPO_NAME}"

# --- 检查文件或目录是否存在 ---
check_dir_exists() {
    if [ ! -d "$1" ]; then
        echo "[错误] 目录不存在: $1"
        exit 1
    fi
}

check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[错误] 文件不存在: $1"
        exit 1
    fi
}

# 日志输出路径检查
echo "检查文件路径：${SCRIPT_PATH}"
echo "GT路径：${GT_SUB_DIR}"
echo "预测路径：${OUTPUT_SUB_DIR}"

# 检查关键文件路径
check_file_exists "${SCRIPT_PATH}"
check_dir_exists "${GT_SUB_DIR}"
check_dir_exists "${OUTPUT_SUB_DIR}"

# 执行测试脚本
echo "=== 开始处理仓库 ${REPO_NAME} ==="
python "${SCRIPT_PATH}" \
    --pred_dir "${OUTPUT_SUB_DIR}" \
    --gt_dir "${GT_SUB_DIR}" \
    --result "${RESULT_JSON}"

# 执行状态检查
if [ $? -eq 0 ]; then
    echo "[成功] 输出文件: ${RESULT_JSON}"
else
    echo "[失败] 请检查以上错误信息！"
    exit 1
fi
