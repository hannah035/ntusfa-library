from flask import render_template, current_app, request, redirect
import time
import math
import pickle


books_per_page = 48

def load_dict():
    global mapp
    with open("ntusfa-library/app/datas/mapp.pickle", "rb") as f:
        mapp = pickle.load(f)

def create_routes(app):
    @app.route('/')
    def index():
        new_books = [
            {'title': '1984', 'author': 'George Orwell'},
            {'title': 'Brave New World', 'author': 'Aldous Huxley'},
        ]
        reviews = [
            {'user': 'Alice', 'comment': 'Great book!', 'book_title': '1984'},
            {'user': 'Bob', 'comment': 'Very interesting read.', 'book_title': 'Brave New World'},
        ]
        bookshelves = ['Shelf 1', 'Shelf 2', 'Shelf 3']
        
        return render_template('index.html', new_books=new_books, reviews=reviews, bookshelves=bookshelves)
    
    @app.route('/bookshelf/<page>', methods=['POST'])
    def my_form_post(page):
            text = request.form['query']
            book_keys=[]
            for key in mapp.keys():
                query = text
                if query in key:
                        book_keys.append('book:'+mapp[key])
            books = []
            page = 1
            page_start = 1
            page_end = math.ceil(len(book_keys)/books_per_page)
            # showing from books[book_start] to books[book_end]
            book_start = (page-1)*books_per_page
            book_end = page*books_per_page
            print(page_end)
            i = 0

            for key in book_keys: 
                if i>=book_start and i<book_end:
                    book = current_app.redis.hgetall(key)
                    book_details = {k: v for k, v in book.items()}
                    # added book_key in book_details
                    book_details['book_key'] = key
                    books.append(book_details)
                if i>=book_end:
                    break
                i+=1
            book_end = i
            return render_template('bookshelf.html', books=books, books_count =len(book_keys), page_current = page, page_start = page_start, page_end = page_end, book_start=book_start+1, book_end = book_end)
    @app.route('/bookshelf/<page>')
    def bookshelf(page):
        
        book_keys=[]
        for key in mapp.keys():
            book_keys.append('book:'+mapp[key])
        books = []
        page = int(page)
        page_start = 1
        page_end = math.ceil(len(book_keys)/books_per_page)
        # showing from books[book_start] to books[book_end]
        book_start = (page-1)*books_per_page
        book_end = page*books_per_page
        i = 0

        for key in book_keys: 
            if i>=book_start and i<book_end:
                book = current_app.redis.hgetall(key)
                book_details = {k: v for k, v in book.items()}
                # added book_key in book_details
                book_details['book_key'] = key
                books.append(book_details)
            if i>=book_end:
                break
            i+=1
        book_end = i 
        return render_template('bookshelf.html', books=books, books_count =len(book_keys), page_current = page, page_start = page_start, page_end = page_end, book_start=book_start+1, book_end=book_end)
    @app.route('/side')
    def side():
        return render_template('side.html')
    @app.route('/side', methods=['POST'])
    def borrow_book():
        ## get userID and bookID from form(borrow)
        identifier = request.form['identifier']
        if identifier == 'review':
            bookID = request.form['bookId']
            review = request.form['review']
            print('review', bookID, review)
        else:
            bookID = request.form['bookId']
            userID = request.form['userId']
            print('borrow',bookID, userID)
       
        # current_app.redis.rpush(f'review:{bookID}', review)

        
        # TODO: send borrow request to database
        return redirect(request.referrer)
    @app.route('/book/<isbn>')
    def book_detail(isbn):
        # book_key = f'book:{isbn}'
        # 避免book:book:isbn的情況
        book_key = f'{isbn}'
        # 獲取書籍詳細信息
        book = current_app.redis.hgetall(book_key)
        book_details = {k: v for k, v in book.items()}
        
        return render_template('book_detail.html', book=book_details)

def init_app(app):
    load_dict()
    create_routes(app)