### SI 506 - FINAL PROJECT ###

import requests
import requests.auth
import json
import pickle
import unittest
from pprint import pprint
from ast import literal_eval


## Setting up data request and/or caching ##

cache_fname = "final_cache.txt"
try:
    fobj = open(cache_fname, 'rb')
    saved_cache = pickle.load(fobj)
    fobj.close()
except:
    print "There is no existing cache file. The program will create one now."
    saved_cache = {}

def requestURL(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = params)
    prepped = req.prepare()
    return prepped.url

def get_with_caching(base_url, params_diction, cache_diction, cache_fname):
    full_url = requestURL(base_url, params_diction)
    if full_url in cache_diction:
    	# print "from cache, retrieving data from the API associated with " + full_url
    	return cache_diction[full_url]
    else:
    	try:
    		response = requests.get(base_url, params_diction)
    		# print "adding saved data to cache file for " + full_url
    		cache_diction[full_url] = response.text
    		fobj = open(cache_fname, "wb")
    		pickle.dump(cache_diction, fobj)
    		fobj.close()
    		data = response.text
    	except:
    		print "Error. Unable to retrieve data from the API."
    		data = {}
    	return data

def get_with_caching2(base_url, params_diction, headers, cache_diction, cache_fname):
    full_url = requestURL(base_url, params_diction)
    if full_url in cache_diction:
    	# print "retrieving data from the API associated with " + full_url
    	return cache_diction[full_url]
    else:
    	try:
    		response = requests.get(base_url, params=params_diction, headers=headers)
    		# print "adding saved data to cache file for " + full_url
    		cache_diction[full_url] = response.text
    		fobj = open(cache_fname, "wb")
    		pickle.dump(cache_diction, fobj)
    		fobj.close()
    		data = response.text
    	except:
    		print "Error. Unable to retrieve data from the API."
    		data = {}
    	return data


## Reddit API information ##

CLIENT_ID = "zzezd9HW-lfYjA"
CLIENT_SECRET = "ZUKEvGunXEnvLba-4VD8EM6XPC0"
REDIRECT_URI = "https://www.si.umich.edu/programs/courses/506"

# Get user authorization #

"""
baseurl_r = "https://www.reddit.com/api/v1/authorize?"
params_r = {'client_id': CLIENT_ID, 'response_type':'code', 'state':'kombuchaya', 
          'redirect_uri':REDIRECT_URI, 'duration':'permanent', 'scope':['read']}
reddit_response = requests.get(baseurl_r, params_r, headers={'User-Agent':'etemeete/0.1'})
pprint(reddit_response.url) #prints url that user must follow to authorize app access to reddit account
"""

# Get access token #

"""
client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
post_data = {"grant_type": "authorization_code",
           "code": "oH_uLp5iwU2veNLA-gjjATD9U3k", #found in url from above step. can only be used one time!
           "redirect_uri": REDIRECT_URI}
headers = {"User-Agent": 'etemeete/0.1'}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
print response.json()   #get access_token and refresh_token
"""

access_token = "1jYydkoWqFVq4e7UDhnedL2C3Ls"
refresh_token = "59692324-MbgHLqgizoppcLqw42hG1NQo6zw"  

"""
The access_token expires after 1hr. However with the refresh_token I can permanently 
refresh the access_token w/o getting a new authorization from the user. Thus the 
<Get user authorization> and <Get access token> blocks need never be run again.
"""

# Refreshing the access token #

"""
(1) if you get an error when running the <Using the access token code> block, uncomment the 
    code below and run it 
(2) replace the string in the variable access_token with the new access token.
(3) comment out the lines below once more, and rerun the desired code block
"""

"""
client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
post_data = {"grant_type": "refresh_token",
           "refresh_token": refresh_token} 
headers = {"User-Agent": 'etemeete/0.1'}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
print response.json()
"""


###########################################################################################
print "\n", "Welcome to etemeete, your safe makeup resource! \n"
print "In this app you can find information on safe makeup brands such as their safety score and popularity. You can also find the name, rating, and price of their products. And compare products by type across different brands.  \n"
print "It's beauty. Made safe. \n\n\n"

