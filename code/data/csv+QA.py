import os
import pandas
from pipeline import preprocess, translate, generate_answer


if __name__ == '__main__':
    game = "Viktor_Axelsen_Ng_Ka_Long_Angus_YONEX_Thailand_Open_2021_Finals"
    player_A = "Viktor Axelsen"
    player_B = "Ng Ka Long Angus"
    competition = "YONEX Thailand Open 2021 Finals"
    
    QA_output = f"{competition}: {player_A} v.s. {player_B}"
    csv_output = f"{competition}: {player_A} v.s. {player_B}"
    
    # Get list of filenames in the folder
    filenames = os.listdir(f"data/{game}/")
    os.makedirs(f"csv/{game}/", exist_ok=True)
    os.makedirs(f"QA/{game}/", exist_ok=True)
    # print("filenames:", filenames)
    set = 1
    for filename in filenames:
        print(f"> Read file {filename}...")
        data = pandas.read_csv(f"data/{game}/{filename}")
        input_df = pandas.DataFrame(data)
        # print("input_df:", input_df)

        print(f"> Preprocess...")
        preprocessed_df = preprocess(input_df)
        # print("preprocessed_df:", preprocessed_df)
        
        print("> Translate...")
        translated_df = translate(preprocessed_df)
        # print("translated_df:", translated_df)
        translated_df.to_csv(f"csv/{game}/{filename}", index=False)
        
        with open(f"csv/{game}/{filename}", "r") as f:
            csv = f.read()
            csv_output += f"\n\nSet {set}:\n{csv}"
        
        print("> Generate answer...")
        answers = generate_answer(translated_df, player_A, player_B)
        # print("answers:", answers)
        
        QA_output += f"\n\nSet {set}:{answers}"
        set += 1

    # Output
    print("Output...")
    with open(f"QA/{game}/QA.txt", "w") as f:
        f.write(QA_output)
        
    with open(f"csv/{game}/csv.txt", "w") as f:
        f.write(csv_output)
