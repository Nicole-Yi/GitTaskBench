#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

REPO_NAME="SuperResolution_03"
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth"
OUTPUT_DIR="${DEFAULT_EVALING_DIR}/output"
SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results"

mkdir -p "${OUTPUT_DIR}/${REPO_NAME}"
mkdir -p "${RESULT_DIR}/${REPO_NAME}"
mkdir -p "${SCRIPT_DIR}/${REPO_NAME}"
mkdir -p "${GT_DIR}/${REPO_NAME}"

check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[错误] 文件不存在: $1"
        exit 1
    fi
}

OUTPUT_SUB_DIR="${OUTPUT_DIR}/${REPO_NAME}"
RESULT_JSON="${RESULT_DIR}/${REPO_NAME}/results.jsonl"
TEST_SCRIPT="${SCRIPT_DIR}/${REPO_NAME}/test_script.py"
INPUT_IMAGE="${GT_DIR}/${REPO_NAME}/gt.png"

check_file_exists "${TEST_SCRIPT}"
check_file_exists "${INPUT_IMAGE}"

echo "=== 开始处理仓库 ${REPO_NAME} ==="
echo "输入图像: ${INPUT_IMAGE}"

# 查找 output.*
file=$(find "$OUTPUT_SUB_DIR" -maxdepth 1 -type f -name 'output.*' | head -n1)

if [[ -n "$file" ]]; then
    OUTPUT_IMAGE="$file"
    echo "输出图像: ${OUTPUT_IMAGE}"

    python "${TEST_SCRIPT}" \
        --input_path "${INPUT_IMAGE}" \
        --output_path "${OUTPUT_IMAGE}" \
        --result "${RESULT_JSON}"

    if [ $? -eq 0 ]; then
        echo "[成功] 输出文件: ${RESULT_JSON}"
    else
        echo "[失败] 请检查以上错误信息！"
    fi
else
    echo "[错误] 文件不存在: ${OUTPUT_SUB_DIR}/output.*"
    exit 1
fi
