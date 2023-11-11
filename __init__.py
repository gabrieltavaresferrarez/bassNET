#import libs
import os
from .unet import unet
import torch
import torchaudio
import sys
from .utils import to_mono, to_spec, complex_to_real_imag, resize_time_axis_in_spec, real_imag_to_complex, to_wave

sys.dont_write_bytecode = True

str_device = 'cuda' if torch.cuda.is_available() else 'cpu'

listFuction_preProcess = [to_mono, to_spec, complex_to_real_imag, resize_time_axis_in_spec]
listFuction_postProcess = [real_imag_to_complex, to_wave]

str_pathModule = os.path.dirname(__file__)
str_pathWeights = os.path.join(str_pathModule, 'model_epoch_00002.pth')

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

model = unet().to(str_device)
model.load_state_dict(torch.load(str_pathWeights, map_location=str_device))
model.eval()