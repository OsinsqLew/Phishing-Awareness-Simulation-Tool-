## Model
- https://huggingface.co/HuggingFaceH4/zephyr-7b-beta

## Instalacja PyTorch
- https://stackoverflow.com/questions/63974588/how-to-install-pytorch-with-pipenv-and-save-it-to-pipfile-and-pipfile-lock

Pipfile: 
```ini
# [...]

[[source]]
# PyTorch repo (currently CUDA 12.6)
name = "pytorch"
url = "https://download.pytorch.org/whl/cu126"
verify_ssl = true

[packages]
torch = {index = "pytorch", version = "==2.6.0"}
torchaudio = {index = "pytorch", version = "==2.6.0"}
torchvision = {index = "pytorch", version = "==0.21.0"}

# [...]
```
