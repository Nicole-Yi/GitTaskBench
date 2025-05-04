import cv2
import numpy as np

def style_transfer(content_path, style_path, output_path):
    # Load the content and style images
    content_img = cv2.imread(content_path)
    style_img = cv2.imread(style_path)
    
    # Resize style image to match content image size
    style_img = cv2.resize(style_img, (content_img.shape[1], content_img.shape[0]))
    
    # Convert images to float32
    content_img = content_img.astype(np.float32)
    style_img = style_img.astype(np.float32)
    
    # Normalize images to [0, 1]
    content_img /= 255.0
    style_img /= 255.0
    
    # Simple style transfer using weighted average
    # This is a very basic approach, not neural style transfer
    alpha = 0.7  # Weight for content image
    beta = 0.3   # Weight for style image
    
    # Blend the images
    output_img = cv2.addWeighted(content_img, alpha, style_img, beta, 0)
    
    # Convert back to uint8 and save
    output_img = (output_img * 255).astype(np.uint8)
    cv2.imwrite(output_path, output_img)
    
    print(f"Style transfer complete. Output saved to {output_path}")

if __name__ == "__main__":
    content_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_01/input/images.jpeg'
    style_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_01/input/style.jpeg'
    output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/StyleTransfer_01/output.jpg'
    
    style_transfer(content_path, style_path, output_path)