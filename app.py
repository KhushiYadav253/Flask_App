from flask import Flask, session, render_template, request
from db import init_db, insert_user, dispay_users, get_user, user_exists, get_role_admin, get_role_user, update_login_details, display_users_for_admin, mark_user_inactive
import uuid
#from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'K@345'
#app.permanent_session_lifetime = timedelta(days=5)


@app.route("/")
def hello_world():
  return render_template('home.html')


@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
  username = request.form.get('username')
  password = request.form.get('password')
  print(f"Username: {username}, Password: {password}")

  if username and user_exists(username):

    print(f"User found: {username}")
    user = get_user(username)

    if user and user['password'] == password:
      #session.permanent = True
      session['user_id'] = user['id']
      session['username'] = user['username']
      session['role'] = user['role']
      session['workspace_id'] = user['workspace_id']
      session['workspace_name'] = user['workspace_name']

      session_uuid = str(uuid.uuid4())
      session['session_uuid'] = session_uuid
      #workspace_name = user['workspace_name']
      update_login_details(username)

      if get_role_admin(username):
        users = display_users_for_admin()
        print(users)
        return render_template('welcome.html',
                               username=username,
                               workspace_name=user['workspace_name'],
                               users=users,
                               session_uuid=session_uuid)
      elif get_role_user(username):
        return render_template('user_wlcm.html',
                               username=username,
                               workspace_name=user['workspace_name'])

    else:
      return render_template('home.html', error='Invalid Password or Username')
  else:
    return render_template('home.html')
  return render_template('home.html')


# @app.route("/logout")
# def logout():
#     session.pop('user_id', None)
#     session.pop('username', None)
#     session.pop('role', None)
#     return render_template('home.html')
#     # return redirect(url_for('hello_world'))


@app.route("/logout", methods=['GET', 'POST'])
def logout():
  username = session.get('username')
  if username:
    mark_user_inactive(username)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    session.pop('workspace_name', None)
    session.pop('workspace_id', None)
  return render_template('home.html')


if __name__ == "__main__":
  init_db()
  insert_user()
  dispay_users()
  app.run(debug=True)
