import json
import os
import openai


# CONFIGURATION VARIABLES


OPENAI_API_KEY = "OPENAI KEY(It is a secret key so cant upload to github)"  
openai.api_key = OPENAI_API_KEY

INPUT_FILE = "prompts.txt"
OUTPUT_FILE = "responses.json"
MODEL_NAME = "gpt-4o-mini"  


# HELPER FUNCTIONS


def read_prompts_from_file(file_path: str) -> list[str]:
    """
    Reads prompts from a text file. Each non-empty line is a separate prompt.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def call_openai_api(prompt: str) -> str:
    """
    Sends a single prompt to OpenAI GPT API and returns the response text.
    """
    response = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content


def save_responses_to_json(responses: dict, file_path: str):
    """
    Saves all responses to a JSON file in a structured format.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(responses, file, indent=4, ensure_ascii=False)


# MAIN SCRIPT


def main():
    prompts = read_prompts_from_file(INPUT_FILE)
    if not prompts:
        print("⚠️ No prompts found in input file.")
        return

    responses = {}

    print(f"Processing {len(prompts)} prompts sequentially...\n")

    for index, prompt in enumerate(prompts, start=1):
        print(f"[{index}/{len(prompts)}] Processing prompt: {prompt[:50]}...")
        try:
            response_text = call_openai_api(prompt)
            responses[prompt] = response_text
        except Exception as e:
            responses[prompt] = f"Error: {e}"
            print(f"❌ Error for prompt {index}: {e}")

    save_responses_to_json(responses, OUTPUT_FILE)
    print(f"\n✅ Done! Responses saved in '{OUTPUT_FILE}'.")



if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')  
    main()
