import os
from openai import OpenAI


if __name__ == '__main__':
    metrics = "coherence"
    model = "gpt-3.5-turbo-0125"
    
    # Get list of filenames in the folder
    games = os.listdir(f"report/")
    
    for game in games:
        print("==================================")
        print("game:", game)
        
        reports = os.listdir(f"report/{game}/GPT-3.5/")
        
        for report in reports:
            print("report:", report)
            
            with open(f"report/{game}/GPT-3.5/{report}", "r") as f:
                data = f.read()
                
            with open(f"prompt/evaluation/{metrics}.txt", "r") as f:
                prompt = f.read()
                
            prompt = prompt.replace("{Badminton Report}", data)
            print("prompt:\n", prompt)

            client = OpenAI()

            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            evaluation = completion.choices[0].message.content
            print("evaluation:\n", evaluation)

            os.makedirs(f"evaluation/{game}/GPT-3.5/{report}/", exist_ok=True)
            with open(f"evaluation/{game}/GPT-3.5/{report}/{metrics}.txt", "w") as f:
                f.write(evaluation)
