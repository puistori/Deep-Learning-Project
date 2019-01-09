import gzip,pickle,csv

# the clean data thing has 633897
# compare 805903


neep = pickle.load(open("imdb","rb"))











def sort_em_and_do_em(dictionary):
    my_list = []

    for key in neep:
        for index in range(len(my_list)+1):

            if index == len(my_list):
                my_list.append(key)

            elif dictionary[key][1] <= dictionary[my_list[index]][1]:
                print("Passing on, kuz %s is less then or ekwil to %s"%(dictionary[key][1],dictionary[my_list[index]][1]))
                pass
            else:

                temp = my_list[:index]
                temp.append(key)
                temp = temp + my_list[index:]
                my_list = temp
        if len(my_list) > 10:
            return(my_list)
    return(my_list)

jem = sort_em_and_do_em(neep)

for num in range(21):
    print("%s with %s"%(jem[num],neep[jem[num]]))





"""
tsvin_ratings = gzip.open("title.ratings.tsv.gz",'rt',encoding='utf-8')
#tsvin_basics = str(tsvin_basics)
tsvin_ratings = csv.reader(tsvin_ratings,delimiter='\t')

tsvin_basics = gzip.open("title.basics.tsv.gz",'rt',encoding='utf-8')
#tsvin_basics = str(tsvin_basics)
tsvin_basics = csv.reader(tsvin_basics,delimiter='\t')
"""
### this was to create a dictionary mapping names to upvotes.
"""
codename_upvotes = {}
for element in tsvin_ratings:
    codename_upvotes[element[0]] = element[2]

codename_name = {}
for element in tsvin_basics:
    codename_name[element[0]] = element[2]


final_dict = {}

for codename in codename_name:
    if codename in codename_upvotes:
        final_dict[codename_name[codename]] = codename_upvotes[codename]

pickle_out = open("names to upvotes","wb")
pickle.dump(final_dict,pickle_out)
pickle_out.close()
"""





"""
purge_me = pickle.load(open("ibmd_data","rb"))

adult_movie_list = []
normal_movies = []
tsvin_basics = gzip.open("title.basics.tsv.gz",'rt',encoding='utf-8')
#tsvin_basics = str(tsvin_basics)
tsvin_basics = csv.reader(tsvin_basics,delimiter='\t')

ibmd_data = pickle.load(open("ibmd_data","rb"))

not_adult = None
for element in tsvin_basics:
    if element[0] == "tt0091587":
        #print("gotit!")
        not_adult =  element[4]
        break

for element in tsvin_basics:
    #print(element)
    if element[4] != not_adult:
        #print("we've gotta kreeper! %s"%element[2])
        adult_movie_list.append(element[2])

    else:
        normal_movies.append(element[2])




new_ibmd_data = {}

for movie in normal_movies:
    if movie in ibmd_data:
        new_ibmd_data[movie] = ibmd_data[movie]
    else:
        print("this one didn't make it :( %s"%movie)


pickle_out = open("ibmd_data_clean","wb")
pickle.dump(new_ibmd_data,pickle_out)
pickle_out.close()


"""


"""
print("kreepers!")
print(len(adult_movie_list))

for adult_movie in adult_movie_list:
    if adult_movie in ibmd_data:
        print("yuck! this one got through: %s"%(adult_movie))
print("normals!")
print(normal_movies)
for normal_movie in normal_movies:
    if normal_movie in ibmd_data:
        #print("ya good! this movie is fine and went through %s"%(normal_movie))
        pass
"""


