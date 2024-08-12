from flask import render_template, current_app

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

    @app.route('/bookshelf')
    def bookshelf():
        book_keys = current_app.redis.keys('book:*')
        books = []
        for key in book_keys:
            book = current_app.redis.hgetall(key)
            book_details = {k: v for k, v in book.items()}
            # added book_key in book_details
            book_details['book_key'] = key
            books.append(book_details)
            print(key, book_details)
        
        return render_template('bookshelf.html', books=books)

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
    create_routes(app)