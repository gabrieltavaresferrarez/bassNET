#import libs
import os
from .unet import unet
import torch
import torchaudio
import sys
from .utils import to_mono, to_spec, complex_to_real_imag, resize_time_axis_in_spec, real_imag_to_complex, to_wave
import zipfile
import shutil

sys.dont_write_bytecode = True

# CONSTANTS
str_device = 'cuda' if torch.cuda.is_available() else 'cpu'
str_fileWeights = 'weights.pth'



listFuction_preProcess = [to_mono, to_spec, complex_to_real_imag, resize_time_axis_in_spec]
listFuction_postProcess = [real_imag_to_complex, to_wave]


def get_weights_file():
  str_pathModule = os.path.dirname(__file__)
  list_filesModule = os.listdir(str_pathModule)

  if str_fileWeights  not in list_filesModule: # check if file is in module folder  
    raise FileExistsError('Weights file dont exists. Looking for {} or {} in {}'.format(str_fileWeights, str_pathModule))

  str_pathWeights = os.path.join(str_pathModule, str_fileWeights)
  return str_pathWeights


def preProcess(tensor_audio, device=str_device): 
  tensor_audio.to(device)
  tensor_processed = tensor_audio
  for function in listFuction_preProcess:
    tensor_processed = function(tensor_processed, device = device)
  tensor_processed = torch.unsqueeze(tensor_processed, dim=0) # add audio to batch
  return tensor_processed

def postProcess(tensor_audio, device=str_device): 
  tensor_audio.to(device)
  tensor_processed = tensor_audio[0] # remove do batch de saida
  for function in listFuction_postProcess:
    tensor_processed = function(tensor_processed, device = device)
  return tensor_processed

def load_audio(str_pathAudio):
  if '.mp3' in str_pathAudio:
    raise ValueError('Arquivo .mp3 inválido. Apenas arquivo .wav')
  else:
    return torchaudio.load(str_pathAudio)

def save_audio(tensor_audio:torch.Tensor, str_pathOut:str, normalize:bool=False, sample_rate:int=44_100):
  tensor_audio = tensor_audio if len(tensor_audio.size()) == 2 else tensor_audio.unsqueeze(dim=0) # convert to correct audio size (2 Dims)
  if normalize:
    tensor_max = torch.max(abs(tensor_audio.max()),abs(tensor_audio.min()))
    tensor_audio = tensor_audio/tensor_max
  torchaudio.save(str_pathOut, tensor_audio.to('cpu'), sample_rate)

def model():
  model = unet().to(str_device)
  model.load_state_dict(torch.load(get_weights_file(), map_location=str_device))
  model.eval()
  return model