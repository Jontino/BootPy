from flask import render_template, flash, redirect, url_for, request
from . import site
from.chart import get_chart_date_labels
from..models import Relay


@site.route('/', methods=['GET', 'POST'])
@site.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', relays=Relay.get_relays(), chart_labels=get_chart_date_labels())


@site.route('/relays/<int:relay_id>', methods=['GET', 'POST'])
def relay_by_id(relay_id):
    if request.method == 'POST':
        if 'Action' in request.form:
            action = str(request.form['Action'])

            if action == 'Reboot':
                Relay.reboot(relay_id)
            elif action == "Reset":
                Relay.reset_counter(relay_id)

    return redirect(url_for('site.index'))

