#!/bin/bash

# 获取脚本所在目录的绝对路径（兼容macOS和Linux）
get_abs_path() {
    local path="$1"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        [[ $path = /* ]] && echo "$path" || echo "$PWD/${path#./}"
    else
        # Linux
        readlink -f "$path"
    fi
}

SCRIPT_DIR=$(dirname "$(get_abs_path "$0")")
TEST_SCRIPTS_DIR=$(dirname "$SCRIPT_DIR")
WORKSPACE_DIR=$(dirname "$TEST_SCRIPTS_DIR")

# --- 定义全局路径变量 ---
########################################################################################################
# --- 定义仓库名称 ---
REPO_NAME="VideoPose3D_01"

# --- 设置目录路径 ---
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
        return 1
    fi
    return 0
}

# --- 定义文件路径 ---
OUTPUT_SUB_DIR="$OUTPUT_DIR/$REPO_NAME"
RESULT_JSONL="$RESULT_DIR/$REPO_NAME/results.jsonl"
TEST_SCRIPT="$SCRIPT_DIR/test_script.py"

# --- 检查测试脚本是否存在 ---
echo "检查必要的文件..."
check_file_exists "$TEST_SCRIPT"
if [ $? -ne 0 ]; then
    echo "[错误] 测试脚本不存在，无法继续执行"
    exit 1
fi

# --- 查找输出文件 ---
echo "查找输出文件..."
# 在output目录下查找以output开头的文件
INPUT_FILE=$(find "$OUTPUT_SUB_DIR" -maxdepth 1 -type f -name 'output*' | head -n1)

if [ -z "$INPUT_FILE" ]; then
    echo "[错误] 在 $OUTPUT_SUB_DIR 目录下未找到以output开头的文件"
    # 记录错误信息到结果文件
    python "$TEST_SCRIPT" \
        --input "$INPUT_FILE" \
        --result "$RESULT_JSONL"
    exit 1
fi

# --- 执行核心命令 ---
echo "=== 开始评估 $REPO_NAME 输出 ==="
echo "输入文件: $INPUT_FILE"
echo "结果文件: $RESULT_JSONL"

# 确保结果目录存在
mkdir -p "$(dirname "$RESULT_JSONL")"

# 使用python3确保兼容性
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

$PYTHON_CMD "$TEST_SCRIPT" \
    --input "$INPUT_FILE" \
    --result "$RESULT_JSONL"

# --- 检查执行结果 ---
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "[成功] 评估完成，结果满足要求！"
    echo "结果已保存到: $RESULT_JSONL"
    if [ -f "$RESULT_JSONL" ]; then
        echo "结果内容:"
        tail -n 1 "$RESULT_JSONL"
    fi
else
    echo "[失败] 评估完成，结果不满足要求。"
    if [ -f "$RESULT_JSONL" ]; then
        echo "结果内容:"
        tail -n 1 "$RESULT_JSONL"
    fi
fi

# 返回Python脚本的退出码
exit $EXIT_CODE 