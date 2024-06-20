import json
from read_write_json import read_json
import os
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Create metadata.jsonl files for each model based on generated image_data.js files.")
parser.add_argument('--javascript_file', type=str, required=True, help="Path to the javascript file containing image data.")
parser.add_argument('--answers_keys', type=str, required=True, help="Comma-separated list of keys to extract from the image data.")
parser.add_argument('--output_folder', type=str, required=True, help="Path to the output folder for metadata.jsonl files.")
args = parser.parse_args()

image_data = read_json(args.javascript_file)
answers_keys = args.answers_keys.split(',')
output_folder = args.output_folder

models = ["cogvlm", "deepseek", "llava"]

def transform_image_data_to_jsonl(image_data, answers_keys, output_folder='metadata'):
    # Create folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for model in models:
        with open(f'{output_folder}/metadata_{model}.jsonl', 'w') as outfile:
            for image_id, image_item in image_data.items():
                concatenated_text = " ".join([image_item[model + '_answers'].get(key, '') for key in answers_keys])
                json_line = json.dumps({"file_name": image_id, "text": concatenated_text})
                outfile.write(json_line + '\n')

transform_image_data_to_jsonl(image_data, answers_keys, output_folder)
