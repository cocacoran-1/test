from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import random
import json
import os

# Flask 앱 초기화
app = Flask(
    __name__,
    template_folder="../templates",  # 템플릿 경로
    static_folder="../static"        # 정적 파일 경로
)

app.secret_key = "your_secret_key"  # 세션 암호화 키

# JSON 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'categories.json')

# JSON 파일 로드 함수
def load_categories():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# 초기 데이터 로드
categories = load_categories()

@app.route('/')
def home():
    """
    메인 페이지: 카테고리와 데이터를 전달
    """
    # 각 카테고리의 닉네임을 정렬
    sorted_categories = {category: sorted(nicknames) for category, nicknames in categories.items()}
    category_list = list(categories.keys())

    # 전체 참가자 수 계산
    total_participants = sum(len(nicknames) for nicknames in categories.values())

    return render_template(
        'index.html',
        categories=sorted_categories,
        category_list=category_list,
        total_participants=total_participants
    )


@app.route('/generate_teams', methods=['POST'])
def generate_teams():
    """
    팀 생성 페이지: 선택된 카테고리에서 팀 구성
    """
    selected_category = request.form.get('category')  # 선택된 카테고리
    chosen_nicknames = categories.get(selected_category, [])  # 해당 카테고리의 닉네임 목록

    n = len(chosen_nicknames)
    if n < 3:
        return "팀을 생성할 충분한 인원이 없습니다!", 400

    # 팀 구성 로직
    team_size = 3  # 한 팀당 인원 수
    max_teams = 8  # 최대 팀 수

    if n >= team_size * max_teams:
        selected_people = random.sample(chosen_nicknames, team_size * max_teams)
        num_teams = max_teams
    else:
        selected_people = chosen_nicknames
        num_teams = n // team_size

    # 참가자 무작위 섞기
    random.shuffle(selected_people)

    # 팀 나누기
    teams = [selected_people[i * team_size:(i + 1) * team_size] for i in range(num_teams)]

    # 잔여 인원 분배
    remainder = len(selected_people) % team_size
    if remainder != 0:
        for i, person in enumerate(selected_people[-remainder:]):
            teams[i % num_teams].append(person)

    # 남은 사람 리스트 저장
    session['remaining_people'] = [p for p in chosen_nicknames if p not in selected_people]
    session['current_teams'] = teams

    return render_template(
        'teams.html',
        teams=teams,
        selected_category=selected_category,
        enumerate=enumerate  # Jinja2 템플릿에서 enumerate 사용 가능
    )


@app.route('/add_data', methods=['POST'])
def add_data():
    global categories

    # 요청 데이터 디버그 출력
    print("요청 데이터:", request.form)

    category = request.form.get('category')
    nicknames = request.form.get('nicknames')

    if not category or not nicknames:
        print("카테고리 또는 닉네임이 비어 있음")
        return jsonify({"message": "카테고리와 닉네임을 입력해주세요.", "status": "error"}), 400

    nickname_list = [name.strip() for name in nicknames.split('/') if name.strip()]
    print("추가할 닉네임:", nickname_list)

    if category in categories:
        duplicate_nicknames = [name for name in nickname_list if name in categories[category]]
        if duplicate_nicknames:
            print("중복된 닉네임:", duplicate_nicknames)
            return jsonify({"message": f"중복된 닉네임: {', '.join(duplicate_nicknames)}", "status": "error"}), 400

        # 중복되지 않은 닉네임 추가
        categories[category].extend(nickname_list)
        categories[category] = list(set(categories[category]))

        # JSON 파일 저장
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)

        return jsonify({"message": "데이터가 성공적으로 추가되었습니다.", "status": "success"}), 200

    return jsonify({"message": "유효하지 않은 카테고리입니다.", "status": "error"}), 400

@app.route('/add_to_team', methods=['POST'])
def add_to_team():
    """
    기존 팀에 추가로 사람을 뽑기
    """
    additional_count = int(request.form.get('additional_count', 0))

    if 'current_teams' not in session or 'remaining_people' not in session:
        return jsonify({"status": "error", "message": "기존 팀 정보가 없습니다. 먼저 추첨을 진행하세요."})

    current_teams = session['current_teams']
    remaining_people = session['remaining_people']

    if not remaining_people:
        return jsonify({"status": "error", "message": "추가로 뽑을 사람이 없습니다."})

    additional_people = random.sample(remaining_people, min(additional_count, len(remaining_people)))

    # 기존 팀에 추가 인원 분배
    for i, person in enumerate(additional_people):
        current_teams[i % len(current_teams)].append(person)

    # 남은 사람 업데이트
    session['remaining_people'] = list(set(remaining_people) - set(additional_people))
    session['current_teams'] = current_teams

    return jsonify({"status": "success", "message": f"{len(additional_people)}명이 추가되었습니다.", "teams": current_teams})
    
