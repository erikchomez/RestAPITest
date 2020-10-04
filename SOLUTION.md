# Simple API solutions
In order to run this application, simply create a virtual environment and pip install flask.
No other libraries besides the built-ins os, csv, and json were used. You can run app.py and you will be able to use
localhost:8088. However, if you run api_functions.py, you can see how each endpoint is implemented as well as change 
requests directly. 

Place the entire zip contents in the same folder or grab the files from the following link: 
https://github.com/erikchomez/RestAPITest


Having never designed an API, let alone a REST API, this assignment turned out to be a fun challenge.
My program runs on Python and utilizes Flask as a support. 

The design of the program is very simple. The index page displays all possible endpoints available and very brief 
instructions on how to format each query parameter if needed. When an endpoint is called, the appropriate checking
is done to ensure the query parameters were formatted correctly. If there is an error, it will be displayed on the
index page.

The main function in api_functions.py has examples of each endpoint being used. 

For endpoint 2, I was not able to figure out how to process the request through the URL, so I simply hardcoded the
solution. This can be found in the main function, however, changing search_request will still work. 


### Endpoint 0: All
This simply produces all the products.

### Endpoint 1: Autocomplete
Inside a for loop, we check the request type and then check if the prefix provided exists in either brand name,
title, or category name. If the prefix does exist in the type, then we add it to a set. We use a set to keep track
any matches because we do not want to repeat things. At the end, we convert the set to a list to match the response
example given.

Since we loop through the entire data, time complexity will be O(n) and space complexity will be O(n).


### Endpoint 2: Search
This endpoint was the hardest for me to implement, and I did not figure out how to accommodate the request. However,
the program has been hardcoded to accept a request in the format provided in the instructions. This is to demonstrate
that the program does work.

 
Inside a for loop we iterate through the data, and we initialize a boolean variable to True. We then loop through 
the conditions and if any condition is not met, the boolean variable is set to False. Once we are done looping through
the conditions, we check if the boolean variable is still True, if it is, we append it to a list. We then check if the 
length of the list meets the pagination size specified.

Since we have a nested for loop, time complexity is O(n<sup>2</sup>) and space complexity is O(n).

### Endpoint 3: Keywords
We first iterate through the values of keywords, inside we create a new dictionary with the key being the current value,
and the value being 0. We then iterate through the data and if the current value appears in the title, we increment
the dictionary value. We do this for every keyword value, and create a list that holds a dictionary with each value and 
count.

Since we have a nested for loop, time complexity is O(n<sup>3</sup>) and space complexity is O(n).


### Endpoint 4: Most frequent
In a nested for loop, we create a dictionary containing every keyword that exists in all of the data. We also check for
small words such as 'for', 'with', or 'and', and we omit these keywords. We also do not include any keyword of size 1, for
example 'a' or '-'.

In another for loop, we sort this new dictionary so we can access the top 10 most frequently occurring keywords.

Since we have a nested for loop, time complexity is O(n<sup>3</sup>) and space complexity is O(n).