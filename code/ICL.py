import os
from openai import OpenAI


if __name__ == '__main__':
    data_type = "QA"  # csv or QA
    prompt_type = "few-shot"
    filename = data_type + "+" + prompt_type
    model = "gpt-3.5-turbo-0125"
    
    print("filename:", filename)

    # Get list of filenames in the folder
    games = os.listdir(f"{data_type}/")
    for game in games:
        print("==================================")
        print("game:", game)
        with open(f"{data_type}/{game}/{data_type}.txt", "r") as f:
            data = f.read()
            
        with open(f"prompt/{filename}.txt", "r") as f:
            prompt = f.read()
            
        if data_type == "csv":
            prompt = prompt.replace("{csv table}", data)
        elif data_type == "QA":
            prompt = prompt.replace("{Q&A}", data)
            
        print("prompt:\n", prompt)

        client = OpenAI()

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        report = completion.choices[0].message.content
        print("report:\n", report)

        os.makedirs(f"report/{game}/GPT-3.5/", exist_ok=True)
        with open(f"report/{game}/GPT-3.5/{filename}.txt", "w") as f:
            f.write(report)
