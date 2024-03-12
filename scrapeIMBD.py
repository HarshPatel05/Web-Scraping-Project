from bs4 import BeautifulSoup
import requests
import csv


# Open CSV file in write mode, 'w' means the file is in write mode
csvfile = open('IMBD_Movie_Ratings.csv', 'w')
writer = csv.writer(csvfile)

# Writing column headers
writer.writerow(['Rank', 'Movie', 'Year', 'IMDB Rating', 'No. of Ratings'])


try:
    # We were getting a "403 Client Error: Forbidden for url: https://www.imdb.com/chart/top/" error. 
    # This is the most common reason for a website to block a web scraper and return a 403 error is because you is telling the website you are a scraper in the user-agents you send to the website when making your requests.
    # The solution to this problem is to configure your scraper to send a fake user-agent with every request. This way it is harder for the website to tell if your requests are coming from a scraper or a real user.
    # Got this solution from, "https://scrapeops.io/web-scraping-playbook/403-forbidden-error-web-scraping/"
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E14'}
    
    # Using request module to access the website from which we want to scrape the data
    # What does line6 do? It access the website and return a response object, this response object is being stored in the varaible source. The response object "source" is going to have the html source code of the website.
    # Always put the response object "source" in try and except block, because if the website is down or the url is wrong, then the code will throw an error.
    source = requests.get('https://www.imdb.com/chart/top/', headers=HEADERS)

    # This raise for status is going to throw an error if the website is down or the url is wrong.
    source.raise_for_status()
    
    # In this line, BeautifulSoup is going to take the html content/source code of this website/webpage and parse it using the html parser. This is going to return a BeautifulSoup object which is going to be stored in my varaible soup.
    soup = BeautifulSoup(source.text, 'html.parser')
    
    # This line will print the html source code of the website in text format. (just for testing purpose)
    # print(soup) 
    
    # Writing the HTML source code to a text file
    # with open('imdb_source.txt', 'w', encoding='utf-8') as file:
    #     file.write(str(soup))    
    # print("HTML source code saved to 'imdb_source.txt'")
    
    # find is method that is available with the beautiful soup object, find is going to basically fetch the first match.
    # In this case, I am trying to find a tag 'ul' with a class name. The class name or class is kind of like a identifier in pyhton it can be anything a "class", "data-testid", "id", "role", "style", etc. Notice whenever we try to access a class we write "class_" with the underscore.
    # So here the 'ul' tag consists of all the data for 250 movies, that is why we are fetching it
    
    # !!!!! movies = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base") !!!!!!
    
    # This line will print the movie data for 250 movies in text format. (just for testing purpose)
    # print(movies)
    
    # Writing the movie data to a text file
    # with open('imdb_movieData.txt', 'w', encoding='utf-8') as file:
    #     file.write(str(movies))
    # print("Movie data saved to 'imdb_movieData.txt'")
    
    # After getting the whole bunch of data we fetch the 250 movies individually using the find_all method, the tag that stores data of each movie they all start with 'li' and have a class name so we use that in find_all. Now, here find_all will return a list.
    movies = soup.find('ul', class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base").find_all('li', class_="ipc-metadata-list-summary-item sc-10233bc-0 iherUv cli-parent")
    
    # This line will print the length of movie list which should be 250 cause we have 250 movies (just for testing purpose)
    # print(len (movies))
    
    for movie in movies:
        
        # To understand the next few lines of code, be sure you have the source code directly from the website open up or open the imbd_movieData.txt file and use 'Ctrl+f' to search the following tags or class to get an idea of what are dealing with or how we are dealing with. You do have to uncomment the code that lets you make a txt file that contains the source code and movie data once you uncomment them just run and you will see them.

        
        # fetching the movie name from the h3 tag and also giving the find method the class name(if you don't have the class name then it is fine it will just give you the data of the first tag it finds). get_text converts the data into text so we can strip it and split it since the movie name and rank is in 1 string. Ex: 1. The Shawshank Redemption, so we split at '.' to get rank and movie seperately. To get the movie we get the index 1.
        
        # Note: 'strip=True' specifies that any leading or trailing whitespace characters should be removed from the text before returning it. So when strip=True, it ensures that any whitespace characters such as spaces, tabs, or newline characters at the beginning or end of the text are removed.
        name = movie.find('h3', class_="ipc-title__text").get_text(strip=True).split('. ')[1] 
        
        # To get the rank we get the index 0
        rank = movie.find('h3', class_="ipc-title__text").get_text(strip=True).split('. ')[0]
        
        
        # Now, year is in a different tag. First, find the tag enter the class if you have that information and if you look at the data the year is embbeded in the another tag under the div named span. Now to print it we have to convert it to text so we do span.text. We do have 3 span tag with exact same class name but the year is stored in the first tag and remember that find method only gives us the first occurance.
        year = movie.find('div', class_="sc-b0691f29-7 hrgukm cli-title-metadata").span.text
        
        
        # Rating is also stored in somewhat similar manner to year, embbeded in the another tag under the div(a different div look at the class name they are different) named span. But the format is a bit weird because rating and no. of rating are 1 string ['9.3(2.9M)']. So to get the rating we first split the at '(' and get index 0 cause rating is stored first.
        rating = movie.find('div', class_="sc-e2dbc1a3-0 ajrIH sc-b0691f29-2 bhhtyj cli-ratings-container").span.get_text(strip=True).split('(')[0]
        
        # To get the no. of ratings we get the index 1 but we also strip the single backet ')' cause we do not need it
        num_rating = movie.find('div', class_="sc-e2dbc1a3-0 ajrIH sc-b0691f29-2 bhhtyj cli-ratings-container").span.get_text(strip=True).split('(')[1].strip(')')
        
        # print(rank, name, year, rating, num_rating) # printing all 250 movies
        
        writer.writerow([rank, name, year, rating, num_rating]) # appending details of each movie after each iterations
        
    # print("Data saved to IMDB_Movie_Ratings.csv")
        
except Exception as e:
    print(e)
