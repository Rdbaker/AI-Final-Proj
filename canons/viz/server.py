from flask import Flask, render_template
app = Flask(__name__, static_folder='logs')


@app.route('/')
def viz():
    print 'hello'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
