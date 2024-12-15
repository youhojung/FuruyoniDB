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
        'SELECT * FROM CardInfo WHERE cardchara = ? AND cardID LIKE ?',
        (charaname, f'%-{another}-%')
    ).fetchall()
    complete_card_data = []
    for card in card_data:
        if card['cardname'] is None:
            card_parts = card["cardID"].split("-")
            card_chara = card_parts[2]
            card_another = card_parts[3]
            
            if card_another != "O":
                card_parts[3] = "O"
            
            replacement_card_id = "-".join(card_parts)
            replacement_card = cursor.execute(
                'SELECT * FROM CardInfo WHERE cardchara = ? AND cardID = ?',
                (card_chara, replacement_card_id)
            ).fetchone()

            if replacement_card:
                complete_card_data.append(replacement_card)
            else:
                complete_card_data.append(card)
        else:
            complete_card_data.append(card)

    db.close()

    return render_template(
        'cardInfo.html',
        charaname=charaname,
        another=another,
        chara_info=chara_info,
        card_data=complete_card_data
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