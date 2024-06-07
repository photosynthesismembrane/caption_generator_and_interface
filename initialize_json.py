import json
import os
from read_questions import read_questions
from read_write_json import read_json

def initialize_json(images_folder: str = "images", questions_file_path: str = "questions.js", json_file_path: str = "image_data.js"):

    # List of models
    models = ["cogvlm", "llava", "deepseek"]

    # Initial data
    data = {}

    # When data already exists
    if os.path.exists(json_file_path):
        data = read_json(json_file_path)

    # Initial data structure
    for image_filename in os.listdir(images_folder):
        # Skip image names that are already in the list
        if image_filename in data:
            continue

        # Initialize a dictionary for the image
        data[image_filename] = {}

        # Initialize a dictionary for each model
        for model in models:
            data[image_filename][f"{model}_answers"] = {}

    # Convert the data to a JSON string
    json_data = json.dumps(data, indent=4)

    # Create the JavaScript content
    js_content = f"const image_data = {json_data};"

    # Write the content to a .js file
    with open(json_file_path, 'w') as file:
        file.write(js_content)

    print("Initial data has been written to image_data.js")
