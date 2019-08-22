from flask import render_template, redirect, url_for, request, flash, session
from app import app
from app.models import Experiment, Interviewee
from app.forms import IntervieweeForm, ExperimentForm, LoadExperimentForm, CommentForm

from datetime import datetime
import json
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/create_new_experiment', methods=['GET', 'POST'])
def create_new_experiment():
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
    if request.method == 'POST':
        new_interviewee = Interviewee(request.form)
        session['Interviewee'] = new_interviewee.__dict__
        return redirect(url_for('start', uuid_inter=new_interviewee.uuid_inter))
    return render_template('new_quiz.html', form=form)


@app.route('/start/<uuid_inter>')
def start(uuid_inter):
    with open('./app/exp_config/current', 'r') as current:
        data = current.read()
    current_exp = Experiment(data)
    dataset = current_exp.randomize_dataset()
    response = {}
    for i,item in enumerate(dataset):
        response[str(i)] = {
            'response': 0,
            'timestamp': 0,
            'comment': '',
            'item': item
        }
    session['Experiment'] = current_exp.__dict__
    session['Response'] = response
    print(session['Response'])
    return render_template('start.html', uuid_inter=uuid_inter)

@app.route('/test/<uuid_inter>', methods=['GET', 'POST'])
def test(uuid_inter):
    max_step = int(session['Experiment']['amount_of_pic'])
    step = int(request.args.get('step', 0))
    time_to_response = int(session['Experiment']['time_to_response'])
    if step < max_step:
        items = session['Response'][str(step)]['item']
        dump(uuid_inter, items)
        if request.method == 'POST':
            resp = request.form.get('response', '0')
            session['Response'][str(step)]['response'] = resp  
            session['Response'][str(step)]['timestamp'] = datetime.utcnow().isoformat() 
            session.modified = True
            return redirect(url_for('comment', step=step, uuid_inter=uuid_inter))
        return render_template('test.html', step=step, uuid_inter=uuid_inter, time_to_response=time_to_response)
    return redirect(url_for('finish', uuid_inter=uuid_inter))


def dump(uuid_inter, items):
    with open('./app/tmp/'+uuid_inter, 'w') as current:
        current.write(json.dumps(items))

@app.route('/comment/<uuid_inter>', methods=['GET', 'POST'])
def comment(uuid_inter):
    step = int(request.args.get('step', 0))
    form = CommentForm()
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        session['Response'][str(step)]['comment'] = comment  
        session.modified = True
        return redirect(url_for('test', step=step+1, uuid_inter=uuid_inter))
    return render_template('comment.html', form=form)

 

@app.route('/first')
def first():
    uuid_inter = request.args.get('uuid_inter')
    with open('./app/exp_config/current', 'r') as current:
        data = current.read()
    current_exp = Experiment(data)
    pic_name = current_exp.dataset.split(',')
    if len(pic_name) > 0:
        this_pic = pic_name[0]
    else:
        return 404
    print(this_pic)
    return render_template('page.html', this_pic=this_pic, uuid_inter=uuid_inter)

@app.route('/second')
def second():
    uuid_inter = request.args.get('uuid_inter')
    with open('./app/exp_config/current', 'r') as current:
        data = current.read()
    current_exp = Experiment(data)
    pic_name = current_exp.dataset.split(',')
    if len(pic_name) > 1:
        this_pic = pic_name[1]
    else:
        return 404
    return render_template('page.html', this_pic=this_pic, uuid_inter=uuid_inter)

@app.route('/third')
def third():
    uuid_inter = request.args.get('uuid_inter')
    with open('./app/exp_config/current', 'r') as current:
        data = current.read()
    current_exp = Experiment(data)
    pic_name = current_exp.dataset.split(',')
    if len(pic_name) > 2:
        this_pic = pic_name[2]
    else:
        return 404
    print(this_pic)
    return render_template('page.html', this_pic=this_pic, uuid_inter=uuid_inter)

@app.route('/notifications')
def notifications():
    uuid_inter = request.args.get('uuid_inter')
    key = request.args.get('key')
    try:
        with open('./app/tmp/'+uuid_inter, 'r') as current:
            data = current.read()
            data = json.loads(data)
            send_data = data[key]
    except:
        send_data = ''
    return send_data
    

@app.route('/finish/<uuid_inter>')
def finish(uuid_inter):
    print(session['Response'])
    with open('./app/result/' + uuid_inter, 'w') as new_res:
        new_res.write(json.dumps(session['Experiment']))
        new_res.write(json.dumps(session['Interviewee']))
        new_res.write(json.dumps(session['Response']))
    os.remove('./app/tmp/'+uuid_inter)
    session['Response'] = None
    session['Interviewee'] = None
    return render_template('finish.html')
