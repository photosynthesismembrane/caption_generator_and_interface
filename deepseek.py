from PIL import Image
import torch
from transformers import AutoModelForCausalLM
from deepseek_vl.deepseek_vl.models import VLChatProcessor, MultiModalityCausalLM
from vision_language_model import VisionLanguageModel


# Example subclass that implements the abstract method
class Deepseek(VisionLanguageModel):

    def __init__(self, image_folder: str = "images", questions_file_path: str = "questions.js", json_file_path: str = "image_data.js") -> None:
        super().__init__('deepseek', image_folder, questions_file_path, json_file_path)

    def load_model(self):
        model_path = "deepseek-ai/deepseek-vl-7b-chat"
        self.vl_chat_processor: VLChatProcessor = VLChatProcessor.from_pretrained(model_path)
        self.tokenizer = self.vl_chat_processor.tokenizer

        self.vl_gpt: MultiModalityCausalLM = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
        self.vl_gpt = self.vl_gpt.to(torch.bfloat16).cuda().eval()

    def unload_model(self):
        del self.vl_chat_processor
        del self.tokenizer
        del self.vl_gpt
        torch.cuda.empty_cache()

    def answer_question(self, image: Image.Image, question: str) -> str:

        ## single image conversation example
        conversation = [
            {
                "role": "User",
                "content": f"<image_placeholder>{question}",
            },
            {"role": "Assistant", "content": ""},
        ]

        prepare_inputs = self.vl_chat_processor(
            conversations=conversation,
            images=[image],
            force_batchify=True
        ).to(self.vl_gpt.device)

        # run image encoder to get the image embeddings
        inputs_embeds = self.vl_gpt.prepare_inputs_embeds(**prepare_inputs)

        # run the model to get the response
        outputs = self.vl_gpt.language_model.generate(
            inputs_embeds=inputs_embeds,
            attention_mask=prepare_inputs.attention_mask,
            pad_token_id=self.tokenizer.eos_token_id,
            bos_token_id=self.tokenizer.bos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            max_new_tokens=512,
            do_sample=False,
            use_cache=True
        )

        return self.tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)