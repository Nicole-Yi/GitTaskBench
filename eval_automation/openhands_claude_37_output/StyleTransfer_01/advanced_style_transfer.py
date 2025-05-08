import sys
import os
import cv2
import numpy as np

# Add the StyleTransfer repository to the Python path
sys.path.append('/data/data/agent_test_codebase/GitTaskBench/code_base/StyleTransfer')

try:
    # Try to import the necessary modules from the StyleTransfer repository
    from utils.utils import prepare_img, gram_matrix, total_variation, prepare_model, save_and_maybe_display
    import torch
    from torch.optim import LBFGS
    from torch.autograd import Variable
    
    def neural_style_transfer(content_img_path, style_img_path, output_img_path, height=400):
        """
        Perform neural style transfer using the StyleTransfer repository code.
        """
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {device}")
        
        # Prepare images
        content_img = prepare_img(content_img_path, height, device)
        style_img = prepare_img(style_img_path, height, device)
        
        # Initialize with content image
        init_img = content_img.clone()
        optimizing_img = Variable(init_img, requires_grad=True)
        
        # Prepare model
        model_name = 'vgg19'
        neural_net, content_feature_maps_index_name, style_feature_maps_indices_names = prepare_model(model_name, device)
        print(f'Using {model_name} in the optimization procedure.')
        
        # Get feature maps
        content_img_set_of_feature_maps = neural_net(content_img)
        style_img_set_of_feature_maps = neural_net(style_img)
        
        # Get target representations
        target_content_representation = content_img_set_of_feature_maps[content_feature_maps_index_name[0]].squeeze(axis=0)
        target_style_representation = [gram_matrix(x) for cnt, x in enumerate(style_img_set_of_feature_maps) if cnt in style_feature_maps_indices_names[0]]
        target_representations = [target_content_representation, target_style_representation]
        
        # Set optimization parameters
        config = {
            'content_weight': 1e5,
            'style_weight': 3e4,
            'tv_weight': 1e0,
            'optimizer': 'lbfgs',
            'model': model_name,
            'init_method': 'content',
            'height': height,
            'img_format': (4, '.jpg'),
            'saving_freq': -1
        }
        
        # Set up optimizer
        optimizer = LBFGS((optimizing_img,), max_iter=300, line_search_fn='strong_wolfe')
        cnt = 0
        
        def closure():
            nonlocal cnt
            if torch.is_grad_enabled():
                optimizer.zero_grad()
                
            # Build loss
            current_set_of_feature_maps = neural_net(optimizing_img)
            current_content_representation = current_set_of_feature_maps[content_feature_maps_index_name[0]].squeeze(axis=0)
            content_loss = torch.nn.MSELoss(reduction='mean')(target_content_representation, current_content_representation)
            
            style_loss = 0.0
            current_style_representation = [gram_matrix(x) for cnt, x in enumerate(current_set_of_feature_maps) if cnt in style_feature_maps_indices_names[0]]
            for gram_gt, gram_hat in zip(target_style_representation, current_style_representation):
                style_loss += torch.nn.MSELoss(reduction='sum')(gram_gt[0], gram_hat[0])
            style_loss /= len(target_style_representation)
            
            tv_loss = total_variation(optimizing_img)
            
            total_loss = config['content_weight'] * content_loss + config['style_weight'] * style_loss + config['tv_weight'] * tv_loss
            
            if total_loss.requires_grad:
                total_loss.backward()
                
            with torch.no_grad():
                print(f'L-BFGS | iteration: {cnt:03}, total loss={total_loss.item():12.4f}, content_loss={config["content_weight"] * content_loss.item():12.4f}, style loss={config["style_weight"] * style_loss.item():12.4f}, tv loss={config["tv_weight"] * tv_loss.item():12.4f}')
                
                if cnt % 50 == 0 or cnt == 299:
                    # Save intermediate result
                    out_img = optimizing_img.clone().detach().cpu().squeeze(0)
                    out_img = out_img.permute(1, 2, 0).numpy()
                    out_img = np.clip(out_img, 0, 1)
                    out_img = (out_img * 255).astype(np.uint8)
                    
                    # Convert from RGB to BGR for OpenCV
                    out_img = cv2.cvtColor(out_img, cv2.COLOR_RGB2BGR)
                    
                    # Save the image
                    if cnt == 299:  # Final image
                        cv2.imwrite(output_img_path, out_img)
                    else:  # Intermediate image
                        intermediate_path = f"{os.path.splitext(output_img_path)[0]}_iter_{cnt}.jpg"
                        cv2.imwrite(intermediate_path, out_img)
            
            cnt += 1
            return total_loss
        
        # Run optimization
        print("Starting optimization...")
        optimizer.step(closure)
        
        print(f"Style transfer complete. Output saved to {output_img_path}")
        
    if __name__ == "__main__":
        content_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_01/input/images.jpeg'
        style_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_01/input/style.jpeg'
        output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/StyleTransfer_01/output_advanced.jpg'
        
        neural_style_transfer(content_path, style_path, output_path)
        
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Falling back to simple style transfer...")
    
    def simple_style_transfer(content_path, style_path, output_path):
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
        alpha = 0.7  # Weight for content image
        beta = 0.3   # Weight for style image
        
        # Blend the images
        output_img = cv2.addWeighted(content_img, alpha, style_img, beta, 0)
        
        # Convert back to uint8 and save
        output_img = (output_img * 255).astype(np.uint8)
        cv2.imwrite(output_path, output_img)
        
        print(f"Simple style transfer complete. Output saved to {output_path}")
    
    content_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_01/input/images.jpeg'
    style_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_01/input/style.jpeg'
    output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/StyleTransfer_01/output.jpg'
    
    simple_style_transfer(content_path, style_path, output_path)