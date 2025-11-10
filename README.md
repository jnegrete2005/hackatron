# ⚡ HackaTron Server

Welcome to **HackaTron** — an AI-powered Tron-style arena where bots battle it out in real time!  
This repository contains the **server** that runs the matches between two bots.  
Each bot decides its next move based on the current game state sent by the server.

---

## 🚀 Getting Started

### 1️⃣ Clone the repo:

```bash
git clone git@github.com:jnegrete2005/hackatron.git
cd hackatron
```

### 2️⃣ Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up your environment:

Make sure Python can find the source code:

```bash
# On macOS / Linux
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# On Windows (Command Prompt)
set PYTHONPATH=%cd%\src;%PYTHONPATH%
```

---

## 🕹️ Running a Local Game

To run a game, you must provide the server with the Docker images for the two competing bots.

The `main.py` script accepts two arguments: `--bot1` and `--bot2`, which are the Docker image names of the bots. By default, it uses the [random bot image](https://hub.docker.com/r/jokkess/hackatron-random-bot) from Docker Hub.

To run a local game between your bot and the random bot, use the following command:

```bash
python3 src/main.py --bot1 <YOUR_DOCKER_IMAGE> --bot2 jokkess/hackatron-random-bot
```

Replace `<YOUR_DOCKER_IMAGE>` with the name of your bot's Docker image.

Or if you want, you can test your bot against itself:

```bash
python3 src/main.py --bot1 <YOUR_DOCKER_IMAGE> --bot2 <YOUR_DOCKER_IMAGE>
```

The server will start a game. To continue to the next game tick, press any key on your keyboard.  
However, if you want to run the game automatically without waiting for key presses, you can use the `--auto` flag:

```bash
python3 src/main.py --bot1 <YOUR_DOCKER_IMAGE> --auto
```

---

## 🏆 Good luck, and may the best bot win!

Made with ❤️ by the HackaTron Team
