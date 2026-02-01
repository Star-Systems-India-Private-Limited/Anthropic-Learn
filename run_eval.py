import ast
import json
import os
import re
from statistics import mean

import client


def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0


def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0


def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0


def run_prompt(test_case):
    prompt = f"""
    Please solve the following task:
    
    {test_case['task']}
    
    * Respond only with Python, JSON, or a plain Regex
    * Do not add any comments or commentary or explanation
    """
    messages = []
    client.add_user_message(messages, prompt)
    client.add_assistant_message(messages, "```code")
    test = client.chat(messages)
    return test


def grade_syntax(response, test_case):
    format = test_case["format"]
    if format == "json":
        return validate_json(response)
    elif format == "python":
        return validate_python(response)
    else:
        return validate_regex(response)


def grade_by_model(test_case, output):
    # Create evaluation prompt
    eval_prompt = f"""
    You are an expert code reviewer. Evaluate this AI-generated solution.

    Task: {test_case}
    Solution: {output}

    Provide your evaluation as a structured JSON object with:
    - "strengths": An array of 1-3 key strengths
    - "weaknesses": An array of 1-3 key areas for improvement  
    - "reasoning": A concise explanation of your assessment
    - "score": A number between 1-10
    """

    messages = []
    client.add_user_message(messages, eval_prompt)
    client.add_assistant_message(messages, "```json")

    eval_text = client.chat(messages, stop_sequences=["```"])
    return json.loads(eval_text)


def run_test_case(test_case):
    output = run_prompt(test_case)
    model_grade = grade_by_model(test_case['task'], output)
    model_score = model_grade["score"]
    reasoning = model_grade["reasoning"]

    syntax_score = grade_syntax(output, test_case)

    score = (model_score + syntax_score) / 2

    return {
        "output": output,
        "test_case": test_case,
        "score": score,
        "reasoning": reasoning
    }


def run_eval(datasets):
    results = []
    for dataset in datasets:
        results.append(run_test_case(dataset))

    average_score = mean([result["score"] for result in results])
    print(f"Average score: {average_score}")
    return results


if __name__ == '__main__':
    with open(os.path.join(client.get_media_dir(), 'dataset.json'), 'r') as f:
        _datasets = json.load(f)
    _results = run_eval(_datasets)
    # print(_datasets[0])
    print(json.dumps(_results, indent=4))
