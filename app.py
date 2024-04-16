from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

#You need an OMDb API Key for this. https://www.omdbapi.com/
omdbApiKey = '<OMDB API KEY>'

#MySQL Connection
conn = mysql.connector.connect(
    host = 'localhost', 
    user = 'root', 
    password = '<DB PASSWORD>', 
    database = 'FlaskProject')

@app.route('/')
def home():
    cursor = conn.cursor()
    #Find newest reviews by highest ID in database.
    cursor.execute("SELECT * FROM reviews ORDER BY id DESC LIMIT 4")
    reviews = cursor.fetchall()
    return render_template('home.html', reviews = reviews, apikey = omdbApiKey)

@app.route('/genres')
def genres():
   return render_template('genres.html')

@app.route('/genres/<string:genre>')
def searchGenre(genre):
    cursor = conn.cursor()
    # https://www.w3schools.com/sql/sql_like.asp
    searchQuery = f'%{genre}%'
    #Search for reviews by genre
    cursor.execute('SELECT * FROM reviews WHERE genre LIKE %s', (searchQuery, ))
    reviews = cursor.fetchall()
    if not reviews:
        return render_template('pageNotFound.html')
    return render_template('searchResults.html', reviews = reviews, apikey = omdbApiKey)

@app.route('/reviews')
def allReviews():
    cursor = conn.cursor()
    #Fetching all reviews
    cursor.execute("SELECT * FROM reviews")
    reviews = cursor.fetchall()
    return render_template('allReviews.html', reviews = reviews, apikey = omdbApiKey)

@app.route('/search', methods=['GET','POST'])
def searchMovie():
    if request.method == 'POST':
        #Takes input from search field and passes it on
        query = request.form['search_movie']
        return redirect(url_for('movieResults', movie=query))
    return render_template('searchReview.html')

@app.route('/search/<string:movie>', methods=['GET'])
def movieResults(movie):
    cursor = conn.cursor()
    # https://www.w3schools.com/sql/sql_like.asp
    searchQuery = f'%{movie}%'
    cursor.execute('SELECT * FROM reviews WHERE name LIKE %s', (searchQuery, ))
    reviews = cursor.fetchall()
    if not reviews:
        return render_template('pageNotFound.html')
    return render_template('searchResults.html', reviews = reviews, apikey = omdbApiKey)

@app.route('/review/<int:id>', methods=['GET','POST'])
def renderReview(id):
    cursor= conn.cursor()
    #If method is POST, this is a comment. Add to DB.
    if request.method == 'POST':
        date = datetime.now()
        # https://www.w3schools.com/python/python_datetime.asp
        commentdate = date.strftime('%Y-%m-%d')
        comment = request.form['review_comment']
        cursor.execute('INSERT INTO comments (comment_text, review_id, comment_date) values(%s, %s, %s)', (comment, id, commentdate))
        conn.commit()
        current_url = request.url
        return redirect(current_url)
    cursor.execute('SELECT * FROM reviews WHERE id=%s', (id, ))
    review = cursor.fetchone()
    #If review is not found, render page not found.
    if not review:
        return render_template('pageNotFound.html')
    #Find comments for specified review.
    cursor.execute('SELECT * FROM comments WHERE review_id=%s', (id, ))
    comments = cursor.fetchall()
    return render_template('movieReview.html', review = review, comments = comments, apikey = omdbApiKey)


@app.route('/admin', methods=['GET','POST'])
def adminLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #Checking to see if username and password are admin
        if username == 'admin' and password == 'admin':
            return redirect(url_for('adminHome', alert=None))
        else:
            #If login is not correct, will return with an error
            return render_template('adminLogin.html', error='Error')
    return render_template('adminLogin.html', error=None)

@app.route('/admin/home')
def adminHome():
    alert = request.args.get('alert')
    return render_template('adminHome.html', alert=alert)

@app.route('/admin/addReview', methods=['GET','POST'])
def addReview():
    if request.method == 'POST':
        name = request.form['movie_name']
        rating = request.form['rating']
        author = request.form['author']
        genre = request.form['genre']
        review = request.form['review']
        date = datetime.today().date()
        pubdate = date.strftime('%Y-%m-%d')
        imdbid = request.form['imdbid']
        cursor= conn.cursor()
        #Add all form responses as review to DB
        cursor.execute('INSERT INTO reviews (name, rating, author, genre, pubdate, review, imdbid) values(%s, %s, %s, %s, %s, %s, %s)',(name, rating, author, genre, pubdate, review, imdbid))
        conn.commit()
        return redirect(url_for('adminHome', alert=True, alert_message="Successfully added new review!"))
    return render_template('adminAddReview.html')

@app.route('/admin/updateReview/<int:id>', methods=['GET','POST'])
def updateReview(id):
    cursor= conn.cursor()
    if request.method == 'POST':
        name = request.form['movie_name']
        rating = request.form['rating']
        author = request.form['author']
        genre = request.form['genre']
        review = request.form['review']
        date = datetime.today().date()
        pubdate = date.strftime('%Y-%m-%d')
        imdbid = request.form['imdbid']
        #Updating DB with new information
        cursor.execute('UPDATE reviews SET name=%s, rating=%s, author=%s, genre=%s, pubdate=%s, review=%s, imdbid=%s WHERE id=%s', (name, rating, author, genre, pubdate, review, imdbid, id))
        conn.commit()
        return redirect(url_for('adminHome'))
        
    cursor.execute('SELECT * FROM reviews WHERE id=%s', (id, ))
    review = cursor.fetchone()
    return render_template('adminUpdateReview.html', review=review)

@app.route('/admin/listAdminReviews', methods=['GET'])
def listAdminReviews():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM reviews')
    reviews = cursor.fetchall()
    return render_template('adminListReviews.html', reviews = reviews)

@app.route('/admin/deleteReview/<int:id>', methods=['GET'])
def deleteReview(id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM reviews WHERE id=%s', (id,))
    conn.commit()
    return redirect(url_for('listAdminReviews', alert=True, alert_message='Successfully deleted review!'))


if __name__=='__main__':
    app.run(debug=True)
