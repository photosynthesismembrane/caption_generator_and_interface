from cogvlm import Cogvlm
from deepseek import Deepseek
from llava import Llava
import argparse

def main(**kwargs):
    image_folder = kwargs.get("image_folder")
    questions_file_path = kwargs.get("questions_file_path")
    json_file_path = kwargs.get("json_file_path")

    cogvlm = Cogvlm(image_folder, questions_file_path, json_file_path)
    cogvlm.load_model()
    cogvlm.answer_questions_for_images()
    cogvlm.unload_model()

    llava = Llava(image_folder, questions_file_path, json_file_path)
    llava.load_model()
    llava.answer_questions_for_images()
    llava.unload_model()

    deepseek = Deepseek(image_folder, questions_file_path, json_file_path)
    deepseek.load_model()
    deepseek.answer_questions_for_images()
    deepseek.unload_model()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some folders.")
    parser.add_argument('--image_folder', type=str, default="images", help='Path to the image folder')
    parser.add_argument('--questions_file_path', type=str, default="questions.js", help='Path to the questions file')
    parser.add_argument('--json_file_path', type=str, default="image_data.js", help='Path to the json file')

    args = parser.parse_args()

    # Convert parsed args to a dictionary and pass to main
    main(**vars(args))
