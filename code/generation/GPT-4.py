import os
from openai import OpenAI


if __name__ == '__main__':
    model = "gpt-4-turbo-2024-04-09"
    ICLs = ["CSV+zero-shot", "CSV+one-shot", "CSV+few-shot", "CSV+CoT",
            "QA+zero-shot", "QA+one-shot", "QA+few-shot", "QA+CoT"]

    for ICL in ICLs:
        print("> ICL:", ICL)

        with open(f"prompt/generation/{ICL}.txt", "r") as f:
            prompt = f.read()

        data_type = ICL.split("+")[0]
        print("> data_type:", data_type)

        # Get list of filenames in the folder
        games = os.listdir(f"{data_type}/")
        for game in games:
            print(">> game:", game)
            with open(f"{data_type}/{game}/{data_type}.txt", "r") as f:
                data = f.read()

            if data_type == "CSV":
                prompt_data = prompt.replace("{CSV}", data)
            elif data_type == "QA":
                prompt_data = prompt.replace("{QA}", data)

            print(">> prompt_data:\n", prompt_data)

            client = OpenAI()

            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt_data}
                ]
            )

            report = completion.choices[0].message.content
            print(">> report:\n", report)

            os.makedirs(f"generation/{game}/GPT-4/", exist_ok=True)
            with open(f"generation/{game}/GPT-4/{ICL}.txt", "w") as f:
                f.write(report)

            print("===============================================")
