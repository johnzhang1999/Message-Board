from flask import Flask

app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
    return "user name is %s" % username

@app.route('/post/<int:post_id>')
def show_post_id(post_id):
    return "Post id is: %d" % post_id

if __name__ == '__main__':
    app.run()