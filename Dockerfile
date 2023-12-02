FROM fedora:38

RUN dnf upgrade -y && \
    dnf install -y \
      autoconf \
      autogen \
      libtool \
      git \
      vim \
      llvm-devel \
      clang \
      make \
      cmake \
      ninja-build \
      gcc-c++ \
      python3 \
      python3-devel \
      python3-pip \
      python3-cffi \
      python3-jinja2 \
      python3-jsonschema \
      gtest-devel \
      fish \
      which \
      python-unversioned-command \
      diffutils

RUN mkdir /experiment
WORKDIR /experiment

RUN git clone https://github.com/viktormalik/diffkemp.git
WORKDIR /experiment/diffkemp
RUN mkdir build && \
    cd build && \
    cmake .. -GNinja -DCMAKE_BUILD_TYPE=Release && \
    ninja -j4 && \
    cd ..
RUN pip install -r requirements.txt && \
    pip install -e .

WORKDIR /experiment
RUN git clone https://github.com/zacikpa/diffkemp-analysis.git

COPY config /experiment/config

ENTRYPOINT /bin/fish



