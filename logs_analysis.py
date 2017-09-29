#!/usr/bin/env python2.7.13  # shebang line for the used Python version

# Python code for database queries and display of the answers.
# Pls also refer to the README-logs_analysis.md file for further explanations.


import psycopg2  # importing postgresql as databese

DBNAME = "news"  # definition of the variable for the database

# procedure to get the most popular articles with a select clause
# using a join and a substring function.


def get_popular_articles():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("""select articles.title, count(articles.title) as views
                        from log, articles
                        where SUBSTRING(log.path, 10) = articles.slug
                        group by articles.title
                        order by views desc
                        limit 3""")
    return cursor.fetchall()
    db.close()


# procedure to get the most popular authors with a select clause
# using a join and a view top_articles


def get_popular_authors():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("""select authors.name, top_articles.views
                        from authors, top_articles
                        where authors.id = top_articles.author""")
    return cursor.fetchall()
    db.close()


# procedure to get the days with > 1% errors with a select clause
# using a join and a divide function
# and the views errors_per_day, views_per_day.


def get_errors():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("""select errors_per_day.date,
                      round(100.0 * errors_per_day.errors::decimal
                      /views_per_day.views, 1) as percent
                        from errors_per_day, views_per_day
                        where errors_per_day.date = views_per_day.date
                        AND round(100.0 * errors_per_day.errors::decimal
                        /views_per_day.views, 1) > 1""")
    return cursor.fetchall()
    db.close()


# procedure to display the answers to the first question.


def display_answer_1():
    # variable to store the database query, stored in a list
    answers_1 = get_popular_articles()
    print "\n", \
          "Q1: What are the most popular three articles of all time?", \
          "\n"
    # while loop to display the answers in different lines
    i = 0
    while i < len(answers_1):
        print "    -  " + answers_1[i][0], \
              " -- " + str(answers_1[i][1]), \
              " views" + "\n"
        i += 1
    return "\n"


# procedure to display the answers to the second question.


def display_answer_2():
    # variable to store the database query, stored in a list
    answers_2 = get_popular_authors()
    print "\n", \
          "Q2: Who are the most popular article authors of all time? ", \
          "\n"
    # while loop to display the answers in different lines
    i = 0
    while i < len(answers_2):
        print "    -  " + answers_2[i][0], \
              " -- " + str(answers_2[i][1]), \
              " views" + "\n"
        i += 1
    return "\n"


# procedure to display the answers to the third question.


def display_answer_3():
    # variable to store the database query, stored in a list
    answers_3 = get_errors()
    print "\n", \
          "Q3: On which days did more than 1% of requests lead to errors?", \
          "\n"
    # while loop to display the answers in different lines
    i = 0
    while i < len(answers_3):
        print "    -  " + answers_3[i][0], \
              " -- " + str(answers_3[i][1]), \
              " %" + "\n"
        i += 1
    return "\n"


# gotta print out the answers!


print display_answer_1()
print display_answer_2()
print display_answer_3()
