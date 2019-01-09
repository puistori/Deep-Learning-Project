import os
import re
import random
import pickle
import string

def generate_comment_dict():
    file_dict = {}
    for file in os.listdir('movie_data'):
        the_file = open("movie_data/%s"%file,'rt')
        comments = []
        for comment in the_file:
            processed_comment = re.sub("\n", "", comment)
            comments.append(processed_comment)
        file_dict[file] = comments
    return (file_dict)



def make_batches(comments,amount_of_batches,batch_size,as_many_as_you_can=False):
    # makes batches out of a given list of comments.
    movie_batches = []
    comments_left = comments

    if as_many_as_you_can:
        while len(comments_left)>batch_size:
            new_batch,comments_left = make_batch(batch_size,comments_left)
            movie_batches.append(new_batch)
        return(movie_batches)
    else:
        for number in range (amount_of_batches):
            # Maybe do a "while comments left < batch size?
            if len(comments_left) < batch_size:
                #maybe do a zero padded or just stop.
                break
            new_batch,comments_left = make_batch(batch_size,comments_left)
            movie_batches.append(new_batch)
        return (movie_batches)

def make_batch(batch_size,comments_left):
    # makes a single batch out of the list of
    # First, we need to generate the indexes of the things we want to take.
    indexes = []
    for number in range(batch_size):
        keep_going = True
        while keep_going:
            rand_number = random.randint(0,len(comments_left)-1)
            if rand_number not in indexes:
                indexes.append(rand_number)
                keep_going = False

    # Now, we will make our batch which is one large sting,
    added_comments = []
    for index in indexes:
        added_comments.append(comments_left[index])
    batch = ""
    for addable in added_comments:
        batch += addable
        batch += " "
    # and then we need to remove it from the comments so we don't reuse the same ones.
    comments_left = [a for a in comments_left if a not in added_comments]
    return(batch,comments_left)


def factorial(number):
    answer = 1
    for numberillo in range(number+1):
        if numberillo != 0:
            answer *= numberillo
    return (answer)
def permutations(n,k):
    top = factorial(n)
    bottom = factorial((n-k))
    answer = top/bottom
    return(answer)

def make_all_the_batches_and_answers(data,dict,amount_of_batches,batch_size,as_many_as_you_can=False):
    master_list = []
    answer_list = []
    for movie in dict:
        if re.sub(".txt","",movie) in data:
            comments = dict[movie]
            print("Yo're on this movie, %s"%(movie))
            movie_batches = make_batches(comments,amount_of_batches,batch_size,as_many_as_you_can)
            for batch in movie_batches:
                master_list.append(batch)
                answer_list.append(data[re.sub(".txt","",movie)][0])
        else:
            print("Sorry! The movie %s was not in the imdb data!!! "%(movie))

    return(master_list,answer_list)

def make_some_duplicates(data,dict,comment_min,comment_max,amount_of_batches,batch_size):
    master_list = []
    answer_list = []
    for movie in dict:
        if re.sub(".txt", "", movie) in data and (len(dict[movie]) < comment_max and len(dict[movie]) > comment_min):
            comments = dict[movie]
            print("Yo're on this movie, %s" % (movie))
            movie_batches = make_batches_even_redundant_ones(comments, amount_of_batches, batch_size)
            for batch in movie_batches:
                master_list.append(batch)
                answer_list.append(data[re.sub(".txt", "", movie)][0])
        else:
            print("Sorry! The movie %s was not in the imdb data!!! " % (movie))

    return (master_list, answer_list)

def make_batches_even_redundant_ones (comments,amount_of_batches,batch_size):
    # it does need to make at least a permutation.
    comments = comments
    new_batches = []
    operational_batch_amount = amount_of_batches
    if permutations(len(comments),batch_size) < amount_of_batches:
        operational_batch_amount = permutations(len(comments),batch_size)
    for number in range(operational_batch_amount):
        no_new_yet = True
        while no_new_yet:
            new_batch,z = make_batch(batch_size,comments)
            if new_batch not in new_batches:
                no_new_yet = False
                new_batches.append(new_batch)
    return (new_batches)

imbd_data = pickle.load(open("punctuated_imdb","rb"))

comment_dict = generate_comment_dict()
for movie in comment_dict:
    print(movie)
#batches,answers = make_all_the_batches_and_answers(imbd_data,comment_dict,100,10,True)
batches,answers = make_some_duplicates(imbd_data,comment_dict,15,100,50,10)
for index in range(len(batches)):
    print(batches[index])
    print(answers[index])

