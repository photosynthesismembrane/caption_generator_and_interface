from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration
from vision_language_model import VisionLanguageModel
import torch


# Example subclass that implements the abstract method
class Llava(VisionLanguageModel):

    def __init__(self, image_folder: str = "images", questions_file_path: str = "questions.js", json_file_path: str = "image_data.js") -> None:
        super().__init__('llava', image_folder, questions_file_path, json_file_path)

    def load_model(self):
        # Model and processor initialization
        self.model = LlavaForConditionalGeneration.from_pretrained("llava-hf/llava-1.5-7b-hf").to("cuda")
        self.processor = AutoProcessor.from_pretrained("llava-hf/llava-1.5-7b-hf")

    def unload_model(self):
        del self.model
        del self.processor
        torch.cuda.empty_cache()

    def answer_question(self, image: Image.Image, question: str) -> str:

        question = f"<image>\nUSER: {question}\nASSISTANT:"

        # Create embeddings
        inputs = self.processor(text=question, images=image, return_tensors="pt").to("cuda")

        # Generate
        generate_ids = self.model.generate(**inputs, max_length=600)
        result = self.processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

        # Extract answer
        answer = ""
        result_split = result.split('ASSISTANT: ')
        if len(result_split) > 1:
            answer = result_split[1]
            
        return answer