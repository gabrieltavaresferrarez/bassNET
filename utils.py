import os
import torch
import torchaudio
from _myPath import Path
device = 'cuda' if torch.cuda.is_available() else 'cpu'


# Create directory
def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# convert to spectogram with complex type
    # obs: n_fft+1 must be multiple of 16 -> ex n_fft=1023 correct, because (1023+1)%16 = 0
                                            #   n_fft=1024 incorrect, because (1024+1)%16 = 1
def to_spec(tensor_audio, device = device):
    transform = torchaudio.transforms.Spectrogram(n_fft = 1023, power = None).to(device)
    return transform(tensor_audio)
def to_wave(tensor_spec, device = device):
    transform = torchaudio.transforms.InverseSpectrogram(n_fft=1023).to(device)
    return transform(tensor_spec)


# make audio stereo to mono
def to_mono(tensor_audio, device=device):
    if tensor_audio.shape[0] != 1: # audio não mono
        tensor_mono = torch.mean(tensor_audio, dim=0)
    else:
        tensor_mono = tensor_audio[0]
    return tensor_mono.to(device)


#transforms a spectogram with 2d complex type tensor to a 3d (2 chanels of float -> real and imag) float time
def complex_to_real_imag(tensor_complex, device=device):
    return torch.stack((tensor_complex.real, tensor_complex.imag), dim=0).to(device)

def real_imag_to_complex(tensor_real_imag, device=device):
    return torch.complex(tensor_real_imag[0], tensor_real_imag[1]).to(device)

#transforms a spectogram with 2d complex type tensor to a 3d (2 chanels of float -> abs and angle) float time
def complex_to_abs_angle(tensor_complex, device=device):
    return torch.stack((tensor_complex.abs(), tensor_complex.angle()), dim=0).to(device)

def abs_angle_to_complex(tensor_abs_angle, device=device):
    tensor_real = tensor_abs_angle[0]*torch.cos(tensor_abs_angle[1])
    tensor_imag = tensor_abs_angle[0]*torch.sin(tensor_abs_angle[1])
    return torch.complex(tensor_real, tensor_imag).to(device)




#add zero columns to spectogram to be multiple by a number
def resize_time_axis_in_spec(spectogram, multiple_by=16, device=device):
    size = spectogram.size()
    device_tensor = spectogram.device
    time=size[-1]
    n_fft = size[-2]
    if (time%multiple_by) == 0:
        return spectogram
    else:
        time_to_add = multiple_by - (time%multiple_by)
    zeros_size = torch.cat( (torch.tensor(size)[:-1], torch.tensor([time_to_add])), dim=0)
    zeros = torch.zeros(zeros_size.tolist()).to(device_tensor)
    spectogram = torch.cat([spectogram, zeros], dim = -1)
    return spectogram.to(device)

def sec2min(float_sec):
    int_hours = int(float_sec//3600)
    int_min = int(float_sec//60)%60
    int_sec = int(float_sec)%60
    if int_hours > 0:
        string_time = f'{int_hours}h {int_min}min {int_sec}s'
    elif int_min > 0:
        string_time = f'{int_min}min {int_sec}s'
    else:
        string_time = f'{int_sec}s'
    return string_time

SECS = 44_100


# export audio 
def save_audio(tensor_audio, path_file, normalize:bool=False, sample_rate:int=44_100):
  tensor_audio = tensor_audio if len(tensor_audio.size()) == 2 else tensor_audio.unsqueeze(dim=0) # convert correct audio size (2 Dims)
  if type(path_file) == str:
    path_file = Path(path_file)
  if normalize:
    tensor_max = torch.max(abs(tensor_audio.max()),abs(tensor_audio.min()))
    tensor_audio = tensor_audio/tensor_max
  torchaudio.save(path_file.path, tensor_audio.to('cpu'), sample_rate)