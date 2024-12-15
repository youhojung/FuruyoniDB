from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__, template_folder="templates")

@app.route('/')
@app.route('/furuDB/')
def furuDBmain():
    return render_template('index.html')

@app.route('/furuDB/cardDB/')
def cardDBmenu():
    db = sqlite3.connect("furuyoni_project.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    items = cursor.execute('SELECT Kname, charaname, another, cNum FROM CharaInfo ORDER BY cNum').fetchall()
    db.close()
    return render_template('cardDBmenu.html', chara=items)

@app.route('/furuDB/cardDB/<string:charaname>-<string:another>/')
def cardInfo(charaname, another):
    db = sqlite3.connect("furuyoni_project.db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    chara_info = cursor.execute(
        'SELECT * FROM CharaInfo WHERE charaname = ? AND another = ?',
        (charaname, another)
    ).fetchone()
    card_data = cursor.execute(
        'SELECT * FROM CardInfo WHERE cardchara = ? AND cardID Like ?',
        (charaname, f'%-{another}-%')
    ).fetchall()
    db.close()
    return render_template(
        'cardInfo.html',
        charaname=charaname,
        another=another,
        chara_info=chara_info,
        card_data=card_data
    )


@app.route('/furuDB/matchDB/')
def matchDBmenu():
    db = sqlite3.connect('furuyoni_project.db')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    items = cursor.execute('SELECT * FROM MatchInfo').fetchall()
    db.close()
    return render_template('matchDBmenu.html', match=items)

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)