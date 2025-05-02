docker run -it --gpus all \
  --name neurogenesis-cuda-container \
  --ipc=host \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  --cpus=16 \
  --memory=30g \
  --memory-swap=30g \
  -v ~/edu/mestrado/proj/neurogenesis:/workspace \
  -v ~/.miniconda3/envs/neurogenesis:/envs/neurogenesis \
  -w /workspace \
  nvcr.io/nvidia/tensorflow:24.02-tf2-py3
