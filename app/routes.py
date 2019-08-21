from flask import render_template, redirect, url_for, request, flash, session
from app import app
from app.models import Experiment
from app.forms import IntervieweeForm, ExperimentForm, LoadExperimentForm

from datetime import datetime
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/create_new_experiment', methods=['GET', 'POST'])
def new_experiment():
    form = ExperimentForm()
    if request.method == 'POST':
        NewExperiment = Experiment(request.form)
        NewExperiment.save()
        return redirect('index')
    return render_template('new_experiment.html', form=form)


@app.route('/change_current_experiment', methods=['GET', 'POST'])
def change_current_experiment():
    form = LoadExperimentForm()
    if request.method == 'POST':
        data = form.config_file.data.read()
        current_exp = Experiment(data)
        current_exp.set_current()
        return redirect(url_for('index'))
    return render_template('change_current_experiment.html', form=form)


@app.route('/new_quiz', methods=['GET', 'POST'])
def new_quiz():
    form = IntervieweeForm()
    if form.validate_on_submit():
        user_id = 1
        redirect(url_for('start', user_id=user_id))
    return render_template('new_quiz.html')


@app.route('/start/<user_id>')
def start(user_id):
    with open('./app/exp_config/current', 'r') as current:
        data = current.read()
    current_exp = Experiment(data)
    dataset = current_exp.randomize_dataset()
    response = {}
    for i,item in enumerate(dataset):
        response[str(i)] = {
            'response': 0,
            'timestamp': 0,
            'item': item
        }
    session['Experiment'] = current_exp.__dict__
    session['Response'] = response
    return render_template('start.html', user_id=user_id)

@app.route('/test', methods=['GET', 'POST'])
def test():
    max_step = int(session['Experiment']['amount_of_pic'])
    step = int(request.args.get('step', 0))
    items = session['Response'][str(step)]['item']
    dump(items)
    if request.method == 'POST':
        resp = request.form.get('response', '0')
        session['Response'][str(step)]['response'] = resp  
        session['Response'][str(step)]['timestamp'] = datetime.utcnow().isoformat() 
        return redirect(url_for('test', step=step+1))
    return render_template('test.html', step=step, max_step=max_step)

def dump(items):
    with open('./app/tmp/123', 'w') as current:
        current.write(json.dumps(items))

@app.route('/first')
def first():
    with open('./app/exp_config/current', 'r') as current:
        data = current.read()
    current_exp = Experiment(data)
    pic_name = current_exp.dataset.split(',')
    if len(pic_name) > 0:
        this_pic = pic_name[0]
    else:
        return 404
    print(this_pic)
    return render_template('page.html', this_pic=this_pic)

@app.route('/second')
def second():
    with open('./app/exp_config/current', 'r') as current:
        data = current.read()
    current_exp = Experiment(data)
    pic_name = current_exp.dataset.split(',')
    if len(pic_name) > 1:
        this_pic = pic_name[1]
    else:
        return 404
    print(this_pic)
    return render_template('page.html', this_pic=this_pic)

@app.route('/third')
def third():
    with open('./app/exp_config/current', 'r') as current:
        data = current.read()
    current_exp = Experiment(data)
    pic_name = current_exp.dataset.split(',')
    if len(pic_name) > 2:
        this_pic = pic_name[2]
    else:
        return 404
    print(this_pic)
    return render_template('page.html', this_pic=this_pic)

@app.route('/notifications')
def notifications():
    key = request.args.get('key')
    with open('./app/tmp/123', 'r') as current:
        data = current.read()
    data = json.loads(data)
    send_data = data[key]
    return send_data
    