from flask import render_template, redirect, url_for, request, flash, abort
from app import app
from app.models import Experiment
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
    if request.method == 'POST' and form.validate():
        NewExperiment = Experiment(request.form)
        NewExperiment.save()
        return redirect('index')
    return render_template('new_experiment.html', form=form)


@app.route('/change_current_experiment', methods=['GET', 'POST'])
def change_current_experiment():
    form = LoadExperimentForm()
    if request.method == 'POST':
        data = form.config_file.data.read()
        print(data)
        app.data['current_exp'] = Experiment(data)
        return redirect(url_for('index'))
    return render_template('change_current_experiment.html', form=form)


@app.route('/new_quiz', methods=['GET', 'POST'])
def new_quiz():
    form = IntervieweeForm()
    if request.method == 'POST':
        app.data['interviewee'] = request.form
        return redirect(url_for('start'))
    return render_template('new_quiz.html', form=form)


@app.route('/start')
def start():
    try:
        current_exp = app.data['current_exp']
    except KeyError:
        return redirect(url_for('change_current_experiment'))
    reverse = True if app.data['interviewee'].get('reverse', False) else False
    response = current_exp.randomize_dataset(reverse)

    app.data['experiment'] = current_exp.__dict__
    app.data['answers'] = response
    return render_template('start.html',)

@app.route('/test', methods=['GET', 'POST'])
def test():
    max_step = int(len(app.data['answers']))
    step = int(request.args.get('step', 0))
    with_comments = True if app.data['interviewee'].get('with_comments') else False
    if step == 0:
        app.data['experiment']['start_time'] = datetime.now().isoformat()
        app.data['experiment']['is_complete'] = False

    time_to_response = int(app.data['experiment']['time_to_response'])
    if step < max_step:
        if 'view_time' not in app.data['answers'][step]:
            app.data['answers'][step]['view_time'] = datetime.now().isoformat()
        if request.method == 'POST':
            print(step)
            resp = request.form.get('response', None)
            comment = request.form.get('comment', None)
            app.data['answers'][step]['answer_time'] = datetime.now().isoformat()
            app.data['answers'][step]['response'] = app.config['RESP_DICT'].get(resp, None)
            app.data['answers'][step]['response_text'] = resp
            app.data['answers'][step]['comment'] = comment
            return redirect(url_for('test', step=step+1))
        return render_template('alt_test.html', step=step, max_step=max_step,
                               time_to_response=time_to_response, with_comments=with_comments,
                               task=app.data['experiment'].get('task', 'UNDEFINED TASK'), items=app.data['answers'][step])
    app.data['experiment']['is_complete'] = True
    return redirect(url_for('finish'))


# @app.route('/comment', methods=['GET', 'POST'])
# def comment():
#     max_step = int(len(app.data['answers']))
#     step = int(request.args.get('step', 0))
#     form = CommentForm()
#     if request.method == 'POST':
#         comment = request.form.get('comment', '')
#         app.datamodified = True
#         app.data['answers'][step]['comment'] = comment
#         return redirect(url_for('test', step=step+1,))
#     return render_template('comment.html', form=form, step=step, max_step=max_step)


# @app.route('/page/<name>')
# def page(name):
#     names = ['original', 'left', 'right']
#     if name not in names:
#         abort(404)
#     current_exp = app.data['current_exp']
#     height =  getattr(current_exp, name+'_w')
#     try:
#         height = int(height)
#     except:
#         height = 0
#     return render_template('page.html', this_pic=name, title=name, height=height)


# @app.route('/notifications')
# def notifications():
#     key = request.args.get('key')
#     try:
#         send_data= os.path.join(os.path.dirname(app.data['experiment']['rel_dataset']),
#                      app.data['items'][key])
#     except:
#         send_data = ''
#     return send_data


@app.route('/finish')
def finish():
    app.data['items'] = {}
    app.data['experiment']['finish_time'] = datetime.now().isoformat()
    result = {
                "experiment": app.data['experiment'],
                "interviewee": app.data['interviewee'],
                "answers": app.data['answers']
    }
    username = app.data['interviewee']['username']
    result_filename = datetime.now().strftime("%Y%m%dT%H%M%S") + '_' + username + '.json'
    with open(os.path.join('./app/result/' + result_filename), 'w') as new_res:
        json.dump(result, new_res, indent=2, sort_keys=True, ensure_ascii=False)

    app.data['answers'] = None
    app.data['interviewee'] = None
    return render_template('finish.html')

# @app.route('/page_response')
# def page_response():
#     key = request.args.get('key')
#     app.data['page'][key] = True

# @app.route('/check_page')