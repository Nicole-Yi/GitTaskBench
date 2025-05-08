import cv2
import numpy as np

def color_transfer(source, target):
    """
    Transfers the color distribution from the source to the target
    image using the mean and standard deviations of the L*a*b*
    color space.
    
    This implementation is (loosely) based on to the "Color Transfer
    between Images" paper by Reinhard et al., 2001.
    """
    
    # Convert the images from the RGB to L*a*b* color space, being
    # sure to utilizing the floating point data type (note: OpenCV
    # expects floats to be 32-bit, so use that instead of 64-bit)
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # Compute color statistics for the source and target images
    (lMeanSrc, lStdSrc, aMeanSrc, aStdSrc, bMeanSrc, bStdSrc) = image_stats(source)
    (lMeanTar, lStdTar, aMeanTar, aStdTar, bMeanTar, bStdTar) = image_stats(target)

    # Subtract the means from the target image
    (l, a, b) = cv2.split(target)
    l -= lMeanTar
    a -= aMeanTar
    b -= bMeanTar

    # Scale by the standard deviations
    l = (lStdTar / lStdSrc) * l
    a = (aStdTar / aStdSrc) * a
    b = (bStdTar / bStdSrc) * b

    # Add in the source mean
    l += lMeanSrc
    a += aMeanSrc
    b += bMeanSrc

    # Clip the pixel intensities to [0, 255] if they fall outside
    # this range
    l = np.clip(l, 0, 255)
    a = np.clip(a, 0, 255)
    b = np.clip(b, 0, 255)

    # Merge the channels together and convert back to the RGB color
    # space, being sure to utilize the 8-bit unsigned integer data
    # type
    transfer = cv2.merge([l, a, b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)
    
    # Return the color transferred image
    return transfer

def image_stats(image):
    """
    Computes the mean and standard deviation of each channel
    """
    # Compute the mean and standard deviation of each channel
    (l, a, b) = cv2.split(image)
    (lMean, lStd) = (l.mean(), l.std())
    (aMean, aStd) = (a.mean(), a.std())
    (bMean, bStd) = (b.mean(), b.std())

    # Return the color statistics
    return (lMean, lStd, aMean, aStd, bMean, bStd)

def blend_images(content_img, style_img, alpha=0.7):
    """
    Blend the content and style images using a weighted average
    """
    return cv2.addWeighted(content_img, alpha, style_img, 1.0 - alpha, 0)

def apply_texture_transfer(content_img, style_img):
    """
    Apply texture transfer from style image to content image
    """
    # Convert to grayscale
    content_gray = cv2.cvtColor(content_img, cv2.COLOR_BGR2GRAY)
    style_gray = cv2.cvtColor(style_img, cv2.COLOR_BGR2GRAY)
    
    # Apply histogram equalization to enhance texture
    content_eq = cv2.equalizeHist(content_gray)
    style_eq = cv2.equalizeHist(style_gray)
    
    # Create texture masks
    content_texture = cv2.Laplacian(content_eq, cv2.CV_8U, ksize=3)
    style_texture = cv2.Laplacian(style_eq, cv2.CV_8U, ksize=3)
    
    # Blend textures
    blended_texture = cv2.addWeighted(content_texture, 0.5, style_texture, 0.5, 0)
    
    # Create a 3-channel texture image
    texture_img = cv2.merge([blended_texture, blended_texture, blended_texture])
    
    # Blend with original content
    result = cv2.addWeighted(content_img, 0.7, texture_img, 0.3, 0)
    
    return result

def advanced_style_transfer(content_path, style_path, output_path):
    """
    Perform advanced style transfer using multiple techniques
    """
    # Load the content and style images
    content_img = cv2.imread(content_path)
    style_img = cv2.imread(style_path)
    
    # Resize style image to match content image size
    style_img = cv2.resize(style_img, (content_img.shape[1], content_img.shape[0]))
    
    # Step 1: Color transfer from style to content
    color_transferred = color_transfer(style_img, content_img)
    
    # Step 2: Apply texture transfer
    texture_transferred = apply_texture_transfer(content_img, style_img)
    
    # Step 3: Blend the color and texture results
    result = blend_images(color_transferred, texture_transferred, alpha=0.6)
    
    # Step 4: Final blend with original content for better content preservation
    final_result = blend_images(result, content_img, alpha=0.8)
    
    # Save the output image
    cv2.imwrite(output_path, final_result)
    print(f"Advanced style transfer complete. Output saved to {output_path}")

if __name__ == "__main__":
    content_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_01/input/images.jpeg'
    style_path = '/data/data/agent_test_codebase/GitTaskBench/queries/StyleTransfer_01/input/style.jpeg'
    output_path = '/data/data/agent_test_codebase/GitTaskBench/eval_automation/output/StyleTransfer_01/output.jpg'
    
    advanced_style_transfer(content_path, style_path, output_path)