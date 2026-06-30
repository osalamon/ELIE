import os
from google import genai

# Assuming prompting is a custom module, we'll keep its import.
# If it's not relevant to the Gemini API, you might remove it.
from elie.prompting import build_further_prompt, parse_terms

# Configure the Gemini API key
# It's highly recommended to load this from environment variables for security.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY environment variable not set. LLM calls will fail.")

GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# interaction = client.interactions.create(
#     model="gemini-3.5-flash",
#     input="Explain how AI works in a few words"
# )
# print(interaction.output_text)


def call_gemini_llm(prompt: str) -> str:
    """
    Makes an API call to the Google Gemini model to generate content.

    Args:
        prompt (str): The user's prompt.

    Returns:
        str: The generated content from the Gemini model, or an error message.
    """
    try:
        prpt = client.models.generate_content(GEMINI_MODEL_NAME)
        # print(f"Sending message to Gemini model: {GEMINI_MODEL_NAME}")
        # print(f"Prompt: {prompt}")

        # Use generate_content for single turn conversations
        response = client.generate_content(prpt)

        # Access the generated text
        if response.candidates:
            # Each candidate has a 'content' attribute, which in turn has 'parts'
            # We are interested in the 'text' part of the first content part of the first candidate.
            if response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                return "❌ Error: No content parts found in Gemini response."
        else:
            return "❌ Error: No candidates found in Gemini response."

    except Exception as e:
        return f"❌ An unexpected error occurred: {e}"


if __name__ == "__main__":
    # Example usage with build_further_prompt (assuming it's defined in elie.prompting)
    prompt_for_gemini = build_further_prompt(
        "quaternion", ["3D", "4D"], ["vectors", "rotation matrices"]
    )
    response = call_gemini_llm(prompt_for_gemini)
    print(f"Gemini LLM response: {response}")

    # Example usage of parse_terms (assuming it's defined in elie.prompting)
    parsed_terms = parse_terms(response)
    print(f"Parsed terms: {parsed_terms}")
