import base64
import os
import random
import boto3
import json


prompt_data = """
A high-resolution scene featuring a quirky, 
green alien with multiple eyes, 
standing beside Rick and Morty-style characters. 
They're on a bizarre, colorful alien planet with swirling skies, 
strange plants, and glowing crystals. The characters have goofy expressions, 
and the scene has a vibrant, animated style, like a frame from a Rick and Morty episode.
"""


def main():
    for i in range(0, 5):
        seed = random.randint(0, 100000)
        generate_image(prompt=prompt_data, seed=seed, index=i)


def generate_image(prompt: str, seed: int, index: int):
    payload = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 12,
        "seed": seed,
        "steps": 80,
    }

    # Create the client and invoke the model.
    bedrock = boto3.client(service_name="bedrock-runtime")
    body = json.dumps(payload)
    model_id = "stability.stable-diffusion-xl-v1"
    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )

    # Get the image from the response. It is base64 encoded.
    response_body = json.loads(response.get("body").read())
    artifact = response_body.get("artifacts")[0]
    image_encoded = artifact.get("base64").encode("utf-8")
    image_bytes = base64.b64decode(image_encoded)

    # Save image to a file in the output directory.
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    file_name = f"{output_dir}/generated-{index}.png"
    with open(file_name, "wb") as f:
        f.write(image_bytes)


if __name__ == "__main__":
    main()