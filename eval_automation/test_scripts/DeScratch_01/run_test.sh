#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
EVAL_AUTOMATION_DIR="$(dirname "$SCRIPT_DIR")"
WORKSPACE_DIR="$(dirname "$EVAL_AUTOMATION_DIR")"

# --- 定义全局路径变量 ---
########################################################################################################
# 需要修改
# --- 定义仓库名称（将此变量替换为实际仓库名）---
REPO_NAME="DeScratch_01"  # ⚠️ 修改此行！！！
DEFAULT_EVALING_DIR="${WORKSPACE_DIR}"
# GitTaskBench文件夹
GIT_ROOT_DIR="${WORKSPACE_DIR}/.."

### 下为临时修改 为了run 划痕检测并输出
#DeScratch下Gloabl文件夹
MASK_DETECTION="${GIT_ROOT_DIR}/code_base/DeScratch/Global"

DETECTION="${MASK_DETECTION}/detection.py"
###

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

#detection.py输出的划痕图像地址：“autodl-tmp/GitTaskBench/eval_automation/output/DeScratch_01”
DETECT_OUTPUT_DIR="${OUTPUT_SUB_DIR}"     


########################################################################################################
# 需要修改，是否涉及01 02，格式 
TEST_SCRIPT="${SCRIPT_DIR}/${REPO_NAME}/test_script.py"


check_file_exists "${TEST_SCRIPT}"

# --- 执行核心命令 ---
#1.划痕检测
echo "==开始划痕检测=="
python "${DETECTION}" \
        --test_path "${OUTPUT_SUB_DIR}"\
        --output_dir "${DETECT_OUTPUT_DIR}"\
        --GPU -1
        
#这个运行完，mask后的文件在/root/autodl-tmp/GitTaskBench/eval_automation/output/DeScratch_01/mask里面名字为test_path中文件的名字.png,在这里叫output.png


#2.验证划痕
echo "=== 开始处理仓库 ${REPO_NAME} ==="
#file:经过dectection.py处理后的掩码图片，即test_script.py的输入
# 定义目录
mask_dir="${DETECT_OUTPUT_DIR}/mask"

# 查找所有以 output 开头的文件
file=$(find "$mask_dir" -maxdepth 1 -type f -name 'output.*' | head -n1)

if [[ -n "$file" ]]; then
    python "${TEST_SCRIPT}" \
        --output "${file}" \
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