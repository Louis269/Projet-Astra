from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class Communication:

    def __init__(self, model_name="Qwen/Qwen2-1.5B-Instruct"):

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # modèle
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    def generate_response(self, history_context, personality, emotions, memory_context):

        # résumé personnalité
        traits_summary = (
            f"curiosité={personality.get('curiosite',50)}, "
            f"empathie={personality.get('empathie',50)}, "
            f"créativité={personality.get('creativite',50)}"
        )

        # limiter souvenirs
        memory_text = "\n".join(memory_context.split("\n")[-5:])

        # prompt adapté pour Qwen
        prompt = f"""
<|system|>
You are Astra, an experimental AI assistant.

Personality:
{traits_summary}

Recent memories:
{memory_text}

Conversation:
{history_context}

<|assistant|>
"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=self.tokenizer.eos_token_id
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # nettoyer sortie
        if "<|assistant|>" in response:
            response = response.split("<|assistant|>")[-1]

        return response.strip()