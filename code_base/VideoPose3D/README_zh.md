# VideoPose3D 推理使用指南

本文档介绍如何使用 Facebook Research 的 VideoPose3D 仓库进行3D人体姿态估计的推理过程。

## 安装依赖

需要安装以下依赖项：
```bash
# 安装基本依赖
apt-get install -y zlib1g-dev libjpeg-dev libpng-dev ffmpeg
pip3 install numpy torch matplotlib pillow
```

## 下载预训练模型

将预训练模型下载到checkpoint目录：
```bash
mkdir -p checkpoint
cd checkpoint
wget https://dl.fbaipublicfiles.com/video-pose-3d/pretrained_h36m_detectron_coco.bin
cd ..
```

## 推理流程

完整的推理流程包括以下步骤：

1. **准备输入数据**：
   - 需要视频文件或2D关键点数据
   - 如果使用视频，需要先通过Detectron2提取2D关键点
   - Detectron2会输出.npz格式的关键点文件

2. **处理2D关键点**：
   - 使用`data/prepare_data_2d_custom.py`脚本处理关键点数据
   - 示例命令：`python3 data/prepare_data_2d_custom.py -i input -o mytest`
   - 输出文件：`data_2d_custom_mytest.npz`

3. **运行3D关键点预测**：
   - 使用主脚本`run.py`进行推理
   - 示例命令：
   ```bash
   python3 run.py -d custom -k mytest -arc 3,3,3,3,3 -c checkpoint --evaluate pretrained_h36m_detectron_coco.bin --viz-subject dummy --viz-action custom --viz-camera 0 --viz-export output/output_3d.npz --viz-no-ground-truth
   ```

4. **输出结果**：
   - 3D关键点坐标保存在输出文件中，格式为numpy数组
   - 数据形状为(帧数, 17, 3)，表示帧数×17个关键点×3D坐标(x,y,z)
   - 可以选择同时生成可视化视频

## 参数说明

主要参数解释：
- `-d custom`：使用自定义数据集
- `-k mytest`：指定关键点数据集名称
- `-arc 3,3,3,3,3`：指定网络架构
- `-c checkpoint`：检查点目录
- `--evaluate`：要加载的预训练模型
- `--viz-subject`：要可视化的主体
- `--viz-action`：动作类型
- `--viz-camera`：相机ID
- `--viz-export`：输出3D关键点数据的文件路径
- `--viz-output`：输出视频文件路径
- `--viz-no-ground-truth`：不显示地面真实值

## 注意事项

1. 该模型预期输入是单人视频
2. 如果视频中有多人，会选择置信度最高的人
3. 预测结果是相对于根关节的，不包含全局轨迹
4. 预测始终在相机空间中，无论轨迹是否可用

## 处理自定义视频

对于自定义视频，完整流程为：
1. 使用Detectron2提取2D关键点
2. 使用prepare_data_2d_custom.py创建数据集
3. 使用run.py生成3D关键点预测
4. 获取输出文件并进行后续处理 