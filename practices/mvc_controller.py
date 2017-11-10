from flask import Flask, redirect, abort
# from werkzeug.utils import redirect
import urllib.request

app = Flask(__name__)

@app.route('/html')
def HelloHtml():
    return'''
    <h1> Hello HTML</h1>
    <p>Welcome to the World of Python</p>
    <ul>
    <li>Newbie</li>
    <li>Beginner</li>
    <li>Intermediate</li>
    <li>Mastery</li>
    </ul>
    '''

@app.route('/css')
def HelloCSS():
    return '''
   <body style="background-color:yellow">
   <h1 style="text-align:center">Hello CSS</h1>
   <p style="font-family:arial;color:red;font-size:20px;">欢迎了解HTML+CSS</p>
   </body>
    '''

@app.route('/user/<name>')
def show_user_name(name):
    if name == 'baidu':
        return redirect('http://baidu.com')
    elif name == '404':
        return abort(404)
    return '<h1>Hello %s!</h1>' % name

@app.route('/google')
def load_google():
    data = urllib.request.urlopen('http://google.com', timeout=10).read()
    return data

if __name__ == '__main__':
    app.run()