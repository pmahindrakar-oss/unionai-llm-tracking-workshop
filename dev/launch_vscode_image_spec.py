"""This file builds the image used in launch_vscode."""

from flytekit import ImageSpec
from imagespec_fast_builder import FastImageBuilder

image = ImageSpec(
    name="flyte_playground",
    builder="fast-builder",
    python_version="3.11",
    apt_packages=["wget", "tar"],
    packages=[
        "unionai==0.1.14",
        "flyteidl==1.11.1b",
        "flytekitplugins-flyteinteractive==1.11.0",
        "transformers==4.39.1",
        "https://download.pytorch.org/whl/cpu-cxx11-abi/torch-2.0.1%2Bcpu.cxx11.abi-cp311-cp311-linux_x86_64.whl#sha256=b0bb23f28e5fc8fee76b8547c9ec0ecff9476da32225c7734090b658fbbc3d38",
    ],
    registry="ghcr.io/thomasjpfan",
    source_root="interact_root",
    env={"PATH": "/tmp/code-server/code-server-4.19.0-linux-amd64/bin:$PATH"},
    commands=[
        "mkdir -p /tmp/code-server",
        "wget --no-check-certificate -O /tmp/code-server/code-server-4.19.0-linux-amd64.tar.gz https://github.com/coder/code-server/releases/download/v4.19.0/code-server-4.19.0-linux-amd64.tar.gz",
        "wget --no-check-certificate https://open-vsx.org/api/ms-python/python/2023.20.0/file/ms-python.python-2023.20.0.vsix -P /tmp/code-server",
        "wget --no-check-certificate https://open-vsx.org/api/ms-toolsai/jupyter/2023.9.100/file/ms-toolsai.jupyter-2023.9.100.vsix -P /tmp/code-server",
        "tar -xzf /tmp/code-server/code-server-4.19.0-linux-amd64.tar.gz -C /tmp/code-server/",
        "chown -R flytekit /tmp",
        "su -c 'code-server --install-extension /tmp/code-server/ms-python.python-2023.20.0.vsix' flytekit",
        "su -c 'code-server --install-extension /tmp/code-server/ms-toolsai.jupyter-2023.9.100.vsix' flytekit",
    ],
)

FastImageBuilder()._build_image(image, push=False)
