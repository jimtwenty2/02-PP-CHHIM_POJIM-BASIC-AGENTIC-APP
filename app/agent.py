import json
import os

import openai
from dotenv import load_dotenv

from app.config import MAX_ITERATIONS, MAX_TOOL_CALLS, SYSTEM_PROMPT
from app.harness import run_tool
from app.schemas import TOOLS

load_dotenv()

MODEL = os.getenv("MODEL", "qwen2.5:7b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

client = openai.OpenAI(base_url=OLLAMA_BASE_URL, api_key="dummy")


def run_agent(user_request, user_role):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_request}
    ]
    tool_calls_used = 0

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n[iteration {iteration}]")

        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOLS,
                temperature=0,
            )
        except openai.OpenAIError:
            return "Error: cannot reach the model. Is Ollama running?"

        message = response.choices[0].message

        if not message.tool_calls:
            print("MODEL     : final answer (no tool call)")
            return message.content

        message.tool_calls = message.tool_calls[:1]

        messages.append(message.model_dump(exclude_none=True))
        call = message.tool_calls[0]

        # tool-call limit
        if tool_calls_used >= MAX_TOOL_CALLS:
            return "Stopped: too many tool calls."
        tool_calls_used += 1

        # run the tool through the harness
        name = call.function.name
        try:
            args = json.loads(call.function.arguments)
        except json.JSONDecodeError:
            args = None

        if isinstance(args, dict):
            # user_role comes from the application, never from the model
            result = run_tool(name, args, user_role)
        else:
            result = {"ok": False, "error": "INVALID_INPUT"}

        print(f"TOOL CALL : {name}({args})")
        print(f"RESULT    : {result}")

        # give the result back to the model
        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": json.dumps(result),
        })

    return "Stopped: reached the maximum number of iterations."