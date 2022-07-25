from flask import Flask, request, render_template, redirect
import sqlite3
import uuid

app = Flask(__name__)


@app.route('/stds', methods=['GET'])
def stds():

    users = sqlite3.connect('users.db')
    c = users.cursor()
    c.execute('select * from std')
    rows = c.fetchall()
    return render_template('results.html', content=rows)


@app.route('/greater', methods=['GET'])
def gt():
    users = sqlite3.connect('users.db')
    c = users.cursor()
    c.execute('select * from std st where st.st_grade >= 85')
    rows = c.fetchall()

    return render_template('results.html', content=rows)


@app.route('/update', methods=['POST'])
def ust():
    users = sqlite3.connect('users.db')
    c = users.cursor()
    if(request.method == 'POST'):
        s_id = request.form['st_id']
        s_nme = request.form['name']
        s_grade = request.form['grade']
        c.execute("update std set st_name = '{0}', st_grade = {1} where stu_id = '{2}'".format(
            s_nme, s_grade, s_id))
        users.commit()
        users.close()
        return redirect('/', code=302)


@app.route('/delete', methods=['POST'])
def dst():
    users = sqlite3.connect('users.db')
    c = users.cursor()
    if(request.method == 'POST'):
        d_id = request.form['del']
        c.execute('delete from std where stu_id = ?', [d_id])
        users.commit()
        users.close()
        return redirect('/',  code=302)


@app.route('/', methods=['GET', 'POST'])
def st():
    if(request.method == 'POST'):
        users = sqlite3.connect('users.db')
        c = users.cursor()
        c.execute(
            'create table if not exists std (stu_id varchar(255), st_name varchar(255), st_grade integer(2));')
        users.commit()

        d_id = uuid.uuid4()

        s_nme = request.form['name']
        s_grade = request.form['grade']

        c.execute("insert into std (stu_id, st_name, st_grade) values (?,?,?)", [
                  str(d_id), str(s_nme), int(s_grade)])

        users.commit()

        users.close()

    return render_template('Home.html')


app.run(host='localhost', port=5003, debug=True)
