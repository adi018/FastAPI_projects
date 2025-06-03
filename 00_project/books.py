from fastapi import Body, FastAPI

app = FastAPI()
### GET => Read Data
### POST => Creation of new Data
### PUT => Update existing Data
### DELETE => Delete existing Data

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

### GET => Read Data
### GET => Cannot have Body() in GET requests
# Get all books
@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/mybook")
async def read_all_books():
    return {"book_title": "favourite book", "author": "favourite author", "category": "favourite category"}

## PARAMETERS: PATH
# Get all books with a dynamic parameter
# For example: for "param1" value, the URL would be:
# http://127.0.0.1:8000/books/param1
@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param: str):
    return {"dynamic_param": dynamic_param, "message": "This is a dynamic parameter example"}
    
# Get a specific book by title using path parameters
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

## PARAMETERS: QUERY
# Get all books from a specific category using path parameters
# For example: for "math" category, the URL would be:
# http://127.0.0.1:8000/books/?category=math
@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# Get all books from a specific author using path or query parameters
# For example: for "Author One", the URL would be:
# http://127.0.0.1:8000/books/byauthor/?author=author%20one
@app.get("/books/byauthor/")
async def read_books_by_author_path(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)

    return books_to_return

## PARAMETERS: PATH + QUERY
# For example: for "Author Two", the URL for query "category=science" would be:
# http://127.0.0.1:8000/books/Author%20Two/?category=science
# Here, the author is passed as a path parameter
# and the category as a query parameter
# %20 is the URL encoding for a space character; Author%20Two = Author Two
@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


### POST => Creation of new Data
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

### PUT => Update existing Data
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

### DELETE => Delete existing Data
# Here, we delete a book by its title i.e. PATH PARAMETER {book_title}
# if the book title is "Title Four", the URL would be:
# http://127.0.0.1:8000/books/delete_book/title%20four
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

### Assignemnt
## Using PATH PARAMETER:
# for example, for "Author Two", the URL would be:
# http://127.0.0.1:8000/books/all_path/author%20two
@app.get("/books/all_path/{author}")
async def all_books_from_author_using_path(author: str):
    all_books = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            all_books.append(book)
    if not all_books:
        return {"message": f"No books found for author: {author}"}
    return all_books

## Using QUERY PARAMETER:
# for example, for "Author Two", the URL would be:
# http://127.0.0.1:8000/books/all_query/?category=author%20two
@app.get("/books/all_query/")
async def all_books_from_author_using_category(category: str):
    all_books = []
    for book in BOOKS:
        if book.get('author').casefold() == category.casefold():
            all_books.append(book)
    if not all_books:
        return {"message": f"No books found for author: {category}"}
    return all_books