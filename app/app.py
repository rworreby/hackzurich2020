from flask import Flask, render_template, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('main'))


@app.route('/main')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
