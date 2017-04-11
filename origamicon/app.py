from flask import Flask, render_template, request, make_response

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("landing.html")


@app.route("/", methods=["POST"])
def update_avatar():
    text = request.form["text"]
    if not text:
        return render_template("landing.html")

    import generator as gen

    image = gen.get_image(text)

    return render_template("main.html", name=text)

if __name__ == "__main__":
    app.run()
