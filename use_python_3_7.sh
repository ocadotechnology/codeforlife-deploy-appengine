#!/bin/bash -ex

rm  -rf ~/.pyenv

curl https://pyenv.run | bash

# Install OpenSSL
wget https://www.openssl.org/source/openssl-1.1.1f.tar.gz
tar xzvf openssl-1.1.1f.tar.gz
cd openssl-1.1.0f
./Configure
# ./config -Wl,--enable-new-dtags,-rpath,'$(LIBRPATH)'
make
sudo make install

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

eval "$(pyenv init -)"

pyenv install 3.7.7

pyenv global 3.7.7
