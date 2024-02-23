# AI plays Flappy Bird

In this project, an evolutive algorithm was introduced to learn how to play _Flappy Bird_.

The game starts with a generation of 20 birds, each one composed by a neural networks to predict if it has to jump or not.
Once all the birds of a generation die, 20 new birds are defined considering the best ones from previous generation.

When a generation finds a bird which can estimate when to jump with a good accuracy, this bird will have the capacity to play the game forever.

![flappy_nn](imgs/Flappy_bird.gif)

## Setup and run

1. Install the requirements:

```shell
pip install -r src/flappy_bird/requirements.txt
```

2. Launch the code:

```commandline
python src/flappy_bird/neat_ai.py
```

Playing the game with the computer is not supported by the code.
