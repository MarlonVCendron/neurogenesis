# docker run -it --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 -v $(pwd):/workspace -v

docker start -ai neurogenesis-cuda-container
# docker exec -it neurogenesis-cuda-container bash -c "conda activate /envs/neurogenesis && bash"

