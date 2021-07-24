from attendance.views.forms import GuestForm, MemberForm, AdminForm
from flask import render_template, url_for, flash, Blueprint, redirect, request
from attendance import db, admin, bcrypt
from attendance.models import User, Attendance
from flask_admin.contrib import sqla
from flask_admin.menu import MenuLink
from flask_login import login_user, current_user, logout_user
from datetime import date
from flask_admin.model import typefmt

views = Blueprint('views', __name__)


def date_format(view, value):
    return value.strftime('%d/%m/%Y')


DATE_FORMATER = dict(typefmt.BASE_FORMATTERS)
DATE_FORMATER.update({
    date: date_format
})


class AdminHomeView(sqla.ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('views.admin_login', next=request.url))


class UserView(AdminHomeView):
    column_editable_list = ('if_admin', 'if_member', 'name', 'email',
                            'mobile')
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    #form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list
    form_edit_rules = ('if_admin', 'if_member', 'name', 'email',
                       'mobile')
    form_create_rules = ('if_admin', 'if_member', 'name', 'email',
                         'mobile')

    can_export = True
    edit_modal = True
    details_modal = True
    can_view_details = True


class AttendanceView(AdminHomeView):
    column_type_formatters = DATE_FORMATER
    can_export = True
    can_create = False


class AdminLogoutMenuLink(MenuLink):
    def is_accessible(self):
        admins = User.query.filter_by(if_admin=True).all()
        admin_emails = []
        for admin in admins:
            admin_emails.append(admin.email)
        return current_user.is_authenticated and current_user.email in admin_emails


admin.add_view(UserView(User, db.session))
admin.add_view(AttendanceView(Attendance, db.session))
admin.add_link(AdminLogoutMenuLink(name='Logout', category='', url="/logout"))


@views.route('/')
def home():
    return render_template('home.html')


@views.route('/guest', methods=['GET', 'POST'])
def guest():
    form = GuestForm()
    if form.validate_on_submit():
        enter_mobile = form.mobile.data.replace(" ", "")
        format_mobile = enter_mobile[:-6] + " " + \
            enter_mobile[-6:-3] + " " + enter_mobile[-3:]
        new_guest = User(if_member=False, name=form.name.data.strip().lower().title(),
                         email=form.email.data.lower(), mobile=format_mobile)
        db.session.add(new_guest)
        db.session.commit()
        flash('Your attendance has been recorded!', 'success')
        return redirect(url_for('views.home'))
    return render_template('guest.html', title='Guest Attendance', form=form)


@views.route('/member', methods=['GET', 'POST'])
def member():
    names = User.query.filter_by(if_member=True).all()
    form = MemberForm()
    form.member_names.choices = [(name, name) for name in names]
    if form.validate_on_submit():
        member = User.query.filter_by(name=form.member_names.data).first()

        new_attendance = Attendance(user_id=member.id)
        db.session.add(new_attendance)
        db.session.commit()
        flash('Your attendance has been recorded!', 'success')
        return redirect(url_for('views.home'))
    return render_template('member.html', title='Member Attendance', form=form)


@views.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    admins = User.query.filter_by(if_admin=True).all()
    for admin in admins:
        if admin.password != None:
            password = admin.password
        else:
            admin.password = password
            db.session.commit()
    not_admins = User.query.filter_by(if_admin=False).all()
    for not_admin in not_admins:
        if not_admin.password != None:
            not_admin.password = None
            db.session.commit()
    form = AdminForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        admins = User.query.filter_by(if_admin=True).all()
        if user in admins:
            if bcrypt.check_password_hash(admin.password, form.password.data):
                login_user(admin)
                return redirect(url_for('admin.index'))
            else:
                flash('Login unsuccessful. Please check email and password', 'danger')
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('admin_login.html', title='Admin Login', form=form)


@views.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('views.home'))
