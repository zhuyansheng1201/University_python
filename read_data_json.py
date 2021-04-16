import json
import csv
import time

# 操作するjsonの名前
in_name = 'demo_json'

# 始まるドン！！
try:
    # Jsonを開く
    with open('data/'+in_name+'.json', "r", encoding='utf-8') as myd:
        md = json.load(myd)

# 処理するjsonが見つからない場合
except FileNotFoundError:
    text = '-'
    print(text.center(30, '-'))
    print('ファイル名'+in_name+'が見つかりません')
    print(text.center(30, '-'))

else:
    # 整理が終わったjsonの名前を定義する
    out_time = str(time.strftime("%m%d_%H%M%S", time.localtime()))
    out_name = in_name + '_' + out_time + 'f.csv'

    # 数例を指定する
    button = ['']
    reward1 = ['']
    reward2 = ['']
    feedback1 = ['']
    feedback2 = ['']
    answer_happy = ['']
    happiness = []
    f_reward = []
    left = ["0", "1"]
    right = ["2", "3", "4", "5", "6"]
    Trial = 0
    trial = ['']

    for dic in md:
        if "button_pressed" in dic:
            # 何番目の試行かを記入
            Trial += 1
            trial.append(Trial)
            # 選択したボタン
            button.append(dic["button_pressed"])
            # 見せた刺激
            reward1.append(dic["reward_s01"])
            reward2.append(dic["reward_s02"])
            feedback1.append((dic["feedback01"]))
            feedback2.append((dic["feedback02"]))
            # 気持ち
            answer_happy.append("")
        elif "response" in dic:
            answer_happy.pop()
            answer_happy.append((dic["response"]))

    # データ欠損の場合、50を入れる
    for i in answer_happy:
        if type(i) is str:
            happiness.append(i)
        else:
            happiness.append(50)

    # どっちのデータを採用するか判断する
    n = 0
    for i in button:
        if i in left:
            f_reward.append(reward1[n])
            n += 1
        elif i in right:
            f_reward.append(reward2[n])
            n += 1
        else:
            f_reward.append(feedback2[n])
            n += 1

    # データの形整理
    def beauty():
        del trial[0]
        del reward1[0]
        del reward2[0]
        del feedback1[0]
        del feedback2[0]
        del f_reward[0]
        del happiness[1]
    beauty()
    trial = trial[:150]
    for i in range(4):
        del reward1[0]
        del reward2[0]
        del feedback1[0]
        del feedback2[0]
        del f_reward[0]
    for i in range(4):
        del happiness[1]

    # 実験上　CR　EV　RPE　が必要とされたので、追加する
    CR = []
    EV = []
    RPE = []
    for i in range(150):
        if f_reward[i] == reward1[i]:
            CR.append(reward1[i])
            EV.append(0)
            RPE.append(0)
        else:
            CR.append(0)
            EV.append((float(feedback1[i])+float(feedback2[i]))/2)
            RPE.append(float(f_reward[i]) - (float(feedback1[i]) + float(feedback2[i]))/2)

    # csvに書き込み
    with open('data/' + out_name, 'w', newline='') as f:
        myWriter = csv.writer(f)
        myWriter.writerow(['Trial', 'reward1', 'reward2',
                           'feedback1', 'feedback2', 'f_reward',
                           'happiness', 'CR', 'EV', 'RPE'])
        for i in range(len(trial)):
            myWriter.writerow([trial[i], reward1[i], reward2[i],
                               feedback1[i], feedback2[i],
                               f_reward[i], happiness[i],
                               CR[i], EV[i], RPE[i]])

    text = '-'
    text_f = '処理終了'
    print(text_f.center(30, '-'))
    print('綺麗なデータになったよ～')
    print('試行回数:', len(trial))
    print('ファイルへの名は', out_name)
    print(text.center(30, '-'))
