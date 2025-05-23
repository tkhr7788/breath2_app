from flask import Flask, render_template, request

app = Flask(__name__)

# 点数 → HFpEF 発症確率（%）
SCORE_TO_PROB = {
    0: 4,
    1: 4,
    2: 19,
    3: 19,
    4: 50,
    5: 50,
    6: 77,
    7: 77,
    8: 93,
    9: 93
}

def calc_breath2_score(form):
    score = 0

def classify_risk(score):
    if score >= 6:
        return "high"
    elif score >= 4:
        return "intermediate"
    else:
        return "low"

def calc_breath2_score(form):
    score = 0
    for fld, pts in {
        "age65": 2,
        "ntprobnp125": 2,
        "anemia": 1,
        "cad": 1,
        "af": 1,
        "cardiomegaly": 1,
        "lvh": 1,
    }.items():
        # form.get(fld) は "1", "2" などの文字列なので、存在チェックして int で加算
        if fld in form:
            score += int(form.get(fld))
    return score


@app.route("/", methods=["GET", "POST"])
def index():
    score = prob = risk = None
    msg = ""
    if request.method == "POST":
        score = calc_breath2_score(request.form)
        prob  = SCORE_TO_PROB.get(score, "N/A")
        risk  = classify_risk(score)

        if risk == "high":
            msg = "HFpEFの可能性 高"

    return render_template(
        "index.html",
        score=score,
        prob=prob,
        risk=risk,
        msg=msg
    )

if __name__ == "__main__":
    # Render の Python サービスはポートを自動割当てするため、
    # 環境変数 PORT が設定されている場合はそれを使う。
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
