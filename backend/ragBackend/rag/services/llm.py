from langchain_community.llms import LlamaCpp
import os


class CustomLLM:
    """LLM service using llama.cpp"""

    def __init__(self):
        # Set environment variable to prefer the discrete GPU
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Use first GPU (RTX 4070)

        self.llm = LlamaCpp(
            model_path="/home/sred/models/DeepSeek-R1-Distill-Qwen-7B-Q6_K.gguf",
            temperature=0.4,
            max_tokens=512,
            n_ctx=4096,
            n_gpu_layers=32,  # Use all layers on GPU
            n_batch=512,
            f16_kv=True,
            verbose=True,
            # Additional GPU parameters
            use_mlock=False,
            seed=-1,
            gpu_device=0,  # Explicitly select device 0 (RTX 4070)
        )

    def get_llm(self):
        return self.llm
