# cgi-bin/world.py: 웹 용 파이썬
import sys
sys.stdout.reconfigure(encoding="utf-8")    # 한글 깨짐 방지

v1 = "자료1"
v2 = "두 번째 자료"

# 클라이언트 브라우저로 파이썬 처리 값 출력
print("Content-Type:text/html; charset=utf-8")
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>메인</title>
</head>
<body>
    <b>world 페이지</b>
    <br/>
    자료 출력: {0}, {1}
    <br/>
    <img src="../images/image.jpeg"/>
    <br/>
    <a href="../index.html">메인으로</a>
</body>
</html>
""".format(v1, v2)
)