from flask import render_template, url_for, request, redirect, flash
from contacts_app import app, db, bcrypt
from contacts_app.models import Contact, User
from contacts_app.forms import ContactForm, RegisterForm, LoginForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/", methods=["POST", "GET"])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('index', user_id=current_user.id))
    return render_template("home.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index', user_id=current_user.id))
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=username, email=email, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {username}. Now you can login!', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index', user_id=current_user.id))
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('Username does not exist', 'danger')
            return render_template("login.html", form=form)

        if not bcrypt.check_password_hash(user.password, password):
            flash('Wrong password', 'danger')
            return redirect("/login")

        login_user(user)
        flash(f'{username} logged in', 'success')
        return redirect(f"/{user.id}/contact_list")

    return render_template("login.html", form=form)


@ app.route("/<int:user_id>/contact_list", methods=["POST", "GET"])
@login_required
def index(user_id):
    user = User.query.get_or_404(user_id)
    form = ContactForm()

    if form.validate_on_submit():
        contact_name = form.name.data
        contact_email = form.email.data
        contact_mob = form.mob.data

        contact = Contact.query.filter_by(user_id=user_id, email=contact_email).first()
        if contact:
            flash(f"There is already an existing contact named '{contact.name}' with this email!", 'danger')
            return redirect(f'/{user.id}/contact_list')

        contact = Contact.query.filter_by(user_id=user_id, mob=contact_mob).first()
        if contact:
            flash(f"There is already an existing contact named '{contact.name}' with this mobile no.!", 'danger')
            return redirect(f'/{user.id}/contact_list')

        new_contact = Contact(name=contact_name, email=contact_email, mob=contact_mob, user_id=user.id)

        try:
            db.session.add(new_contact)
            db.session.commit()
            flash(f'Contact created for {contact_name}!', 'success')
            return redirect(f'/{user.id}/contact_list')
        except:
            flash('Some error occured', 'warning')
            return redirect(f'/{user.id}/contact_list')

    contacts = Contact.query.filter_by(user_id=user.id).order_by(Contact.name).all()
    return render_template("index.html", user=user, contacts=contacts, form=form)


@ app.route("/<int:user_id>/delete/<int:contact_id>")
@login_required
def delete(user_id, contact_id):
    contact_to_delete = Contact.query.get_or_404(contact_id)
    try:
        db.session.delete(contact_to_delete)
        db.session.commit()
        flash(f'Contact {contact_to_delete.name} deleted!', 'warning')
        return redirect(f'/{contact_to_delete.user_id}/contact_list')
    except:
        return "Problem deleting"


@ app.route("/<int:user_id>/update/<int:contact_id>", methods=["POST", "GET"])
@login_required
def update(user_id, contact_id):
    form = ContactForm()
    contact_to_update = Contact.query.get_or_404(contact_id)

    if form.validate_on_submit():
        contact_to_update.name = form.name.data
        contact_to_update.email = form.email.data
        contact_to_update.mob = form.mob.data
        try:
            db.session.commit()
            flash(f'Contact {contact_to_update.name} updated!', 'success')
            return redirect(f'/{user_id}/contact_list')
        except:
            return "Problem updating"
    else:
        return render_template("update.html", contact=contact_to_update, form=form)



@ app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
