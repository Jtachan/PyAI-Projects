# AI plays Flappy Bird

In this project, an evolutive algorithm was introduced to learn how to play _Flappy Bird_.
After this section, a more in-depth explanation is given for it.

The game starts with a generation of 20 birds, each one composed by a neural networks to predict if it has to jump or not.
Once all the birds of a generation die, 20 new birds are defined considering the best ones from previous generation.

When a generation finds a bird which can estimate when to jump with a good accuracy, this bird will have the capacity to play the game forever.

![flappy_nn](imgs/Flappy_bird.gif)

[See the code.](../src/flappy_bird)

The algorithm can be installed and run by anyone. To do so, only two steps are needed:

1. Install the requirements:

```shell
pip install -r src/flappy_bird/requirements.txt
```

2. Launch the code:

```commandline
python src/flappy_bird/neat_ai.py
```

Playing the game with the computer is not supported by the code.

-----
## Understanding the algorithm

The algorithm defines multiple candidates per generation. 
This is possible thanks to the [NEAT-Python](https://neat-python.readthedocs.io/en/latest/index.html) package, which generates neural networks as candidates to evolve.

The steps to understand and resolve how to train the network to play the game are few, but required:

### The game: Flappy Bird

The game seems quite simple: the bird advances going through pipes. Or does it?
Sometimes, our human perception makes us believe things that are not. For instance, the bird does not advance, but remains still at the same horizontal position.

Thus, the first step if to fully understand the game. These are the key points of it:

- The bird remains still at the horizontal position.
- The bird falls, but it can "jump" to update its vertical position.
- Pipes are moving from right to left at random heights, but all with the same gap in between.
- If the bird touches a pipe or falls to the floor, it is game over.
- The bird can only pass the pipes through the gap.

The last point might seem redundant.
However, if the vertical position of the bird is not limited on the top, the most effective way to win the game is to always jump and pass all the pipes through the top.
Consider that, just because it cannot be seen, pipes are not of infinite size.

### Defining the network

Now the rules of the game are understood, next step is to prepare the MPL (multi perceptron layer) network.
All this information is defined in a configuration file, needed to be parsed to the NEAT algorithm.

#### Inputs and outputs

The input vector for the network can be of any size, with as many variables as possible.
There is a minimum number to be given too, otherwise the MLP won't know what to do.

The inputs are what the MLP can see. If something is not given, this could be calculated, but only if enough information is provided.
For example, imagine playing the game without knowing where the bird is. For sure, in this case no one would reach far enough.

Thus, the **inputs** for the network are:
- The Y position of the bird.
- The top-left corner of the next not-passes lower pipe.
- The bottom-left corner of the next not-passes top pipe.

While it's possible to discuss if other inputs actually could be needed, the main idea for these inputs is for the MLP to learn how to maintain the bird at the needed height until the pipe is passed.

The **output** of the network is quite easy to guess:
- Whether the bird should jump or not.

So the known structure of our network is 3 inputs and 1 output.

#### Type of network

After considering what the inputs are, some networks are discarded as candidates to solve this problem. For example, a 2D convolutional network would not work here.

Other characteristics that define the type of network to use are the types of the input values, as well as the output value, and considering if the network needs of memory (from past instants).

This is quite a simple case, which can be solved using a fully-connected multi layer perception network.

#### Activation function

The activation function define the output of a neuron given a certain input value.
While there are many functions, the one I chose to continue with is the **sigmoid**.

<img alt="sigmoid" src="imgs/sigmoid.png" width="300"/>

The important features of the sigmoid for this problem are:
- It provides a float value in the range [0.0, 1.0]
- It is centered at 0, which value provides an output of 0.5

Considering these features, I programmed the network to give the "jump" order when the output is higher than 0.5.

#### Reward and penalization

For the algorithm to know it is doing something good, a system of reward and penalization has to be set.
Here is why learning about the game's rules are so important, as we won't be able to control the behavior of the network, so it must understand what is the best strategy to play.

The rewards are:
- +0.1 for every second the bird stays alive.
- +5 for every passed pipe.

And the consequences are:
- -1 if the game is over.

#### Number of hidden layers

With all configured, there seems only one last question to do: set the number of hidden layers.
As one of my AI professors would say: "This answer must appear in at least one of the stages working with deep learning solutions".
And the specified answer is: **we don't know**.

It sounds like a very bad answer to give, but it is actually the correct one.
The whole goal is not to teach the network how to play, but just to show it enough rules, so it learns by itself how to play.

A feature of the NEAT algorithm is that it modifies the networks by adding and/or removing nodes. 
If the code sets a checkpoint to save the network weights, then these values could be known, but we are not the ones to set them.

## Play with it

Not with the game, I did not enable any button for a user to play. 
But feel free to modify my network configuration and see how the whole behavior is affected. 
