docker run -it --gpus all \
  --name neurogenesis-cuda-container \
  --ipc=host \
  --ulimit memlock=-1 \
  --ulimit stack=67108864 \
  -v $(pwd):/workspace \
  -v /home/marlon/.miniconda3/envs/neurogenesis:/envs/neurogenesis \
  -w /workspace \
  nvcr.io/nvidia/tensorflow:24.02-tf2-py3