"""
Section 1: Check the Safety of a Brand 
"""

class brandCheck():
    brand = ""
    unsafe = ""
    def __init__(self, safe_brands, brand_tags, brand_score, brand):
        if brand in safe_brands:
            self.brand = brand
            self.tags = [str(tag) for tag in brand_tags[brand]]
            lst = [i[1] for i in brand_score if i[0] == self.brand]
            self.ss = lst[0]
        else:
            self.unsafe = brand

    def safe_check(self):
        if self.unsafe != "":
            return "Our research indicates that {} is not a safe brand.".format(self.unsafe)
        else:
            return "Our research indicates that {} is a safe brand!".format(self.brand)

    def safe_score(self):
        if self.unsafe != "":
            return self.safe_check()
        else:
            return "The safety score for {} is {}.".format(self.brand, self.ss)

    def __str__(self):
        if self.brand != "":
            return ("{} offers the following product types: {}.\n"
                    "{}% of the products sold by {} are safe. \n".format(self.brand, self.tags, self.ss, self.brand)
                    )
        else:
            return self.safe_check()


# Step (1): Get count of products for brands offering safe products.
baseurl_m = 'http://makeup-api.herokuapp.com/api/v1/products.json'

params_s1 = {'product_tags':'Natural'}
params_s2 = {'product_tags':'Non-GMO'}
params_s3 = {'product_tags':'Vegan'} 
params_s4 = {'product_tags':'Organic'}
safe_data1 = json.loads(get_with_caching(baseurl_m, params_s1, saved_cache, cache_fname))
safe_data2 = json.loads(get_with_caching(baseurl_m, params_s2, saved_cache, cache_fname))
safe_data3 = json.loads(get_with_caching(baseurl_m, params_s3, saved_cache, cache_fname))
safe_data4 = json.loads(get_with_caching(baseurl_m, params_s4, saved_cache, cache_fname))

for i in safe_data2:            
    if i not in safe_data1:
        safe_data1.append(i)     
for i in safe_data3:
    if i not in safe_data1:
        safe_data1.append(i)
for i in safe_data4:
    if i not in safe_data1:
        safe_data1.append(i)

"""
Some of the brands were None, but by reading the product name I was able to manually fill 
in the brand name. 
"""
def noneFix(safe_dict):
    safe_dict2 = [i for i in safe_dict if i['brand'] != None]
    names = ['earth lab', 'physicians formula', 'earth lab', 'earth lab', 'dalish', 'dalish', 'saint', 'saint']
    nones = []
    for i in safe_dict:
        if i['brand'] == None:
            nones.append(i)
    for j in range(8):
        nones[j]['brand'] = names[j]
    safe_dict2 += nones
    return safe_dict2

safe_data = noneFix(safe_data1)

def getCounts(safe_dict):
    safe_count = {}
    brand_tags = {}
    for i in safe_dict:
        if i['brand'] not in safe_count:
            safe_count[i['brand']] = 0
            brand_tags[i['brand']] = [t for t in i['tag_list']]
        safe_count[i['brand']] += 1
        for j in i['tag_list']:
            if j not in brand_tags[i['brand']]:
                brand_tags[i['brand']].append(j)
    return safe_count, brand_tags

safe_count = getCounts(safe_data)[0]
brand_tags = getCounts(safe_data)[1]

# Step (2): Get total count of products sold by the safest companies 

"""
Since there appears to be an issue with the brand parameter, I will get the counts 
manually by searching for the various keywords within each dictionary['name'] in the 
list of all products returned by queriying by product_type instead of by brand 
"""

product_type = ['blush', 'bronzer', 'eyebrow', 'eyeliner', 'eyeshadow', 'foundation', 'lip liner', 'lipstick', 'mascara', 'nail polish']

total_data = []
for i in product_type:
    params_t = {'product_type':i}
    total_data += json.loads(get_with_caching(baseurl_m, params_t, saved_cache, cache_fname))

total_count = {}
for i in total_data:
    for brand in safe_count:
        if brand in i['name'].lower() or brand in i['description'].lower():
            if brand not in total_count:
                total_count[brand] = 0
            total_count[brand] += 1


