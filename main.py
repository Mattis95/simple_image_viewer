from flask import Flask, render_template, request, url_for
import argparse
import os
import time

app = Flask(__name__)

class ImageGetter:
    def __init__(self, path, reload_time):
        self._path = path
        self._time = 0
        self._reload_time = reload_time
        self.img_list = []

    def get_image_list(self):
        if time.time()-self._time > self._reload_time:
            img_list = []
            for file in os.listdir(self._path):
                if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".avif"):
                    img_list.append(file)
            self.img_list = img_list
            self._time = time.time()
        return self.img_list

@app.route('/', methods=['GET', 'POST'])
def home_page():
    img_list = img_getter.get_image_list() 
    if request.method == 'POST':
        if 'Next' in request.form.keys():
            idx = img_list.index(request.form['images'])
            idx = idx+1 if idx+1<len(img_list) else 0
            img_name = img_list[idx]

        elif 'Previous' in request.form.keys():
            idx = img_list.index(request.form['images'])
            idx = idx-1 if idx-1>=0 else len(img_list)-1
            img_name = img_list[idx]
        
        else:
            img_name = request.form['images']
        image_file = url_for("static", filename=img_name)
        return render_template('index.html', img_list = img_list, img_name = img_name, img_data = image_file)
    else:
        if len(img_list)>0:
            return render_template('index.html', img_list = img_list, img_name=img_list[0])
        else:
            return render_template('index.html', img_list = img_list, img_name="Image path empty")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", help="Port of flask application", type=int, default=8001)
    parser.add_argument("--path", help="Path to image dir", type=str, default="./")
    parser.add_argument("--external", help="Whether external access is allowed", action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()
    app.static_folder = args.path
    path = args.path
    img_getter = ImageGetter(path, 30)
    img_list = img_getter.get_image_list()
    host = '0.0.0.0' if args.external else '127.0.0.1'
    app.run(debug=True, host=host, port=args.port)