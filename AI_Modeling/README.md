# OpenVINO Training Extensions

## Install dependencies
```
sudo apt update
sudo apt-get install g++ freeglut3-dev build-essential libx11-dev libxmu-dev libxi-dev libglu1-mesa libglu1-mesa-dev gcc-multilib dkms mesa-utils
sudo apt upgrade
```

## Download and install CUDA 11.7
Note, link below is for Ubuntu20.04. For other versoins please refer [CUDA Toolkit 11.7 Downloads](https://developer.nvidia.com/cuda-11-7-0-download-archive)
```bash
cd ~/Downloads/
wget https://developer.download.nvidia.com/compute/cuda/11.7.0/local_installers/cuda_11.7.0_515.43.04_linux.run
sudo sh cuda_11.7.0_515.43.04_linux.run
```


## OTX install
<!-- Source code install
```bash
mkdir -p ~/repo && cd $_
git clone https://github.com/openvinotoolkit/training_extensions.git
cd training_extensions
git checkout develop
```
-->


```bash
# Create virtual env.
python3 -m venv .otx

# Activate virtual env.
source .otx/bin/activate
```

```bash
pip install wheel setuptools

# install command for torch==1.13.1 for CUDA 11.7:
pip install torch==1.13.1 torchvision==0.14.1 --extra-index-url https://download.pytorch.org/whl/cu117
pip install otx[full]
```

# AI_Modeling

## Download Dataset

### Links

* Handwritten math symbols dataset
    https://www.kaggle.com/datasets/xainano/handwrittenmathsymbols

* A command that is able to download in Server
```
scp -r /home/<userid>/Downloads/dataset/ <userid>@xxx.xxx.xxx.xxx:/dir01/dir02/
```

### Check number of files

A command combination that shows number of files under given directory.
```bash
find ./ -maxdepth 2 –type d | while read –r dir; do printf “%s:\t” “$dir”; find “$dir” –type f | wc –l; done
```


## Training

### Build

```
otx build --train-data-roots /dir01/dir02/dataset/ --model MobileNet-V3-large-1x --workspace ./MobileNet-V3-large-1x
```

### Train

```
cd MobileNet-V3-large-1x
otx train params --learning_parameters.batch_size 16 --learning_parameters.num_iters 10
```

### Eval

```
otx eval --test-data-roots ./splitted_dataset/val/ --load-weight ./outputs/latest_trained_model/logs/best_epoch_8.pth
```

### Export

```
otx export
```

## Model Generated

```
cd outputs/20xx.mm.dd_hhmmss_export/openvino
```
Generated 3 files