# Step (3): Get the percentage of products sold per brand that are safe 

brand_score = []
for i in safe_count:
    brand_score += [(i, round(safe_count[i]/float(total_count[i])*100, 1))]
brand_score = sorted(brand_score, key=lambda x:x[1], reverse = True)


"""
Section 2: Get Information on Brand Products
"""

class brandProducts():
    def __init__(self, total_data, brand, product_type):
        self.brand = brand
        self.prod_type = product_type
        self.total_data = total_data
        self.product_data = [i for i in self.total_data if i['brand'] == self.brand if i['product_type'] == self.prod_type]
        
    def product_info(self):
        products = ""
        ratings = []
        for i in self.product_data:
            self.name = str(i['name'])
            self.price = str(i['price'])
            self.rating = i['rating']
            ratings.append(self.rating)
            products += "{}, price: ${}, rating: {}.\n".format(self.name, float(self.price), self.rating)
        return products, ratings
            
    def similar_prod(self):
        self.similar = [j for j in self.total_data if j['brand'] != self.brand if j['product_type'] == self.prod_type] 
        self.similar = [str(j['name']) for j in self.similar if j['rating'] in self.product_info()[1]]
        if len(self.similar) == 0:
            return "There are currently no similar products on the market.\n"
        else:
            return "Some similar products on the market: ", self.similar


"""
Section 3: Get Brand Popularity
"""

# Step (1): Get a list of makeup-related subreddits sorted by activity

headers = {'Authorization': "bearer " +access_token, "User-Agent": "etemeete/0.1"}

baseurl_r2 = "https://oauth.reddit.com/subreddits/search"  
params_r2 = {'q':'makeup', 'sort':'activity', 'limit':100}  

makeup_reddits= json.loads(get_with_caching2(baseurl_r2, params_r2, headers, saved_cache, cache_fname))
makeup_subs = makeup_reddits['data']['children']
go = True
while go:
    params_r2['after'] = makeup_reddits['data']['after']
    makeup_reddits = json.loads(get_with_caching2(baseurl_r2, params_r2, headers, saved_cache, cache_fname))
    makeup_subs += makeup_reddits['data']['children']
    if makeup_reddits['data']['after'] == None:
        go = False


# Step (2): Store the top 11 active subreddits

"""
I examined the description of the first 50 returned subreddits in makeup_subs. Based on their
descriptions I selected the following 11 to put store as the top makeup subreddits.
"""
actives = ["MakeupAddiction", "PanPorn", "Makeup", "MakeupAddictionCanada", "MakeupAddicts", "sugarfreemua", "brownbeauty", "Makeup101", "newbieMUA", "MakeupEducation", "drugstoreMUA"]

makeup_top = [sub for sub in makeup_subs if sub['data']['display_name'] in actives]


# Step (3): Search each active subreddit by safe brand name

def postNumber(brand, lst):
    post_dict = {}
    params_r3 = {'q':brand, 'sort':'relevance', 'restrict_sr':'on', 't':'year', 'limit':100}  
    for sub in lst:
        baseurl_r3 = "https://oauth.reddit.com/r/{}/search".format(sub) 
        posts = json.loads(get_with_caching2(baseurl_r3, params_r3, headers, saved_cache, cache_fname))
        all_posts = posts['data']['children']
        if posts['data']['after'] != None:
            go = True
            while go:
                params_r3['after'] = posts['data']['after']
                posts = json.loads(get_with_caching2(baseurl_r3, params_r3, headers, saved_cache, cache_fname))
                all_posts += posts['data']['children']
                if posts['data']['after'] == None:
                    go = False
        if brand not in post_dict:
            post_dict[brand] = 0
        post_dict[brand] += len(all_posts)
    return post_dict[brand]


class brandPopularity():
    def __init__(self, brand, actives):
        self.brand = brand
        self.a = [(i, postNumber(i, actives)) for i in safe_count if i != 'pure anada'] + [('pure anada',0)]
     
    def popularity(self):
        self.p = postNumber(self.brand, actives)
        self.tot = sum([x[1] for x in self.a])
        self.pop = round(self.p/float(self.tot)*100, 1)
        return "{}% of makeup posts are about {}.".format(self.pop, self.brand)
    
    def rank(self):
        for i in range(len(self.a)):
            if self.a[i][0] == self.brand:
                return "Of all safe makeup brands, {} is ranked at {}.".format(self.brand, i)
   

