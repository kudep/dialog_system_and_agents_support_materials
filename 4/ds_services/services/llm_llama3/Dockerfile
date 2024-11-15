# syntax=docker/dockerfile:1
FROM nvidia/cuda:12.5.0-devel-ubuntu22.04

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git build-essential \
    python3 python3-pip gcc wget curl \
    ocl-icd-opencl-dev opencl-headers clinfo \
    libclblast-dev libopenblas-dev \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

ENV POETRY_VERSION=1.8.3 \ 
    POETRY_HOME="/opt/poetry"

ENV PATH="$POETRY_HOME/bin:$PATH"
ENV PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
    
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV CUDA_DOCKER_ARCH=all \
    LLAMA_CUBLAS=1 \
    CMAKE_ARGS="-DGGML_CUDA=on"

WORKDIR /app

# copy packages dirs 
COPY common_packages /common_packages
# copy files
COPY services/llm_llama3/pyproject.toml services/llm_llama3/poetry.lock ./

RUN poetry install

# sync with all service data
COPY services/llm_llama3/ .

CMD ["poetry", "run", "fastapi", "run"]
