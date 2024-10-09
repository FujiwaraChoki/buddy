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

Run the necessary models:

```bash
ollama run llava:13b # Vision Model
ollama run llama3.1 # Text Generation (LLM) Model
```

Next, you'll need to set your project through the command line tool.

```bash
python3 src/set_project.py [PROJECT_PATH]
```

`[PROJECT_PATH]` is the path to your project. You can also provide a relative path, as it will be converted into an absolute one in all cases.

## ToDo

- [x] Start with modular architecture
- [x] Record Speech from microphone
- [x] Make request to local OLLAMA API
- [x] Put answers in a JSON response
  - [x] Parse and performing the specific action with defined parameters

## How it works

First, the user tells his concern about his code.

Then, buddy goes through the following steps:

1. Let user set current project through CLI
2. Record voice
3. Split into action
   - Possible Actions: [`git`, `files`, `run`, `test`, `install`, `help`, `refactor`, `debug`, `other`]
4. Calls the actions `call` method (found in [actions](/actions) folder)
5. Prints Result/says it out loud.

## Contributing

PR's are welcome. :)
