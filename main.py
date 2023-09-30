from flask import Flask, render_template, request, url_for
import argparse
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        img_name = request.form['images']
        image_file = url_for("static", filename=img_name)
        return render_template('index.html', img_list = img_list, img_name = img_name, img_data = image_file)
    else:
        return render_template('index.html', img_list = img_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Port of flask application", default=8001)
    parser.add_argument("--path", help="path to image dir", default="./")
    args = parser.parse_args()
    app.static_folder = args.path
    img_list = []
    for file in os.listdir(args.path):
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".avif"):
            img_list.append(file)
    app.run(debug=True, port=args.port)