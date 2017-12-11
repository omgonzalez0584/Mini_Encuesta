from flask import Flask, flash, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///encuestas.sqlite3'
app.config['SECRET_KEY'] = 'uippc3'

db = SQLAlchemy(app)

class encuesta(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    pregunta = db.Column(db.String(100))
    opcion1 = db.Column(db.String(50))
    opcion2 = db.Column(db.String(50))
    voto1 = db.Column(db.Integer)
    voto2 = db.Column(db.Integer)
    cantidad = db.Column(db.Integer)


    def __init__(self, pregunta, opcion1, opcion2, voto1,voto2,cantidad):
        self.pregunta = pregunta
        self.opcion1 = opcion1
        self.opcion2 = opcion2
        self.voto1 = voto1
        self.voto2 = voto2
        self.cantidad = cantidad


@app.route('/')
def principal():
    print(encuesta.query.all())
    return render_template('principal.html', encuesta=encuesta.query.all())


@app.route('/nueva_encuesta/', methods=['GET','POST'])
def nueva_encuesta():
    if request.method == 'POST':
        if not request.form['pregunta']:
            flash('Por favor debe introducir una pregunta', 'error')

        elif  not request.form['opcion1'] and not request.form['opcion2']:
            flash('Debe introducir al menos dos opcion,Error')


        elif not request.form['opcion2']:
            flash('Debe introducir la opcion 2!')

        else:
            voto1 = 0
            voto2 = 0
            cantidad = 0
            data_ = encuesta(request.form['pregunta'],request.form['opcion1'],request.form['opcion2'],voto1,voto2,cantidad)
            db.session.add(data_)
            db.session.commit()
            flash('Se crea encuesta exitosamente!')
            return redirect(url_for('principal'))



    return render_template('nueva_encuesta.html')

@app.route('/votar/', methods = ['GET','POST'])
def votar():
    if request.method == 'POST':
        opc = request.form['id']
        print(opc)
        u = encuesta.query.get(opc)
        print(u)
        return render_template('votacion.html',u=encuesta.query.get(opc))


@app.route('/conteo/',methods = ['GET','POST'])
def conteo():
    if request.method == 'POST':
        opc = request.form['opc']
        id = request.form['id']
        u = encuesta.query.get(id)
        print(u)
        if opc == 'a':
            flag = int(u.voto1)
            flag = flag + 1
            u.voto1 = flag
            cant = int(u.cantidad)
            cant = cant + 1
            u.cantidad = cant
            db.session.commit()

        else:
            flag = int(u.voto2)
            flag = flag + 1
            u.voto2 = flag
            cant = int(u.cantidad)
            cant = cant + 1
            u.cantidad = cant
            db.session.commit()

    return redirect(url_for('principal'))





if __name__=='__main__':
    app.run()
    db.create_all()



