FROM fedora:latest

# Copying all contents of rpmbuild repo inside container
COPY . .

# Installing tools needed for rpmbuild
RUN dnf install -y rpm-build python3-dnf rpmdevtools git rpmlint

ENTRYPOINT ["python3.14", "/src/main.py"]
