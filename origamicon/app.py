from flask import Flask, render_template, request, send_file

import io
import base64 as b64

import generator

app = Flask(__name__)


def page(**kwargs):
    return render_template('main.html', **kwargs)


@app.route("/")
def home():
    return page()


@app.route("/", methods=['POST'])
def update_origamicon():
    text = request.form['origamicon-text']
    if not text:
        return page()

    buffer = io.BytesIO()
    origamicon = generator.create_origamicon(text)
    origamicon.save(buffer, format='PNG')
    image_data = buffer.getvalue()
    image_data = b64.b64encode(image_data).decode()
    image = 'data:;base64, {}'.format(image_data)

    return page(name=text, image=image)


@app.route("/<text>", methods=['GET'])
def load_origamicon(text):
    buffer = io.BytesIO()
    origamicon = generator.create_origamicon(text)
    origamicon.save(buffer, format='PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')


if __name__ == '__main__':
    app.run()
