#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
EVAL_AUTOMATION_DIR=$(dirname "$SCRIPT_DIR")
WORKSPACE_DIR=$(dirname "$EVAL_AUTOMATION_DIR")

# --- 定义全局路径变量 ---
########################################################################################################
# 需要修改
# --- 定义仓库名称（将此变量替换为实际仓库名）---
REPO_NAME="SpeechEnhance_01"  # ⚠️ 修改此行！！！
DEFAULT_EVALING_DIR="$WORKSPACE_DIR"
GIT_ROOT_DIR="$WORKSPACE_DIR/.."

GT_DIR="$WORKSPACE_DIR/groundtruth"
OUTPUT_DIR="$WORKSPACE_DIR/output"
RESULT_DIR="$WORKSPACE_DIR/test_results"

# --- 自动创建缺失目录 ---
echo "创建必要的目录..."
mkdir -p "$GT_DIR/$REPO_NAME"
mkdir -p "$OUTPUT_DIR/$REPO_NAME"
mkdir -p "$RESULT_DIR/$REPO_NAME"

# --- 检查关键文件是否存在 ---
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[错误] 文件不存在: $1"
        exit 1
    fi
}

# 验证测试脚本和输入文件
OUTPUT_SUB_DIR="$OUTPUT_DIR/$REPO_NAME"
RESULT_JSONL="$RESULT_DIR/$REPO_NAME/results.jsonl"
TEST_SCRIPT="$SCRIPT_DIR/test_script.py"

echo "检查必要的文件..."
check_file_exists "$TEST_SCRIPT"
check_file_exists "$OUTPUT_SUB_DIR/output.wav"
check_file_exists "$GT_DIR/$REPO_NAME/gt.wav"

# --- 执行核心命令 ---
echo "=== 开始处理仓库 $REPO_NAME ==="
echo "输入文件: $OUTPUT_SUB_DIR/output.wav"
echo "参考文件: $GT_DIR/$REPO_NAME/gt.wav"
echo "结果文件: $RESULT_JSONL"

python3 "$TEST_SCRIPT" \
    "$OUTPUT_SUB_DIR/output.wav" \
    "$GT_DIR/$REPO_NAME/gt.wav" \
    --pesq-thresh 2.0 \
    --snr-thresh 15.0 \
    --result "$RESULT_JSONL"

# --- 检查执行结果 ---
if [ $? -eq 0 ]; then
    echo "[成功] 测试完成！"
    echo "结果已保存到: $RESULT_JSONL"
    echo "结果内容:"
    tail -n 1 "$RESULT_JSONL" | python3 -m json.tool
else
    echo "[失败] 测试执行出错，请检查以上错误信息！"
    exit 1
fi 