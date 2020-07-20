from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import copy_current_request_context
from DBcm1 import UseDatabase
from DBcm1 import MyConnectionError
from DBcm1 import CredentialsError
from DBcm1 import SQLError
from checker import check_logged_in
from threading import Thread
from odd import search4letters

app = Flask(__name__)
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'a17051974',
                          'database': 'vsearchlogDB', }


@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'


# def log_request(req: 'flask_request', res: str) -> None:
#     with UseDatabase(app.config['dbconfig']) as cursor:
#         _SQL = """insert into log
#         (phrase, letters, ip, browser_string, results)
#         values
#         (%s, %s, %s, %s, %s)"""
#         cursor.execute(_SQL, (req.form['phrase'],
#                               req.form['letters'],
#                               req.remote_addr,
#                               req.user_agent.browser,
#                               res,))


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """insert into log
            (phrase, letters, ip, browser_string, results)
            values
            (%s, %s, %s, %s, %s)"""
            cursor.execute(_SQL, (req.form['phrase'],
                                  req.form['letters'],
                                  req.remote_addr,
                                  req.user_agent.browser,
                                  res,))

    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your result'
    results = str(search4letters(phrase, letters))
    try:
        t = Thread(target=log_request, args=(request, results))
        t.start()
        # log_request(request, results)
    except Exception as err:
        print('***** Login failed with error: ', str(err))
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
@check_logged_in
def view_log() -> 'html':
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results
    from log"""
            cursor.execute(_SQL)
            content = cursor.fetchall()
            titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View log',
                               the_row_titles=titles,
                               the_data=content, )
    except MyConnectionError as err:
        print('Cannot connect to db: ', str(err))
    except CredentialsError as err:
        print('User-id/Password issues. Error:', str(err))
    except SQLError as err:
        print('Is your query correct? Error:', str(err))
    except Exception as err:
        print('Something went wrong:', str(err))
    return 'Error'


app.secret_key = 'YouWillNeverGuessMySecretKey'

if __name__ == '__main__':
    app.run(debug=True)
