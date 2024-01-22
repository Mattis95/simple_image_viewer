from flask import Flask, render_template, request, url_for
import argparse
import os

app = Flask(__name__)

global idx_cache

@app.route('/', methods=['GET', 'POST'])
def home_page():
    global idx_cache
    if request.method == 'POST':
        print(request.form)
        if 'Next' in request.form.keys():
            print(request.form['Next'])
        if idx_cache:
            print(idx_cache)
            if request.form['Next']=='Next':
                idx_cache = idx_cache+1 if idx_cache+1<len(img_list) else 0
                img_name = img_list[idx_cache]
            elif request.form['Previous']=='Previous':
                idx_cache = idx_cache-1 if idx_cache-1>0 else len(img_list)-1
                img_name = img_list[idx_cache]
            
        if 'img_name' not in locals():
            img_name = request.form['images']
            idx_cache = img_list.index(img_name)
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
    app.run(debug=True, host='0.0.0.0', port=args.port)