@app.route('/delete_data', methods=['POST'])
def delete_data():
    """
    선택된 닉네임 삭제
    """
    global categories
    category = request.form.get('category')
    nickname = request.form.get('nickname')

    if category in categories and nickname in categories[category]:
        categories[category].remove(nickname)

        # JSON 파일 업데이트
        with open(JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(categories, f, ensure_ascii=False, indent=2)

        # JSON 파일 다시 로드
        categories = load_categories()

        return redirect(url_for('home'))
    else:
        return "잘못된 요청입니다.", 400

@app.route('/update_team', methods=['POST'])
def update_team():
    """
    특정 인원을 제거하고, 부족한 팀에 새로운 인원을 추가
    """
    remove_people = request.json.get('remove_people', [])  # 제거할 인원 리스트

    # 기존 팀과 남은 사람 정보 가져오기
    if 'current_teams' not in session or 'remaining_people' not in session:
        return jsonify({"status": "error", "message": "기존 팀 정보가 없습니다. 먼저 추첨을 진행하세요."})

    current_teams = session['current_teams']
    remaining_people = session['remaining_people']

    # 1. 팀에서 제거할 인원 삭제
    updated_teams = []
    for team in current_teams:
        updated_team = [member for member in team if member not in remove_people]
        updated_teams.append(updated_team)

    # 2. 남은 사람 업데이트
    updated_remaining_people = remaining_people + remove_people

    # 3. 부족한 팀에 새로운 인원을 추가
    for team in updated_teams:
        while len(team) < 3 and updated_remaining_people:
            new_member = updated_remaining_people.pop(0)  # 남은 사람에서 추가
            team.append(new_member)

    # 4. 세션 데이터 업데이트
    session['current_teams'] = updated_teams
    session['remaining_people'] = updated_remaining_people

    return jsonify({
        "status": "success",
        "message": "팀이 성공적으로 업데이트되었습니다.",
        "teams": updated_teams,
    })


@app.route('/save_team', methods=['POST'])
def save_team():
    try:
        # 제목 확인
        title = request.form.get('title')
        if not title:
            return jsonify({"status": "error", "message": "제목을 입력해주세요."}), 400

        # 저장 경로
        save_path = os.path.join(BASE_DIR, 'saved_teams.json')

        # JSON 파일 초기화 또는 읽기
        if not os.path.exists(save_path):
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

        with open(save_path, 'r', encoding='utf-8') as f:
            saved_teams = json.load(f)

        # `saved_teams`가 딕셔너리인지 확인
        if not isinstance(saved_teams, dict):
            saved_teams = {}

        # 중복 제목 확인
        if title in saved_teams:
            return jsonify({"status": "error", "message": "이미 존재하는 제목입니다."}), 400

        # 데이터 저장
        saved_teams[title] = {
            "teams": session.get('current_teams', []),
            "remaining_people": session.get('remaining_people', [])
        }

        # JSON 파일 쓰기
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(saved_teams, f, ensure_ascii=False, indent=2)

        return jsonify({"status": "success", "message": f"'{title}'로 저장되었습니다."}), 200
    except Exception as e:
        print(f"[ERROR] 저장 중 오류 발생: {str(e)}")
        return jsonify({"status": "error", "message": "저장 중 오류가 발생했습니다."}), 500
        


@app.route('/saved_teams', methods=['GET'])
def saved_teams():
    try:
        save_path = os.path.join(BASE_DIR, 'saved_teams.json')
        print(f"[DEBUG] 저장된 팀 경로: {save_path}")

        if not os.path.exists(save_path):
            print("[DEBUG] 저장된 팀 파일이 없습니다.")
            return jsonify({"teams": []})  # 저장된 팀이 없으면 빈 리스트 반환

        with open(save_path, 'r', encoding='utf-8') as f:
            saved_teams = json.load(f)
            print(f"[DEBUG] 저장된 팀 데이터: {saved_teams}")

        return jsonify({"teams": list(saved_teams.keys())})  # 제목 목록 반환
    except Exception as e:
        print(f"[ERROR] 저장된 팀 로드 중 오류 발생: {str(e)}")
        return jsonify({"teams": []}), 500

@app.route('/load_team/<title>', methods=['GET'])
def load_team(title):
    save_path = os.path.join(BASE_DIR, 'saved_teams.json')
    print(f"[DEBUG] 불러오기 요청 제목: {title}")
    print(f"[DEBUG] 저장된 파일 경로: {save_path}")

    # 파일 존재 여부 확인
    if not os.path.exists(save_path):
        print("[ERROR] 저장된 팀 파일이 없습니다.")
        return jsonify({"status": "error", "message": "저장된 데이터가 없습니다."}), 404

    # JSON 파일 읽기
    with open(save_path, 'r', encoding='utf-8') as f:
        saved_teams = json.load(f)
        print(f"[DEBUG] 저장된 팀 목록: {list(saved_teams.keys())}")

    # 요청 제목 확인
    if title not in saved_teams:
        print(f"[ERROR] 요청된 제목 '{title}'이 저장된 데이터에 없습니다.")
        return jsonify({"status": "error", "message": "존재하지 않는 제목입니다."}), 404

    # 세션 데이터 설정
    session['current_teams'] = saved_teams[title]['teams']
    session['remaining_people'] = saved_teams[title]['remaining_people']

    return render_template('teams.html', teams=session['current_teams'], enumerate=enumerate)


@app.route('/delete_team/<title>', methods=['DELETE'])
def delete_team(title):
    """
    제목에 해당하는 팀 데이터를 삭제
    """
    save_path = os.path.join(BASE_DIR, 'saved_teams.json')
    if not os.path.exists(save_path):
        return jsonify({"status": "error", "message": "저장된 데이터가 없습니다."}), 404

    with open(save_path, 'r', encoding='utf-8') as f:
        saved_teams = json.load(f)

    if title not in saved_teams:
        return jsonify({"status": "error", "message": "존재하지 않는 제목입니다."}), 404

    # 데이터 삭제
    del saved_teams[title]

    # JSON 파일 업데이트
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(saved_teams, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "success", "message": f"'{title}'이 삭제되었습니다."})



if __name__ == '__main__':
    app.run(debug=True)
