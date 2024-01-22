# simple_image_viewer
Code for a simple image viewer, based on Flask. Becomes very slow with to many images (>10000)
Depends only on Flask, so run:
```
pip install flask
```
Then run the app:
```
python main.py --port 5000 --path /path/to/image/folder/
```
Add the```--external``` option to add access from different devices