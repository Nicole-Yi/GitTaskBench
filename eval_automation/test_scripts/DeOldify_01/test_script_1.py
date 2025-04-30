'''
Author: Nicole-Yi studyworklove@foxmail.com
Date: 2025-04-29 15:04:22
LastEditors: Nicole-Yi studyworklove@foxmail.com
LastEditTime: 2025-04-29 15:45:04
FilePath: \codes\test_automation\test_scripts\DeOldify\test_script_1.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#!/usr/bin/env python3
import os
import sys
import argparse
import requests
from io import BytesIO
from datetime import datetime

import numpy as np
from PIL import Image
from skimage.color import rgb2lab, deltaE_ciede2000
from basicsr.metrics.niqe import calculate_niqe

def download_image(path_or_url: str) -> Image.Image:
    """下载或读取本地图片，返回 RGB 模式的 PIL.Image。"""
    if path_or_url.startswith(('http://', 'https://')):
        resp = requests.get(path_or_url, timeout=10)
        if resp.status_code != 200:
            raise ValueError(f"无法下载图片：{path_or_url} (状态码 {resp.status_code})")
        data = BytesIO(resp.content)
    else:
        if not os.path.isfile(path_or_url):
            raise ValueError(f"文件不存在：{path_or_url}")
        data = path_or_url
    return Image.open(data).convert('RGB')

def compute_ciede2000(ref_img: Image.Image, test_img: Image.Image) -> float:
    """计算平均 CIEDE2000 色差。"""
    arr_ref  = np.asarray(ref_img, dtype=np.float32) / 255.0
    arr_test = np.asarray(test_img, dtype=np.float32) / 255.0
    lab_ref  = rgb2lab(arr_ref)
    lab_test = rgb2lab(arr_test)
    delta    = deltaE_ciede2000(lab_ref, lab_test)
    return float(np.mean(delta))

def compute_niqe(img: Image.Image) -> float:
    """计算 NIQE 分值。"""
    arr = np.asarray(img).astype(np.float32)
    return float(calculate_niqe(arr, crop_border=0))

def main():
    p = argparse.ArgumentParser(
        description="以 CIEDE2000 与 NIQE 两指标评测上色/增强效果，并记录结果")
    p.add_argument("ref", help="参考图像 URL 或本地路径")
    p.add_argument("recon", help="重建图像 URL 或本地路径")
    p.add_argument("--ciede-thresh", type=float, required=True,
                   help="CIEDE2000 最低接受阈值（越大越好）")
    p.add_argument("--niqe-thresh", type=float, required=True,
                   help="NIQE 最高接受阈值（越小越好）")
    p.add_argument("--repo-name", required=True,
                   help="仓库名称，用于结果文件记录")
    p.add_argument("--result-file", help="将记录追加写入该文件", default=None)
    args = p.parse_args()

    # 加载图像
    try:
        img_ref   = download_image(args.ref)
        img_recon = download_image(args.recon)
    except ValueError as err:
        print(f"[ERROR] {err}", file=sys.stderr)
        sys.exit(1)

    # 计算指标
    score_ciede = compute_ciede2000(img_ref, img_recon)
    score_niqe  = compute_niqe(img_recon)

    # 判定
    ok_ciede = score_ciede >= args.ciede_thresh
    ok_niqe  = score_niqe  <= args.niqe_thresh
    overall_ok = ok_ciede and ok_niqe

    # 打印最终 True/False
    print("True" if overall_ok else "False")

    # 记录到文件
    if args.result_file:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M")
        header = "Repo:\t\tResult:\t\tTimePoint:\n"
        line   = f"{args.repo_name}\t\t{overall_ok}\t\t{timestamp}\n"
        # 判断是否需要写入表头
        need_header = not os.path.exists(args.result_file) or os.path.getsize(args.result_file) == 0
        try:
            with open(args.result_file, "a", encoding="utf-8") as f:
                if need_header:
                    f.write(header)
                f.write(line)
        except Exception as e:
            print(f"[ERROR] 无法写入结果文件：{e}", file=sys.stderr)
            sys.exit(1)

    # 退出码：成功返回 0，失败返回 2
    sys.exit(0 if overall_ok else 2)


if __name__ == "__main__":
    main()
