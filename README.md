## Python

```bash
$ python_ver=3.9.15 \
 && proj_ve_name=midi-controller-2-buttons-v1 \
 && pyenv install $python_ver || true \
 && pyenv virtualenv $python_ver $proj_ve_name || true \
 && pyenv local $proj_ve_name \
 && pyenv activate $proj_ve_name \
 && poetry config --local virtualenvs.create false \
 && poetry install
```

## Pycharm

Install plugin MicroPython
Go settings: Editor -> Inspections -> Python -> Code is incompatible with specific Python versions
Enable the options and set 3.6.


## MPY-Cross

```bash
$ boardman get-mpy-compiler
```
