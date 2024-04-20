import pandas

def generate_answer(input_df):
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
    else:
        loser = "A"

    winner_points = input_df.iloc[-1][f"roundscore_{winner}"]
    loser_points = input_df.iloc[-1][f"roundscore_{loser}"]

    answer_1 = f"A1: Player {winner} won the game with {winner_points} points."
    answer_2 = f"A2: Player {loser} lost the game with {loser_points} points."

    # print(question_1)
    # print(answer_1)
    # print(question_2)
    # print(answer_2)

    # Q3
    question_3 = "Q3: When the winner won the game, which type of win_reason showed up most frequently, and how many times did it show up?"

    winner_df = input_df[input_df["win_point_player"] == winner]
    win_reason_count = winner_df.value_counts("win_reason")
    # print(win_reason_count)

    win_count = win_reason_count.iloc[0]
    win_reason = win_reason_count.index[0]

    answer_3 = f"A3: The winner got {win_count} points because {win_reason}."

    # print(question_3)
    # print(answer_3)

    # Q4
    question_4 = "Q4: When the loser lost the game, which type of lose_reason showed up most frequently, and how many times did it show up?"

    loser_df = input_df[input_df["win_point_player"] == winner]
    lose_reason_count = loser_df.value_counts("lose_reason")
    # print(win_reason_count)

    lose_count = lose_reason_count.iloc[0]
    lose_reason = lose_reason_count.index[0]

    answer_4 = f"A4: The loser lost {lose_count} points because {lose_reason}."

    # print(question_4)
    # print(answer_4)

    # Q5
    question_5 = "Q5: Which ball_type did the winner get the most points with? How many points did the player get?"

    winner_df = input_df[(input_df["win_point_player"] == winner) ]#& (input_df["win_reason"] == "wins by landing")]
    #print(winner_df)
    ball_types_count = winner_df.value_counts("ball_types")
    # print(win_reason_count)

    points = ball_types_count.iloc[0]
    ball_type = ball_types_count.index[0]

    answer_5 = f"A5: The winner got {points} points by {ball_type}."

    # print(question_5)
    # print(answer_5)

    # Q6
    question_6 = "Q6: Which ball_type did the loser lose the most points with? How many points did the player lose?"

    winner_df = input_df[(input_df["win_point_player"] == winner) & (
        input_df["win_reason"] != "wins by landing")]
    ball_types_count = winner_df.value_counts("ball_types")
    # print(win_reason_count)

    points = ball_types_count.iloc[0]
    ball_type = ball_types_count.index[0]

    answer_6 = f"A6: The loser lose {points} points by {ball_type}."

    # print(question_6)
    # print(answer_6)

    # Q7
    question_7 = "Q7: Did the winner come from behind and win the game? If yes, which ball_type did he use to overtake the lead? And what were the scores at that time?"

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
        answer_7 = f"A7: Yes, the player {winner} used {ball_types} to overtake the lead at {score_A}:{score_B}."
    else:
        answer_7 = f"A7: No, the player {winner} did not come from behind."

    # print(question_7)
    # print(answer_7)

    # Q8
    question_8 = "Q8: How did the winner end the game?"

    last_round = input_df.iloc[-1]
    win_reason = last_round["win_reason"]
    ball_types = last_round["ball_types"]

    answer_8 = f"A8: The winner ends the game because {win_reason} by {ball_types}."

    # You are a journalist for badminton games. We will give you some details of a game between player A and player B. Please follow the details and write news for this game. You can only write news based on the details provided!

    return answer_1,answer_2,answer_3,answer_4,answer_5,answer_6,answer_7,answer_8