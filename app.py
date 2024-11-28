from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)     #Flaskの初期設定、__name__は定型文的な感じ
#SQLAlchemyを使ってSQLiteデータベースを設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'      #データベースファイルのパス
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False      #余計な警告を抑えるため
db = SQLAlchemy(app)

#Taskクラスでタスクのデータ構造
class Task(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100) , nullable=False)
  done = db.Column(db.Boolean , default=False)      #タスクが完了しているか

#アプリケーションの挙動
@app.route('/')     #メインページを表示
def index():
  tasks = Task.query.all()
  return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])      #methods=['POST']はHTTPリクエストの方法の指定
def add_task():
  if request.method == 'POST':
    task_content = request.form['content']
    if task_content:
      new_task = Task(content=task_content)
      db.session.add(new_task)
      db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
  task_to_delete = Task.query.get_or_404(id)
  db.session.delete(task_to_delete)
  db.session.commit()
  return redirect(url_for('index'))

with app.app_context():
  db.create_all()

#定型文
if __name__ == "__main__":
  app.run(debug=True)