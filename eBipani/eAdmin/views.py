from django.db import connection
from django.shortcuts import render, redirect
from eApp.views import dictfetchall, hash


# Create your views here.
def index(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')
    return render(request, 'adminHome.html')


def check(request):
    if request.session.has_key('email'):
        mail = request.session['email']
        with connection.cursor() as c:
            role = c.callfunc("GET_ROLE", str, [mail])
        if role == 'ADMIN':
            return True
        else:
            return False
    else:
        return False


def customer(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')
    data = {}
    d = {}
    query = """SELECT (c.FIRST_NAME || ' ' || c.SECOND_NAME) as Name, u.EMAIL,u.PHONE,u.CITY,u.COUNTRY,u.POSTAL_CODE from users u join CUSTOMER c on c.EMAIL=u.EMAIL"""
    with connection.cursor() as c:
        c.execute(query)
        data['data'] = dictfetchall(c)
    return render(request, 'customer.html', {'data': data})


def deleteCustomer(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    if request.method == 'POST':
        email = request.POST.get('email')
    data = {}
    d = {}
    query = """SELECT * FROM USERS WHERE EMAIL=%s"""
    with connection.cursor() as c:
        c.execute(query, [email])
        d = dictfetchall(c)
        if len(d) != 0:
            query = """DELETE FROM CUSTOMER WHERE EMAIL=%s"""
            c.execute(query, [email])
            query = """DELETE FROM USERS WHERE EMAIL=%s"""
            c.execute(query, [email])

            data['msg'] = 'User Successfully Deleted'
        query = """SELECT (c.FIRST_NAME || ' ' || c.SECOND_NAME) as Name, u.EMAIL,u.PHONE,u.CITY,u.COUNTRY,u.POSTAL_CODE from users u join CUSTOMER c on c.EMAIL=u.EMAIL"""
        c.execute(query)
        data['data'] = dictfetchall(c)
    return render(request, 'customer.html', {'data': data})


def searchCustomer(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    d = {}
    if request.method == 'POST':
        src = request.POST.get('search')
        s = '%'+src+'%'
        query = """SELECT (c.FIRST_NAME || ' ' || c.SECOND_NAME) as Name, u.EMAIL,u.PHONE,u.CITY,u.COUNTRY,u.POSTAL_CODE from users u join CUSTOMER c on c.EMAIL=u.EMAIL WHERE c.EMAIL LIKE %s OR (c.FIRST_NAME || ' ' || c.SECOND_NAME) LIKE %s"""
        with connection.cursor() as c:
            c.execute(query, ['%'+src+'%', '%'+src+'%'])
            data['data'] = dictfetchall(c)
    return render(request, 'customer.html', {'data': data})


def seller(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    d = {}
    query = """SELECT s.SHOP_NAME,s.REGISTRATION_NO,s.BKASH_NO,u.EMAIL,u.PHONE,u.CITY,u.COUNTRY,u.POSTAL_CODE from users u join SELLER s on s.EMAIL=u.EMAIL"""
    with connection.cursor() as c:
        c.execute(query)
        data['data'] = dictfetchall(c)
    return render(request, 'seller.html', {'data': data})


def deleteSeller(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    if request.method == 'POST':
        email = request.POST.get('email')
    data = {}
    d = {}
    query = """SELECT * FROM USERS WHERE EMAIL=%s"""
    with connection.cursor() as c:
        c.execute(query, [email])
        d = dictfetchall(c)
        if len(d) != 0:
            query = """DELETE FROM SELLER WHERE EMAIL=%s"""
            c.execute(query, [email])
            query = """DELETE FROM USERS WHERE EMAIL=%s"""
            c.execute(query, [email])

            data['msg'] = 'User Successfully Deleted'
        query = """SELECT s.SHOP_NAME,s.REGISTRATION_NO,s.BKASH_NO,u.EMAIL,u.PHONE,u.CITY,u.COUNTRY,u.POSTAL_CODE from users u join SELLER s on s.EMAIL=u.EMAIL"""
        c.execute(query)
        data['data'] = dictfetchall(c)
    return render(request, 'seller.html', {'data': data})


def searchSeller(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    d = {}
    if request.method == 'POST':
        src = request.POST.get('search')
        s = '%'+src+'%'
        query = """SELECT s.SHOP_NAME,s.REGISTRATION_NO,s.BKASH_NO,u.EMAIL,u.PHONE,u.CITY,u.COUNTRY,u.POSTAL_CODE from users u join SELLER s on s.EMAIL=u.EMAIL WHERE s.EMAIL LIKE %s OR s.SHOP_NAME LIKE %s"""
        with connection.cursor() as c:
            c.execute(query, ['%'+src+'%', '%'+src+'%'])
            data['data'] = dictfetchall(c)
    return render(request, 'seller.html', {'data': data})


def shipper(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    query = """SELECT * from SHIPPER """
    with connection.cursor() as c:
        c.execute(query)
        data['data'] = dictfetchall(c)
    return render(request, 'shipper.html', {'data': data})


def addShipper(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    return render(request, 'addShipper.html')


def regShipper(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    if request.method == 'POST':
        cName = request.POST.get('Cname')
        phone = request.POST.get('phone')
        postal = request.POST.get('postal')

        with connection.cursor() as c:
            query = """select * from SHIPPER where POSTAL_CODE = %s"""
            c.execute(query, [postal])
            d = dictfetchall(c)
            if len(d) > 0:
                data['msg'] = 'A Shipper already exist in that area. Please Enter new postal area code.'
            else:
                query = """insert into SHIPPER(COMPANY_NAME,PHONE,POSTAL_CODE) values(%s,%s,%s)"""
                c.execute(query, [cName, phone, postal])
                data['msg'] = 'Shipper Succesfully Added'
    return render(request, 'addShipper.html', {'data': data})


def editShipper(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    if request.method == 'POST':
        id = request.POST.get('id')
        with connection.cursor() as c:
            query = """select * from SHIPPER where SHIPPER_ID = %s"""
            c.execute(query, [id])
            d = dictfetchall(c)
            if len(d) > 0:
                data['id'] = d[0]['SHIPPER_ID']
                data['cName'] = d[0]['COMPANY_NAME']
                data['phone'] = d[0]['PHONE']
                data['postal'] = d[0]['POSTAL_CODE']
            else:
                data['msg'] = 'Shipper Not Found!'
    return render(request, 'editShipper.html', {'data': data})


def updateShipper(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    if request.method == 'POST':
        id = request.POST.get('id')
        cName = request.POST.get('Cname')
        phone = request.POST.get('phone')
        postal = request.POST.get('postal')

        with connection.cursor() as c:
            query = """update SHIPPER
                       set COMPANY_NAME=%s,PHONE=%s,POSTAL_CODE=%s where SHIPPER_ID=%s"""
            c.execute(query, [cName, phone, postal, id])
            data['id'] = id
            data['cName'] = cName
            data['phone'] = phone
            data['postal'] = postal
            data['msg'] = 'success'
    return render(request, 'editShipper.html', {'data': data})


def deleteShipper(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    if request.method == 'POST':
        id = request.POST.get('id')
        with connection.cursor() as c:
            query = """DELETE from SHIPPER where SHIPPER_ID=%s"""
            c.execute(query, [id])
            data['msg'] = 'Shipper Removed'
            query = """SELECT * from SHIPPER"""
            c.execute(query)
            data['data'] = dictfetchall(c)
    return render(request, 'shipper.html', {'data': data})


def searchShipper(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    d = {}
    if request.method == 'POST':
        src = request.POST.get('search')
        s = '%'+src+'%'
        query = """SELECT * from SHIPPER WHERE COMPANY_NAME LIKE %s OR POSTAL_CODE LIKE %s"""
        with connection.cursor() as c:
            c.execute(query, ['%'+src+'%', '%'+src+'%'])
            data['data'] = dictfetchall(c)
    return render(request, 'shipper.html', {'data': data})


def newAdmin(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    return render(request, 'newAdmin.html', {'data': data})


def registerAdmin(request):
    if check(request) is False:
        return redirect('/eApp/users/login/')

    data = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pas = str(hash(request.POST.get('pas')))
        role = "Admin"

    with connection.cursor() as c:
        query = """select * from users where email = %s"""
        c.execute(query, [email])
        d = dictfetchall(c)
        if len(d) > 0:
            data['msg'] = 'Email already Exist'
        else:
            query = """insert into users(EMAIL,PASSWORD,PHONE,ROLE) values(%s,%s,%s,%s)"""
            c.execute(query, [email, pas, phone, role])
            data['msg'] = 'success'
    return render(request, "newAdmin.html", {'data': data})
