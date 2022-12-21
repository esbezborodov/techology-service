from flask import render_template, request, redirect
from forms import ProductForm, LoginForm, AuthozizateForm, CommentForm
from table import Users, Products, Comments, db, app
from flask_login import login_required, logout_user, LoginManager, login_user
from werkzeug.security import check_password_hash, generate_password_hash

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)



        # СПИСОК ТОВАРОВ """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@app.route('/', methods=['GET', 'POST'])
def home():
    global c_a
    def check_admin():
        try:
            if admin == True:
                c_a = True
                return c_a
            else:
                c_a = False
                return c_a 
        except NameError:
            c_a = None
            return c_a
    c_a = check_admin()


    if request.method=="POST":
        select = request.form.get('comp_select')
        if select == "price":
            products = Products.query.order_by(Products.price).all()

        if select == "type1":
            products = Products.query.filter_by(type='Голова').all()
            
        if select == "type2":
            products = Products.query.filter_by(type='Картридж').all()

        if select == "":
            products = Products.query.order_by(Products.id).all()
    else:
        products = Products.query.order_by(Products.id).all()
    return render_template("home.html", products=products, c_a=c_a)



        #СОЗДАНИЕ ТОВАРА (АДМИН) """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        type = request.form['type']
        name = request.form['name']
        description = request.form['description']
        manufacturer = request.form['manufacturer']
        price = request.form['price']
        photo = request.files['photo']

        price = int(price)

        products = Products(type=type, name=name, description=description, manufacturer=manufacturer, price=price, photo=photo.filename)
        db.session.add(products)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add.html', form=ProductForm())



     # АВТОРИЗАЦИЯ """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@app.route('/login', methods=['GET', 'POST'])
def login():
    global admin

    form = LoginForm()

    if form.validate_on_submit():

        login = form.login.data
        password = form.password.data

        user = Users.query.filter_by(login=login).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                user = Users.query.filter_by(login=login).first()
                admin = user.admin
                return redirect('/')
    return render_template('login.html', form=form)



        # РЕГИСТРАЦИЯ """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AuthozizateForm()

    if form.validate_on_submit():

        login = form.login.data
        password = form.password.data

        hash_password = generate_password_hash(password)
        new_user = Users(login=login, password=hash_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    else:
        return render_template('register.html', form=form)



        # ФУНКЦИЯ ВЫХОДА """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    global admin
    del(admin)
    logout_user()
    return redirect('/')



        # СТРАНИЦА ПРОДУКТА """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@app.route('/<int:id>', methods=['GET', 'POST'])
def product_page(id):
    global admin
    product = Products.query.get(id)
    comments = Comments.query.filter_by(prod_id=id).all()
    form = CommentForm()

    if form.validate_on_submit():
        like = form.like.data
        comment = form.comment.data

        new_comment = Comments(prod_id=id, like=like, comment=comment)
        db.session.add(new_comment)
        db.session.commit()
    def check_admin():
        try:
            if admin == True:
                c_a = True
                return c_a
            else:
                c_a = False
                return c_a 
        except NameError:
            c_a = None
            return c_a
    c_a = check_admin()
    
    return render_template("product.html", c_a = c_a, product=product, form=form, comments=comments, )



        # УДАЛЕНИЕ ТОВАРА (АДМИН) """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@app.route('/delete/<int:id>/del')
def delete(id):
    u = db.session.get(Products, id)
    db.session.delete(u)
    db.session.commit()
    return redirect('/')



        # РЕДАКТИРОВАНИЕ ТОВАРА (АДМИН) """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

@app.route('/add/<int:id>/ed', methods=["GET", "POST"])
def edite(id):
    form = ProductForm()
    if request.method == "POST":
        k = Products.query.filter_by(id=id).first()
        mas_db = [k.type, k.name, k.description, k.manufacturer, k.price, k.photo]
        print(k)
        print(mas_db)
        type = request.form['type']
        name = request.form['name']
        description = request.form['description']
        manufacturer = request.form['manufacturer']
        price = request.form['price']
        photo = request.files['photo']
        mass_db = [type, name, description, manufacturer, price, photo]
        if mass_db[5].filename == "":
            mass_db[5] = str('')
        for i in range(len(mass_db)):
            if mass_db[i] != "":
                mas_db[i] = mass_db[i]
            print(mas_db)
        k.type = str(mas_db[0])
        k.name = str(mas_db[1])
        k.description = str(mas_db[2])
        k.manufacturer = str(mas_db[3])
        k.price = str(mas_db[4])
        k.photo = str(mas_db[5])

        db.session.commit()
        return redirect('/')
    return render_template('edit.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)