from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

bingo_num = [0]
bingo_cards = []
max_bingo_ball = 75


@app.route('/')
def index():
    user_msg = {}
    user_msg['err_msg'] = ''
    return render_template('index.html',message = user_msg)

@app.route('/ball')
def ball():
    user_msg = {}
    user_msg['err_msg'] = ''
    user_msg['get_ball'] = str(bingo_num[-1])
    get_ball_count = len(bingo_num) - 1
    user_msg['ball_count'] = str(get_ball_count)
    bingo_usr_cnt = 0
    reach_usr_cnt = 0
    for index_u in range(len(bingo_cards)):
        if bingo_cards[index_u][0][3] == get_ball_count :
            bingo_usr_cnt += 1
        if bingo_cards[index_u][0][2] > 0 :
            reach_usr_cnt += 1
    user_msg['bingo_user_count'] = str(bingo_usr_cnt)
    user_msg['reach_user_count'] = str(reach_usr_cnt)
    return render_template('ball.html',message = user_msg)

@app.route('/list_ball')
def list_ball():
    global bingo_cards
    global bingo_num
    user_msg = {}
    user_msg['err_msg'] = ''
    user_msg['bingo_num'] = str(bingo_num)
    return render_template('list_ball.html',message = user_msg)

@app.route('/list_user')
def list_user():
    global bingo_cards
    global bingo_num
    user_msg = []
    
    bingo_card_sort = sorted(bingo_cards, key=lambda x: x[0][3], reverse=True)

    for index_u in range(len(bingo_card_sort)):
        user_list = {}
        user_list['user_name'] = bingo_card_sort[index_u][0][0]
        user_list['bingo_count'] = bingo_card_sort[index_u][0][3]
        user_msg.append(user_list)
    
    return render_template('list_user.html',message = user_msg)

@app.route('/get_ball')
def get_ball():
    global bingo_cards
    global bingo_num
    user_msg = {}
    user_msg['err_msg'] = ''
    user_msg['get_ball'] = '0'
    user_msg['ball_count'] = '0'
    user_msg['bingo_user_count'] = '0'
    user_msg['reach_user_count'] = '0'
    get_ball_count = ''
    bingo_usr_cnt = 0
    reach_usr_cnt = 0

    if len(bingo_num) == max_bingo_ball + 1:
        user_msg['err_msg'] = "抽選終了"
        user_msg['get_ball'] = bingo_num[-1]
        return render_template('ball.html',message = user_msg)

    while True:
        get_bingo_ball = int(np.random.rand()*75)+1
        if get_bingo_ball in bingo_num:
            continue
        else:
            bingo_num.append(get_bingo_ball)
            break

    get_ball_count = len(bingo_num) - 1

# 各BINGOカードの当選調査
    for index_u in range(len(bingo_cards)):
        for index_x in range(5):
            for index_y in range(5):
                if get_bingo_ball == bingo_cards[index_u][1][index_x][index_y]:
                    bingo_cards[index_u][2][index_x][index_y] = 1

# 各BINGOカードの立直・BINGO調査
    for index_u in range(len(bingo_cards)):
        z1 = 0
        z2 = 0
        x = np.sum(bingo_cards[index_u][2] ,axis=0 )
        y = np.sum(bingo_cards[index_u][2] ,axis=1 )

        for index_x in range(5):
            for index_y in range(5):
                if index_x == index_y:
                    z1 += bingo_cards[index_u][2][index_x][index_y]
                if index_x == 4 - index_y:
                    z2 += bingo_cards[index_u][2][index_x][index_y]

        user_reach = np.count_nonzero(x == 4) + np.count_nonzero(y == 4)
        if z1 == 4 :
            user_reach += 1
        if z2 == 4 :
            user_reach += 1
        user_bingo = np.count_nonzero(x == 5) + np.count_nonzero(y == 5)
        if z1 == 5 :
            user_bingo += 1
        if z2 == 5 :
            user_bingo += 1

        bingo_cards[index_u][0][1] = user_bingo
        bingo_cards[index_u][0][2] = user_reach

        if bingo_cards[index_u][0][1] > 0 and bingo_cards[index_u][0][3] == 0 :
            bingo_cards[index_u][0][3] = get_ball_count

    for index_u in range(len(bingo_cards)):
        if bingo_cards[index_u][0][3] == get_ball_count :
            bingo_usr_cnt += 1
        if bingo_cards[index_u][0][2] > 0 :
            reach_usr_cnt += 1

    user_msg['get_ball'] = str(get_bingo_ball)
    user_msg['ball_count'] = str(get_ball_count)
    user_msg['bingo_user_count'] = str(bingo_usr_cnt)
    user_msg['reach_user_count'] = str(reach_usr_cnt)
    return render_template('ball.html',message = user_msg)

@app.route('/card')
def card():
    name = str(bingo_cards)
    return name

