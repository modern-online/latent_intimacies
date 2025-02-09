from llama_cpp import Llama
import re

def truncate_sentence(text):
    # Regular expression to find the last complete sentence ending in ., !, or ?
    match = re.search(r'([.!?])\s+[^.!?]*$', text)
    if match:
        # Return the text up to and including the last sentence-ending punctuation
        return text[:match.start(1) + 1]
    else:
        # If there's no clear sentence-ending punctuation, return the original text
        return text

print("Loading LLM...")

llm = Llama(
    model_path="/home/cats/poetry/qwen2-0_5b-instruct-q2_k.gguf",
    n_ctx=100,  # Context length to use
    n_threads=4,            # Number of CPU threads to use
    n_gpu_layers=0
)

print("LLM loaded")

## Generation kwargs
generation_kwargs = {
    "max_tokens": 24,
    "stop":["</s>"],
    "temperature": 0.6,
    "repeat_penalty": 1.1,
    "echo":False, # Echo the prompt in the output# This is essentially greedy decoding, since the model will always return the highest-probability token. Set this value > 1 for sampling decoding
}


# ref prompt

def generate(seen_things):
    ## Run inference
    print("generating haiku...")
    seen_things = ", ".join(seen_things)
   
    prompt = f"Create a Haiku using these words: {seen_things}. Don't output anything else."
    print("Prompt: " + prompt)

    llm.create_chat_completion(
        messages = [
            {"role": "system", "content": "You are a poet. You create haiku."},
            {"role": "user", "content": prompt}
        ]
    )

    res = llm(prompt, **generation_kwargs) # Res is a dictionary
    res = truncate_sentence(res['choices'][0]['text'])

    res = res.replace("<", "").replace(">", "")

    res = res.replace("\n", " ").strip()

    if res[-1] != ".":
        res += "."

    print("Generated answer: ")
    print(res)
    return res