# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort,\
    current_app, request, jsonify
from flask_login import current_user
from ..models import Group
from sqlalchemy import func,extract
from ..forms import EXP
import pymysql
import pandas as pd
from sqlalchemy import create_engine

group = Blueprint('group', __name__, url_prefix='/group')


@group.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    kw = request.args.get('kw')
    Group.is_enable = True
    fenxi = request.args.get('fenxi')
    flt = {Group.is_enable is True}
    if kw is not None and kw != '':
        flt.update({Group.name.ilike('%{}%'.format(kw))})
    pagination = Group.query.filter(*flt).paginate(
        page=page, per_page=current_app.config['GROUP_INDEX_PER_PAGE'], error_out=False)
    if fenxi is not None and fenxi != '':
        return render_template('group/index.html',pagination=pagination, kw=kw, active='group')
    return render_template('group/all_group.html', pagination=pagination, kw=kw, active='group')


@group.route('/<int:group_id>')
def detail(group_id):
    group_obj = Group.query.get_or_404(group_id)
    if not group_obj.is_enable:
        abort(404)
    if request.args.get('event'):
            page = request.args.get('page', default=1, type=int)
            pagination = group_obj.enabled_events().paginate(
                page=page, per_page=current_app.config['GROUP_DETAIL_PER_PAGE'], error_out=False)
            return render_template('group/detail.html', pagination=pagination, panel='events', group=group_obj)
    return render_template('group/detail.html', group=group_obj, panel='about', active='detail')

@group.route("/event_address", methods=['GET', 'POST'])
def event_address():
    return render_template("group/event_address.html")

@group.route("/event2", methods=['GET', 'POST'])
def event2():
    return render_template("group/event2.html")

@group.route("/event3", methods=['GET', 'POST'])
def event3():
    return render_template("group/event3.html")

@group.route("/event4", methods=['GET', 'POST'])
def event4():
    return render_template("group/event4.html")




def conn_db():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", db="job_web", charset="utf8")
    return conn
# def conn_db():
#     engine = create_engine("mysql+mysqldb://root:root@127.0.0.1:3306/job_web")
#     conn = engine.raw_connection()
#     return conn

@group.route("/growthTrend", methods=['GET', 'POST'])
def growthTrend(conn=conn_db()):
    sql = "SELECT DATE_FORMAT(created,'%Y') months, count(1)  Count FROM job_web.`group` GROUP BY months "
    df = pd.read_sql(sql, conn)

    df_pivot = pd.pivot_table(df, columns="months", values="Count", fill_value=0)
    Month = df_pivot.columns.tolist()
    Count = df_pivot.values.tolist()
    sum_Count=[]
    suma=0
    for su in Count[0]:
        suma=suma+su
        sum_Count.append(suma)

    sum_Count1=[]
    sum_Count1.append(sum_Count)

    ProductMName = "year"
    return render_template('group/growthTrend.html', ProductMName=ProductMName,Month=Month, Count=Count,sum_Count1=sum_Count1)
    # return render_template('group/event2.html')

@group.route("/group_address", methods=['GET', 'POST'])
def group_address(conn=conn_db()):
    return render_template('group/group_address.html')
    # return render_template('group/event2.html')


@group.route('/group_analysis', methods=['GET', 'POST'])
def group_analysis():
    group_list = Group.query.all()
    country_count = {}
    category_count = {}
    for group in group_list:
        if group.country in country_count:
            country_count[group.country] += 1
        else:
            country_count[group.country] = 1
        if group.category_name in category_count:
            category_count[group.category_name] += 1
        else:
            category_count[group.category_name] = 1

    country_list = []
    country_counts_list = []
    for country, counts in country_count.items():
        if counts > 1:
            country_list.append(country)
            country_counts_list.append(str(counts))
    category_list = []
    category_counts_list = []
    for category, counts in category_count.items():
        if counts > 1:
            category_list.append(category)
            category_counts_list.append(str(counts))
    return jsonify({'country_list': country_list, 'country_counts_list': country_counts_list,
                    'category_list': category_list, 'category_counts_list': category_counts_list})