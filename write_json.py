import json

# Read the existing data
with open('image_data.js', 'r') as file:
    content = file.read()
    json_data = content.split('const image_data = ')[1].rstrip(';')
    data = json.loads(json_data)

# Update the deepseek fields with content that includes newlines and special characters
for item in data:
    item["dataitem_1_deepseek"] = "updated_deepseek_1 with special chars \" and \n new line"
    item["dataitem_2_deepseek"] = "updated_deepseek_2 with special chars \" and \n new line"

# Convert the updated data back to a JSON string
json_data = json.dumps(data, indent=4)

# Create the updated JavaScript content
js_content = f"const image_data = {json_data};"

# Write the updated content back to the .js file
with open('image_data.js', 'w') as file:
    file.write(js_content)

print("deepseek fields have been updated in image_data.js")
