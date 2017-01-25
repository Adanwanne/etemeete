506 Final Project Readme Template

1. Describe your project in 1-4 sentences. Include the basic summary of what it does, and the output that it should generate/how one can use the output and/or what question the output answers.
—----
I plan on determining which companies have 1) the safest makeup products and 2) the most popular safe makeup products. I will also provide information on specific products offered by a brand, as well as similar products offered by their competitors. To do this I will gather output from the Makeup API about the makeup brands, products, prices, and ratings. From the the Reddit API I will get the popularity of a particular brand by calculating how many posts have been made about the brand in the past year in the top makeup subreddits.


2. Explain exactly what needs to be done to run your program (what file to run, anything the user needs to input, anything else) and what we should see once it is done running (should it have created a new text file or CSV? What should it basically look like?).
(Your program running should depend on cached data, but OK to write a program that would make more sense to run on live data and tell us to e.g. use a sample value in order to run it on cached data.)
EXAMPLE: First run python myproject.py Then, when it asks for a 3-letter airport code, type an airport abbreviation. You should type "DTW" to use the cached data. You should have a new file in your directory afterward called airport_info.csv which contains... <explain further> etc.
—----
To run the program, simply uncomment the portion towards the bottom under “Section 4: Using the Code”. It is meant to run as a tutorial to explain the app to the user. You can move step by step through the program by uncommenting the code one part at a time.


3. List all the files you are turning in, with a brief description of each one. (At minimum, there should be 1 Python file, 1 file containing cached data, and the README file, but if your project requires others, that is fine as well! Just make sure you have submitted them all.)
—----
I am submitting my Python file (etemeete.py), and cached file (final_cache.txt), and my README file.


4. Any Python packages/modules that must be installed in order to run your project (e.g. requests, or requests_oauthlib, or...):
—----
No. All the python modules needed have already been imported at the top.


5. What API sources did you use? Provide links here and any other description necessary.
—----
1) Makeup API: http://makeup-api.herokuapp.com/
-It requires no authentication or account registration
-None of the parameters appear to be required, but the options are: product_type, product_category, product_tags, brand, price_greater_than, price_less_than, rating_greater_than, rating_less_than
2) Reddit API: https://www.reddit.com/dev/api/
-It requires OAuth and a Reddit account (unless you do the Application Only OAuth)
-Depending on the GET being used there are different parameters required. I used:


6. Approximate line numbers in Python file to find the following mechanics requirements (this is so we can grade your code!): - Sorting with a key function: - Use of list comprehension OR map OR filter: - Class definition beginning 1: - Class definition beginning 2: - Creating instance of one class: - Creating instance of a second class: - Calling any method on any class instance (list all approx line numbers where this happens, or line numbers where there is a chunk of code in which a bunch of methods are invoked): - (If applicable) Beginnings of function definitions outside classes: - Beginning of code that handles data caching/using cached data: - Test cases:
—----
- Sorting with a key function: line 250
- Use of list comprehension OR map OR filter: line 139
- Class definition beginning 1: line 132
- Class definition beginning 2: line 257
- Creating instance of one class: line 365
- Creating instance of a second class: line 378
- Calling any method on any class instance (list all approx line numbers where this happens, or line numbers where there is a chunk of code in which a bunch of methods are invoked): line 365 to line 392
- (If applicable) Beginnings of function definitions outside classes: 
- Beginning of code that handles data caching/using cached data: line 12
- Test cases: line 402


7. Rationale for project: why did you do this project? Why did you find it interesting? Did it work out the way you expected?
—----
I’m interested in this product because it extends the Environmental Working Group (EWG) site, which gives information on the safety of beauty products, but no information on their popularity or performance. Shopping for beauty products often requires balancing practicality with safety concerns. I felt this project could help people make better decisions. However, I wasn’t able to get information on performance by product, because (1) there wasn’t enough information to that level, especially since many of the makeup brands were Canadian, and (2) Reddit didn’t allow enough search precision for me to just get posts on “e.l.f. Long Last Mascara”, for example.
