# Base image adequada para aplicações Python
FROM python:3.9-slim

# Evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Atualizar sistema e instalar ferramentas essenciais
RUN apt-get update && apt-get install -y \
    git \
    curl \
    vim \
    make \
    wget \
    zip \
    tree \
    jq \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Criar utilizador não-root
ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=1000

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && usermod -aG sudo $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Definir diretório de trabalho
WORKDIR /app

# Copiar ficheiros da aplicação
COPY . /app

# Instalar dependências Python (se existir requirements.txt)
RUN pip install --no-cache-dir --upgrade pip && \
    if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Instalar ferramentas adicionais (K3D, Tekton, OC CLI)
RUN curl -s https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash && \
    curl -LO https://github.com/tektoncd/cli/releases/download/v0.18.0/tkn_0.18.0_Linux_x86_64.tar.gz && \
    tar xvzf tkn_0.18.0_Linux_x86_64.tar.gz -C /usr/local/bin/ tkn && \
    ln -s /usr/local/bin/tkn /usr/bin/tkn && \
    curl -LO https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz && \
    tar xvzf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz && \
    install openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc /usr/local/bin/oc && \
    ln -s /usr/local/bin/oc /usr/bin/oc

# Expor porta da aplicação
ENV PORT=8000
EXPOSE 8000

# Variável de terminal
ENV TERM=xterm-256color

# Mudar para utilizador não-root (obrigatório para segurança)
USER $USERNAME

# Comando padrão (ajusta conforme tua app Flask)
CMD ["python3", "app.py"]
