from transformers import GPTNeoForCausalLM, GPT2Tokenizer
import nltk
from nltk.tokenize.treebank import TreebankWordDetokenizer
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

# Load GPT Neo ML models
model = GPTNeoForCausalLM.from_pretrained("./gpt-neo-poetry")
tokenizer = GPT2Tokenizer.from_pretrained("./gpt-neo-poetry")

# Load TTS models
preload_models()


# For text cleanup and grammar check
d = TreebankWordDetokenizer()


prompt = "Create jobs? I want to eliminate jobs"

answer_length = 20


def clean_text(input):
    sentences = nltk.sent_tokenize(input)
    sentences[0].strip()
    # If there's at least one complete sentence in generated prophecy
    if len(sentences) > 1:
        sentences.pop()
    sentences = d.detokenize(sentences)
    return sentences


input_ids = tokenizer(prompt, return_tensors="pt").input_ids
gen_tokens = model.generate(input_ids, do_sample=True, temperature=0.9, early_stopping=False, top_k=30, max_length=answer_length, repetition_penalty = 1.2)
prophecy = tokenizer.batch_decode(gen_tokens)[0]
prophecy = prophecy.replace(prompt, "")
prophecy = clean_text(prophecy)
print(str(prophecy))


# TTS response
audio_array = generate_audio(str(prophecy))

# save audio to disk
write_wav("./prophecy.wav", SAMPLE_RATE, audio_array)