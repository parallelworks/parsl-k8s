FROM ubuntu:22.04

# Set non-interactive mode to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    bash \
    curl \
    bind9-host \
    netcat-openbsd \
    iproute2 \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Set the Miniconda installer URL
ENV CONDA_REPO=https://repo.anaconda.com/miniconda/Miniconda3-py312_24.9.2-0-Linux-x86_64.sh

# Install Miniconda
RUN wget --no-check-certificate $CONDA_REPO -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/miniconda && \
    rm miniconda.sh

# Set environment variables to use Conda
ENV PATH="/opt/miniconda/bin:$PATH"

# Configure Conda and install Parsl with Kubernetes dependencies
RUN conda config --add channels conda-forge && \
    conda install -y parsl python-kubernetes && \
    conda clean -afy

# Ensure Conda is activated by default
RUN echo "source /opt/miniconda/bin/activate" >> /etc/profile

# Set default shell
SHELL ["/bin/bash", "-c"]

CMD ["bash"]
