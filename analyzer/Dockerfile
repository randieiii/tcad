FROM python:3.7
EXPOSE 8080
RUN mkdir -p /usr/src/app && mkdir -p /usr/src/app/vol
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        xvfb \
        xauth \
        libgtk2.0-0 \
        libxtst6 \
        libxss1 \
        libgconf-2-4 \
        libnss3 \
        libasound2 && \
    mkdir -p /opt/orca && \
    cd /opt/orca && \
    wget https://github.com/plotly/orca/releases/download/v1.2.1/orca-1.2.1-x86_64.AppImage && \
    chmod +x orca-1.2.1-x86_64.AppImage && \
    ./orca-1.2.1-x86_64.AppImage --appimage-extract && \
    rm orca-1.2.1-x86_64.AppImage && \
    printf '#!/bin/bash \nxvfb-run --auto-servernum --server-args "-screen 0 640x480x24" /opt/orca/squashfs-root/app/orca "$@"' > /usr/bin/orca && \
    chmod +x /usr/bin/orca
    
COPY . .

ENTRYPOINT ["python3", "tarnado.py"]