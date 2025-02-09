from huggingface_hub import snapshot_download

# Download the file again and ensure it's stored locally
model_file = snapshot_download(
    repo_id="Qwen/Qwen2-0.5B-Instruct-GGUF",
    filename="qwen2-0_5b-instruct-q2_k.gguf",
    cache_dir="./models"  # Specify a local directory to ensure proper download
)
print(f"Model downloaded to: {model_file}")