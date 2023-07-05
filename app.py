from flask import Flask, render_template, request
import pickle
import math 
import numpy as np

popular_df = pickle.load(open('popularBooks.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author = list(popular_df['Book-Author'].values),
                           image = list(popular_df['Image-URL-M'].values),
                           votes = list(popular_df['Num-Rating'].values),
                           rating = list(round(ratings, 2) for ratings in popular_df['Avg-Rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    #index fetch
    index = np.where(pt.index==user_input)[0][0]
    #calculate distance with every other book
    #distance = similarity_scores[index]
    #similar books from below formula
    similar_items = sorted(list(enumerate(similarity_scores[index])), key = lambda x:x[1], reverse = True)[1:11]
    
    data = []
    for i in similar_items:
        item = []
        ##print(books[books['Book-Title'] == pt.index[i[0]]]) (print the whole dataset that matches with the pt.index value)
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        
        ## append will create extended dimension array so we will use extend function
        #item.append(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        #item.append(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        #item.append(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)
        
    print(data)
    return render_template('recommend.html', data = data)


if __name__ == '__main__':
    app.run(debug=True)
