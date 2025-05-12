import torch
import numpy as np
from torch.optim import Adam, LBFGS
from torch.autograd import Variable
import os
from utils.utils_pillow import prepare_img, save_image
from models.definitions.vgg_nets import Vgg19

def combined_reconstruction(content_fmap_path, style_fmap_path, output_dir, height=500, optimizer='lbfgs', model='vgg19'):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load feature maps
    content_fmap = torch.load(content_fmap_path).to(device)
    style_fmap = torch.load(style_fmap_path).to(device)
    
    # Initialize model
    neural_net = Vgg19().to(device).eval()
    
    # Initialize image to optimize (starting from noise)
    img_shape = (1, 3, height, int(height * 1.5))  # Approximate shape
    white_noise_img = np.random.uniform(-90., 90., img_shape).astype(np.float32)
    optimizing_img = Variable(torch.from_numpy(white_noise_img).float().to(device), requires_grad=True)
    
    # Optimization parameters
    num_iterations = {'adam': 3000, 'lbfgs': 350}[optimizer]
    
    # Loss weights
    content_weight = 1e5
    style_weight = 1e4
    
    def closure():
        nonlocal optimizing_img
        
        if optimizer == 'lbfgs':
            optimizer_lbfgs.zero_grad()
            
        # Forward pass
        set_of_feature_maps = neural_net(optimizing_img)
        
        # Content loss
        current_content = set_of_feature_maps[4].squeeze(axis=0)  # conv4_2
        content_loss = content_weight * torch.nn.MSELoss(reduction='mean')(content_fmap, current_content)
        
        # Style loss
        style_grams = [gram_matrix(fmaps) for i, fmaps in enumerate(set_of_feature_maps) if i in [0,1,2,3,5]]
        style_loss = 0
        for gram_gt, gram_hat in zip(style_fmap, style_grams):
            style_loss += (style_weight / len(style_fmap)) * torch.nn.MSELoss(reduction='sum')(gram_gt[0], gram_hat[0])
        
        # Total loss
        total_loss = content_loss + style_loss
        total_loss.backward()
        
        return total_loss
    
    # Run optimization
    if optimizer == 'adam':
        optimizer_adam = Adam((optimizing_img,))
        for it in range(num_iterations):
            optimizer_adam.step(closure)
            print(f'Iteration: {it}, loss: {closure().item()}')
    else:  # lbfgs
        optimizer_lbfgs = LBFGS((optimizing_img,), max_iter=num_iterations, line_search_fn='strong_wolfe')
        optimizer_lbfgs.step(closure)
    
    # Save result
    result_path = os.path.join(output_dir, 'output.jpg')
    save_image(optimizing_img, result_path)
    return result_path

def gram_matrix(feature_maps):
    batch_size, num_channels, height, width = feature_maps.size()
    features = feature_maps.view(batch_size * num_channels, height * width)
    gram = torch.mm(features, features.t())
    return gram.div(batch_size * num_channels * height * width)

if __name__ == "__main__":
    content_path = "/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_03/input/StyleTransfer_03_input_02.jpg"
    style_path = "/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_03/input/StyleTransfer_03_input_01.jpg"
    output_dir = "/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/StyleTransfer_03"
    
    result = combined_reconstruction(content_path, style_path, output_dir)
    print(f"Reconstruction complete. Result saved to: {result}")