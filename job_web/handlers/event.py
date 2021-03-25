# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort,\
    current_app, request
from flask_login import current_user
from ..models import Event
from sqlalchemy import func,extract
from ..forms import EXP
import pymysql
import pandas as pd


event = Blueprint('event', __name__, url_prefix='/event')


@event.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    kw = request.args.get('kw')
    fenxi = request.args.get('fenxi')
    Event.is_enable = True
    flt = {Event.is_enable is True}
    if kw is not None and kw != '':
        flt.update({Event.name.like('%{}%'.format(kw))})
    pagination = Event.query.filter(*flt).paginate(
            page=page,
            per_page=current_app.config['EVENT_INDEX_PER_PAGE'],
            error_out=False
        )
    if fenxi is not None and fenxi != '':
        return render_template('event/index.html',pagination=pagination, kw=kw, active='event')
    return render_template('event/all_event.html', pagination=pagination,
                           kw=kw, filter=EXP, active='event')



@event.route('/<string:event_id>')
def detail(event_id):
    event_obj = Event.query.get_or_404(event_id)
    if not event_obj.is_enable:
        abort(404)
    # if request.args.get('job'):
    #         page = request.args.get('page', default=1, type=int)
    #         pagination = event_obj.enabled_jobs().order_by(Event.updated_at.desc()).paginate(
    #             page=page, per_page=current_app.config['COMPANY_DETAIL_PER_PAGE'], error_out=False)
    #         return render_template('event/detail.html', pagination=pagination, panel='jobs', company=event_obj)
    return render_template('event/detail.html', event=event_obj, panel='about', active='detail')



@event.route("/event_address", methods=['GET', 'POST'])
def event_address():
    return render_template('event/event_address.html')
    # return render_template('event/event2.html')
