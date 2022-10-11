## Python

```bash
python_ver=3.9.13 \
 && proj_ve_name=midi-controller-2-buttons-v1 \
 && pyenv install $python_ver \
 && pyenv virtualenv $python_ver $proj_ve_name \
 && pyenv local $proj_ve_name \
 && poetry install
```

## Pycharm

Install plugin MicroPython
Go settings: Editor -> Inspections -> Python -> Code is incompatible with specific Python versions
Enable the options and set 3.6.


## MPY-Cross

```bash
micropython_ver=1.19.1 \
 && curl -L -o micropython-$micropython_ver.zip "https://github.com/micropython/micropython/archive/refs/tags/v$micropython_ver.zip" \
 && unzip micropython-$micropython_ver.zip \
 && rm -f micropython-$micropython_ver.zip \
 && cd micropython-$micropython_ver/mpy-cross \
 && make \
 && cd ../..
```
