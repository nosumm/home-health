from website.models import people
from flask import current_app
from website.about import bp
from flask import Flask, render_template

@bp.route('/about')
def about():
    return render_template('about/about.html', people=people.people)

@bp.route('/hardware_team')
def hardware():
    return render_template('about/hardware_team.html', people=people.people)

@bp.route('/software_team')
def software():
    return render_template('about/software_team.html', people=people.people)

@bp.route('/introduction')
def introduction():
    return render_template('about/introduction.html', people=people.people)

@bp.route('/progress')
def progress():
    return render_template('about/progress.html', people=people.people)
