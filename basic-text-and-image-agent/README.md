# AWS Bedrock Demo Script

A simple Python script example showing how to use AWS bedrock via the Python SDK.

To use this you'll first need also need to have the AWS CLI already installed and configured.

You'll also need to enable the Claude, Jurassic and Stability models in your AWS account. These all use
the AWS `us-east-1` region.

## Generate Text Content Using Claude AI

```sh
python generate_text_claude.py
```

Update the `prompt_data` variable to change what it generates.

```python
prompt_data = """
What are the top 3 benefits of cloud computing?
"""
```

Example output:

```text
Cloud computing provides scalability, flexibility, and cost savings by delivering on-demand compute resources, applications, and storage over the internet.
```

```python
prompt_data = """
Write a one-liner 90s style B-movie horror/comedy pitch about
a giant man-eating Python,
with a hilarious and surprising twist.
"""
```

Example output:

````text
When a genetically-engineered 30-foot python escapes from a research facility and terrorizes a small town, it's up to a plucky teen who can inexplicably speak to snakes, a bumbling sheriff afraid of danger, and a kooky pet psychic to stop the beast before it swallows up the entire senior prom in one gulp.
```

## Generate Text Content Using Jurassic

```sh
python generate_text_j2.py
````

Example output:

```text
Cloud computing provides on-demand access to a shared pool of computing resources, enabling scalable, flexible, and cost-effective IT solutions.
```

## Generate Image Using Stable Diffusion XL

```sh
python generate_image.py
```

Update the `prompt_data` variable to change what it generates.

```python
prompt_data = """
A high-resolution scene featuring a quirky, 
green alien with multiple eyes, 
standing beside Rick and Morty-style characters. 
They're on a bizarre, colorful alien planet with swirling skies, 
strange plants, and glowing crystals. The characters have goofy expressions, 
and the scene has a vibrant, animated style, like a frame from a Rick and Morty episode.
"""
```

They'll be generated to the `output` directory.

Example outputs:

![Image_1](output\generated-0.png)

![Image_2](output\generated-2.png)

**Original Repo:** [https://github.com/pixegami/aws-bedrock-demo](https://github.com/pixegami/aws-bedrock-demo)