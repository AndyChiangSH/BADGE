import os
from openai import OpenAI


if __name__ == '__main__':
    model = "gpt-4-turbo-2024-04-09"
    metrics = ["coherence", "consistency", "fluency", "excitement"]
    
    # Get list of filenames in the folder
    games = os.listdir(f"report/")
    
    for game in games:
        print("game:", game)
        
        with open(f"report/{game}/human/human.txt", "r") as f:
            data = f.read()
            
        for metric in metrics:
            print("metric:", metric)
            
            with open(f"prompt/evaluation/{metric}.txt", "r") as f:
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

            os.makedirs(f"evaluation/{game}/human/", exist_ok=True)
            with open(f"evaluation/{game}/human/{metric}.txt", "w") as f:
                f.write(evaluation)
                
            print("==================================")
