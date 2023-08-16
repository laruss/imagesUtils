from enum import Enum

"""
WARNING: If you want to use formatting in the prompt, use item as instance of ProcessedItem
    e.g. item.title, item.description
    (check insta_post prompt as example)
"""


class Prompts(Enum):
    insta_post = '''
The following photo was described as: \"{item.description}\". 
Also it has the name of \"{item.title}\". 

Please distribute this photo among the following interest groups, estimating the likelihood of belonging to each one from 0 (does not fit at all) to 1 (fits perfectly): 

1. sports
2. art
3. music
4. cinema
5. literature
6. technologies
7. travel
8. fashion
9. foodAndDrink
10. natureAndAnimals
11. cars
12. videoGames
13. news
14. eroticism

Create 5 different descriptions of the photo on behalf of the user who would have posted this photo (as first-person view, don't use any names).

Return your answer as a VALID JSON object with two fields: 'parameters' (a dictionary where each key is an interest group and the value is a likelihood score) and 'descriptions' (a list of five descriptions).
The descriptions should be in different style and in different length, as they were written by different people, some of them may use slang, it could be also that some of them may use emojis as well. Some of them may use just several words or only emojis.
!If eroticism > 0.2, then descriptions should be made from the human being which displayed on photo!
Just return the JSON object, don't comment anything.
'''
