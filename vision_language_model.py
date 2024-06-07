from abc import ABC, abstractmethod
from PIL import Image
from read_questions import read_questions
import os
from read_write_json import read_json, write_json
from typing import List, Union, Dict, Any

class VisionLanguageModel(ABC):

    def __init__(self, name: str = None, image_folder: str = "images", questions_file_path: str = "questions.js", json_file_path: str = "image_data.js"):
        self.name = name
        self.image_folder = image_folder
        self.questions_file_path = questions_file_path
        self.json_file_path = json_file_path

    @abstractmethod
    def answer_question(self, image: Image.Image, question: str) -> str:
        """
        Takes a PIL image object and a question about the image, and returns the answer.
        
        :param image: A PIL Image object
        :param question: The question about the image
        :return: The answer to the question
        """
        pass

    def answer_questions_for_image(self, image : Image.Image, questions: List[str], json_data: Union[List[Any], Dict[str, Any]]):
        answers = []
        for question in questions:
            answers.append(self.answer_question(image, question))
        return answers
    
    def answer_questions_for_images(self) -> list:

        json_data = read_json(self.json_file_path)
        questions = read_questions(self.questions_file_path)
        
        for image_filename in os.listdir(self.image_folder):
            if image_filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(self.image_folder, image_filename)
                image = Image.open(image_path).convert("RGB")

                # Check if the image filename is in the data, if not, add it
                if image_filename not in json_data:
                    json_data[image_filename] = {f"{self.name}_answers": {}}

                # Check if the model is not yet in the data structure
                if f"{self.name}_answers" not in json_data[image_filename]:
                    json_data[image_filename][f"{self.name}_answers"] = {}

                data = json_data[image_filename]

                for question in questions:
                    label = question["label"]
                    question_text = question["question"]
                    
                    # Check if the question is already answered
                    if label in data[f"{self.name}_answers"]:
                        continue
                    
                    # Answer the question and update the data
                    data[f"{self.name}_answers"][label] = self.answer_question(image, question_text)

        write_json(self.json_file_path, json_data)

            