@app.route('/card_input', methods=["POST", "GET"])
def card_input():
    global bingo_cards
    user_card = []
    user_card_temp = []
    user_msg = {}
    user_msg['user_name'] = ''
    user_msg['error_msg'] = ''
    user_msg['row_b'] = []
    user_msg['row_i'] = []
    user_msg['row_n'] = []
    user_msg['row_g'] = []
    user_msg['row_o'] = []

    if request.method == "GET":
        return render_template('card_input.html',message = user_msg)

    else:
        if request.form["user_name"] == "":
            user_msg['error'] = "お名前がありません。"
            return render_template('card_input.html',message = user_msg)

        else:
            try:
               if request.form["submit"] == "カードを作る":

                   user_card = []
                   i = 0
                   j = 0
                   while i < 5:
                       row_list = []
                       while j < 5:
                           get_number = int(np.random.rand()*15)+1 +(15 * i)
                           if get_number in row_list:
                               continue
                           else:
                               row_list.append(get_number)
                           j += 1
                       j = 0
                       user_card.append(row_list)
                       i += 1
                   user_msg = {}
                   user_msg['user_name'] = request.form["user_name"]
                   user_msg['row_b'] = user_card[0]
                   user_msg['row_i'] = user_card[1]
                   user_msg['row_n'] = user_card[2]
                   user_msg['row_g'] = user_card[3]
                   user_msg['row_o'] = user_card[4]

                   for index in range(len(bingo_cards)):
                       if request.form["user_name"] == bingo_cards[index][0][0] :
                           user_msg['error'] = "★同じお名前があります★"

                   return render_template('card_input.html', message=user_msg)

               elif request.form["submit"] == "登録する":

                   user_card.append([request.form["user_name"],0,0,0])
                   user_card_temp.append([int(request.form["B1"]),int(request.form["B2"]),int(request.form["B3"]),int(request.form["B4"]),int(request.form["B5"]) ])
                   user_card_temp.append([int(request.form["I1"]),int(request.form["I2"]),int(request.form["I3"]),int(request.form["I4"]),int(request.form["I5"]) ])
                   user_card_temp.append([int(request.form["N1"]),int(request.form["N2"]),int(request.form["N3"]),int(request.form["N4"]),int(request.form["N5"]) ])
                   user_card_temp.append([int(request.form["G1"]),int(request.form["G2"]),int(request.form["G3"]),int(request.form["G4"]),int(request.form["G5"]) ])
                   user_card_temp.append([int(request.form["O1"]),int(request.form["O2"]),int(request.form["O3"]),int(request.form["O4"]),int(request.form["O5"]) ])
                   user_card.append(user_card_temp)
                   user_card_temp = []
                   user_card_temp.append([0,0,0,0,0])
                   user_card_temp.append([0,0,0,0,0])
                   user_card_temp.append([0,0,1,0,0])
                   user_card_temp.append([0,0,0,0,0])
                   user_card_temp.append([0,0,0,0,0])
                   user_card.append(user_card_temp)
                   
                   user_msg = {}
                   user_msg['user_name'] = request.form["user_name"]
                   user_msg['row_b'] = user_card[1][0]
                   user_msg['row_i'] = user_card[1][1]
                   user_msg['row_n'] = user_card[1][2]
                   user_msg['row_g'] = user_card[1][3]
                   user_msg['row_o'] = user_card[1][4]

                   for index in range(len(bingo_cards)):
                       if request.form["user_name"] == bingo_cards[index][0][0] :
                           user_msg['error'] = "★同じお名前があります★"
                           return render_template('card_input.html', message=user_msg)

                   num_count = 0
                   for index_x in range(5):
                       for index_y in range(5):
                           for index_z in range(5):
                               if user_card[1][index_z].count(user_card[1][index_x][index_y]) > 0 :
                                   num_count +=1
                   if num_count > 25 :
                       user_msg['error']= "★同じ数字があります★"
                       return render_template('card_input.html',message=user_msg)
                   
                   for index in range(len(bingo_cards)):
                       if user_card[1] == bingo_cards[index][1] :
                           user_msg['error'] = "★同じBINGOカードがあります★"
                           return render_template('card_input.html', message=user_msg)

                   bingo_cards.append(user_card)
                   return render_template('card_list_301.html',u_name = request.form["user_name"] )

               else:
                   pass
                   user_msg['error']= "★想定外の入力です★"
                   return render_template('card_input.html',message=user_msg)
            except:
                user_msg = {}
                user_msg['error'] = "処理に異常が起こりました"
                return render_template('card_input.html',message = user_msg)


@app.route('/card_list')
def card_list():
    username = request.args.get('user_name')
    global bingo_cards
    user_msg = {}
    user_msg['user_name'] = '　'
    user_msg['error_msg'] = '　'
    user_msg['row_b'] = ['　','　','　','　','　']
    user_msg['row_i'] = ['',' ',' ',' ',' ']
    user_msg['row_n'] = [' ',' ',' ',' ',' ']
    user_msg['row_g'] = [' ',' ',' ',' ',' ']
    user_msg['row_o'] = [' ',' ',' ',' ',' ']
    user_msg['row_b_a'] = [' ',' ',' ',' ',' ']
    user_msg['row_i_a'] = [' ',' ',' ',' ',' ']
    user_msg['row_n_a'] = [' ',' ',' ',' ',' ']
    user_msg['row_g_a'] = [' ',' ',' ',' ',' ']
    user_msg['row_o_a'] = [' ',' ',' ',' ',' ']
    for index in range(len(bingo_cards)):
        if username == bingo_cards[index][0][0] :
            user_msg['user_name'] = bingo_cards[index][0][0]
            user_msg['user_bingo'] = bingo_cards[index][0][1]
            user_msg['user_reach'] = bingo_cards[index][0][2]
            user_msg['user_bingo_no'] = bingo_cards[index][0][3]
            user_msg['row_b'] = bingo_cards[index][1][0]
            user_msg['row_i'] = bingo_cards[index][1][1]
            user_msg['row_n'] = bingo_cards[index][1][2]
            user_msg['row_g'] = bingo_cards[index][1][3]
            user_msg['row_o'] = bingo_cards[index][1][4]
            user_msg['row_b_a'] = bingo_cards[index][2][0]
            user_msg['row_i_a'] = bingo_cards[index][2][1]
            user_msg['row_n_a'] = bingo_cards[index][2][2]
            user_msg['row_g_a'] = bingo_cards[index][2][3]
            user_msg['row_o_a'] = bingo_cards[index][2][4]

    return render_template('card_list.html', message = user_msg)




## おまじない
if __name__ == "__main__":
    app.run(debug=True, threaded=True)

