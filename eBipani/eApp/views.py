from django.shortcuts import redirect, render
from django.db import connection

# Create your views here.


def hash(a):
    hv = 0
    p = 47
    m = 1e9 + 9
    p_pow = 1
    for c in a:
        hv = (hv + ord(c) * p_pow) % m
        p_pow = (p_pow * p) % m

    return int(hv)


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def searchProducts(request):
    td = []

    if request.method == 'GET' and 'searchBtn' in request.GET:
        searched = request.GET.get('searchBox')
        arr = searched.split()
        arr.insert(0, searched)
        query = """ (SELECT	CATEGORY_NAME,	PRODUCT_ID,	PRODUCT_NAME,	UNIT_PRICE,	UNITS_IN_STOCK,	IMAGE,	DESCRIPTION 
                    FROM	PRODUCT
                    WHERE UPPER(PRODUCT_NAME) LIKE %s )
                    UNION
                    (SELECT	CATEGORY_NAME,	PRODUCT_ID,	PRODUCT_NAME,	UNIT_PRICE,	UNITS_IN_STOCK,	IMAGE,	DESCRIPTION 
                    FROM	PRODUCT
                    WHERE UPPER(CATEGORY_NAME) LIKE %s )
                    UNION
                    (SELECT	CATEGORY_NAME,	PRODUCT_ID,	PRODUCT_NAME,	UNIT_PRICE,	UNITS_IN_STOCK,	IMAGE,	DESCRIPTION 
                    FROM	PRODUCT
                    WHERE UPPER(SUB_CATEGORY) LIKE %s )
                """
        for a in arr:
            a = '%' + a.upper() + '%'
            try:
                with connection.cursor() as c:
                    c.execute(query, [a, a, a])
                    tdata = dictfetchall(c)
                    if len(tdata) > 0:
                        td += tdata
            except:
                pass

    data = []
    [data.append(x) for x in td if x not in data]

    return render(request, 'productByCategory.html', {'data': data})


def sellerRegistration(request):
    data = {}
    if request.method == 'POST':
        sname = request.POST.get('sname')
        sregi = request.POST.get('sregi')
        mail = request.POST.get('mail')
        city = request.POST.get('city')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        bkash = request.POST.get('bkashno')
        pas = str(hash(request.POST.get('pas')))
        postal = request.POST.get('postal')
        role = 'Seller'

        with connection.cursor() as c:
            query = """select count(*) as flag from users where email = %s"""
            c.execute(query, [mail])
            d = dictfetchall(c)
            if d[0]['FLAG'] > 0:
                data['msg'] = 'Email already Exist'
            else:
                query = """insert into users values(%s,%s,%s,%s,%s,%s,%s)"""
                c.execute(query, [mail, pas, phone,
                          city, country, postal, role])
                query = """insert into SELLER values(%s,%s,%s,%s)"""
                c.execute(query, [mail, sname, sregi, bkash])
                data['msg'] = 'success'

    return render(request, "sellonhere.html", {'data': data})


def userSignin(request):
    data = {}
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        mail = request.POST.get('mail')
        city = request.POST.get('city')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        pas = str(hash(request.POST.get('pas')))
        postal = request.POST.get('postal')
        role = 'Customer'

        with connection.cursor() as c:
            query = """select count(*) as flag from users where email = %s"""
            c.execute(query, [mail])
            d = dictfetchall(c)
            if d[0]['FLAG'] > 0:
                data['msg'] = 'Email already Exist'
            else:
                query = """insert into users values(%s,%s,%s,%s,%s,%s,%s)"""
                c.execute(query, [mail, pas, phone,
                          city, country, postal, role])
                query = """insert into customer values(%s,%s,%s)"""
                c.execute(query, [mail, fname, lname])
                data['msg'] = 'success'

    return render(request, "signin.html", {'data': data})


def index(request):
    with connection.cursor() as c:
        query = """WITH temp_table AS 
        ( SELECT PRODUCT_ID, CATEGORY_NAME, PRODUCT_NAME, IMAGE, row_number ( ) over ( partition BY CATEGORY_NAME ORDER BY UNIT_PRICE ) AS rn 
        FROM PRODUCT ) 
        SELECT PRODUCT_ID, CATEGORY_NAME, PRODUCT_NAME, IMAGE 
        FROM temp_table 
        WHERE rn <= 5"""
        c.execute(query)

        t_data = dictfetchall(c)

        data = []
        while len(t_data) != 0:
            dt = [t_data[0]]

            i = 0
            for j in range(1, len(t_data)):
                if dt[0]["CATEGORY_NAME"] == t_data[j]["CATEGORY_NAME"]:
                    dt.append(t_data[j])
                    i = j
                else:
                    break

            t_data = t_data[i + 1:]
            data.append(dt)

    return render(request, 'index.html', {'data': data})


def productByCategory(request, category):
    with connection.cursor() as c:
        query = """ SELECT * 
                    FROM PRODUCT 
                    WHERE CATEGORY_NAME = %s"""
        c.execute(query, [category])
        data = dictfetchall(c)

    return render(request, 'productByCategory.html', {'data': data})


def individualProduct(request, category, id):
    data = {}
    query = """ SELECT PRODUCT_ID, PRODUCT_NAME, UNIT_PRICE, UNITS_IN_STOCK, IMAGE, DESCRIPTION
                FROM PRODUCT 
                WHERE CATEGORY_NAME = %s
                AND PRODUCT_ID = %s"""
    query1 = '''SELECT FIRST_NAME AS NAME, CUSTOMER_COMMENT AS REVIEW
                FROM REVIEW JOIN CUSTOMER
                ON REVIEW.CUSTOMER_EMAIL = CUSTOMER.EMAIL
                WHERE REVIEW.PRODUCT_ID = %s AND LENGTH(REVIEW.CUSTOMER_COMMENT) > 0'''

    with connection.cursor() as c:
        c.execute(query, [category, id])
        prod = dictfetchall(c)
        data['prod'] = prod

        c.execute(query1, [id])
        reviews = dictfetchall(c)
        data['reviews'] = reviews

    return render(request, 'individualProduct.html', data)


def userLogin(request):
    data = {}
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = str(hash(request.POST.get('password')))

            if request.session.has_key('email'):
                del request.session['email']

            with connection.cursor() as c:
                query = """SELECT ROLE
                            FROM C##EBIPANI.USERS 
                            WHERE EMAIL = %s AND PASSWORD = %s"""
                c.execute(query, [email, password])
                d = dictfetchall(c)

                if len(d) == 0:
                    data['msg'] = 'wrong credentials'
                elif d[0]['ROLE'] == 'Admin':
                    request.session['email'] = email
                    return redirect('/eApp/users/admin/')
                elif d[0]['ROLE'] == 'Seller':
                    request.session['email'] = email
                    return redirect('/eApp/users/seller/')
                elif d[0]['ROLE'] == 'Customer':
                    request.session['email'] = email
                    return redirect('/eApp/users/customer/')
                else:
                    data['msg'] = 'wrong credentials'

    except:
        pass

    return render(request, 'login.html', {'data': data})


def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return redirect('/eApp')
