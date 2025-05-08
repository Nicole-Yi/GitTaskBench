#!/usr/bin/env python3
"""
Example script to load and use the 3D pose data
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load the data
data = np.load('output.npz')
positions_3d = data['positions_3d']

print(f"Loaded 3D pose data with shape: {positions_3d.shape}")
print(f"Number of frames: {positions_3d.shape[0]}")
print(f"Number of joints: {positions_3d.shape[1]}")

# Access a specific frame and joint
frame_idx = 0
joint_idx = 0
joint_position = positions_3d[frame_idx, joint_idx]
print(f"\nJoint {joint_idx} position (x, y, z) in frame {frame_idx}: {joint_position}")

# Define the connections between joints for visualization
edges = [
    (0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (5, 6),
    (0, 7), (7, 8), (8, 9), (9, 10), (8, 11), (11, 12),
    (12, 13), (8, 14), (14, 15), (15, 16)
]

# Function to visualize a specific frame
def visualize_frame(frame_idx):
    frame = positions_3d[frame_idx]
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the joints
    ax.scatter(frame[:, 0], frame[:, 1], frame[:, 2], c='red', marker='o')
    
    # Plot the connections between joints
    for edge in edges:
        ax.plot([frame[edge[0], 0], frame[edge[1], 0]],
                [frame[edge[0], 1], frame[edge[1], 1]],
                [frame[edge[0], 2], frame[edge[1], 2]], c='blue')
    
    # Set labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'3D Human Pose (Frame {frame_idx})')
    
    # Set equal aspect ratio
    max_range = np.max([
        np.max(frame[:, 0]) - np.min(frame[:, 0]),
        np.max(frame[:, 1]) - np.min(frame[:, 1]),
        np.max(frame[:, 2]) - np.min(frame[:, 2])
    ])
    mid_x = (np.max(frame[:, 0]) + np.min(frame[:, 0])) * 0.5
    mid_y = (np.max(frame[:, 1]) + np.min(frame[:, 1])) * 0.5
    mid_z = (np.max(frame[:, 2]) + np.min(frame[:, 2])) * 0.5
    ax.set_xlim(mid_x - max_range * 0.5, mid_x + max_range * 0.5)
    ax.set_ylim(mid_y - max_range * 0.5, mid_y + max_range * 0.5)
    ax.set_zlim(mid_z - max_range * 0.5, mid_z + max_range * 0.5)
    
    plt.show()

# Example usage:
# visualize_frame(0)  # Visualize the first frame
# visualize_frame(10)  # Visualize the 10th frame

print("\nTo visualize a specific frame, uncomment and run one of the visualize_frame() calls at the end of this script.")