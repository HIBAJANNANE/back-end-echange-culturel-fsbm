from flask import session
from app import *

@app.route('/logout')
def logout():
    session.clear()