#!/bin/bash


curl -s https://api.github.com/repos/gitleaks/gitleaks/releases/latest \
| grep "browser_download_url.*linux_x64.tar.gz" \
| cut -d '"' -f 4 \
| wget -qi -
ls gitleaks_*_linux_x64.tar.gz | xargs tar -xvzf
sudo mv gitleaks /usr/local/bin/


