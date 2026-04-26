import requests
import json
import yaml
import time
from app.config import llmApiEndpoint, llmModelName

def load_instruction(filePath):
    with open(filePath, 'r') as instructionFile:
        return yaml.safe_load(instructionFile)

def generate_prompt(instructionData, sourceCode, fileName):
    formattedPrompt = instructionData['prompt_template'].replace('{file_name}', fileName)

    completePrompt = f"{formattedPrompt}\n\n```cpp\n{sourceCode}\n```"
    return completePrompt

def query_llm(promptText, maxRetries=3, retryDelay=5):
    """Query the Ollama LLM with retry logic and JSON format enforcement."""
    for attempt in range(1, maxRetries + 1):
        print(f"    - Sending prompt to Ollama API (attempt {attempt}/{maxRetries})...")
        try:
            apiResponse = requests.post(
                llmApiEndpoint,
                json={
                    "model": llmModelName,
                    "prompt": promptText,
                    "stream": False,
                    "format": "json"  # Enforce JSON output at the API level
                },
                timeout=120  # 2-minute timeout per request
            )
            apiResponse.raise_for_status()
            print("    - Response received successfully.")

            responseData = json.loads(apiResponse.text)
            return responseData.get("response", "")

        except requests.exceptions.HTTPError as httpError:
            print(f"    - HTTP error on attempt {attempt}: {httpError}")
            if attempt < maxRetries:
                print(f"    - Retrying in {retryDelay}s...")
                time.sleep(retryDelay)
                retryDelay *= 2  # Exponential backoff
            else:
                print("    - All retries exhausted.")
                return None

        except requests.exceptions.RequestException as apiError:
            print(f"    - Connection error: {apiError}")
            return None
