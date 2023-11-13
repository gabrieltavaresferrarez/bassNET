# bassNET

This is the repository wich contains the segmentation network designed and trained to segment the bass audio from a music audio.

## Dependencies

The external modules needed in this project are:

* torch
* torhcaudio
* pandas
* cv2
* numpy

## The model

This is a U-Net model trained to segment audio. To do so, tha audio needs to be reshaped to it`s spectogram. Then the model works as a filter mask wich filter every sound that is not a bass and outputs a spectogram

## Module API

**This module has a few functional methods**

First import the module

```
import bassNET 
```

Instanteate the neural network module

```
model = bassNET.model()
```

By default, the neural network is loaded in the computer GPU (if it is available) to increase segmentation speed. If we want to use it in CPU, I recommend to use

```
model = model.to('cpu')
```

The model, processes torch tensors. To facilitate this process, there is a load_audio function in this module

```
str_pathAudio = 'song.wav'
tensor_audio, int_sr = bassNET.load_audio(str_pathAudio)
```

With the audio loaded in the scpoe, we need to preprocess this tensor before inputing it into the netowork. This process do the following process:

- convert the audio from stereo to mono
- makes a spectogram of the audio
- converts the 2D tensor of complex number to a 3D tensor of real and imag dimensions
- resize the time to fit the spectogram

```
tensor_audioProcessed = bassNET.preProcess(tensor_audio, device='cpu')
```

After that, we may load the audio into the model

```
tensor_out = model(tensor_audioProcessed)
```

Just like the input, the network outputs an spectogram witch needs to be converted to audio again.

```
tensor_audioOut = bassNET.postProcess(tensor_out)
```

The `tensor_audioOut` variable contains an audio Tensor that may be displayed using the same signal rate as loaded in `int_sr`
