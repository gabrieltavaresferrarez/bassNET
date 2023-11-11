import torchaudio
import torch
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np
import pandas as pd



# API DO TIPO

# waveForm.generateImage(audio, notesFile, pathImage)

'''posicao -> (x1,y1, x2,y2)
cores -> (B, G, R)
opacidade -> float [0.0:1.0]'''
def draw_rectangle(imagem, posicao, cor_preenchimento, cor_borda, espessura_borda, opacidade):
  imagem_retangulo = np.copy(imagem)
  cv2.rectangle(imagem_retangulo, (posicao[0], posicao[1]), (posicao[2], posicao[3]), cor_preenchimento, -1)  # -1 preenche o retângulo
  cv2.rectangle(imagem_retangulo, (posicao[0], posicao[1]), (posicao[2], posicao[3]), cor_borda, espessura_borda)
  
  imagem_com_retangulo = cv2.addWeighted(imagem, 1 - opacidade, imagem_retangulo, opacidade, 0)
  return imagem_com_retangulo


dict_notasCores = {
  'A' : (66, 209, 245),
  'A#': (66, 141, 245),
  'B' : (66, 90, 245),
  'C' : (105, 66, 245),
  'C#': (197, 66, 245),
  'D' : (245, 66, 179),
  'D#': (245, 66, 75),
  'E' : (245, 135, 66),
  'F' : (245, 203, 66),
  'F#': (239, 245, 66),
  'G' : (156, 245, 66),
  'G#': (66, 245, 224),
}

'''generateImage
Args:
  - str_pathAudio : path to audio file
  - str_pathNotes : path to csv of notes
  - str_pathImage : path to image output
Keywords
  - pixelsPerSecond : number of pixels per second in image waveform
  - heightImage : height of image
'''
def generateImage(str_pathAudio:str, str_pathNotes:str, str_pathImage:str, pixelsPerSecond:int = 100, heightImage:int = 100):
  # verificação de argumentos 
  if '.png' not in str_pathImage:
    raise ValueError('Imagem deve ser .png')
  if '.wav' not in str_pathAudio:
    raise ValueError('Audio deve ser .wav')
  
  # parametros
  int_pixelsPerSecond = pixelsPerSecond
  str_pathModule = os.path.dirname(__file__)
  str_imagemTemp = os.path.join(str_pathModule, 'waveform_temp.png')
  int_heightImage = heightImage

  # le audio  --------------------------------------------------------------------
  tensor_audio, sr = torchaudio.load(str_pathAudio)
  int_numMiliSeconds = tensor_audio.shape[1]*1000//sr
  int_numMiliSeconds -= int_numMiliSeconds%100 # converte para um numero redondo de milisegundo 
  tensor_audio = tensor_audio[0][0:int_numMiliSeconds//1000*sr] #converte o audio para pegar o numero certo de amostras

  # parametros da imagem
  int_width = int_numMiliSeconds//1000*int_pixelsPerSecond

  # reduz o número de pontos para desenhar
  list_range = torch.linspace(0, tensor_audio.shape[0]-1, 1000*10, dtype=int).tolist()
  tensor_audioReduced = tensor_audio[list_range]

  # gera waveform  --------------------------------------------------------------------
  int_dpi = 100
  fig, ax = plt.subplots(figsize=(int_width / int_dpi, int_heightImage / int_dpi))
  plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
  ax.set_xlim(0, len(tensor_audioReduced)-1)
  ax.set_ylim(-1, 1)
  ax.plot(tensor_audioReduced)

  fig.savefig(str_imagemTemp, dpi=int_dpi) 

  # le notas  --------------------------------------------------------------------
  df_notas = pd.read_csv(str_pathNotes, sep=';', header=None, names=['nota', 'start_ms', 'end_ms'])
  df_notas['start_ms'] = df_notas['start_ms'].apply(lambda x: int(float(x)*1000))
  df_notas['end_ms'] = df_notas['end_ms'].apply(lambda x: int(float(x)*1000))
  df_notas['nota'] = df_notas['nota'].apply(lambda x: x.strip().replace('s', '#')[:-1])
  df_notas

  # desenha notas  --------------------------------------------------------------------
  image_waveform = cv2.imread(str_imagemTemp)
  int_offSetBordasVertical = 5
  int_alturaQuadrados = image_waveform.shape[0] - 2*int_offSetBordasVertical

  for _, line_nota in df_notas.iterrows():
    str_nota = line_nota['nota']
    int_xStart = int(line_nota['start_ms'])*10//int_pixelsPerSecond
    int_xEnd = int(line_nota['end_ms'])*10//int_pixelsPerSecond

    posicao = (int_xStart, int_offSetBordasVertical, int_xEnd , int_alturaQuadrados)

    cor_preenchimento = dict_notasCores[str_nota]
    cor_borda= (0,0,0)
    espessura_borda = 2
    opacidade = 0.5
    
    image_waveform = draw_rectangle(image_waveform, posicao, cor_preenchimento, cor_borda, espessura_borda, opacidade)

    x, y = posicao[0] + 10, posicao[1] + 20
    fonte = cv2.FONT_HERSHEY_SIMPLEX 
    width_font = 1
    image_waveform = cv2.putText(image_waveform, str_nota, (x, y), fonte, 0.5, (0,0,0), width_font)

  cv2.imwrite(str_pathImage, image_waveform)
  os.remove(str_imagemTemp)