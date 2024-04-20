import pandas
from prompt import generate_answer

def csv_preprocess(filename):
    data = pandas.read_csv(filename)
    df = pandas.DataFrame(data)

    # df = df.drop(columns=['rally','ball_round','time','frame_num','end_frame_num','server','aroundhead',
    #                 'backhand','hit_height','hit_area','hit_x','hit_y','landing_height','landing_area','landing_x','landing_y',
    #                 'flaw','player_location_area','player_location_x','player_location_y','opponent_location_area',
    #                 'opponent_location_x','opponent_location_y','db','player'])
    for i in df:
        if i not in ['getpoint_player','win_reason','type','lose_reason','roundscore_A','roundscore_B']:
            #print(i)
            df = df.drop(columns=[i])
 
    for j,i in enumerate(df['getpoint_player']):
        if i != 'A' and i != 'B':
            df = df.drop([j])

    df.rename(columns = {'getpoint_player':'win_point_player'}, inplace = True) 
    df.rename(columns = {'type':'ball_types'}, inplace = True) 
    df = df.iloc[:, [5,4,2,3,0,1]]

    df.to_csv('out_test.csv', index=False)

    a1,a2,a3,a4,a5,a6,a7,a8 = generate_answer(df)
    print(a1)
    print(a2)
    print(a3)
    print(a4)
    print(a5)
    print(a6)
    print(a7)
    print(a8)
    #path = 'ans.txt'

if __name__ == '__main__':
    csv_preprocess(
        'data/An_Se_Young_Ratchanok_Intanon_YONEX_Thailand_Open_2021_QuarterFinals/set1.csv')
