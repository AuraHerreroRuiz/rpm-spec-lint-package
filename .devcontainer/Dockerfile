FROM fedora:latest

ARG USERNAME=dev
ARG UID=1000
ARG GID=$UID

RUN groupadd -g $GID $USERNAME \
	&& useradd -m -u $UID -g $GID $USERNAME \
	&& usermod -aG wheel $USERNAME \
	&& echo "%wheel ALL=(ALL:ALL) NOPASSWD: ALL" >> /etc/sudoers
# Alternative mirror for openh264
RUN dnf config-manager addrepo --from-repofile=https://negativo17.org/repos/fedora-multimedia.repo
# Development
RUN dnf install -y ruff git moby-engine docker-cli iptables-nft
# Python binding
RUN dnf install -y rpm-build rpmdevtools rpmlint python3-dnf python3-libdnf5 dnf5-plugins

USER $USERNAME
