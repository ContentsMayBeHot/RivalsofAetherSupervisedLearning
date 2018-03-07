
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

After setting up SerpentAI, clone the [game plugin](https://github.com/ContentsMayBeHot/SerpentRivalsofAetherGamePlugin) and [game agent plugin](https://github.com/ContentsMayBeHot/SerpentRivalsofAetherGameAgentPlugin) to _/.../SerpentAI/plugins/_. This should result in the following directory tree:
```
├── SerpentAI
│   ├── config
│   ├── datasets
│   └── plugins
│       ├── SerpentRivalsofAetherGameAgentPlugin
│       └── SerpentRivalsofAetherGamePlugin
```

_SerpentRivalsofAetherGameAgentPlugin_ contains submodules, so be sure to open it in Git Bash (or your preferred equivalent) and run **git submodule update --init --recursive**. In the future, you can update the submodule to the latest commit by entering it in Git Bash and running **git pull remote master**.

Next, you will need to open the following file in a text editor: _/.../SerpentAI/plugins/SerpentRivalsofAetherGameAgentPlugin/files/helpers/roa.ini_. Then, add the following lines:

```
[RivalsofAether]
PathToReplays = /.../users/[username]/AppData/Local/RivalsofAether/replays/
Version = x.x.x
```

Substitute the path given above with the path to your game's replays folder. For example, my replays folder is located at _C:\Users\matth\AppData\Local\RivalsofAether\replays_. You will also want to replace "x.x.x" with the installed game version, e.g. "1.0.2".

<h2>Usage</h2>

<h3>Preparing your replay files</h3>

Move all of your _roa_ files to the game's replays folder. Next, run **python /plugins/SerpentRivalsofAetherGameAgentPlugin/files/helpers/manager/replaymanager.py** to automatically move your replay files into folders corresponding with their respective game versions. This will result in a directory tree that looks something like this:

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

"00_15_07" refers to game version 0.15.7, "01_02_01" to 1.2.1, and so on. The frame collector agent will use the version string you entered in roa.ini to identify the correct game version folder. For example, if you are running _Rivals of Aether_ version 1.0.2, then you should have written "1.0.2" in roa.ini. This will tell replaymanager.py to look for a folder called "01_00_02".

<h3>Collecting frames</h3>

Launch Anaconda Prompt, activate the project environment, navigate to _/.../SerpentAI/_, and run the following commands: 1) **serpent activate SerpentRivalsofAetherGamePlugin**, and 2) **serpent activate SerpentRivalsofAetherGameAgentPlugin**. You can also run **serpent plugins** to check available and activated plugins.

To collect frames effectively, we will need to override the game frame limiter setting for our game agent. Open _/.../SerpentAI/config/config.plugins.yml_ in a text editor and update the FPS value for _SerpentRivalsofAetherGameAgentPlugin_. We found that 10 FPS offers a decent balance.

Make sure Steam is running and _Rivals of Aether_ is installed. We recommend that you also turn off the Steam overlay so that inventory and friend notifications don't appear on the screen. Next, run **serpent launch RivalsofAether**. Once the game has finished loading the main menu, go to the replays menu by going to extras -> replays. Finally, run **serpent play RivalsofAether SerpentRivalsofAetherGameAgent COLLECT** in Anaconda Prompt. The game agent will begin collecting game frames and parsed player input data and dumping them as binary files located in _/.../replays/frames_ and _/.../replays/labels_, respectively. A directory structure similar to this will develop:

```
├── replays
│   ├── 00_15_07
│   ...
│   ├── 01_02_02
│   └── frames
│   │   ├── 2017-11-07-234316128959
│   │   ├── ...
│   │   └── 2017-11-07-234241093349
│   │       ├── 0.npy
│   │       ├── ...
│   │       └── 4475.npy
│   └── labels
│       ├── 2017-11-07-234316128959
│       ├── ...
│       └── 2017-11-07-234241093349
│           ├── roa_1.npy
│           └── roa_2.npy
```

Avoid taking focus away from the game's window while the frame collector agent is running. If you need to stop the agent, bring Anaconda Prompt into focus. Doing so will automatically pause the agent. Next, press CTRL+C to terminate the agent. If a replay was in progress, then be sure to delete the corresponding frames and labels folders.

Please be aware that the collector agent dumps about 1 GB of frame buffer data for every 4 minutes of playback. During our  initial experiments we processed just over 330 replay files, which resulted in more 40 GB of frame buffer data. If you are concerned about space requirements, you can set up a symbolic link from _/.../replays/frames_ to a different storage device with a higher capacity.
