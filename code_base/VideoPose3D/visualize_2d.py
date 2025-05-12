import numpy as np
import matplotlib.pyplot as plt
import os

def visualize_keypoints(input_path, output_dir):
    # Load data
    data = np.load(input_path, allow_pickle=True)
    keypoints = data['keypoints']
    metadata = data['metadata'].item()
    
    # Create output directory if needed
    os.makedirs(output_dir, exist_ok=True)
    
    # Plot each frame
    for i, kp in enumerate(keypoints):
        plt.figure(figsize=(10, 6))
        plt.scatter(kp[:,0], metadata['h']-kp[:,1])  # Flip y-axis
        plt.xlim(0, metadata['w'])
        plt.ylim(0, metadata['h'])
        plt.title(f'Frame {i}')
        plt.savefig(f'{output_dir}/frame_{i:03d}.png')
        plt.close()

if __name__ == '__main__':
    input_path = '/data/data/agent_test_codebase/GitTaskBench/queries/VideoPose3D_01/input/VideoPose3D_01_input.npz'
    output_dir = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/VideoPose3D_01/2d_visualization'
    visualize_keypoints(input_path, output_dir)