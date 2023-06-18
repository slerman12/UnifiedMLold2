<img width="20%" src="https://github.com/slerman12/Assets/assets/9126603/32c5d597-15e1-4197-9279-a727459d2615"><br><br>

# Welcome

[//]: # (Cheat sheet)

[//]: # (Small scale &#40;horizontally below&#41;, medium scale, large scale)

[//]: # (Broad examples with links below ./Examples ./1. blablabla 2. blablabla)

## Install

```console
pip install UnifiedML
```

## Quick start

```python
from torch import nn

import ML

model = nn.Sequential(nn.Linear(3 * 32 * 32, 128),
                      nn.Linear(128, 10))

if __name__ == '__main__':
    # Launch training on CIFAR-10 according to the defaults of task "classify"
    ML.launch(Model=model, Dataset='CIFAR10', task='classify')
```

Tasks (```task=```) include ```classify```, ```regression```, ```RL```, and ```generate```.

### Command-line

Let's now run it with the command-line tool instead:

```diff
# MyApp.py
from torch import nn

model = nn.Sequential(nn.Linear(3 * 32 * 32, 128),
                      nn.Linear(128, 10))

# Command-line
+ # ML Model=MyApp.model Dataset=CIFAR10 task=classify
```

The command-line flags accept paths such as ```Model=MyApp.model``` or a custom dataset ```Dataset=Path.To.MyDataset```.

### Pure-Code example

**Run.py:**

```python
from torch import nn

import ML

model = nn.Sequential(nn.Linear(3 * 32 * 32, 128), nn.Linear(128, 10))

ML.launch(Model=model, Dataset='CIFAR10')
```

**Run it:**

```console
python Run.py
```

## Architecture shapes

UnifiedML automatically detects the shape signature of your model.

**Run.py:**

```diff
from torch import nn

import ML

class Model(nn.Module): 
+   def __init__(self, in_features, out_features):
        super().__init__()
        
        self.model = nn.Sequential(nn.Linear(in_features, 128), nn.Linear(128, out_features))

    def forward(self, x):
        return self.model(x)

ML.launch(Model=Model, Dataset='CIFAR10')
```

Inferrable signature arguments include ```in_shape```, ```out_shape```, ```in_features```, ```out_features```, ```in_channels```, ```out_channels```, ```in_dim```, ```out_dim```.

```console
python Run.py
```

## Acceleration

With ```accelerate=True```, you get:
* Memory mapping
* Adaptive RAM caching
* Truly-shared RAM parallelism
* Automatic 16-bit mixed precision
* Multi-GPU automatic detection and parallel training

```console
python Run.py accelerate=true
```

**or in Run.py:**

```python
...

ML.launch(accelerate=True)
```

For image classification, extra hard disk memory is used to store the re-formatted dataset. For RL, there's no downside.

## Hyperparams

Hyperparams can be passed in via command-line, code, recipe, or any combination thereof.

---

**Here's how to write the same program in 5 different ways:**

### 1. Purely command-line

```console
ML task=classify Dataset=MNIST Eyes=CNN +eyes.depth=5
```

Trains a 5-layer CNN classifier on MNIST.

### 2. Command line

**Run.py:**

```python
import ML
ML.launch()
```

**Run it:**

```console
python Run.py task=classify Dataset=MNIST Eyes=CNN +eyes.depth=5
```

### 3. Code

**Run.py:**
```python
import ML
ML.launch('+eyes.depth=5', task='classify', Dataset='MNIST', Eyes='CNN')
```

**Run it:**

```console
python Run.py
```

### 4. Recipe

Define recipes in a ```.yaml``` file like this one:

**Recipe.yaml:**

```yaml
defaults:
  - classify@_global_
  - _self_
Dataset: MNIST
Eyes: CNN
eyes:
  depth: 5
```

**Run it:**

```console
ML task=Recipe
```

### 5. All of the above

The order of hyperparam priority is command-line > code > recipe.


**Recipe.yaml:**

```yaml
defaults:
  - classify@_global_
  - _self_
Eyes: CNN
eyes:
  depth: 5
```

**Run.py:**
```python
import ML
from torchvision.datasets import MNIST

ML.launch(Dataset=MNIST)  # Note: Can directly pass in classes
```

**Run it:**

```console
python Run.py task=recipe 
```

---

### Syntax

1. The ```+hyperparam.``` syntax is used to modify arguments of flag ```Hyperparam```. We reserve ```Uppercase=Path.To.Class``` for the class itself and ```+lowercase.key=value``` for argument tinkering, as in ```+eyes.depth=5``` [in 1, 2, and 3](#1-purely-command-line).
2. Note: we often use "```task```" and "```recipe```" terms interchangeably.

## Example: Training a ResNet18 on CIFAR10

Define recipes in a ```.yaml``` file like this one:

**cifar_recipe.yaml:**

Then use ```task=``` to select the recipe:

```console
ML task=cifar_recipe accelerate=true
```

This recipe exactly trains CIFAR10 to 94% accuracy in 5 minutes on 1 GPU.

* ```ResNet18``` points to the architecture [here]().
* We could have also written the direct path:
```diff
+ Eyes: UnifiedML.Blocks.Architectures.Vision.ResNet18.ResNet18
```

### Plot it:

We can plot the result as follows:

```console
Plot task=cifar_recipe
```

Corresponding plots save in ```Benchmarking/Experiment-Name/Plots/```:

We can use flags like ```experiment=``` to distinguish experiments.

* Another option is to use [WandB]():

    ```console
    ML task=cifar_recipe accelerate=true wandb=true
    ```

## Recipes

### RL Recipe - Train a humanoid to walk from images, 1.2x faster than the SOTA DrQV2

Define your own recipe in a ```.yaml``` file like this one:

**humanoid_from_images.yaml:**

* ```DrQV2Agent``` points [here]().

**Train:**

```console
ML task=humanoid_from_images
```

**Generate plots:**

SOTA scores at 1.2x the speed.

**Render a video:**

### RL Recipe - Atari to human-normalized score in 1m steps

The ```-m``` flag enables sweeping over comma-separated hyperparams, in this case a standard benchmark 26 games in the Atari ALE. For more sophisticated sweep tools, check out [SweepsAndPlots]().

**Train:**

```console
ML -m experiment=ALE task=RL Env=Atari +env.game=alien,amidar,assault,asterix,bankheist,battlezone,boxing,breakout,choppercommand,crazyclimber,demonattack,freeway,frostbite,gopher,hero,jamesbond,kangaroo,krull,kungfumaster,mspacman,pong,privateeye,qbert,roadrunner,seaquest,upndown
```
* ```task=RL``` points [here](), ```Env=Atari``` points [here]().

**Generate plots:**

```console
Plot experiment=ALE
```

We can also plot it side by side with the DeepMind Control Suite RL benchmark:

**Train some tasks in the DMC suite:**

```console
ML -m experiment=DMC task=RL Env=DMC +env.task=cartpole_balance,quadruped_walk,walker_walk,cheetah_run
```

**Generate plots:**

```console
Plot experiments=[ALE,DMC]
```

### Generative Recipe - DCGAN celebrity faces in 5 minutes

**humanoid_from_images.yaml:**
* ```DCGAN``` points [here]().

**Train:**

```console
ML task=dcgan
```

[//]: # (Plots, reel)
[//]: # (caption: something .. as saved in ```Benchmarking/```.)

```task=dcgan``` refers to one of the pre-defined task recipes in [UnifiedML/Hyperparams/task](). These — like all UnifiedML recipes, search paths, and features — can be accessed from anywhere.

## More docs

<details>
<summary>
Click to expand
</summary>

## Useful flags

* ```norm=true```: enables normalization
* ```offline=true```: ...
* ```Optim=```

## When to use ```Eyes```? When to use ```Model```?

Use ```Eyes``` if your architecture only has a body, and not a head. Use ```Model``` when your architecture has a head.

```input → Eyes → Model → output```

You can combine both.

**The defaults are:**

```yaml
Eyes: Identity
Model: MLP
```

Other parts include ```Aug```, ```Pool```, ```Trunk```, and ```Discriminator```. [Each may serve different optimization purposes.]()

By organizing these parts into blocks (```encoder```, ```actor```, ```critic```), UnifiedML is able to unify them via the multi-task framework and API, even across vast domains.

* An architecture "has a head" when it can adapt to one or more of: ```out_shape```, ```out_features```, ```out_channels```, ```out_dim``` as signature arguments.

## Sequentials and direct code

Sequentials and direct code can be passed in as follows:

```console
# Sequential ViT construction
ML task=classify Dataset=MNIST Eyes=[CNN,Transformer] +eyes.1.depth=5

# End-to-end model
ML task=classify Dataset=MNIST Model=[CNN,nn.Flatten(),nn.Linear] +model.depth=5
```

Tinkering arguments can be explicitly indexed or inferred.

## Saving/loading

### Saving

Checkpoints will automatically save to ```Checkpoints/Experiment-Name/Agent/Task-Name_Seed.pt``` at the end of training.

Disable automatic saving with ```save=false```.

Save periodically with ```save_per_steps=```:

```console
# Saves periodically every 10000 steps
python Run.py save_per_steps=10000
```

### Loading

#### By exact match

```console
# Loads the agent/model that matches the current hyperparams
python Run.py load=true
```

#### Searching checkpoint paths

Let's say you have an explicit load path that is different from your current hyperparams: ```Checkpoints/MyExp/Dataset/GANAgent/MNIST_0.pt```.

There are two ways to load it:

```console
# 1. Via sufficiently-identifying string keywords (nearest match):
python Run.py load='MyExp MNIST'

# 2. Or, explicit path:
python Run.py load=Checkpoints/MyExp/Dataset/GANAgent/MNIST_0.pt
```

#### In-code

Load in-code via the same syntax:

```python
import ML

# Resume training, potentially w/ different hyperparams
agent = ML.launch(load='MyExp', experiment='MyExp', Agent='GANAgent', Dataset='MNIST')  # The launcher also returns the agent.
```

or with ```ML.load_agent(path)```:

```python
import ML

# Load 
agent = ML.load_agent('MyExp')

# Resume training, potentially w/ different hyperparams
agent = ML.launch(experiment='MyExp', Agent=agent, Dataset='MNIST')  # The launcher also returns the agent.
```

## Building an agent

We recommend using UnifiedML blocks for wrapping architectures and optimizing them with Utils.optimize.

## Building environments

## Defining datasets

### Saving/loading experience replays

An experience replay can be saved and/or loaded with the ```replay.save=true``` or ```replay.load=true``` flags, and the same analogous syntax.

By default, replays in reinforcement learning temporarily save to ```/Datasets/ReplayBuffer/Experiment-Name/Agent/Task-Name_Seed``` and are deleted at the end of training unless ```replay.save=true```.

By default, classify tasks are offline, meaning you don't have to worry about loading or saving replays. Since the dataset is static, creating/loading is non-optional and handled entirely automatically.

<details>
<summary>
Click here to learn more about replays
</summary>
<br>

<img width="25%" alt="flowchart" src="https://github.com/AGI-init/Assets/assets/92597756/15f749d8-1fcf-4075-bc0d-99fc98f0429d"><br><br>

**In UnifiedML, replays are an efficient accelerated storage format for data that support both static and dynamic (changing/growing) datasets.**

You can disable the use of replays with ```stream=true```, which just sends data to the Agent directly from the environment. In RL, this is equivalent to on-policy training. In classification, it means you'll just directly use the Pytorch Dataset, without all the fancy replay features and accelerations.

Replays are recommended for RL because on-policy algorithmic support is currently limited.

~

</details>

## Example publication

## Example generalist agent

</details>

---

The code in this repo was programmed and conceived by **Sam Lerman** under the support of PhD advisor [Dr. Chenliang Xu](), project PI lead [Dr. Niaz Abdolrahim](), and funding from the NSF Materials Science something-something grant [#]().

[Sam Lerman]() will graduate in 2023 and needs your support.

Please [sponsor]() this work if you find it useful.

[//]: # (**We need funding.**)

[//]: # (<br>Please [Sponsor]&#40;https://github.com/sponsors/AGI-init&#41; us.)

#

[MIT license Included.](MIT_LICENSE)