from flask import Flask
from flask import render_template
from flask import request
from flask import escape
from odd import search4letters
import mysql.connector

app = Flask(__name__)
dbconfig = {'host': '127.0.0.1',
            'user': 'vsearch',
            'password': 'a17051974',
            'database': 'vsearchlogDB', }


def log_request(req: 'flask_request', res: str) -> None:
    with UseDatabase(dbconfig) as cursor:
        _SQL = """insert into log
        (phrase, letters, ip, browser_string, results)
        values
        (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res, ))
        conn.commit()


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your result'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_title=title,
                           the_results=results)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to search4letters on Wev')


@app.route('/viewlog')
def view_log() -> 'html':
    with UseDatabase(dbconfig) as cursor:
        _SQL = """select * from log"""
        cursor.execute(_SQL)
        content = []
        for row in cursor.fetchall():
            content.append([])
            for item in row:
                content[-1].append(escape(item))
        titles = ('id', 'Date', 'Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View log',
                           the_row_titles=titles,
                           the_data=content, )


if __name__ == '__main__':
    app.run(debug=True)
