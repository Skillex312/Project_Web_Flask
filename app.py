from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def main():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('sign_up.html')

if __name__ == "__main__":
    app.run()