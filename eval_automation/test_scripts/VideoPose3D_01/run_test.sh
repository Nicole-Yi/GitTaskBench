#!/bin/bash

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# --- 定义全局路径变量 ---
########################################################################################################
# 仓库名称
REPO_NAME="VideoPose3D_01"  # 更新为实际仓库名称

DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output"
SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results"

# --- 自动创建缺失目录 ---
mkdir -p "${OUTPUT_DIR}/${REPO_NAME}"
mkdir -p "${RESULT_DIR}/${REPO_NAME}"
mkdir -p "${SCRIPT_DIR}/${REPO_NAME}"
mkdir -p "${GT_DIR}/${REPO_NAME}"

# --- 检查关键文件是否存在 ---
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[错误] 文件不存在: $1"
    fi
}

# 验证测试脚本和输入文件
OUTPUT_SUB_DIR="${OUTPUT_DIR}/${REPO_NAME}"
RESULT_JSON="${RESULT_DIR}/${REPO_NAME}/results.jsonl"
TEST_SCRIPT="${SCRIPT_DIR}/${REPO_NAME}/test_script.py"


check_file_exists "${TEST_SCRIPT}"


# --- 执行核心命令 ---
echo "=== 开始处理仓库 ${REPO_NAME} ==="
# 在 output/ 下，查找名为 output 后跟任意后缀的文件
file=$(find "$OUTPUT_SUB_DIR" -maxdepth 1 -type f -name 'output.*' | head -n1)
if [[ -n "$file" ]]; then
    echo "找到输出文件: $file"
    python "${TEST_SCRIPT}" \
        --input "${file}" \
        --result "${RESULT_JSON}"
else
    echo "[错误] 未找到匹配的输出文件 (output_*.jpg)"
fi

# --- 检查执行结果 ---
if [ $? -eq 0 ]; then
    echo "[成功] 输出文件: ${RESULT_JSON}"
else
    echo "[失败] 请检查以上错误信息！"
fi
