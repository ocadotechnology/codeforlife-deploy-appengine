#!/bin/bash -ex

git clone https://github.com/pyenv/pyenv.git ~/.pyenv

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

if command -v pyenv 1>/dev/null 2>&1; then
  eval "$(pyenv init -)"
fi

pyenv install 3.7.7

pyenv global 3.7.7
