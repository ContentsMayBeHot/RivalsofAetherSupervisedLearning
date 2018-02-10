
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

Also, you will need to add the following to _{path to SerpentAI}\plugins\SerpentRivalsofAetherGameAgentPlugin\files\helpers\roa.ini_:

```
[RivalsofAether]
PathToReplays = {path to your replays folder}
```

You should be able to find your replays folder at the following location: _{path to your user folder}\AppData\Local\RivalsofAether\replays_

<h2>Usage</h2>

<h3>Preparing your dataset</h3>

Place all of your replay files inside of your replays folder; this is the the same folder that the game uses and that you provided a path to in the roa.ini file.