"""
Section 4: Using the Code
"""

## Part 1 ##

print "The following tutorial will show you how to interact with the app.\n"
print "Suppose you'd like to check if your favorite makeup brand is also a safe one: "
brandA = brandCheck(safe_count, brand_tags, brand_score, 'maybelline')
print brandA.safe_check()

print "\nLet's check another brand: "
brandB = brandCheck(safe_count, brand_tags, brand_score, 'e.l.f.')
print brandB.safe_check()
print brandB.safe_score()
print brandB

## Part 2 ##

print "Now that we've found a safe brand, let's get information on it's products.\n"
print "Let's say you're interested in purchasing mascara from e.l.f. \n"
elf_mascara = brandProducts(total_data, 'e.l.f.', 'mascara')
print "We can get information on the different mascara products that e.l.f. sells: "
print elf_mascara.product_info()[0]
print "As well information on similar products offered by other safe brand competitors: "
print elf_mascara.similar_prod()

## Part 3 ##

print ("\nIf you have any concerns about the performance of the brand given that it uses less "
        "durable ingredients, you can check the popularity of the brand within online makeup "
        "communities. For example: ")

elf_popularity = brandPopularity('e.l.f.', actives)
print elf_popularity.popularity()
print elf_popularity.rank()

## Part 4 ##

print "\nThat concludes the tutorial."
print "We hope etemeete can make it easy to choose safe beauty!"

print "\n\n\n"

##### TESTS BELOW, DO NOT CHANGE #########
class Sec1a(unittest.TestCase):
    def testA(self):
        self.assertEqual(len(safe_data), len(safe_data1), "Checking that all dictionaries in the list are retained by the function")
    
    def testB(self):
        self.assertEqual(len([i for i in safe_data if i['brand'] == 'earth lab']), 3, "All three earth lab brands are added by this function")

    def testC(self):
        self.assertEqual([i for i in safe_data if i['brand'] == None], [], "All none brands have been removed, so this should be an empty list")

class Sec1b(unittest.TestCase):
    def testA(self):
        self.assertEqual(safe_count['e.l.f.'], 21, "e.l.f. appears three times")

    def testB(self):
        self.assertEqual(type(brand_tags), type({}), "should be a dictionary with lists as values")
        self.assertEqual(brand_tags['milani'], ['Vegan'], 'milani sells vegan products')

    def testC(self):
        self.assertEqual([x[1] for x in brand_score if x[0] == 'mineral fusion'], [87.5], "87.5% of mineral fusion products are safe")

class Class1(unittest.TestCase):
    def testA(self):
        self.assertEqual(brandCheck(safe_count, brand_tags, brand_score, "maybelline").safe_check(), "Our research indicates that maybelline is not a safe brand.", "maybelline is not a safe brand, when this method is called it should tell the user that")
    
    def testB(self):
        self.assertEqual(brandCheck(safe_count, brand_tags, brand_score, "pure anada").ss, 100.0, "pure anada is a safe brand, when this method is called it should show the safety score of 100")
    
class Class2(unittest.TestCase):
    def testA(self):
        self.assertEqual(len(brandProducts(total_data, "e.l.f.", "mascara").similar_prod()[1]), 16, "Number of non-e.l.f. mascara products with ratings of 4.0, 4.3, or 4.8")

class Sec3(unittest.TestCase):
    def testA(self):
        test_post = postNumber('e.l.f.', actives)
        self.assertEqual(test_post, 175, 'The total number of posts this year about e.l.f.')

class Class3(unittest.TestCase):
    def testA(self):
        t = brandPopularity('e.l.f.', actives)
        self.assertEqual(t.rank(), 'Of all safe makeup brands, e.l.f. is ranked at 1.', 'this string should be returned by the function')
        self.assertEqual(t.popularity(), "24.8% of makeup posts are about e.l.f..", 'this string should be returned by the function')

unittest.main(verbosity=2)