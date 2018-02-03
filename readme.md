
<h1>Capstone Project: Supervised Learning in Rivals of Aether </h1>

<h2>Setup</h2>

<h3>Dependences</h3>

<h4>Required</h4>

- Python 3
- Conda
- Keras
- SerpentAI
- Rivals of Aether

<h4>Recommended</h4>

- TensorFlow-GPU
- Anaconda Distribution
  
<h3>Instructions</h3>

Install all dependencies listed above. Please refer to their respective installation guides for your platform.

After setting up SerpentAI, it is recommended that you use the mklink command create a symbolic link from {path to SerpentAI}\plugins to {path to repository}\plugins; this will allow you to keep the plugins up to date without having to manually copy any files.

Also, you will need to add the following to {path to repository}\scripts\roa.ini:

```
[RivalsofAether]
PathToReplays = {path to your replays folder}
```

You should be able to find your replays folder at the following location: C:\Users\{your user name}\AppData\Local\RivalsofAether\replays

<h2>Usage</h2>

<h3>Dataset Management</h3>

Place all of your replay files inside of your replays folder; this is the the same folder that the game uses and that you provided a path to in the roa.ini file.

Next, run the version sorter program in the scripts folder of the repository. This will result in all of your replays being moved to subdirectories named after game versions.
