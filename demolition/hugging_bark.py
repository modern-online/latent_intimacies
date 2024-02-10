from transformers import AutoProcessor, BarkModel
from scipy.io.wavfile import write as write_wav
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = AutoProcessor.from_pretrained("suno/bark-small")
model = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float32).to(device)
sample_rate = model.generation_config.sample_rate
model.enable_cpu_offload()
model =  model.to_bettertransformer()

inputs = processor(["Hello, my dog is cute"], return_tensors="pt")

audio_array = model.generate(**inputs, do_sample=True)
print(audio_array)
audio_array = audio_array.cpu().numpy().squeeze()
print(audio_array)


write_wav("tts.wav", rate=sample_rate, data=audio_array)