### ok this is me just making the actual imdb data set
"""
tsvin1 = gzip.open("title.ratings.tsv.gz",'rt',encoding='utf-8')
#print(tsvin1)
#tsvin1 = str(tsvin1)
tsvin2 = csv.reader(tsvin1,delimiter='\t')
#print(tsvin2)
print("a here a we a go again")
print("here we don't go")
count = 0



id_to_name_dict = {}
id_to_year_dict = {}
id_to_genre_dict = {}
id_to_is_adult_dict = {}
tsvin_basics = gzip.open("title.basics.tsv.gz",'rt',encoding='utf-8')
#tsvin_basics = str(tsvin_basics)
tsvin_basics = csv.reader(tsvin_basics,delimiter='\t')

not_adult = None
for element in tsvin_basics:
    if element[0] == "tt0091587":
        #print("gotit!")
        not_adult =  element[4]
        break


for element in tsvin_basics:

    if element[4] == not_adult and element[1] == 'movie':
        id_to_name_dict[element[0]] = element[2]
        id_to_year_dict[element[0]] = element[5]
        id_to_genre_dict[element[0]] = element[1]
        id_to_is_adult_dict[element[0]] = element[4]

final_dict = {}

for element in tsvin2:
    if element[0] in id_to_name_dict:
        name = id_to_name_dict[element[0]]
        entry = [element[1],element[2],id_to_year_dict[element[0]],id_to_genre_dict[element[0]],id_to_is_adult_dict[element[0]]]
        final_dict[name] = tuple(entry)
        count+=1

print("final dict!")
for line in final_dict:
    print("%s : %s"%(line,final_dict[line]))


pickle_out = open("imdb","wb")
pickle.dump(final_dict,pickle_out)
pickle_out.close()
"""
"""
count = 0
movie_dict = {}
ibmd_data = pickle.load(open("ibmd_data","rb"))
for element in ibmd_data:
    if ibmd_data[element][3] == 'movie':
        movie_dict[element] = ibmd_data[element]




pickle_out = open("ibmd_data_movies","wb")
pickle.dump(movie_dict,pickle_out)
pickle_out.close()
"""

"""
import urllib.request
import bs4
import re

def is_it_average_rating(string):
    if "Average Rating:" in string:
        return True
    else:
        return False

def is_it_fresh(string):
    if "Fresh" in string:
        return True
    else:
        return False
def is_it_rotten(string):
    if "Rotten" in string:
        return True
    else:
        return False

source = urllib.request.urlopen('https://www.rottentomatoes.com/m/fantastic_beasts_the_crimes_of_grindelwald').read()

soup = bs4.BeautifulSoup(source,'lxml')

# body
step = soup.find("div",class_="body_main container")

# body 2
step = step.find("div",id="main_container",class_="container")
# scorepanel
step = step.find("div", id="scorePanel")

## divergence 1: scorestats
scorestats = step.find("div",id="scoreStats")
scorestats = scorestats.find_all("span")
average_rating = None
Fresh = None
Rotten = None
for span in scorestats:
    if is_it_average_rating(span.text):
        average_rating = span
        #average_rating = average_rating[0]
        average_rating = average_rating.parent
        average_rating = average_rating.text
    elif is_it_fresh(span.text):
        Fresh = span
        #Fresh = Fresh[0]
        Fresh = Fresh.parent
        Fresh = Fresh.text

    elif is_it_rotten(span.text):
        Rotten = span
        #Rotten = Rotten[0]
        Rotten = Rotten.parent
        Rotten = Rotten.text
print(average_rating,Fresh,Rotten)
# divergence 2: user ratings
def audience_panel(string):
    if string== None:
        return False
    elif "audience-panel" in string:
        return True
    else:
        return False
def meter_value(string):
    if string== None:
        return False
    elif "meter-value" in string:
        return True
    else:
        return False
def audience_info(string):
    if string== None:
        return False
    elif "audience-info" in string:
        return True
    else:
        return False
audience = step.find(class_=audience_panel)


meterValue = audience.find(class_=meter_value)
meterValue = meterValue.text
audienceInfo = audience.find(class_=audience_info)
audienceInfo_list = audienceInfo.findAll("div")

audience_avg = audienceInfo_list[0].text
user_ratings = audienceInfo_list[1].text
print("round 2")
print(meterValue,audience_avg,user_ratings)











#https://blog.michalszalkowski.com/python/python-3-utf-8-codec-cant-decode-byte-0x8b-in-position-1-invalid-start-byte/
"""





















# https://wiki.python.org/moin/How%20to%20I%20use%20gzip%20module%20with%20pickle%3F