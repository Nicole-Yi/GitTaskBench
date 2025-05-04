#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # 无颜色

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# 获取项目根目录（脚本目录的上两级）
ROOT_DIR="$( cd "$SCRIPT_DIR/../.." && pwd )"
# 输入/输出目录
INPUT_DIR="${ROOT_DIR}/output/NeuroKit_02"
RESULTS_DIR="${ROOT_DIR}/test_results/NeuroKit_02"

# 确保结果目录存在
mkdir -p "$RESULTS_DIR"

# 命令行参数处理
RUN_TESTS=0
RESULT_FILE="${RESULTS_DIR}/results.jsonl"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --run-tests|-r)
            RUN_TESTS=1
            shift
            ;;
        --result)
            RESULT_FILE="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}错误: 未知的参数 $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}工作目录: $SCRIPT_DIR${NC}"
echo -e "${BLUE}输入目录: $INPUT_DIR${NC}"
echo -e "${BLUE}结果目录: $RESULTS_DIR${NC}"

# 结果汇总
echo -e "\n${YELLOW}================ EDA 评估开始 =================${NC}"

# 如果需要运行测试，检查测试脚本是否存在
if [ $RUN_TESTS -eq 1 ]; then
    # 检查是否存在测试脚本
    if [ ! -f "${SCRIPT_DIR}/test_script.py" ]; then
        echo -e "${RED}错误: 测试脚本 'test_script.py' 不存在${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}运行测试脚本...${NC}"
    # 确保输入和输出目录存在
    mkdir -p "${INPUT_DIR}"
    
    # 运行测试脚本（如果有指定输出目录的参数，应添加在此处）
    cd "$SCRIPT_DIR" && python3 test_script.py
    
    # 检查测试是否成功
    if [ $? -ne 0 ]; then
        echo -e "${RED}测试脚本运行失败!${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}测试脚本运行完成${NC}"
else
    # 检查输入目录是否存在及是否有内容
    if [ ! -d "${INPUT_DIR}" ] || [ -z "$(ls -A ${INPUT_DIR} 2>/dev/null)" ]; then
        echo -e "${RED}错误: 输入目录 '${INPUT_DIR}' 不存在或为空${NC}"
        echo -e "${YELLOW}提示: 使用 --run-tests 或 -r 参数运行测试脚本生成输出${NC}"
        exit 1
    fi
fi

# 检查评估脚本是否存在
if [ ! -f "${SCRIPT_DIR}/test_script.py" ]; then
    echo -e "${RED}错误: 评估脚本 'test_script.py' 不存在${NC}"
    exit 1
fi

# 运行评估脚本
echo -e "${BLUE}运行评估脚本...${NC}"
cd "$SCRIPT_DIR" && python3 test_script.py --input "$INPUT_DIR" --result "$RESULT_FILE"

# 检查JSONL结果文件是否存在
if [ ! -f "$RESULT_FILE" ]; then
    echo -e "${RED}错误: JSONL结果文件 '$RESULT_FILE' 未生成${NC}"
    exit 1
fi

# 提取评估结果
SUCCESS_STATUS=$(grep -o '"Result": true' "$RESULT_FILE" || echo "false")

if echo "$SUCCESS_STATUS" | grep -q "true"; then
    echo -e "${GREEN}评估成功!${NC}"
    
    # 提取匹配分数（如果存在）
    MATCH_SCORE=$(grep -o '"score": [0-9.]*' "$RESULT_FILE" | awk '{print $2}' || echo "不适用")
    if [ "$MATCH_SCORE" != "不适用" ]; then
        echo -e "${GREEN}与groundtruth匹配度: $MATCH_SCORE%${NC}"
    fi
    
    # 提取结论（如果存在）
    CONCLUSION=$(grep -o '"comments": "[^"]*"' "$RESULT_FILE" | cut -d'"' -f4 || echo "无结论")
    echo -e "${BLUE}结论: $CONCLUSION${NC}"
    
    RESULT="${GREEN}成功 - EDA分析结果符合预期${NC}"
else
    echo -e "${RED}评估失败!${NC}"
    
    # 提取失败消息（如果存在）
    ERROR_MSG=$(grep -o '"错误:[^"]*' "$RESULT_FILE" | head -1 || echo "未知错误")
    if [ "$ERROR_MSG" == "未知错误" ]; then
        ERROR_MSG=$(grep -o '"comments": "[^"]*"' "$RESULT_FILE" | cut -d'"' -f4 || echo "未知错误")
    fi
    echo -e "${RED}错误: $ERROR_MSG${NC}"
    
    RESULT="${RED}失败 - $ERROR_MSG${NC}"
fi

echo -e "\n${YELLOW}================ 评估结果 =================${NC}"
echo -e "${BLUE}皮肤电活动分析: ${RESULT}${NC}"

echo -e "\n${YELLOW}================ 评估结束 =================${NC}"

# 显示使用说明
echo -e "\n${BLUE}使用说明:${NC}"
echo -e "  ${YELLOW}./run_evaluation.sh${NC}             - 仅评估现有输出结果"
echo -e "  ${YELLOW}./run_evaluation.sh -r${NC}          - 先运行测试脚本生成输出，再评估结果"
echo -e "  ${YELLOW}./run_evaluation.sh --result FILE${NC} - 指定JSONL结果文件保存路径" 