## Modele
- https://huggingface.co/deepseek-ai/deepseek-llm-7b-base
- https://huggingface.co/HuggingFaceH4/zephyr-7b-beta

## Instalacja PyTorch
- https://stackoverflow.com/questions/63974588/how-to-install-pytorch-with-pipenv-and-save-it-to-pipfile-and-pipfile-lock

Pipfile: 
```shell
# [...]

[[source]]
# PyTorch CUDA 12.6 repo[[source]]
name = "pytorch-cu126"
url = "https://download.pytorch.org/whl/cu126"
verify_ssl = true

# [...]
```
