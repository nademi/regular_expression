# Regular Expressions
This file explain how to use the code to extract various date type information.

## Instructions
- Clone the repository
- Using a terminal navigate to the "code" subdirectory (regular-expressions/code as on github)
- No extra python libraries needed outside of standard library (re, sys, os, math, csv)
- From the terminal run the command ```python3 .\main.py <data path> <output path>```
- The train data path should be a relative path to a directory containing the text files you will implement regular expressions
- The output path is where the csv files will be created after implementing regular expression

## example
```bash
python main.py ./data/dev/ ./output/ 

```

## Data

The data can be found inside [data/dev](data/dev).



## Introduction
In this project, we explored the use of regular expressions to extract information from written text. This method has been widely applied in information retrieval, and it is used in text processing applications and research.

A regular expression is a notation used to match strings in a text. It works like the CTRL+F search feature in browsers, but it has the added bonus of allowing the use of special characters to count, exclude, and group specific strings. Like in a language, regular expressions have a set of characters with predefined functions, and these characters can be used to create search patterns. For example, the character + means one or more occurrences. The regular expression /e+/ searches for strings of one or more “e”s. In the string “Feed the Birds”, this regular expression would match “ee”.
## Task
In this project we are going to use regular expressions to search for date expressions in news texts. We are interested in two types of date expressions. The first one is simple date expressions, strings like “14 June 2019” and “Fall 2020” which represent absolute points in time and are independent of when you are reading them. The second type is deictic date expressions, dates that are relative to the current time, for example, “the day before yesterday”, “next Friday”, and “two weeks prior”.
## Input: news articles
News is a genre that makes use of dates to convey more information about when an event took place and to help the readers place future and past occurrences in time. The input dataset is a collection of news articles that discusses several topics, such as politics, tech, and business. 

Article 265 in this dataset has sentences like this:

“Pipa conducted the poll from 15 November 2004 to 3 January 2005 across 22 countries in face-to-face or telephone interviews.”
## Output: CSV file, code, and documentation
## CSV file
As mentioned before, news articles usually have a lot of time references, and we want you to search for those references in the input data. The output of the search is a CSV file with all of the dates expressions found. The file contains four columns, one column for the id of the article, one for the type of date expression found, one for the date expression itself, and one for the offset in characters from the beginning of the file to the beginning of the date expression, that is the position of the first character of the date expression in the file.

- The output is like:
- article_id, expr_type, value, char_offset
- 265.txt, date, 15 November 2004, 30
- 265.txt, date, 3 January 2005, 50



# More information
- Book Chapter: [Chapter 2](https://web.stanford.edu/~jurafsky/slp3/2.pdf)

- Learning Objectives : Learn how to use regular expressions to extract information from text.


This is a solution to Assignment 1 for CMPUT 501 - Intro to NLP at the University of Alberta, created during the Fall 2021 semester.
