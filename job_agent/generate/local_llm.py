import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "Qwen/Qwen2.5-1.5B-Instruct"


class LocalLLM:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID,
            trust_remote_code=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            device_map="cpu",
            torch_dtype="auto",
            low_cpu_mem_usage=True,
            trust_remote_code=True
        )

        self.model.eval()

    def generate(self, messages, max_new_tokens=350) -> str:
        """
        messages: list[dict] with roles (system/user)
        """

        # 🔑 Convert chat messages → single text prompt
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=2048
        )

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.4,
                top_p=0.9,
                repetition_penalty=1.1,
                eos_token_id=self.tokenizer.eos_token_id,
            )

        # 🔑 Strip the prompt from the output
        generated = outputs[0][inputs.input_ids.shape[-1]:]

        return self.tokenizer.decode(
            generated,
            skip_special_tokens=True
        )
