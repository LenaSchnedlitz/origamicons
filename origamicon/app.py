from flask import Flask, render_template, request

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
def update_avatar():
    text = request.form['origamicon-text']
    if not text:
        return page()

    buffer = io.BytesIO()
    image = generator.create_origamicon(text)
    image.save(buffer, format='PNG')
    image_data = buffer.getvalue()
    image_data = b64.b64encode(image_data).decode()

    return page(name=text, image='data:;base64, {}'.format(image_data))


if __name__ == '__main__':
    app.run()
