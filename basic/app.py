# Flask : untuk membuat API
# render_template : untuk memberikan response berupa HTML
# render_template secara otomatis mencari folder 'template'
# request : untuk menerima data yang dikirim dari browser
from flask import Flask, render_template, request

app = Flask(__name__)

# Home (Path)
@app.route('/') # '/' > untuk setting URL/alamat/link
def index():
    return '<h1> Hello Flask ~ </h1>'

# Menerima data ketika ada request yang masuk
@app.route('/base/<p_name>/<p_rain>')
def base(p_name, p_rain):

    name = p_name
    todo = ['Running', 'Swimming', 'McD', 'Smoking', 'Walking']
    rain = p_rain == 'Hujan'

    return render_template(
        'basic.html', 
        name=name, 
        MyToDo=todo, 
        condition=rain
    )

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/registration')
def registration():
    username = request.args.get('username')
    password = request.args.get('password')
    color = request.args.get('color')

    print('username', username)
    print('password', password)
    print('color', color)

    return render_template('registration.html', uname = username)

# Error Handling
@app.errorhandler(404) # harus memiliki parameter 404 untuk error handler
def page_not_found(e):
    return render_template('404.html')


















# Saat running file app.py maka var __name__ berisi string '__main__'
if __name__ == '__main__':
    # debug : True memiliki dua efek
    # 1. Setiap ada pembaharuan kode, API akan restart secara otomatis
    # 2. Memungkinkan menampilkan pesan error di browser, sehingga mudah dibaca
    app.run(debug = True)