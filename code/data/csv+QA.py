import os
import pandas
from pipeline import preprocess, translate, generate_answer


if __name__ == '__main__':
    game = "Kento_MOMOTA_CHOU_Tien_Chen_Denmark_Open_2018_Finals"
    player_A = "Kento MOMOTA"
    player_B = "CHOU Tien Chen"
    competition = "Denmark Open 2018 Finals"
    
    QA_output = f"{competition}: {player_A} v.s. {player_B}"
    csv_output = f"{competition}: {player_A} v.s. {player_B}"
    
    # Get list of filenames in the folder
    num_set = len(os.listdir(f"data/{game}/"))
    os.makedirs(f"csv/{game}/", exist_ok=True)
    os.makedirs(f"QA/{game}/", exist_ok=True)
    for set in range(1, num_set+1):
        filename = f"set{set}"
        
        print(f"> Read file {filename}...")
        data = pandas.read_csv(f"data/{game}/{filename}.csv")
        input_df = pandas.DataFrame(data)
        # print("input_df:", input_df)

        print(f"> Preprocess...")
        preprocessed_df = preprocess(input_df)
        # print("preprocessed_df:", preprocessed_df)
        
        print("> Translate...")
        translated_df = translate(preprocessed_df)
        # print("translated_df:", translated_df)
        
        translated_df_copy = translated_df.copy()
        translated_df_copy.replace(
            {'win_point_player': {"A": player_A, "B": player_B}}, inplace=True)
        
        translated_df_copy.to_csv(f"csv/{game}/{filename}.csv", index=False)
        
        with open(f"csv/{game}/{filename}.csv", "r") as f:
            csv = f.read()
        
        csv_output += f"\n\nSet {set}:\n{csv}"
        
        print("> Generate answer...")
        answers = generate_answer(translated_df, player_A, player_B)
        # print("answers:", answers)
        
        QA_output += f"\n\nSet {set}:{answers}"

    # Output
    print("Output...")
    with open(f"QA/{game}/QA.txt", "w") as f:
        f.write(QA_output)
        
    with open(f"csv/{game}/csv.txt", "w") as f:
        f.write(csv_output)
