
# LayoutFlow Documentation

## Overview
LayoutFlow is a repository for flow-based layout generation models. It includes implementations of `LayoutFlow` (flow-based) and `LayoutDMx` (diffusion-based) models, along with tools for training and evaluation.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/marshmallow-code/LayoutFlow.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Training
To train the `LayoutFlow` model, run:
```bash
python src/train.py
```

### Testing
To test the model, run:
```bash
python src/test.py
```

## Configuration
Configuration files are located in `conf/`:
- `model/`: Model-specific configurations.
- `dataset/`: Dataset configurations.
- `train.yaml`: Training settings.
- `test.yaml`: Testing settings.

## Models
### LayoutFlow
A flow-based model for layout generation. Key features:
- Uses `ConditionalFlowMatcher` for training.
- Supports different attribute encodings (`AnalogBit`, `discrete`).

### LayoutDMx
A diffusion-based model for layout generation.

## Datasets
Supported datasets:
- `PubLayNet`
- `RICO`

## Pretrained Models
Pretrained models are available in `pretrained/` for evaluation.

## License
This project is licensed under the MIT License. See `LICENSE` for details.