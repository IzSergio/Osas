from flask import render_template
#наша новая функция сайта
@app.route("/data_to")
def data_to():
 #создаем переменные с данными для передачи в шаблон
 some_pars = {'user':'Ivan','color':'red'}
 some_str = 'Hello my dear friends!'
 some_value = 10
 #передаем данные в шаблон и вызываем его
 return render_template('simple.html',some_str = some_str,
 some_value = some_value,some_pars=some_pars) 
# модули работы с формами и полями в формах
from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
# модули валидации полей формы
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
# используем csrf токен, можете генерировать его сами
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
# используем капчу и полученные секретные ключи с сайта google 
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = 'сюда поместить ключ из google'
app.config['RECAPTCHA_PRIVATE_KEY'] = 'сюда поместить секретный ключ из google'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
# обязательно добавить для работы со стандартными шаблонами
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
# создаем форму для загрузки файла
class NetForm(FlaskForm):
 # поле для введения строки, валидируется наличием данных
 # валидатор проверяет введение данных после нажатия кнопки submit
 # и указывает пользователю ввести данные если они не введены
 # или неверны
 openid = StringField('openid', validators = [DataRequired()])
 # поле загрузки файла
 # здесь валидатор укажет ввести правильные файлы
 upload = FileField('Load image', validators=[
 FileRequired(),
 FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 # поле формы с capture
 recaptcha = RecaptchaField()
 #кнопка submit, для пользователя отображена как send
 submit = SubmitField('send')
# функция обработки запросов на адрес 127.0.0.1:5000/net
# модуль проверки и преобразование имени файла
# для устранения в имени символов типа / и т.д.
from werkzeug.utils import secure_filename
import os
# подключаем наш модуль и переименовываем
# для исключения конфликта имен
import net as neuronet
# метод обработки запроса GET и POST от клиента
@app.route("/net",methods=['GET', 'POST'])
def net():
 # создаем объект формы
 form = NetForm()
 # обнуляем переменные передаваемые в форму
 filename=None
 neurodic = {}
 # проверяем нажатие сабмит и валидацию введенных данных
 if form.validate_on_submit():
 # файлы с изображениями читаются из каталога static
 filename = os.path.join('./static', secure_filename(form.upload.data.filename))
 fcount, fimage = neuronet.read_image_files(10,'./static')
 # передаем все изображения в каталоге на классификацию
 # можете изменить немного код и передать только загруженный файл
 decode = neuronet.getresult(fimage)
 # записываем в словарь данные классификации
 for elem in decode:
 neurodic[elem[0][1]] = elem[0][2]
 # сохраняем загруженный файл
 form.upload.data.save(filename)
 # передаем форму в шаблон, так же передаем имя файла и результат работы нейронной
 # сети если был нажат сабмит, либо передадим falsy значения
 return render_template('net.html',form=form,image_name=filename,neurodic=neurodic)
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
В папке templates создадим шаблон net.html для обработки форм.
{% extends "bootstrap/base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
<!-- задаем заголовок страницы -->
{% block title %}This is an page{% endblock %}
<!-- блок body -->
{% block content %}
{{ wtf.quick_form(form, method='post',enctype="multipart/form-data", action="net") }}
<!-- один из стандартных тэгов html - заголовок второго уровня -->
<h2>Classes: </h2> 
<!-- проверяем есть ли данные классификации -->
{% if neurodic %}
 <!-- запускаем цикл прохода по словарю и отображаем ключ-значение -->
 <!-- классифицированных файлов -->
 {% for key, value in neurodic.items() %}
 <h3>{{key}}: {{value}}</h3>
 {% endfor %}
{% else %}
 <h3> There is no classes </h3>
{% endif %}
<h2>Image is here: </h2>
<!-- отображаем загруженное изображение с закругленными углами -->
<!-- если оно есть (после submit) -->
{% if image_name %}
 <p>{{image_name}}
 <p><img src={{image_name}} class="img-rounded" alt="My Image" width = 224 height=224 />
{% else %}
 <p> There is no image yet </p>
{% endif %}
{% endblock %}
