# My Coding Buddy

This Project is designed to keep you company while you're coding. It is not a software-only project, and specific hardware is required in order to run the code in this repository.

## Install

First, clone the repository using the `git` CLI-Tool:

```bash
git clone https://github.com/FujiwaraChoki/buddy
cd buddy
```

Then, install all the necessary requirements using `pip`. Make sure you have also activated your Virtual Environment (`venv`-Tool).

```bash
python -m venv venv

# WINDOWS
.\venv\Scripts\activate

# UNIX
source ./venv/bin/activate

pip install -r requirements.txt
```

Last but not least, check your system in order to determine whether `ollama` is installed, using the following command:

```
ollama --version
```

If you don't have it installed, download it from [here](https://ollama.com/).

## ToDo

- [x] Start with modular architecture
- [x] Record Speech from microphone
- [x] Make request to local OLLAMA API
