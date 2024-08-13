# Blog with Flask
This is a project for a simple blog developed with Flask and Python, using HTML and CSS for the frontend. The site allows users to create, edit, and delete posts. The post information is stored in an SQLite database located in the instance folder.

## Features
- **Create Posts**: Users can create new blog posts.
- **Edit Posts**: Existing posts can be edited.
- **Delete Posts**: Users can delete posts they no longer wish to display.
- **View Posts**: All posts are displayed on the blog's homepage.

## Requirements
- **Python 3.x**: Make sure you have Python 3.x installed in your environment.
- **IDE**: For this project, I used <a href="https://www.jetbrains.com/pycharm/download/?section=windows">PyCharm</a> (Community Edition).
- **Flask**: A micro web framework for Python.
- **Flask-SQLAlchemy**: A Flask extension that makes it easier to use databases with SQLAlchemy.
- <a href="https://sqlitebrowser.org/dl/">**DB Browser for SQLite**</a>: An optional GUI software recommended for viewing and editing the SQLite database.

To install Flask and Flask-SQLAlchemy, you can use the following command:

`pip install Flask Flask-SQLAlchemy`

## Initial Appearance

You can create your posts by filling out the input field and clicking ***submit***. The posts will appear on the same page.

<p align="center">
<img src="https://github.com/user-attachments/assets/dd59f869-5fe9-4523-8344-fd76c1c71433" alt="" width="900">
</p>

Clicking ***edit*** redirects you to the post editing page:
<p align="center">
<img src="https://github.com/user-attachments/assets/c64493db-3d31-4a38-b7f1-20898d957c2b" alt="" width="900">
</p>

Clicking ***delete*** removes the post from the database.

## Database

To use **DB Browser for SQLite** as the database, simply import the `blog.sqlite3` file. Step-by-step:

1. Open DB Browser for SQLite and click _Open Database_.
2. Select the `blog.sqlite3` file (inside the `instance` folder) in the `flask_app` directory.
3. To navigate through the _posts_ table, simply click on _Browse Data_.

### Additional Information
Feel free to explore and contribute to this project. Your feedback and suggestions are highly appreciated.
