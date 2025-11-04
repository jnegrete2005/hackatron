Tron AI Environment
======================

This repository contains a simple Tron AI environment where two players can compete against each other. Each player is controlled by a bot that decides its moves based on the current game state.

# Getting Started
----------------
Clone the repo:

```bash
git clone git@github.com:jnegrete2005/hackatron.git
cd tron-ai-environment
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Set the `PYTHONPATH` environment variable to include the `src` directory:

```bash
export PYTHONPATH=$(pwd)/src:$PYTHONPATH
```

Run the main script to start a game:

```bash
python src/main.py
```