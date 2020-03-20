from flask import Flask, jsonify, request

app = Flask(__name__)
app.users = {}
app.id_count = 1
app.tweets = {}
# 그냥 유저 정보에 팔로워 아이디 집합을 추가하면 될 듯


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

@app.route("/sign-up", methods=['POST'])  #method's'
def sign_up():
    new_user = request.json   # 새로운 아이디 객체 들어옴 (request를 통해 json 양식으로 - 이를 파이썬 딕셔너리 형식으로 변환)
    new_user["id"] = app.id_count  #아이디라는 새로운 객체 속성 설정 후 아이디값 삽입
    app.users[app.id_count] = new_user   #이것은 인덱스 + 1 에 새로운 유저를 딕셔너리에 저장!
    app.id_count = app.id_count + 1     #새로운 아이디 삽입을 대비해 미리 아이디 값 + 1 해둠

    return jsonify(new_user)  #json으로 전송

@app.route("/sendtweet", methods=['POST'])
def send_tweet():
    new_tweet = request.json
    user_id = int(new_tweet["user_id"])  # 유저 아이디를 받아올 때는 정수 값으로 변환 작업 나중에는 안해도 되겠지?
    tweet = new_tweet["tweet"]

    if len(tweet) > 300:
        return "300자 넘음 ㅋㅋ", 400
    
    if user_id not in app.users:
        return "유저 아이디 없음 ㅋㅋ", 400
    
    # app.id_tw_count = app.id_tw_count + 1   ==> 이건 필요없음 어차피 우저 아이디 하나로만 할거라
    app.tweets.update({   #새로운 트윗 객체를 저장한다, 딕셔너리에는 append가 없다 대신 update 이용!!!!
        'user_id': user_id,
        'tweet': tweet
    })
    return "성공", 200   #그냥 성공했음울 알린다?


@app.route("/follow", methods=['POST'])  #자꾸 메소드s에서 s 빼먹는다
def followup():  # 당연히 팔로우니까 대상과 팔로워를 특정해야 한다
    follow_info = request.json
    target = int(follow_info["target_id"])
    follower = int(follow_info["follower_id"])
    if target not in app.users:
        return "u cant follow unregistered user", 400
    if follower not in app.users:
        return "no user found", 400
     # 여기서는 반환해야하는건 성공 메세지도 좋지만 확인을 위해 user가 업데이트된 정보를 보여준다
    target_user = app.users[target] #내가 아직 파이선 딕셔너리 자료형에 대해 이해가 부족하다 더 검색해서 공부하자

    target_user.setdefault("follower", set()).add(follow_info["follower_id"]) # 그런데 굳이 이렇게 set을 사용하는 번거로움이 필요한가? 그냥 불린 타입으로 관리하면 안되는가?
    return jsonify(target_user)