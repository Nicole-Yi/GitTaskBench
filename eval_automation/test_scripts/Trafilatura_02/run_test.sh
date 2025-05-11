#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# === 基本变量配置 ===
REPO_NAME="Trafilatura_02"
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

SCRIPT_DIR="${DEFAULT_EVALING_DIR}/test_scripts/${REPO_NAME}"
GT_DIR="${DEFAULT_EVALING_DIR}/groundtruth/${REPO_NAME}"
OUT_DIR="${DEFAULT_EVALING_DIR}/output/${REPO_NAME}"
RESULT_DIR="${DEFAULT_EVALING_DIR}/test_results/${REPO_NAME}"

TEST_SCRIPT="${SCRIPT_DIR}/test_script.py"
PRED_PATH="${OUT_DIR}/output.md"        # 预测结果的 Markdown 文件路径
GT_PATH="${GT_DIR}/gt.md"            # ground truth 的 Markdown 文件路径
RESULT_JSONL="${RESULT_DIR}/results.jsonl"  # 结果存储路径

# === 自动创建必要目录 ===
mkdir -p "${SCRIPT_DIR}" "${GT_DIR}" "${OUT_DIR}" "${RESULT_DIR}"

# === 检查必要文件 ===
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[❌ 错误] 文件不存在: $1"
    fi
    if [ ! -s "$1" ]; then
        echo "[❌ 错误] 文件为空: $1"
    fi
}

check_file_exists "${TEST_SCRIPT}"
check_file_exists "${PRED_PATH}"
check_file_exists "${GT_PATH}"

# === 执行测试脚本 ===
echo "=== [$(date)] 测试开始: ${REPO_NAME} ==="

python "${TEST_SCRIPT}" \
    --pred_path "${PRED_PATH}" \
    --gt_path "${GT_PATH}" \
    --result "${RESULT_JSONL}"

# === 结果状态判断 ===
if [ $? -eq 0 ]; then
    echo "[✅ 成功] 测试完成，结果写入: ${RESULT_JSONL}"
else
    echo "[❌ 失败] 脚本执行出错"
fi
