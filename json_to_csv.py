#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
import os
import re

def clean_text(text):
    """清理文本，去除换行符和多余空格"""
    if text is None:
        return ""
    # 替换换行符为空格
    text = re.sub(r'\n', ' ', str(text))
    # 将多个空格替换为一个
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def json_to_csv(json_file, output_dir='output'):
    """将JSON文件转换为CSV格式"""
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 处理"未找到结果"
    not_found_results = data.get("未找到结果", [])
    if not_found_results:
        with open(f'{output_dir}/not_found_results.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['路径'])
            for path in not_found_results:
                writer.writerow([path])
    
    # 处理"未找到测试脚本"
    not_found_scripts = data.get("未找到测试脚本", [])
    if not_found_scripts:
        with open(f'{output_dir}/not_found_scripts.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['路径'])
            for path in not_found_scripts:
                writer.writerow([path])
    
    # 处理"计算过程错误"
    errors = data.get("计算过程错误", [])
    if errors:
        with open(f'{output_dir}/computation_errors.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['任务ID', '错误信息', '源结果路径', '目标路径', '日志摘要'])
            for error in errors:
                writer.writerow([
                    error.get('task_id', ''),
                    clean_text(error.get('error', '')),
                    error.get('source_result_path', ''),
                    error.get('dst_path', ''),
                    clean_text(error.get('logs', ''))
                ])
    
    # 处理"任务评分结果"
    results = data.get("任务评分结果", [])
    if results:
        with open(f'{output_dir}/task_results.csv', 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                '任务ID', 
                '处理成功', 
                '结果成功', 
                '时间点', 
                '评论',
                '源结果路径'
            ])
            
            for result in results:
                # 处理结果成功状态
                result_success = result.get('Result_success')
                if result_success is None:
                    # 尝试从result中获取
                    result_obj = result.get('result', {})
                    if isinstance(result_obj, dict):
                        # 先查找Results键
                        result_success = result_obj.get('Results')
                        # 如果没有Results键，再查找Result键
                        if result_success is None:
                            result_success = result_obj.get('Result')
                
                # 转换为字符串形式
                result_success = str(result_success) if result_success is not None else ""
                
                # 处理评论
                comments = result.get('result', {}).get('comments', '')
                if not comments and 'Comments' in result.get('result', {}):
                    comments = result.get('result', {}).get('Comments', '')
                
                writer.writerow([
                    result.get('task_id', ''),
                    result.get('process_success', ''),
                    result_success,
                    result.get('result', {}).get('TimePoint', ''),
                    clean_text(comments),
                    result.get('source_result_path', '')
                ])
    
    # 创建任务总览CSV，汇总所有任务状态
    with open(f'{output_dir}/task_summary.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['任务ID', '状态', '处理成功', '结果成功'])
        
        # 添加任务评分结果
        for result in results:
            process_success = result.get('process_success')
            result_success = result.get('Result_success')
            
            if process_success and result_success:
                status = "通过"
            elif process_success and not result_success:
                status = "处理成功但结果失败"
            else:
                status = "处理失败"
                
            writer.writerow([
                result.get('task_id', ''),
                status,
                str(process_success) if process_success is not None else "",
                str(result_success) if result_success is not None else ""
            ])
        
        # 添加计算过程错误的任务
        for error in errors:
            writer.writerow([
                error.get('task_id', ''),
                "计算过程错误",
                "False",
                "False"
            ])
        
        # 添加未找到测试脚本的任务
        for script_path in not_found_scripts:
            task_id = os.path.basename(os.path.dirname(script_path))
            writer.writerow([
                task_id,
                "未找到测试脚本",
                "False",
                "False"
            ])
        
        # 添加未找到结果的任务
        for result_path in not_found_results:
            # 从路径中提取任务ID
            match = re.search(r'/([^/]+)_\d+/', result_path)
            task_id = match.group(1) + "_??" if match else "未知"
            writer.writerow([
                task_id,
                "未找到结果",
                "False",
                "False"
            ])

if __name__ == "__main__":
    json_file = "all_result.json"
    output_dir = "csv_results"
    json_to_csv(json_file, output_dir)
    print(f"CSV文件已保存到 {output_dir} 目录") 