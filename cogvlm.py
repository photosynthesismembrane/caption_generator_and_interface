from PIL import Image
import torch
from transformers import AutoModelForCausalLM, LlamaTokenizer
from accelerate import init_empty_weights, infer_auto_device_map, load_checkpoint_and_dispatch
from vision_language_model import VisionLanguageModel


# Example subclass that implements the abstract method
class Cogvlm(VisionLanguageModel):

    def __init__(self, image_folder: str = "images", questions_file_path: str = "questions.js", json_file_path: str = "image_data.js") -> None:
        super().__init__('cogvlm', image_folder, questions_file_path, json_file_path)

    def load_model(self):
        # Model and processor initialization
        self.tokenizer = LlamaTokenizer.from_pretrained('lmsys/vicuna-7b-v1.5')
        with init_empty_weights():
            self.model = AutoModelForCausalLM.from_pretrained(
                'THUDM/cogvlm-chat-hf',
                torch_dtype=torch.bfloat16,
                low_cpu_mem_usage=True,
                trust_remote_code=True,
            )
        device_map = infer_auto_device_map(self.model, max_memory={0:'20GiB',1:'20GiB','cpu':'16GiB'}, no_split_module_classes=['CogVLMDecoderLayer', 'TransformerLayer'])
        self.model = load_checkpoint_and_dispatch(
            self.model,
            '/scratch/s1889338/.cache/huggingface/transformers/models--THUDM--cogvlm-chat-hf/snapshots/e29dc3ba206d524bf8efbfc60d80fc4556ab0e3c',   # typical, '~/.cache/huggingface/hub/models--THUDM--cogvlm-chat-hf/snapshots/balabala'
            device_map=device_map,
        )
        self.model = self.model.eval()

    def unload_model(self):
        del self.model
        del self.tokenizer
        torch.cuda.empty_cache()

    def answer_question(self, image: Image.Image, question: str) -> str:

        inputs = self.model.build_conversation_input_ids(self.tokenizer, query=question, history=[], images=[image])  # chat mode
        inputs = {
            'input_ids': inputs['input_ids'].unsqueeze(0).to('cuda'),
            'token_type_ids': inputs['token_type_ids'].unsqueeze(0).to('cuda'),
            'attention_mask': inputs['attention_mask'].unsqueeze(0).to('cuda'),
            'images': [[inputs['images'][0].to('cuda').to(torch.bfloat16)]],
        }
        gen_kwargs = {"max_length": 2048, "do_sample": False}

        with torch.no_grad():
            outputs = self.model.generate(**inputs, **gen_kwargs)
            outputs = outputs[:, inputs['input_ids'].shape[1]:]
            return self.tokenizer.decode(outputs[0])