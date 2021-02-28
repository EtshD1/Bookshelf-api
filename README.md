# Bookshelf API
This is a small RESTful api with testing unit that can some book info.
## Running
You can use `python-dotenv` package to use the `.env` file, install using `pip3 install python-dotenv`, then run `flask run`. API uses SQLAlchemy with the dialect for postgeSQL.

API should run at port 5000 unless modified. All routes send JSON.
## Routes

- `/`:
GET: Sends a "Hello world" message. Used to check if API is running.

- `/books`:
GET: Gets a page if books if any are found in database. You can browse between pages by adding `page` parameter. ex: `/book?page=2`

- `/books/(Book ID)`:
GET: Gets a specifed book with the passed id parameter.

- `/books`:
POST: Creates a new book and adds it to database. Should have 'author' and 'name' in the request's body. Returns created book.

- `/books/(Book ID)`:
DELETE: Delete specified book from databse. Returns a page of books and books count.

- `/books/(Book ID)`:
PATCH: Updates specified book from databse. Should have 'author' and/or 'name' in the request's body. Returns updated book.

- `/books/(Book ID)`:
PUT: Replaces specified book from databse. Should have 'author' and 'name' in the request's body. Returns replaced book.



