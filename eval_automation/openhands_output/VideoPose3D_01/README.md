# 3D Human Pose Estimation from 2D Keypoints

This directory contains the results of 3D human pose estimation from 2D keypoint data using the VideoPose3D model.

## Files

- `output.npz`: Contains the 3D pose estimation results in NumPy format
- `visualization.png`: Visualization of a single frame of the 3D pose
- `multi_frame_visualization.png`: Visualization of multiple frames of the 3D pose

## Data Format

The `output.npz` file contains a single key:
- `positions_3d`: 3D joint positions with shape (num_frames, 17, 3), where:
  - num_frames: Number of frames in the sequence
  - 17: Number of joints in the Human3.6M skeleton
  - 3: 3D coordinates (x, y, z) for each joint

## How to Use

To load and use the 3D pose data:

```python
import numpy as np

# Load the data
data = np.load('output.npz')
positions_3d = data['positions_3d']

# Access a specific frame and joint
frame_idx = 0
joint_idx = 0
joint_position = positions_3d[frame_idx, joint_idx]
print(f"Joint position (x, y, z): {joint_position}")
```

## Process

The 3D pose estimation was generated using the following process:

1. The 2D keypoint data was processed using the VideoPose3D framework
2. A pretrained model (pretrained_h36m_detectron_coco.bin) was used for inference
3. The model architecture was adapted to handle the input sequence length
4. The output 3D poses were saved in NumPy format

## Joint Mapping

The 17 joints in the Human3.6M skeleton correspond to:

0. Hip
1. Right Hip
2. Right Knee
3. Right Ankle
4. Left Hip
5. Left Knee
6. Left Ankle
7. Spine
8. Thorax
9. Neck/Nose
10. Head
11. Left Shoulder
12. Left Elbow
13. Left Wrist
14. Right Shoulder
15. Right Elbow
16. Right Wrist