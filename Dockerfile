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

RUN git clone https://github.com/zacikpa/diffkemp-analysis.git
RUN git clone https://github.com/zacikpa/diffkemp.git
WORKDIR /diffkemp
RUN git checkout structure-pattern
RUN mkdir build && \
    cd build && \
    cmake .. -GNinja -DCMAKE_BUILD_TYPE=Release && \
    ninja -j4 && \
    cd ..
RUN pip install -r requirements.txt && \
    pip install -e .

RUN mkdir /experiment
WORKDIR /experiment

COPY config /experiment/config
COPY custom-patterns /experiment/custom-patterns
COPY experiment-pre.py /experiment/experiment-pre.py

ENTRYPOINT /bin/fish



