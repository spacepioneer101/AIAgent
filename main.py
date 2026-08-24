from email.mime import message
import json
import os, argparse
from urllib import response
from dotenv import load_dotenv
from openai import NoneType, OpenAI
from prompts import system_prompt
from functions_to_use import available_functions
from functions_to_use import call_function


def main():

    print("Starting Application")

    # Load data from environment
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise KeyError("OPENROUTER_API_KEY not found")

    # inits
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", help="The prompt for the AI model")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    userprompt = args.user_prompt;
    verbose = args.verbose;

    # Store the messages
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": userprompt},
    ]

    # Loop for 20 iterations to allow for multiple function calls
    for _ in range(20):

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions
        )

        # get the current message and append to list of messages
        message =  response.choices[0].message
        messages.append(message)

        # do the tool call
        if not response.choices[0].message.tool_calls is None:
            for tool_call in response.choices[0].message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")

                # do the actual function call
                function_response = call_function(tool_call, verbose=verbose)

                # append function call to history
                messages.append(function_response)

                if function_response["content"] is None:
                    raise ValueError(f"Function {tool_call.function.name} returned None")

                if verbose:
                    print(f"-> {function_response['content']}")

        # there is no tool call so end the conversation
        elif not response.choices[0].message.content is NoneType:
            print("Hello from aiagent: " + response.choices[0].message.content)
            break

        if (verbose):
            print("User prompt:" + userprompt)
            print("Prompt tokens: " + str(response.usage.prompt_tokens))
            print("Response tokens: " + str(response.usage.completion_tokens))  


        # is this the last iteration? If so, print a message
        if _ == 19:
            print("Reached maximum number of iterations (20). Ending conversation.")
            exit(1)

        # Print the final response
        if not response.choices[0].message.content is None:
            print("Final response: " + response.choices[0].message.content)


if __name__ == "__main__":
    main()