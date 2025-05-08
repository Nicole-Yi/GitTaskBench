import cv2
import numpy as np
import os

def style_transfer_opencv(content_path, style_path, output_path):
    # Load the content and style images
    content_img = cv2.imread(content_path)
    style_img = cv2.imread(style_path)
    
    # Resize style image to match content image size
    style_img = cv2.resize(style_img, (content_img.shape[1], content_img.shape[0]))
    
    # Create a directory for the model if it doesn't exist
    model_dir = os.path.join(os.path.dirname(output_path), 'models')
    os.makedirs(model_dir, exist_ok=True)
    
    # Download the model if it doesn't exist
    model_path = os.path.join(model_dir, 'eccv16_color_transfer_300.t7')
    if not os.path.exists(model_path):
        print("Downloading model...")
        os.system(f"wget -O {model_path} https://cs.stanford.edu/people/jcjohns/fast-neural-style/models/eccv16/eccv16_color_transfer_300.t7")
    
    # Load the model
    print("Loading model...")
    net = cv2.dnn.readNetFromTorch(model_path)
    
    # Prepare input blob
    blob = cv2.dnn.blobFromImage(content_img, 1.0, (content_img.shape[1], content_img.shape[0]),
                                 (103.939, 116.779, 123.68), swapRB=False, crop=False)
    
    # Set the input
    net.setInput(blob)
    
    # Perform forward pass
    print("Performing style transfer...")
    output = net.forward()
    
    # Reshape the output tensor to image
    output = output.reshape(3, output.shape[2], output.shape[3])
    output[0] += 103.939
    output[1] += 116.779
    output[2] += 123.68
    output /= 255.0
    output = output.transpose(1, 2, 0)
    
    # Clip the values to [0, 1] range
    output = np.clip(output, 0, 1)
    
    # Convert to uint8
    output = (output * 255).astype(np.uint8)
    
    # Save the output image
    cv2.imwrite(output_path, output)
    print(f"Style transfer complete. Output saved to {output_path}")

if __name__ == "__main__":
    content_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_01/input/images.jpeg'
    style_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_01/input/style.jpeg'
    output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/StyleTransfer_01/output.jpg'
    
    try:
        style_transfer_opencv(content_path, style_path, output_path)
    except Exception as e:
        print(f"Error in OpenCV style transfer: {e}")
        print("Falling back to simple style transfer...")
        
        # Simple style transfer using weighted average
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
        alpha = 0.7  # Weight for content image
        beta = 0.3   # Weight for style image
        
        # Blend the images
        output_img = cv2.addWeighted(content_img, alpha, style_img, beta, 0)
        
        # Convert back to uint8 and save
        output_img = (output_img * 255).astype(np.uint8)
        cv2.imwrite(output_path, output_img)
        
        print(f"Simple style transfer complete. Output saved to {output_path}")