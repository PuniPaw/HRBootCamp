from flask import Flask, render_template, request, make_response, redirect, url_for

app = Flask(__name__);

@app.route("/")
def index():
    return render_template("index.html");

# @app.route("/login", methods=["GET", "POST"])
# def loginFunc():
#     name = request.cookies.get("name")
#     visits = request.cookies.get("visits")

#     if name:
#         visits = int(visits or "0") + 1
#         message = f"안녕하세요, {name}님! {visits}번째 방문입니다."
#     else:
#         visits = None
#         message = "이름을 입력하면 방문 횟수를 쿠키로 기억합니다"

#         response = make_response(render_template("login.html", message=message, name=name, visits=visits))

#         if name:
#             response.set_cookie("visits", str(visits), max_age=60*5, httponly=True, samesite="Lax")

    # return response

@app.route("/login", methods=["GET", "POST"])
def loginFunc():
    # 로그인 처리 (POST)
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        response = make_response(redirect(url_for("loginFunc")))
        if name:
            response.set_cookie("name", name, max_age=60*5, httponly=True, samesite="Lax")
            response.set_cookie("visits", "0", max_age=60*5, httponly=True, samesite="Lax")
        return response

    # 화면 표시 (GET)
    name = request.cookies.get("name")
    visits = None

    if name:
        visits = int(request.cookies.get("visits") or "0") + 1
        message = f"안녕하세요, {name}님! {visits}번째 방문입니다."
    else:
        message = "이름을 입력하면 방문 횟수를 쿠키로 기억합니다"

    response = make_response(render_template("login.html", message=message, name=name, visits=visits))
    if name:
        response.set_cookie("visits", str(visits), max_age=60*5, httponly=True, samesite="Lax")
    return response

@app.post("/login")
def loginFunc2():
    name = (request.form.get("name") or "").strip()
    response = make_response(redirect(url_for("loginFunc")))
    response.set_cookie("name", name, max_age=60*5, httponly=True, samesite="Lax")
    response.set_cookie("visits", "0", max_age=60*5, httponly=True, samesite="Lax")
    return response

@app.post("/logout")
def logoutFunc():
    response = make_response(redirect(url_for("loginFunc")))
    response.delete_cookie("name")
    response.delete_cookie("visits")
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)