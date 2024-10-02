import openai
from typing import Dict, Any, List
import json

async def generate_code(prompt: str, api_key: str, context: str = "", language: str = "python", model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
    openai.api_key = api_key
    
    if not prompt:
        raise ValueError("Prompt cannot be empty")
    
    system_message = f"You are an expert {language} programmer. Generate code based on the given prompt and context."
    
    try:
        response = await openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Context: {context}\n\nPrompt: {prompt}"}
            ],
            temperature=0.7,
            max_tokens=1000,
            n=1,
            stop=None,
            functions=[
                {
                    "name": "generate_code_response",
                    "description": "Generate code based on the given prompt and context",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The generated code"
                            },
                            "explanation": {
                                "type": "string",
                                "description": "A brief explanation of the generated code"
                            },
                            "suggestions": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "A list of suggestions for improvement or alternative approaches"
                            }
                        },
                        "required": ["code", "explanation"]
                    }
                }
            ],
            function_call={"name": "generate_code_response"}
        )
        
        function_response = json.loads(response.choices[0].function_call.arguments)
        return function_response
    except Exception as e:
        raise Exception(f"Error generating code: {str(e)}")

async def main():
    api_key = input("Enter your OpenAI API key: ")
    context = input("Enter any context for the code generation (optional): ")
    prompt = input("Enter your code generation prompt: ")
    
    try:
        generated_result = await generate_code(prompt, api_key, context)
        print("\nGenerated Code:")
        print(generated_result['code'])
        print("\nExplanation:")
        print(generated_result['explanation'])
        if 'suggestions' in generated_result:
            print("\nSuggestions:")
            for suggestion in generated_result['suggestions']:
                print(f"- {suggestion}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())