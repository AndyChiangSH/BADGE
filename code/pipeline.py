import pandas
import json
import argparse
from openai import OpenAI
import os


pandas.options.mode.chained_assignment = None


def preprocess(df):
    """Preprocess dataframe
    
    Input: dataframe
    Output: preprocessed dataframe
    """
    
    for i in df:
        if i not in ['getpoint_player', 'win_reason', 'type', 'lose_reason', 'roundscore_A', 'roundscore_B']:
            df = df.drop(columns=[i])

    for j, i in enumerate(df['getpoint_player']):
        if i != 'A' and i != 'B':
            df = df.drop([j])

    df.rename(columns={'getpoint_player': 'win_point_player'}, inplace=True)
    df.rename(columns={'type': 'ball_types'}, inplace=True)
    df = df.iloc[:, [5, 4, 2, 3, 0, 1]]

    return df



def translate(input_df):
    """Translate from Chinese to English
    
    Input: dataframe
    Output: translated dataframe
    """
    
    ball_type_dictionary_path = "dictionary/ball_type_dictionary.json"
    with open(ball_type_dictionary_path, 'r', encoding="utf-8") as file:
        ball_type_dictionary = json.load(file)

    win_reason_dictionary_path = "dictionary/win_reason_dictionary.json"
    with open(win_reason_dictionary_path, 'r', encoding="utf-8") as file:
        win_reason_dictionary = json.load(file)

    lose_reason_dictionary_path = "dictionary/lose_reason_dictionary.json"
    with open(lose_reason_dictionary_path, 'r', encoding="utf-8") as file:
        lose_reason_dictionary = json.load(file)

    ouput_df = input_df

    for index in input_df.index:
        try:
            ouput_df["ball_types"][index] = ball_type_dictionary[input_df["ball_types"][index]]
        except:
            ouput_df["ball_types"][index] = "unknown"

        try:
            ouput_df["win_reason"][index] = win_reason_dictionary[input_df["win_reason"][index]]
        except:
            ouput_df["win_reason"][index] = "unknown"

        try:
            ouput_df["lose_reason"][index] = lose_reason_dictionary[input_df["lose_reason"][index]]
        except:
            ouput_df["lose_reason"][index] = "unknown"

    # print("ouput_df:", ouput_df)

    return ouput_df


def generate_answer(input_df, player_A, player_B):
    """Answer the questions by input data
    
    Input: dataframe
    Output: answer string
    """

    # Q1 & 2
    question_1 = "Q1: Which player won the game? How many points did the winner get?"
    question_2 = "Q2: Which player lost the game? How many points did the loser get?"

    winner = input_df.iloc[-1]["win_point_player"]
    if winner == "A":
        loser = "B"
        winner_name = player_A
        loser_name = player_B
    else:
        loser = "A"
        winner_name = player_B
        loser_name = player_A

    winner_points = input_df.iloc[-1][f"roundscore_{winner}"]
    loser_points = input_df.iloc[-1][f"roundscore_{loser}"]

    answer_1 = f"A1: {winner_name} won the game with {winner_points} points."
    answer_2 = f"A2: {loser_name} lost the game with {loser_points} points."

    # print(question_1)
    # print(answer_1)
    # print(question_2)
    # print(answer_2)

    # Q3
    question_3 = "Q3: When the winner won the game, which type of win reason showed up most frequently, and how many times did it show up?"

    winner_df = input_df[input_df["win_point_player"] == winner]
    win_reason_count = winner_df.value_counts("win_reason")
    # print(win_reason_count)

    win_count = win_reason_count.iloc[0]
    win_reason = win_reason_count.index[0]

    answer_3 = f"A3: {winner_name} got {win_count} points because {win_reason}."

    # print(question_3)
    # print(answer_3)

    # Q4
    question_4 = "Q4: When the loser lost the game, which type of lose reason showed up most frequently, and how many times did it show up?"

    loser_df = input_df[input_df["win_point_player"] == winner]
    lose_reason_count = loser_df.value_counts("lose_reason")
    # print(win_reason_count)

    lose_count = lose_reason_count.iloc[0]
    lose_reason = lose_reason_count.index[0]

    answer_4 = f"A4: {loser_name} lost {lose_count} points because {lose_reason}."

    # print(question_4)
    # print(answer_4)

    # Q5
    question_5 = "Q5: Which ball type did the winner get the most points with? How many points did the player get?"

    winner_df = input_df[(input_df["win_point_player"] == winner) & (
        input_df["win_reason"] == "wins by landing")]
    ball_types_count = winner_df.value_counts("ball_types")
    # print(win_reason_count)

    points = ball_types_count.iloc[0]
    ball_type = ball_types_count.index[0]

    answer_5 = f"A5: {winner_name} got {points} points by {ball_type}."

    # print(question_5)
    # print(answer_5)

    # Q6
    question_6 = "Q6: Which ball type did the loser lose the most points with? How many points did the player lose?"

    winner_df = input_df[(input_df["win_point_player"] == winner) & (
        input_df["win_reason"] != "wins by landing")]
    ball_types_count = winner_df.value_counts("ball_types")
    # print(win_reason_count)

    points = ball_types_count.iloc[0]
    ball_type = ball_types_count.index[0]

    answer_6 = f"A6: {loser_name} lose {points} points by {ball_type}."

    # print(question_6)
    # print(answer_6)

    # Q7
    question_7 = "Q7: Did the winner come from behind and win the game? If yes, which ball type did he use to overtake the lead? And what were the scores at that time?"

    yn = False
    loser_higher = False
    winner_higher = False
    for i in range(len(input_df)):
        row = input_df.iloc[i]
        roundscore_winner = row[f"roundscore_{winner}"]
        roundscore_loser = row[f"roundscore_{loser}"]

        if roundscore_loser > roundscore_winner:
            loser_higher = True

        if not winner_higher:
            if loser_higher:
                if roundscore_winner > roundscore_loser:
                    winner_higher = True
                    yn = True
                    score_A = row["roundscore_A"]
                    score_B = row["roundscore_B"]
                    ball_types = row["ball_types"]

    if yn:
        answer_7 = f"A7: Yes, {winner_name} used {ball_types} to overtake the lead at {score_A}:{score_B}."
    else:
        answer_7 = f"A7: No, {winner_name} did not come from behind."

    # print(question_7)
    # print(answer_7)

    # Q8
    question_8 = "Q8: How did the winner end the game?"

    last_round = input_df.iloc[-1]
    win_reason = last_round["win_reason"]
    ball_types = last_round["ball_types"]

    answer_8 = f"A8: {winner_name} ends the game because {win_reason} by {ball_types}."

    # print(question_8)
    # print(answer_8)

    answers = f"""
{question_1}
{answer_1}
{question_2}
{answer_2}
{question_3}
{answer_3}
{question_4}
{answer_4}
{question_5}
{answer_5}
{question_6}
{answer_6}
{question_7}
{answer_7}
{question_8}
{answer_8}"""

    return answers


def generate_news(answers, model):
    """Generate news
    
    Input: answers from generate_answer()
    Output: news generated by gpt-3.5-turbo
    """
    
    client = OpenAI()

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a journalist for badminton games. We will give you some details of a game between player A and player B. Please follow the details and write news for this game. You can only write news based on the details provided!"},
            {"role": "user", "content": f"Details: {answers}"}
        ]
    )

    news = completion.choices[0].message.content
    
    return news
