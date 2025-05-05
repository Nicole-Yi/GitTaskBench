#!/bin/bash

# 定义根目录
root_dir="/root/autodl-tmp/GitTaskBench/eval_automation/test_scripts"

# 递归遍历文件夹中的所有子文件夹
find "$root_dir" -type f -name "run_test.sh" | while read test_script; do
    echo "Running $test_script..."
    bash "$test_script" # 执行run_test.sh脚本
done
