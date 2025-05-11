#!/bin/bash

# 获取路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# 项目名称（必须改）
REPO_NAME="PyPDF2_02"  # ⚠️ 修改此行为你的仓库名
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

# 路径配置
GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth/${REPO_NAME}"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output/${REPO_NAME}"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results/${REPO_NAME}"
SCRIPT_PATH="${DEFAULT_EVALING_DIR}/test_scripts/${REPO_NAME}/test_script.py"
RESULT_JSON="${RESULT_DIR}/results.jsonl"

mkdir -p "${RESULT_DIR}"

# 检查必要文件夹
check_dir_exists() {
    if [ ! -d "$1" ]; then
        echo "[❌ 错误] 目录不存在: $1"
    fi
}

check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[❌ 错误] 文件不存在: $1"
    fi
}

check_file_exists "${SCRIPT_PATH}"
check_dir_exists "${GT_DIR}"
check_dir_exists "${OUTPUT_DIR}"

# 执行脚本
echo "=== [$(date)] 开始评估 ${REPO_NAME} ==="
python "${SCRIPT_PATH}" \
    --split_dir "${OUTPUT_DIR}" \
    --truth_dir "${GT_DIR}" \
    --result "${RESULT_JSON}"

if [ $? -eq 0 ]; then
    echo "[✅ 成功] 测试完成，结果追加至 ${RESULT_JSON}"
else
    echo "[❌ 失败] 脚本运行出错"
fi
