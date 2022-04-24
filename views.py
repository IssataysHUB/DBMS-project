import pandas as pd
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import cx_Oracle
import matplotlib.pyplot as plt
import base64
import sys
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage



def books(request):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/orclpdb", encoding="UTF8")
    cursor = connection.cursor()
    print("Connected to Oracle")
    sql = "Select * from books"
    cursor.execute(sql)
    rows = cursor.fetchall()

    paginator = Paginator(rows, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    cursor.close()
    return render(request, 'index.html', {'data': contacts})


def upload(request):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/orclpdb", encoding="UTF8")
    cursor = connection.cursor()
    book_id = request.POST.get('id')
    title = request.POST.get('title')
    author = request.POST.get('author')
    price = request.POST.get('price')
    isbn = request.POST.get('isbn')
    cursor.callproc('insert_all_books', [book_id, title, author,
                                        isbn, price])
    upload = request.FILES['upload']
    fss = FileSystemStorage()
    file = fss.save(book_id + ".jpg", upload)
    connection.commit()
    cursor.close()
    return redirect('/football')


def uploadForm(request):
    return render(request, 'upload.html')


def detail(request, book_id):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/orclpdb", encoding="UTF8")
    cursor = connection.cursor()
    cursor.execute("Select * from books where id = " + str(book_id))
    rows = cursor.fetchone()
    connection.commit()
    cursor.close()
    return render(request, 'detail.html', {'data': rows})


def updated(request, book_id):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/orclpdb", encoding="UTF8")
    cursor = connection.cursor()
    title = request.POST.get('title')
    author = request.POST.get('author')
    price = request.POST.get('price')
    isbn = request.POST.get('isbn')
    price = int(price)
    cursor.callproc('update_book', [
                                    book_id,
                                    title,
                                    author,
                                    isbn,
                                    price])
    connection.commit()
    cursor.close()
    return redirect('/books/' + str(book_id))


def edit(request, book_id):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/orclpdb", encoding="UTF8")
    cursor = connection.cursor()
    cursor.execute("Select * from books where id = " + str(book_id))
    rows = cursor.fetchone()
    connection.commit()
    cursor.close()
    return render(request, 'update.html', {'data': rows})


def delete(request, book_id):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/orclpdb", encoding="UTF8")
    cursor = connection.cursor()
    cursor.callproc('delete_book', [book_id])
    connection.commit()
    cursor.close()
    return redirect('/football')


def sort(request):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/orclpdb", encoding="UTF8")
    sorting_filter = request.POST['sorting-name']
    order_type = request.POST['order_type']
    cursor = connection.cursor()
    cursor.execute("Select * from books order by {} {}".format(sorting_filter, order_type))
    rows = cursor.fetchall()
    paginator = Paginator(rows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    connection.commit()
    cursor.close()
    return render(request, 'index.html', {'data': page_obj})


def search(request):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/orclpdb", encoding="UTF8")
    searching_object = request.POST['input-search']
    searching_filter = request.POST['searching-name']
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE {} = '{}'".format(searching_filter, searching_object))
    rows = cursor.fetchall()
    paginator = Paginator(rows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    connection.commit()
    cursor.close()
    return render(request, 'index.html', {'data': page_obj})


def filter(request):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/orclpdb", encoding="UTF8")
    f_author = request.POST['author']

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM books WHERE author = '{}'".format(f_author))
    rows = cursor.fetchall()
    paginator = Paginator(rows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    connection.commit()
    cursor.close()
    return render(request, 'index.html', {'data': page_obj})


def statistics(request):
    connection = cx_Oracle.connect("hr", "hr", "localhost:1521/orclpdb", encoding="UTF8")
    books = pd.read_sql("SELECT * FROM books", con=connection)
    books = books.convert_dtypes()
    books.columns = books.columns.str.lower()
    # pivot2 = cars.pivot_table(index='fueltype', values='manufacturer', aggfunc='count')
    # pivot2.sort_values(by='manufacturer', ascending=False).head(9).plot(figsize=(15, 6), style='o-', grid=True)
    # plt.title("The count of cars grouped by fueltype")
    # plt.ylabel("Count of cars")
    # plt.savefig('my_plot.png')
    #
    # pivot = cars.pivot_table(index='wheel', values='id', aggfunc='count')
    # pivot.plot(y='id', figsize=(10, 10), kind='pie', grid=True)
    # plt.title('Ratio of wheel''s side')
    # plt.ylabel('')
    # plt.savefig('pie.png')

    return render(request, 'statistics.html')