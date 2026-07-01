FROM fedora:latest

ARG USERNAME=dev
ARG UID=1000
ARG GID=$UID

RUN groupadd -g $GID $USERNAME \
    && useradd -m -u $UID -g $GID $USERNAME \
    && usermod -aG wheel $USERNAME \
    && echo "%wheel ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers

RUN dnf install -y rpm-build rpm-python3 python3-dnf rpmdevtools git rpmlint moby-engine docker-cli iptables-nft

USER $USERNAME
