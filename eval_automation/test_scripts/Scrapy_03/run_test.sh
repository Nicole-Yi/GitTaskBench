#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

REPO_NAME="Scrapy_03"
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts/${REPO_NAME}"
GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth/${REPO_NAME}"
OUT_DIR="${DEFAULT_EVALING_DIR}/output/${REPO_NAME}"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results/${REPO_NAME}"

PRED_FILE="${OUT_DIR}/output.xml"
GT_FILE="${GT_DIR}/gt.csv"
RESULT_FILE="${RESULT_DIR}/results.jsonl"
SCRIPT_FILE="${SCRIPT_DIR}/test_script.py"  

# 创建必要的目录
mkdir -p "${SCRIPT_DIR}" "${GT_DIR}" "${OUT_DIR}" "${RESULT_DIR}"

# 检查文件是否存在且非空
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "❌ 文件不存在: $1"
    fi
    if [ ! -s "$1" ]; then
        echo "❌ 文件为空: $1"
    fi
}

# 检查必要的文件
check_file_exists "${SCRIPT_FILE}"
check_file_exists "${PRED_FILE}"
check_file_exists "${GT_FILE}"

echo "=== [$(date)] 开始测试 ${REPO_NAME} ==="

# 执行 Python 脚本进行测试
python "${SCRIPT_FILE}" \
  --pred_file "${PRED_FILE}" \
  --gt_file "${GT_FILE}" \
  --result "${RESULT_FILE}"

# 判断脚本执行结果
if [ $? -eq 0 ]; then
    echo "✅ 测试成功，结果写入: ${RESULT_FILE}"
else
    echo "❌ 测试失败"
fi
