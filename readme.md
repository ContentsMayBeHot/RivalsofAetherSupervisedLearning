
<h1>Capstone Project: Supervised Learning in Rivals of Aether </h1>

<h2>Setup</h2>

<h3>Dependencies</h3>

<h4>Required</h4>

- [Python 3 with Conda/Miniconda](https://conda.io/miniconda.html)
- [TensorFlow](https://www.tensorflow.org/install/install_windows#installing_with_anaconda)
- [Keras](https://keras.io/#installation)
- [SerpentAI](https://github.com/SerpentAI/SerpentAI/wiki/Windows-Installation-Guide)
- [Rivals of Aether](http://www.rivalsofaether.com/)

<h4>Recommended</h4>

- [TensorFlow-GPU](https://www.tensorflow.org/install/install_windows#requirements_to_run_tensorflow_with_gpu_support)
  - [CUDA Toolkit 8.0](http://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/)
  - [cuDNN 6.0](https://developer.nvidia.com/cudnn)
  - [Latest NVIDIA graphics driver](http://www.nvidia.com/Download/index.aspx)
- [Anaconda Distribution](https://www.anaconda.com/download/)

The project is currently only supported on Windows 10; this may change if the game receives a native Linux port.
  
<h3>Instructions</h3>

Install all dependencies listed above. Please refer to their respective installation guides for your platform.

Please note that you must use Pip to install SerpentAI. For all other Python packages we recommend using Conda. Also, some of the guides linked above will ask you to create a conda environment; be sure to create only **one** environment for all of this project's dependencies.

After setting up SerpentAI, clone the [game plugin](https://github.com/ContentsMayBeHot/SerpentRivalsofAetherGamePlugin) and [game agent plugin](https://github.com/ContentsMayBeHot/SerpentRivalsofAetherGameAgentPlugin) to _{path to SerpentAI folder}/plugins_. This should result in the following directory tree:
```
├── SerpentAI
│   ├── config
│   ├── datasets
│   └── plugins
│       ├── SerpentRivalsofAetherGameAgentPlugin
│       └── SerpentRivalsofAetherGamePlugin
```

_SerpentRivalsofAetherGameAgentPlugin_ contains a submodule, so be sure to open it in Git Bash (or your preferred equivalent) and run **git submodule update --init --recursive**. In the future, you can update the submodule to the latest commit by entering it in Git Bash and running **git pull remote master**.

Next, you will need to add the following to _{path to SerpentAI}\plugins\SerpentRivalsofAetherGameAgentPlugin\files\helpers\roa.ini_:

```
[RivalsofAether]
PathToReplays = {path to your replays folder}
Version = {game version you want to use, e.g. 1.2.2}
```

You should be able to find the game's replays folder at _{path to your user folder}\AppData\Local\RivalsofAether\replays_

<h2>Usage</h2>

<h3>Preparing your replay files</h3>

Place all of your replay files inside of the game's folder. Next, run **python {path to SerpentAI}\plugins\SerpentRivalsofAetherGameAgentPlugin\files\helpers\replaymanager.py** to automatically move your replay files into folders corresponding with their respective game versions. This will result in a directory tree that looks something like this:

```
├── replays
│   ├── 00_15_07
│   ├── 00_15_08
│   ├── 00_15_09
│   ├── 00_15_10
│   ├── 00_15_11
│   ├── 01_00_02
│   ├── 01_00_03
│   ├── 01_00_05
│   ├── 01_01_02
│   ├── 01_02_01
│   └── 01_02_02
```

"00_15_07" refers to game version 0.15.7, "01_02_01" to 1.2.1, and so on.

<h3>Collecting frames</h3>

Launch Anaconda Prompt, activate the project environment, change to the SerpentAI setup folder, and run the following commands: 1) **serpent activate SerpentRivalsofAetherGamePlugin**, and 2) **serpent activate SerpentRivalsofAetherGameAgentPlugin**. You can also run **serpent plugins** to check available and activated plugins.

To collect frames effectively we will need to override the game frame limiter setting for our game agent. Open _{path to SerpentAI setup folder}/config/config.plugins.yml and update the FPS value for SerpentRivalsofAetherGameAgentPlugin_.

Make sure Steam is running and _Rivals of Aether_ is installed. Finally, run **serpent launch RivalsofAether** and then run **serpent play RivalsofAether SerpentRivalsofAetherGameAgent COLLECT**. The game agent will begin collecting game frames and dumping them into binary files located in replays\frames. A directory structure like this will develop:

```
├── replays
│   ├── 00_15_07
│   ...
│   ├── 01_02_02
│   └── frames
│       └── 2017-11-07-234241093349
```

The new folders appearing under _replays\frames_ are each associated with a different replay file. The folder shown above _2017-11-07-234241093349_, is associated with a replay file called _2017-11-07-234241093349.roa_.
