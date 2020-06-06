# news documentation
Link to docs:
https://drive.google.com/open?id=1qVu5DfyyM_6Z0pZumnWEhNMLXVaeqsjP

Link to web page:
https://news-only.herokuapp.com/

### How to use news-only:

## Developers:
	1. Clone the project.
	2. In app.py:
	 	Commentout lines: 21, 22 and 29.
	 	Uncomment lines: 23 and 30.
	3. In external_apis.py:
	 	Commentout line: 5
	 	Uncomment line: 6 and use your API_KEY

	Note: visit **[NewsAPI](https://newsapi.org)** to get your API_KEY 

## Users:
After successful signup or login, users will see news headlines from the country that
users have chosen while signup.

### Search: 
	i. Generic search
		This will be available for users as long as users are logged in. So users could search 
		content anytime as this functionality is avialable in top navigation bar.
	ii. Time based search:
		This allows users to search specific news based on time. 
		It will let users to get articles as old as a month.

### Categories:
	In this page users have ability to explore news based on country and categories.

### Sources:
	It has 128 differnt news outlets where users could navigate directly into their webpages.
	Also this page lets users to add the news outlet into their feeds. 
	
### Feed:
	In this page users could create feed where they could add news outlets of their choices from 
	source page. This page also allows users to remove news outlets and feed itself if they do not like
	them. Moreover, it also has a link for each feed where users could see the news only from selected news
	outlets that they have selected from source page.
	
### Board:
	In this page users could create board where they could store articles if they are interested in future
	read. This page also shows the highlights of the articles that belong to corresponding boards. 
	Here users have ability to delete the board. Moreover, it has links to specific
	board where users could see the articles they have stored. 
	
	In specific board page users could check, uncheck and delete the articles.

Note: Each article has add button that allows users to add that article to the board
they have created.

## Improvements:
	1. Add buttons are visible eventhough users do not have feed/board. 
	2. Everytime when user add source in feed and article in board page refreshes.
	We could imporove this by using axios response back to update the portion of page without refreshing a whole page.
	3. All articles are showing in same layout. We could add features to let users to select different layouts.
	4. Add toggle button to switch dark and light mode.

  
