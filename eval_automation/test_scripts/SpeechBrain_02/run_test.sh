#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
EVAL_AUTOMATION_DIR=$(dirname "$SCRIPT_DIR")
WORKSPACE_DIR=$(dirname "$EVAL_AUTOMATION_DIR")

# --- 定义全局路径变量 ---
########################################################################################################
# 需要修改
# --- 定义仓库名称（将此变量替换为实际仓库名）---
REPO_NAME="SpeechBrain_02"  # ⚠️ 修改此行！！！
DEFAULT_EVALING_DIR="$WORKSPACE_DIR"
GIT_ROOT_DIR="$WORKSPACE_DIR/.."

GT_DIR="$WORKSPACE_DIR/groundtruth"
OUTPUT_DIR="$WORKSPACE_DIR/output"
RESULT_DIR="$WORKSPACE_DIR/test_results"

# --- 自动创建缺失目录 ---
mkdir -p "$GT_DIR/$REPO_NAME"
mkdir -p "$OUTPUT_DIR/$REPO_NAME"
mkdir -p "$RESULT_DIR/$REPO_NAME"

# --- 检查关键文件是否存在 ---
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo "[错误] 文件不存在: $1"
    fi
}

# 验证测试脚本和输入文件
OUTPUT_SUB_DIR="$OUTPUT_DIR/$REPO_NAME"
RESULT_JSONL="$RESULT_DIR/$REPO_NAME/results.jsonl"
TEST_SCRIPT="$SCRIPT_DIR/test_script.py"

check_file_exists "$TEST_SCRIPT"
check_file_exists "$GT_DIR/$REPO_NAME/gt.mp3"
check_file_exists "$GT_DIR/$REPO_NAME/gt_01.wav"
check_file_exists "$GT_DIR/$REPO_NAME/gt_02.wav"

# --- 执行核心命令 ---
echo "=== 开始处理仓库 $REPO_NAME ==="
python3 "$TEST_SCRIPT" \
    --mix "$GT_DIR/$REPO_NAME/gt.mp3" \
    --sep1 "$GT_DIR/$REPO_NAME/gt_01.wav" \
    --sep2 "$GT_DIR/$REPO_NAME/gt_02.wav" \
    --result "$RESULT_JSONL"

# --- 检查执行结果 ---
if [ $? -eq 0 ]; then
    echo "[成功] 输出文件: $RESULT_JSONL"
else
    echo "[失败] 请检查以上错误信息！"
fi 