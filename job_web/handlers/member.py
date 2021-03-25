# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, abort,\
    current_app, request
from flask_login import current_user
from ..models import Member
from sqlalchemy import func,extract
from ..forms import EXP
import pymysql
import pandas as pd


member = Blueprint('member', __name__, url_prefix='/member')


@member.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    kw = request.args.get('kw')
    fenxi = request.args.get('fenxi')
    Member.is_enable=True
    flt = {Member.is_enable is True}
    if kw is not None and kw != '':
        flt.update({Member.name.ilike('%{}%'.format(kw))})
    pagination = Member.query.filter(*flt).paginate(
        page=page, per_page=current_app.config['MEMBER_INDEX_PER_PAGE'], error_out=False)
    if fenxi is not None and fenxi != '':
        return render_template('member/index.html',pagination=pagination, kw=kw, active='member')
    return render_template('member/all_member.html', pagination=pagination, kw=kw, active='member')




@member.route('/<int:member_id>')
def detail(member_id):
    member_obj = Member.query.get_or_404(member_id)
    if not member_obj.is_enable:
        abort(404)
    if request.args.get('job'):
            page = request.args.get('page', default=1, type=int)
            pagination = member_obj.enabled_jobs().order_by(Member.updated_at.desc()).paginate(
                page=page, per_page=current_app.config['COMPANY_DETAIL_PER_PAGE'], error_out=False)
            return render_template('member/detail.html', pagination=pagination, panel='jobs', company=member_obj)
    return render_template('member/detail.html', member=member_obj, panel='about', active='detail')


def conn_db():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="root", db="job_web", charset="utf8")

    return conn


@member.route("/growthTrend", methods=['GET', 'POST'])
def growthTrend(conn=conn_db()):
    sql = "SELECT DATE_FORMAT(created,'%Y') months, count(1)  Count FROM job_web.`member` GROUP BY months "
    df = pd.read_sql(sql, conn)
    conn.close()
    df_pivot = pd.pivot_table(df, columns="months", values="Count", fill_value=0)
    Month = df_pivot.columns.tolist()
    Count = df_pivot.values.tolist()
    sum_Count=[]
    suma=0
    for su in Count[0]:
        print(type(su))
        suma=suma+su
        sum_Count.append(suma)
    print(sum_Count)
    sum_Count1=[]
    sum_Count1.append(sum_Count)
    print(sum_Count1)
    ProductMName = "year"
    return render_template('member/growthTrend.html', ProductMName=ProductMName,Month=Month, Count=Count,sum_Count1=sum_Count1)
    # return render_template('member/member2.html')

@member.route("/member_address", methods=['GET', 'POST'])
def member_address(conn=conn_db()):
    return render_template('member/event_address.html')
    # return render_template('member/member2.html')
