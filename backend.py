import os
import json
from google import genai
from google.genai import types

def main():
    # 1. Initialize the client
    # This requires the GEMINI_API_KEY environment variable to be set.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: Please set your GEMINI_API_KEY environment variable.")
        print("Example: export GEMINI_API_KEY='your-key-here'")
        return

    client = genai.Client()

    # 2. Load the transcript
    transcript_path = os.path.join(os.path.dirname(__file__), 'transcript.txt')
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find {transcript_path}")
        return

    # 3. Load the JSON Schema
    schema_path = os.path.join(os.path.dirname(__file__), 'json_schema.json')
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {schema_path}")
        return

    print("Analyzing conversation with Gemini...")

    # 4. Construct the prompt
    prompt = f"""
You are an expert AI health and wellness coaching assistant. Your task is to analyze a conversation transcript between a health coach and their client, and generate a structured intelligence report based on the client's progress, adherence, and well-being.

### Objective
Extract key insights and metrics from the conversation. For every claim or metric extracted, you MUST classify its source type into one of the following categories:
1. **confirmed_fact**: Verifiable data, system logs, or coach-verified facts.
2. **client_reported**: Information directly stated by the client.
3. **ai_inference**: Conclusions logically deduced by the AI but not explicitly stated.
4. **missing_info**: Important metrics that were not reported during the period.

### Extraction Requirements
You must extract the following fields and provide a quote (evidence) from the transcript for each:
- **Weekly client summary**: A brief overview of the week.
- **Engagement level**: High, Medium, or Low.
- **Nutrition adherence**: Quality of meals, skipped meals, etc.
- **Exercise / steps**: Activity levels, types of exercise, step counts.
- **Sleep**: Duration and quality of sleep.
- **Water intake**: Amount of water consumed.
- **Symptoms / stress**: Any reported physical symptoms or mental stress.
- **Key barriers**: Things preventing the client from following the plan.
- **Pending actions**: Tasks the client promised to do but hasn't yet.
- **Risk / attention flags**: Critical issues.
- **Recommended next action for the coach**: AI's suggestion for how the coach should proceed.

### Conversation Transcript:
{transcript}
"""

    # 5. Call the Gemini API using Structured Outputs
    # We use gemini-2.5-flash as it is highly capable and supports strict JSON schema output.
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=schema,
                temperature=0.2, # Lower temperature for analytical extraction
            ),
        )

        # 6. Output the result
        print("\n--- AI Intelligence Report Generated successfully ---")
        
        # Format the output beautifully
        parsed_json = json.loads(response.text)
        print(json.dumps(parsed_json, indent=2))
        
        # Optionally, save this out so the frontend can read it directly
        output_file = os.path.join(os.path.dirname(__file__), 'prototype', 'ai_output.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(parsed_json, f, indent=2)
        print(f"\nResult saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred during generation: {e}")

if __name__ == "__main__":
    main()
