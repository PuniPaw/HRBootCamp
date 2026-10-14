from flask import Flask, render_template, request, render_template_string, make_response, redirect, url_for
# redirect: 브라우저를 다른 url로 이동시키는(302) 리다이렉트 응답을 생성
# url_for: 라우트 함수 이름으로 url을 안전하게 생성
# render_template_string: 문자열로 작성한 jinja 템플릿을 렌더링해 html로 변환하는 함수

app = Flask(__name__);

# 간단 html text로 작성
HOME_HTML = """
    <h2>Flask Cookie Example</h2>
    <form action="/set_cookie" method="post">
        쿠키값: <input type="text" name="name" placeholder="ex: hong">
        <button type="submit">쿠키설정</button>
    </form>
    <p>
        <a href="/read_cookie">쿠키읽기</a>
        <a href="/delete_cookie">쿠키삭제</a>
    </p>
"""

@app.route("/")
def index():
    return render_template_string(HOME_HTML);

@app.post("/set_cookie")
def set_cookie():
    # 쿠키 저장
    irum = request.form.get("name")

    # 클라이언트에 쿠키를 심으려면 응답 객체가 필요
    # 먼저 "read_cookie"페이지로 이동하라는 302 리다이렉트 객체를 만들고
    # 그 응답에 따라 쿠키를 추가한 후 브라우저에 전송
    # response = make_response(redirect("/read_cookie")) # redirect 응답 생성
    response = make_response(redirect(url_for("read_cookie"))) # url_for로 라우트 함수 이름으로 url 생성
    response.set_cookie( # 쿠키 설정
        key = "name",   # 쿠키 이름
        value = irum,   # 사용자가 전송한 값을 쿠키에 저장
        max_age = 60*5, # 유효 시간 - 5분 뒤 만료
        httponly = True,   # 자바스크립트에서 쿠키 접근 불가
        samesite = "Lax"  # CSRF 공격 방지
    )
    return response # 쿠키가 포함된 응답을 브라우저로 반환
                    # 브라우저는 쿠키를 저장하고, redirect 요청에 따라 read_cookie로 다시 요청함

@app.get("/read_cookie")
def read_cookie():
    # 브라우저가 요청에 실어 보낸 모든 쿠키 중에서 내 서버가 만든 쿠키(name)을 꺼냄
    # 만약 없으면 none을 반환(첫 방문/만료/삭제된 경우)

    name = request.cookies.get("name") # 쿠키 읽기

    # 읽은 쿠키 html로 출력
    return f"""
        <h3>쿠키 읽기</h3>
        <p>쿠키 값: {name}</p>
        <p><a href="/">홈으로</a></p>
    """

@app.get("/delete_cookie")
def delete_cookie():
    # 쿠키 삭제 후 홈(/)으로 이동하기 위해 redirect 응답 객체를 생성하고, 쿠키를 만료시킨 후 브라우저로 전송
    response = make_response(redirect(url_for("index")))
    response.set_cookie("name", "", expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)