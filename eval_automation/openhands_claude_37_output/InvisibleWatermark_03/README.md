# Invisible Watermark Embedding and Decoding

This directory contains the result of embedding an invisible watermark "watermark" into an input image using the InvisibleWatermark library.

## Files

- `output.png`: The image with the embedded invisible watermark "watermark"
- `decode_watermark.py`: A Python script to decode the watermark from the image

## How to Decode the Watermark

To decode the watermark from the output image, run:

```bash
python decode_watermark.py
```

Or specify a different image path:

```bash
python decode_watermark.py /path/to/watermarked/image.png
```

## Implementation Details

The watermark was embedded using the `dwtDct` method (Discrete Wavelet Transform + Discrete Cosine Transform), which is the default and fastest method provided by the InvisibleWatermark library.

The watermark text "watermark" was encoded as bytes and embedded into the image. The watermark is invisible to the human eye but can be detected using the appropriate decoding algorithm.

## Requirements

To run the decoding script, you need:
- Python 3.6+
- OpenCV (cv2)
- NumPy
- PyWavelets
- Access to the InvisibleWatermark library

The script automatically adds the InvisibleWatermark library to the Python path.