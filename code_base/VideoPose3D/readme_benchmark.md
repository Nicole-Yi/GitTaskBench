# VideoPose3D 基准测试流程

本文档描述了使用 Facebook Research 的 VideoPose3D 进行3D人体姿态估计的基准测试流程。

## 概述

基准测试流程包括以下步骤：
1. 环境准备
2. 运行推理测试 (test.py)
3. 评估输出结果 (evaluate.py)

## 环境准备

### 系统要求
- Python 3.6+
- CUDA (如果使用GPU)

### 依赖安装
```bash
# 安装系统依赖
apt-get update
apt-get install -y zlib1g-dev libjpeg-dev libpng-dev ffmpeg

# 安装Python依赖
pip3 install numpy torch matplotlib pillow
```

### 下载预训练模型
```bash
mkdir -p checkpoint
cd checkpoint
wget https://dl.fbaipublicfiles.com/video-pose-3d/pretrained_h36m_detectron_coco.bin
cd ..
```

### 准备目录结构
```bash
mkdir -p input output
```

## 运行测试脚本 (test.py)

测试脚本自动执行完整的推理流程，包括数据准备、模型推理和结果输出。

### 脚本功能
- 检查必要的目录和文件
- 下载预训练模型（如果需要）
- 创建测试数据（如果input目录为空）
- 处理2D关键点
- 运行3D关键点预测
- 输出结果到指定位置

### 使用方法
```bash
python3 test.py --input input --output output
```

### 参数说明
- `--input`: 输入目录路径，默认为 "input"
- `--output`: 输出目录路径，默认为 "output"
- `--model`: 预训练模型路径，默认为 "checkpoint/pretrained_h36m_detectron_coco.bin"
- `--tmp_name`: 临时数据集名称，默认为 "mytest"

### 示例
```bash
# 使用默认参数运行
python3 test.py

# 指定自定义路径
python3 test.py --input my_input --output my_output
```

## 评估脚本 (evaluate.py)

评估脚本用于分析输出的3D关键点数据，评估其质量，并生成评估报告。

### 脚本功能
- 加载并分析3D关键点数据
- 检查数据一致性和质量
- 生成评估报告
- 可选：创建可视化图表

### 使用方法
```bash
python3 evaluate.py --input output/output_3d.npz.npy --output output/evaluation_report.txt
```

### 参数说明
- `--input`: 输入3D关键点文件路径，默认为 "output/output_3d.npz.npy"
- `--output`: 评估结果输出路径，默认为 "output/evaluation_report.txt"
- `--visualize`: 是否生成可视化图表，默认为否

### 示例
```bash
# 基本评估
python3 evaluate.py

# 包含可视化
python3 evaluate.py --visualize
```

## 评估标准

评估脚本根据以下指标对输出结果进行评分（0-100分）：

1. **数据完整性**：检查是否有NaN值或缺失数据
2. **骨骼长度一致性**：骨骼长度在不同帧之间应该保持相对稳定
3. **动作平滑度**：相邻帧之间的位移不应该过大

评分标准：
- 90-100分：优秀
- 75-89分：良好
- 60-74分：合格
- 0-59分：不合格

## 完整测试流程

以下是完整的基准测试流程命令：

```bash
# 1. 准备环境
apt-get update
apt-get install -y zlib1g-dev libjpeg-dev libpng-dev ffmpeg
pip3 install numpy torch matplotlib pillow

# 2. 确保目录结构
mkdir -p input output checkpoint

# 3. 下载预训练模型
wget -P checkpoint https://dl.fbaipublicfiles.com/video-pose-3d/pretrained_h36m_detectron_coco.bin

# 4. 运行测试脚本
python3 test.py

# 5. 评估结果
python3 evaluate.py --visualize
```

## 注意事项

1. **输入数据格式**：
   - 若使用视频文件，需先通过Detectron2提取2D关键点
   - 若直接使用2D关键点，需符合特定的.npz格式

2. **性能考虑**：
   - GPU加速可显著提高推理速度
   - 较大的视频文件可能需要更多内存

3. **输出解释**：
   - 输出的3D关键点坐标相对于根关节，不包含全局轨迹
   - 坐标系为相机空间坐标系

4. **故障排除**：
   - 如遇到模型下载问题，可手动下载并放入checkpoint目录
   - 如输出评分低于60分，请检查输入数据质量和处理流程

## 结果验收标准

成功的基准测试应满足以下条件：
1. test.py脚本能成功运行，生成输出文件
2. evaluate.py评估结果达到60分以上
3. 输出的3D关键点数据形状正确，通常为(帧数, 17, 3)

若以上条件均满足，则视为基准测试通过。 