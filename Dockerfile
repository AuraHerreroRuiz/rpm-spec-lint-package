FROM fedora:latest

# Copying all contents of rpmbuild repo inside container
COPY . .

# Installing tools needed for rpmbuild
RUN dnf install -y rpm-build rpmdevtools rpmlint python3-dnf dnf5-plugins

ENTRYPOINT ["python3.14", "/src/main.py"]
