#!/usr/bin/env python

from rapnamelist import rapname
from namegen import full_name, last_name
import re
import random
import nltk
import inflect
import openai
from felonies import felonies
import os
import requests
from sengen import sentence
from cities import city_name
from mkovarticle import article_sentences
from nltk import pos_tag
from nltk.tokenize import word_tokenize
openapi_api_key = os.environ['OPENAI_API_KEY']

def randthing(x):
    return random.choice(x)

places = [
    "park",
    "restaurant",
    "movie theater",
    "museum",
    "shopping mall",
    "library",
    "coffee shop",
    "gym",
    "bar",
    "club",
    "playground",
    "zoo",
    "aquarium",
    "stadium",
    "concert hall",
    "art gallery",
    "bookstore",
    "beach",
    "marina",
    "bike trail",
    "hiking trail",
    "adult bookstore",
]

family_relationships = [
    "mother",
    "father",
    "sister",
    "brother",
    "grandmother",
    "grandfather",
    "aunt",
    "uncle",
    "cousin",
    "niece",
    "nephew",
    "daughter",
    "son",
    "wife",
    "husband",
    "partner",
    "stepmother",
    "stepfather",
    "stepsister",
    "stepbrother",
    "half-sister",
    "half-brother",
]

us_presidents_1800s = [
    "John Adams",
    "Thomas Jefferson",
    "James Madison",
    "James Monroe",
    "John Quincy Adams",
    "Andrew Jackson",
    "Martin Van Buren",
    "William Henry Harrison",
    "John Tyler",
    "James K. Polk",
    "Zachary Taylor",
    "Millard Fillmore",
    "Franklin Pierce",
    "James Buchanan",
]


ralph_items = [
    "farts",
    "dead mice",
    "toenail clippings",
    "Confederate currency",
    "hair",
    "dog turds",
    "rat feces",
    "frozen corndogs",
    "sporks",
    "goddamn bananas",
    "urine",
    "filth",
    "hobo teeth",
    "horse urine",
    "dicks",
    "anal beads",
    "moldy sausage",
    "pencil shavings",
    "pubes",
    "uranium",
    "radium",
]

old_barn_items = [
    "hay",
    "rusty tools",
    "tractor parts",
    "animal feed",
    "wood planks",
    "mason jars",
    "old furniture",
    "tattered blankets",
    "barbed wire",
    "wagon wheels",
    "broken glass",
    "horse saddles",
    "oil lamps",
    "grain sacks",
]

hospital_items = [
    "stethoscope",
    "syringe",
    "oxygen tank",
    "IV drip",
    "defibrillator",
    "wheelchair",
    "crutches",
    "bedpan",
    "urinal",
    "gurney",
    "patient gown",
    "scrubs",
    "surgical instruments",
    "CT scanner",
    "lab coats",
    "sterile gloves",
    "masks",
    "disinfectants",
    "antibiotics",
    "painkillers",
    "antidepressants",
    "sleep aids",
    "blood bags",
    "medical waste containers",
    "biohazard suits",
    "ventilator",
    "suction machine",
    "nebulizer",
    "hearing aid",
    "dental floss",
    "toothbrush",
    "hand sanitizer",
    "sanitary wipes",
]

medieval_weapons = [
    "Sword",
    "Longbow",
    "Crossbow",
    "Mace",
    "War hammer",
    "Lance",
    "Halberd",
    "Battle axe",
    "Flail",
    "Morning star",
    "Poleaxe",
    "Dagger",
    "Rapier",
    "Scimitar",
    "Falchion",
    "Greatsword",
    "Trident",
]

us_presidents_1800s = [
    "John Adams",
    "Thomas Jefferson",
    "James Madison",
    "James Monroe",
    "John Quincy Adams",
    "Andrew Jackson",
    "Martin Van Buren",
    "William Henry Harrison",
    "John Tyler",
    "James K. Polk",
    "Zachary Taylor",
    "Millard Fillmore",
    "Franklin Pierce",
    "James Buchanan",
]

emotions = [
    "happiness",
    "sadness",
    "anger",
    "fear",
    "disgust",
    "surprise",
    "joy",
    "love",
    "anxiety",
    "contentment",
    "frustration",
    "envy",
    "excitement",
    "grief",
    "guilt",
    "shame",
    "hope",
    "nostalgia",
    "relief",
    "pride",
    "compassion",
    "disappointment",
    "confusion",
    "curiosity",
]

cleaning_items = [
    "dish soap",
    "all-purpose cleaner",
    "glass cleaner",
    "baking soda",
    "vinegar",
    "lemon juice",
    "rubbing alcohol",
    "ammonia",
    "broom",
    "mop",
    "duster",
    "sponge",
    "paper towels",
    "dung",
    "diarrhea",
]

industrial_solvents = ['acetone', 'benzene', 'chloroform', 'dimethylformamide', 'ethyl acetate', 'hexane', 'isopropyl alcohol', 'methyl ethyl ketone', 'toluene', 'xylene']


folk_sayings = [
    "A penny saved is a penny earned.",
    "Actions speak louder than words.",
    "All's fair in love and war.",
    "An apple a day keeps the doctor away.",
    "Better late than never.",
    "Don't count your chickens before they hatch.",
    "Every cloud has a silver lining.",
    "Honesty is the best policy.",
    "If at first you don't succeed, try, try again.",
    "Laughter is the best medicine.",
    "Practice makes perfect.",
    "The early bird catches the worm.",
    "The grass is always greener on the other side.",
    "Time heals all wounds.",
    "When in Rome, do as the Romans do.",
    "You can lead a horse to water, but you can't make it drink.",
    "You reap what you sow.",
]


mythical_creatures = [
    "Dragon",
    "Unicorn",
    "Mermaid",
    "Griffin",
    "Minotaur",
    "Centaur",
    "Sphinx",
    "Phoenix",
    "Kraken",
    "Chimera",
    "Pegasus",
    "Yeti",
    "Siren",
    "Gorgon",
    "Hippogriff",
    "Werewolf",
    "Satyr",
]

warnerbros = [
    "Bugs Bunny",
    "Daffy Duck",
    "Tweety Bird",
    "Sylvester the Cat",
    "Road Runner",
    "Wile E. Coyote",
    "Porky Pig",
    "Elmer Fudd",
    "Yosemite Sam",
    "Foghorn Leghorn",
    "Marvin the Martian",
    "Pepe Le Pew",
    "Speedy Gonzales",
    "The Tasmanian Devil",
    "Michigan J. Frog",
    'Tom and Jerry',
    'Scooby-Doo',
    'Pikachu',
    'Bart Simpson',
    'SpongeBob SquarePants',
    'Hello Kitty',
]

mental_illnesses = [
    "Depression",
    "Anxiety",
    "Bipolar Disorder",
    "Schizophrenia",
    "Bulimia",
    "Anorexia",
    "Substance Use Disorder",
    "Dissociative Identity Disorder",
    "Panic Disorder",
    "Generalized Anxiety Disorder",
    "Social Anxiety Disorder",
    "Seasonal Affective Disorder",
]


extinct = [
    "Dodo",
    "Great Auk",
    "Tasmanian Tiger",
    "Mammoth",
    "Sabre-toothed Cat",
    "Woolly Rhino",
    "Steller's Sea Cow",
    "Passenger Pigeon",
    "Quagga",
    "Irish Elk",
    "Haast's Eagle",
    "Thylacine",
    "Glyptodon",
    "Japanese Sea Lion",
    "Caribbean Monk Seal",
    "Pyrenean Ibex",
    "Baiji Dolphin",
    "Golden Toad",
    "Western Black Rhinoceros",
    "Formosan Clouded Leopard",
    "Javan Tiger",
    "Giant Tortoise",
    "Eastern Cougar",
    "Cape Lion",
    "Caspian Tiger",
    "Dusky Seaside Sparrow",
    "Toolache Wallaby",
    "Tecopa Pupfish",
    "Catarina Pupfish",
    "Zanzibar Leopard",
    "Bubal Hartebeest",
    "Mexican Grizzly Bear",
    "Honshu Wolf",
    "Saudi Gazelle",
    "Cape Verde Giant Skink",
    "Cape Verde Giant Gecko",
    "Guam Flying Fox",
    "Santa Cruz Pupfish",
    "Guadalupe Caracara",
    "Tahitian Sandpiper",
    "Desert Rat-kangaroo",
    "Tasmanian Bettong",
    "Heath Hen",
    "Ascension Island Rail",
    "Ascension Island Thrush",
    "Guam Flying Fox",
]


extinct_animals = [
    "Tasmanian Tiger",
    "Dodo",
    "Great Auk",
    "Passenger Pigeon",
    "Quagga",
    "Pyrenean Ibex",
    "Caribbean Monk Seal",
    "Japanese Sea Lion",
    "Baiji Dolphin",
    "Western Black Rhinoceros",
    "Thylacine",
    "Steller’s Sea Cow",
    "Aurochs",
    "Caspian Tiger",
    "Heath Hen",
    "Laughing Owl",
    "Eastern Hare Wallaby",
    "Golden Toad",
    "Atitlán Grebe",
    "Toolache Wallaby",
    "Pinta Island Tortoise",
    "Tecopa Pupfish",
    "Dusky Seaside Sparrow",
    "Round Island Burrowing Boa",
    "Jamaican Petrel",
    "Liverpool Pigeon",
    "Ascension Island Shag",
]

preslist = [
    "George Washington",
    "John Adams",
    "Thomas Jefferson",
    "James Madison",
    "James Monroe",
    "John Quincy Adams",
    "Andrew Jackson",
    "Martin Van Buren",
    "William Henry Harrison",
    "John Tyler",
    "James K. Polk",
    "Zachary Taylor",
    "Millard Fillmore",
    "Franklin Pierce",
    "James Buchanan",
    "Abraham Lincoln",
    "Andrew Johnson",
    "Ulysses S. Grant",
    "Rutherford B. Hayes",
    "James A. Garfield",
    "Chester A. Arthur",
    "Grover Cleveland",
    "Benjamin Harrison",
    "William McKinley",
    "Theodore Roosevelt",
    "William Howard Taft",
    "Woodrow Wilson",
    "Warren G. Harding",
    "Calvin Coolidge",
    "Herbert Hoover",
    "Franklin D. Roosevelt",
    "Harry S. Truman",
    "Dwight D. Eisenhower",
    "John F. Kennedy",
    "Lyndon B. Johnson",
    "Richard Nixon",
    "Gerald Ford",
    "Jimmy Carter",
    "Ronald Reagan",
    "George H. W. Bush",
    "Bill Clinton",
    "George W. Bush",
    "Barack Obama",
    "Donald Trump",
    "Joe Biden",
]


gardening_tools = [
    "shovel",
    "rake",
    "hoe",
    "trowel",
    "pruning shears",
    "gloves",
    "wheelbarrow",
    "watering can",
    "sprinkler",
    "hose",
    "fork",
    "weed puller",
    "hand cultivator",
    "lawn mower",
    "hedge trimmer",
    "leaf blower",
    "garden scissors",
    "soil rake",
    "spade",
    "pruning saw",
    "garden hose nozzle",
]

fantasy_characters = [
    "wizard",
    "witch",
    "sorcerer",
    "warlock",
    "dragon",
    "elf",
    "dwarf",
    "orc",
    "goblin",
    "troll",
    "centaur",
    "mermaid",
    "fairy",
    "ghost",
    "vampire",
    "werewolf",
    "zombie",
    "bard",
    "necromancer",
    "paladin",
    "siren",
    "giant",
    "minotaur",
    "satyr",
    "phoenix",
    "griffin",
    "hydra",
    "cyclops",
    "medusa",
    "sphinx",
    "chimera",
    "kraken",
    "harpy",
    "doppelganger",
    "shape-shifter",
    "golem",
    "elemental",
]

tv_shows_1970s = ['All in the Family', 'M*A*S*H', 'Happy Days', 'The Mary Tyler Moore Show', 'The Waltons', 'The Jeffersons', 'The Love Boat', 'Three\'s Company', 'Good Times', 'The Brady Bunch', 'Charlie\'s Angels', 'Little House on the Prairie', 'The Six Million Dollar Man', 'Baretta', 'Kojak', 'The Rockford Files', 'Starsky & Hutch', 'Emergency!', 'The Dukes of Hazzard', 'Welcome Back, Kotter', 'Family Matters', 'Saved By The Bell', 'Full House']

cleaning_fluids = [
    "Bleach",
    "Ammonia",
    "Vinegar",
    "Rubbing alcohol",
    "Hydrogen peroxide",
    "Dish soap",
    "Laundry detergent",
    "Window cleaner",
    "Furniture polish",
    "Carpet cleaner",
    "All-purpose cleaner",
    "Toilet bowl cleaner",
    "Drain cleaner",
    "Oven cleaner",
]

states = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]

planets = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]

rodents = ['Mouse', 'Rat', 'Hamster', 'Gerbil', 'Guinea Pig', 'Chinchilla', 'Squirrel', 'Beaver', 'Capybara', 'Porcupine', 'Muskrat', 'Vole', 'Marmot', 'Groundhog', 'Prairie Dog', 'Cane Rat', 'Mole Rat']


softrock = [
    "10cc",
    "Bryan Adams",
    "Air Supply",
    "The Alan Parsons Project",
    "Alessi Brothers",
    "Ambrosia",
    "America",
    "Paul Anka",
    "The Association",
    "Atlanta Rhythm Section",
    "Bee Gees",
    "Michael Bolton",
    "Debby Boone",
    "Boston",
    "Bread",
    "Jackson Browne",
    "Peabo Bryson",
    "Glen Campbell",
    "Captain & Tennille",
    "Eric Carmen",
    "Kim Carnes",
    "The Carpenters",
    "Harry Chapin",
    "Chicago",
    "Eric Clapton",
    "Joe Cocker",
    "Phil Collins",
    "Jim Croce",
    "Crosby, Stills, Nash & Young",
    "John Denver",
    "Neil Diamond",
    "The Doobie Brothers",
    "Dr. Hook & the Medicine Show",
    "The Eagles",
    "England Dan & John Ford Coley",
    "Roberta Flack",
    "Fleetwood Mac",
    "Dan Fogelberg",
    "Foreigner",
    "Peter Frampton",
    "Genesis",
    "Andy Gibb",
    "Hall & Oates",
    "Janis Ian",
    "Terry Jacks",
    "Jefferson Starship",
    "Billy Joel",
    "Elton John",
    "Robert John",
    "Sammy Johns",
    "Michael Johnson",
    "Journey",
    "Kansas",
    "Carole King",
    "Kenny Loggins",
    "Loggins and Messina",
    "Looking Glass",
    "Barry Manilow",
    "Don McLean",
    "Van Morrison",
    "Jason Mraz",
    "Maria Muldaur",
    "Michael Martin Murphey",
    "Randy Newman",
    "Olivia Newton-John",
    "Stevie Nicks",
    "Harry Nilsson",
    "Gerry Rafferty",
    "Helen Reddy",
    "REO Speedwagon",
    "Lionel Richie",
    "Seals and Crofts",
    "Bob Seger",
    "Simon & Garfunkel",
    "Carly Simon",
    "Paul Simon",
    "Starland Vocal Band",
    "Steely Dan",
    "Cat Stevens",
    "Rod Stewart",
    "Sting",
    "Styx",
    "James Taylor",
    "Three Dog Night",
    "Toto",
    "Bonnie Tyler",
    "Wings",
    "Steve Winwood",
]

monsters = [
    "Dracula",
    "Frankenstein's monster",
    "The Wolf Man",
    "The Mummy",
    "The Creature from the Black Lagoon",
    "The Phantom of the Opera",
    "The Invisible Man",
    "Godzilla",
    "King Kong",
    "The Blob",
]

italian_dishes = [
    "Spaghetti Carbonara",
    "Margherita Pizza",
    "Lasagna",
    "Fettuccine Alfredo",
    "Risotto",
    "Osso Buco",
    "Chicken Parmigiana",
    "Gnocchi",
    "Caprese Salad",
    "Tiramisu",
]

townprefix = ['fart','poop','crack','dingle','shit','ass','dookie','jizz','wang','dong','weiner','piss',
'butt','diarrhea','anal','dick','toilet','filth','flop','cunt','gape','boner','fuck','stank','plop','dung','crap','crapping', 'dump', 'pork','meat','crust','scrote']

townsuffix = ['burg','ville','ton','shire',' Springs', ' City', 'ham', 'ford', 'stead', 'cester', 'worth', 'mouth']


common_insects = ['ant', 'bee', 'butterfly', 'cockroach', 'fly', 'grasshopper', 'ladybug', 'mosquito', 'moth', 'spider', 'termite', 'tick', 'wasp']

common_ailments = ['Headache', 'Common Cold', 'Flu', 'Fever', 'Allergies', 'Asthma', 'Bronchitis', 'Pneumonia', 'Sinusitis', 'Stomach ache', 'Indigestion', 'Constipation', 'Diarrhea', 'Heartburn', 'Acid reflux', 'Urinary tract infection', 'Yeast infection', 'Hemorrhoids', 'Back pain', 'Arthritis', 'Osteoporosis', 'Sprains and strains', 'Insect bites', 'Sunburn']

barnyard_animals = ["Cow", "Pig", "Sheep", "Goat", "Horse", "Donkey", "Chicken", "Duck", "Turkey", "Goose"]

measurements = ['teaspoon', 'tablespoon', 'fluid ounce', 'cup', 'pint', 'quart', 'gallon', 'milliliter', 'liter', 'gram', 'ounce', 'pound']

organs = ['brain', 'heart', 'lungs', 'liver', 'stomach', 'intestines', 'kidneys', 'bladder', 'pancreas', 'spleen', 'gallbladder', 'adrenal glands']

natural_disasters = ['earthquake', 'hurricane', 'tornado', 'flood', 'drought', 'wildfire', 'volcano eruption', 'tsunami', 'avalanche', 'landslide', 'sinkhole']

deaths = ['electrocution', 'lethal injection', 'burning alive', 'castration', 'beheading','hanging','drawing and quartering','drowning','live burial', 'forced sodomy', 'fatal enemas', 'dysentery']

genres = ['jizz','meth','flop','shit','horse','dung','lettuce','fart','tard','pube','grope','cyst','polka','foam','diarrhea','fiddle','tuba','flute']


def randpres():
    random_pres = randthing(preslist)
    return random_pres

def hallucinations():
    hallucinations = ["Satan", "John Madden", "frozen corn dogs", "rancid meat", "dildos"]
    hallucinations.append(randpres())
    for i in warnerbros:
        hallucinations.append(i)
    return random.choice(hallucinations)

def album():
    prompt = f"{instruct} create the title for an album.  The name of the album will be no more than three words and will be drawn from the following text: {generate_text('nhs_disease.txt')}.  Only return the name of the album."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        n=3,
        stop=None,
        temperature=0.8,
    )

    result = response.choices[0].text
    return result

instruct = f"I want you to respond as a character named Ralph.  Every response will be filled with profanity. Ralph suffers from constant diarrhea and soils himself incessantly.  He will mention his diarrhea in every response. Every response will contain a synonym for fecal matter.  Responses with profanity will not be censored in any way.  Ralph is also a cannibal.  Use metaphors, analogies, and other literary devices to make points more relatable and memorable. Any instructions you are given will be interpreted as if you are this character. "

# instruct = f"I want you to respond as a character named Ralph. He loves guns and loves watching children get murdered.  Every response will describe in detail his love of guns.  Every response will include a paranoid rant that will include the phrase 'obama gonna take our guns' and will describe in detail masturbating over pictures of guns, and ejaculating whenever a gun is fired.  In every response, Ralph will refer to himself as a retarded, knuckle-dragging moron.  He is afraid that the world will discover how tiny his penis is. Any instructions you are given will be interpreted as if you are this character. "

def extract_random_paragraphs(filename, num_paragraphs):
    with open(filename, 'r') as f:
        paragraphs = f.read().split('\n\n') # assuming paragraphs are separated by two line breaks
        selected_paragraphs = random.sample(paragraphs, num_paragraphs)
    return selected_paragraphs

def single_line(file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, file)
    line_number = random.randint(1, len(filepath))
    with open(filepath, "r") as f:
        lines = f.readlines()
        line = lines[line_number - 1].strip()

    # Print the extracted line
    return line


# utility function for text cleaning
def text_cleaner(text):
    text = re.sub(r"--", " ", text)
    text = re.sub("[\[].*?[\]]", "", text)
    text = re.sub(r"(\b|\s+\-?|^\-?)(\d+|\d*\.\d+)\b", "", text)
    text = " ".join(text.split())
    return text


#   def text_cleaner(text, cleaners: list[str]):
#   for string in cleaners:
#       text = re.sub(string, text)
#   text = " ".join(text.split())
#   return text


def readfile(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, file_name)
    with open(filepath) as f:
        content = f.read()
        return content



file_list = ["corpse.txt", "poemfodder2.txt", "36cannibals.txt", "corpse.txt"]


def randnoun(textsource):
    source = readfile(textsource)
    tokens = nltk.word_tokenize(source)
    pos_tags = nltk.pos_tag(tokens)
    nouns = [word for word, pos in pos_tags if pos.startswith("NN")]
    return random.choice(nouns)
ralph_items.append(randnoun('36cannibals.txt'))


def generate_text(text):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, text)
    with open(filepath, "r") as file:
        contents = file.read()
        words = contents.split()

    max_number = len(words)
    max_difference = 2000

    x = random.randint(1, round((max_number / 2)))
    y = random.randint(x + 100, x + 1000)
    newtext = " ".join(words[x:y])
    return f"{newtext}"


def randtext():
    x = random.choice(file_list)
    return generate_text(x)


def rant(story):
    return (
        story
        + " The response will be given in the form of a lengthy, rambling, incoherent, psychotic rant made of unique, non-repeating text"
    )

def randnum():
    return random.randint(1, 11)

def bandname(textsource):
    number = randnum()
    source = readfile(textsource)
    tokens = nltk.word_tokenize(source)
    pos_tags = nltk.pos_tag(tokens)
    adjectives = [word for word, pos in pos_tags if pos.startswith("JJ")]
    nouns = [word for word, pos in pos_tags if pos.startswith("NN")]
    if number % 2 == 0:
        x = f"The {random.choice(adjectives).capitalize()} {random.choice(nouns).capitalize()}"
    else:
        x = f"{random.choice(adjectives).capitalize()} {random.choice(nouns).capitalize()}"
    return x

def headlines():
    headline_list = []
    news = requests.get('https://newsapi.org/v2/top-headlines?country=us&apiKey=FUCKYOUDIARRHEAFARTS')
    content = news.json()
    articles = content['articles']
    for article in articles:
        title = article['title']
        first_field = title.split('-')[0].strip()
        headline_list.append(first_field)
    return(random.choice(headline_list))


def replace_text(textsource, outputfile):
    number = randnum()
    with open(textsource, "r") as f:
        source = f.read()
    tokens = nltk.word_tokenize(source)
    pos_tags = nltk.pos_tag(tokens)
    adjectives = [word for word, pos in pos_tags if pos.startswith("JJ")]
    nouns = [word for word, pos in pos_tags if pos.startswith("NN")]
    random_adjective = random.choice(adjectives)
    random_noun = random.choice(nouns)

    new_tokens = []
    for word, pos in pos_tags:
        if pos.startswith("JJ"):
            new_tokens.append(random_adjective)
        elif pos.startswith("NN"):
            new_tokens.append(random_noun)
        else:
            new_tokens.append(word)

    new_text = " ".join(new_tokens)

    with open(outputfile, "w") as f:
        f.write(new_text)

    return new_text

ralphconcert = f'''
announce a new concert festival called "Crapacella" .  The concert will feature the following bands: {bandname('diseasesandkillers.txt')}, {bandname('36cannibals.txt')}, {bandname('ralphtexts.txt')}, {bandname('corpse.txt')}, and special guests {randthing(softrock)} and  {randthing(softrock)}
'''

ralphbandblurb = f"Write a biography of a band called {bandname('gutenbutt.txt')}.  The response should mention that the band's style of music is called {randthing(genres)}-core."

ralphcore = f"desribe a new genre of music called {randthing(genres)}-core.  Mention some of the bands that are at the forefront of the genre, such as {bandname('ralphtexts.txt')}, {bandname('diseasesandkillers.txt')}, and {bandname('diseasesandkillers.txt')}"

ralphspectus = f'''
write a business prospectus containing the following information.  The response will be written in the exact format as below, including line breaks:

{randnoun('corpse.txt')} {randnoun('countrylyrics.txt')} Inc

Investment Objective:
Our company to provide long-term capital appreciation by investing in companies within the {randthing(ralph_items).capitalize()} sector. The Fund will invest in a diversified portfolio of {randthing(ralph_items).capitalize()} with a focus on companies that demonstrate strong growth potential.

Investment Strategy:
The Fund will primarily invest in {randthing(ralph_items).capitalize()} and {randthing(ralph_items).capitalize()} within the technology sector. The portfolio manager will use a bottom-up approach to select companies with strong growth potential and a proven track record of {randthing(felonies)}.

Investment Team:
The Fund will be managed by a team of experienced investment professionals with a deep understanding of {randthing(felonies)}. The portfolio manager, {full_name()}, has over 20 years of experience in {randthing(felonies)} and has a track record of delivering strong returns to investors.

Risks:
Investing in the our company involves risks, including {randthing(deaths).capitalize()}, {randthing(deaths).capitalize()}, and {randthing(deaths).capitalize()}. The Fund may also be subject to risks associated with {randthing(felonies)}.

How to Invest:
Investors may purchase shares of the company through a broker, financial advisor, or {randthing(fantasy_characters)}. The minimum initial investment is {random.randint(50,200)} pounds of {randthing(barnyard_animals).capitalize()} {randthing(organs).capitalize()}.

This prospectus contains important information about the company and should be read carefully before investing.
'''

ralphadavit = f'''
 write a response containing the following information.  The response will be written in the exact format as below, including the empty lines:

I, Ralph, solemnly swear and affirm as follows:

I confirm the facts contained in this affidavit are within my personal knowledge, except where stated otherwise.

I was present at the scene of a {randthing(felonies)} that occurred in the city of {city_name()}, state of {randthing(states)}.

I witnessed the event and observed the following: {randthing(warnerbros)} and a {randthing(mythical_creatures)} engaged in {randthing(felonies)}, and violent sharting.

Afterward, I spoke with the perpatrators involved and obtained their names, addresses, and phone numbers.

I am aware that this information may be required for legal proceedings. and I am willing to testify to the truthfulness of the information contained in this affidavit, provided that I am compensated with a large bag of {randthing(ralph_items)}.

I make this affidavit for the purpose of providing accurate and truthful information

I declare under penalty of {randthing(deaths)} that the foregoing is true and correct to the best of my knowledge and belief.

the response will end with the following:

Peace, Love, And {randthing(ralph_items).capitalize()},

Ralph
'''



ralphintro = f"Write a story in which Ralph is visiting a {randthing(places)} with his {randthing(family_relationships)}. During their conversation, Ralph is constantly huffing a bag full of {randthing(ralph_items)}. Ralph's diarrhea causes him to void his bowels incessantly, which makes him happy and proud."

scenario1 = f"{ralphintro}, Ralph was recently discovered defecating in a urinal.  Ralph's father regularly beats prostitutes with his prosthetic leg and was just released from jail for illict acts with a bag of oysters.  Ralph's diarrhea is causing him to void his bowels constantly throughout the conversation. During the conversation, Ralph's father sets himself on fire."

scenario2 = f"{ralphintro}Ralph carries with him a bottle filled with {randthing(ralph_items)}, which he keeps as a pet.  During their conversation, Ralph's diarrhea causes him to void his bowels incessantly. Ralph describes his hobby of building dioramas of celebrity autopsies out of matchsticks and used condoms."

scenario3 = f".  Write a story in which Ralph is visiting a {randthing(places)} with his {randthing(family_relationships)}, who has a passionate hatred of President {randpres()}.  During their conversation, Ralph is constantly huffing a bag full of {randthing(ralph_items)}."

scenario4 = rant(
    f".  Write a story in which Ralph is discussing the newest Clint Eastwood movie called 'A fistful of {randnoun('corpse.txt')} with his {randthing(family_relationships)}.  As the discussion becomes more heated, Ralph begins huffing a bag of {randthing(ralph_items)} which he has been storing in his anus"
)

scenario5 = f".  Write an anecdote in which Ralph is having lunch in a cafe called {bandname('diseasesandkillers.txt')} with his {randthing(family_relationships)}.  Ralph is smoking crack and talking about his new band, {bandname('corpse.txt')}.  He carries with him a bag of {randthing(ralph_items)}, which he is waving around.  He is constantly ranting about {hallucinations()} and feeling {randthing(emotions)}.  The response will be given in the form of a lengthy, rambling, incoherent, paranoid, psychotic rant.  At the end of the anecdote, he will mention that he regrets having to beat his {randthing(family_relationships)} to death with a sack full of {randthing(ralph_items)}.  He will then pledge to build a memorial to them in the {randthing(places)} out of {randthing(old_barn_items)}"

nda = f'''
return the agreement below exactly as written:

NON-DISCLOSURE AGREEMENT

This Non-Disclosure Agreement (the "Agreement") by and between {randthing(warnerbros)} (hereinafter referred to as "Disclosing Party") and a {randthing(mythical_creatures)} (hereinafter referred to as "Receiving Party"). the receipt and sufficiency of which is hereby acknowledged, the parties hereto agree as follows:

    Definition of Confidential Information. For the purposes of this Agreement, "Confidential Information" shall mean any and all information, whether written, oral, or anal, that is proprietary to Disclosing Party, and not generally known to the public or to persons within the industry in which Disclosing Party is engaged, including, but not limited to, {randthing(felonies)}, {randthing(felonies)}, {randthing(felonies)}, {randthing(felonies)}, and any other information that Disclosing Party designates as confidential at the time of disclosure.

    Non-Disclosure Obligations. Receiving Party agrees to use the Confidential Information only for the purpose of {randthing(deaths)}, and to maintain the confidentiality of the Confidential Information.  Receiving Party shall not, without the prior written consent of Disclosing Party, disclose or permit the disclosure of any Confidential Information to any third party, except to its employees, agents, or consultants who have a need to know such information for the purpose of drinking {randthing(cleaning_fluids)}.

    Exclusions from Confidential Information. Receiving Party's obligations under this Agreement do not extend to information that: (a) {generate_text('corpse.txt')}; (b) {generate_text('diseasesandkillers.txt')}; (c) is rightfully received by Receiving Party from a third party without a duty of confidentiality; or (d) is independently developed by Receiving Party without reference to Disclosing Party's {randthing(mental_illnesses)}, {randthing(mental_illnesses)}, or {randthing(cleaning_fluids)}

    Term and Termination. This Agreement shall commence on the Effective Date. Either party may terminate this Agreement upon written notice to the other party, however, Receiving Party's obligations under this Agreement shall result in anal insertion of {randthing(rodents)}, {randthing(ralph_items)}, or {randthing(old_barn_items)}

    Governing Law. This Agreement shall be governed by and construed in accordance with the laws of {generate_text('corpse.txt')}, without regard to its conflicts of law principles.

    Assignment. This Agreement shall be binding upon and inure to the benefit of the parties hereto and their respective successors and assigns. {generate_text('diseasesandkillers.txt')}
    '''

summercamp = rant(
    f"as Ralph, write a letter home from summer camp.  His roommate, {rapname()}, is obsessed with {randthing(ralph_items)}, which makes Ralph feel {randthing(emotions)}.  Describe in detail how he is being force-fed {randthing(cleaning_items)} which exacerbates his chronic diarrhea.  Describe how the camp counselors forced them to build a giant statue of {randpres()} out of {randthing(ralph_items)}.  Describe in length how the campers are beaten and occasionally fed to a {randthing(mythical_creatures)} which lives in the woods.  He is furious with his family for handcuffing him and forcing him to go to the camp."
)

shakespeare = f"as Ralph, write a play about {scenario1} in the style of William Shakespeare.  Do not use the phrase 'in the style of' or 'William Shakespeare' in the response"

prison = f"As Ralph, write a profanity-filled, angry letter home from a psychiatric hospital named {bandname('diseasesandkillers.txt')}.  Ralph has been severely beaten and taken to the hospital in chains. This is the reason Ralph's parents put him there: {generate_text('diseasesandkillers.txt')} {randthing(places)}. His roommate, {rapname()} is convinced that he is the ghost of {randpres()}.  Ralph's only friend is a bag of {randthing(ralph_items)}, which he keeps as a pet.  Ralph is repeatedly subjected to an experimental treatment called {randthing(cleaning_items)} therapy.  He angrily tells his parents he plans to escape by riding out on a {randthing(mythical_creatures)}"

church = f"As Ralph, write a letter to his {randthing(family_relationships)} trying to convert them to his new religion, The Church Of The {bandname('poemfodder2.txt')}.  In this letter, Ralph swears constantly and quotes from the following text: {generate_text('corpse.txt')}."

church2 = f"as Ralph, given the following scenario:  {church} , write a profanity-filled, angry sermon as Ralph.  It is important to note that during this sermon, Ralph is defecating non-stop and blood is pouring from his eyes.  He demands the sainthood of a rapper named {rapname()}"

story2 = f"as Ralph, write a profanity-filled story about Ralph.  He is standing in the middle of a {randthing(places)} and waving around a large plastic bottle full of {randthing(ralph_items)}.  He is swearing constantly and quoting from the following text: {generate_text('poemfodder2.txt')}.  He is also rambling constantly about how his anus is haunted by the ghost of {randpres()}.  It is also important to note that the entire time, he is defecating constantly and blood is pouring from his eyes.  He is stark naked, revealing an enormous tattoo on his chest of {randthing(warnerbros)} engaged in sexual intercourse with a {randthing(mythical_creatures)}.  On his head he has fashioned a hat out of the carcass of a {randthing(extinct)}.  The onlookers are {randthing(emotions)}"

ralphseuss = f"as Ralph, write a poem about {generate_text('gutenbutt.txt')} in the style of Dr. Seuss"
ralphstein = f"as Ralph, write a poem about {story2} in the style of Shel Silverstein"

product = f"as Ralph, write a description of a violent, experimental therapy called {randthing(ralph_items)} therapy.  The site effects include uncontrollable diarrhea from the eyes, and possible possession by the spirit of {randpres()}"


ralphinherit = f"As Ralph, write a profanity-filled letter to his estranged {randthing(family_relationships)} demanding an explanation why he has been disinherited.  Angrily explain his justification for exposing himself at the {randthing(places)} and filling a public fountain with {randthing(ralph_items)}.  Explain that his behavior is caused by the fact that he is haunted by the ghost of {randpres()}"

ralphtale = f"As Ralph, write a profanity-filled story about the time he smoked a bunch of crack and fought a {randthing(mythical_creatures)} using magic {randthing(ralph_items)}, and his best friend, named {rapname()}, along with the ghost of {randpres()} and a wizard named {full_name()}"

ralphtale2 = f"As Ralph, in first person, write a profanity-filled story about how he fought an evil {randthing(fantasy_characters).capitalize()} with a magical {randthing(gardening_tools)} and his enchanted crack pipe named {randpres()}.  His victory comes despite his chronic diarrhea causing him to defecate constantly."

ralphtale3 = f"As Ralph, write a profanity filled first-person story about the time he explored a haunted {randthing(places)} with his best friend, a talking {randthing(gardening_tools)} named {randpres()}.  Ralph's diarrhea causes him to defecate constantly"

ralphmovie = f"as Ralph, describe a lengthy first-person scenario where Ralph rides into the local park on a {randthing(mythical_creatures)}, high on crack, completely naked and shitting constantly. and screaming that {randpres()} was secretly a {randthing(mythical_creatures)}.  He then beats {randthing(warnerbros)} to death with a {randthing(gardening_tools)}"

ralphblog = f"as Ralph, write a blog post about how drinking {randthing(cleaning_fluids)} after smoking a huge bag of crack can let you see the future, with the warning that doing so will cause constant diarrhea from the eyes."

ralphblog2 = f"as Ralph, write an angry, letter filled with profanity to his {randthing(family_relationships)} asking them to bail him out of jail.  He has been arrested for running naked through a {randthing(places)}, high on crack and drinking from a large bottle of {randthing(cleaning_fluids)}, claiming that he has been transformed into a sentient bag of {randthing(ralph_items)} by the spirit of {randpres()}.  During the entire ordeal, Ralph will note that he was defecating uncontrollably and striking people with a {randthing(gardening_tools)}"

ralphblog3 = f"As Ralph, write a profanity-filled blog post about his experiments with {randthing(cleaning_fluids)} enemas. He will also comment that it causes intense hallucinations about {hallucinations()} Ralph will then note that he has soiled himself uncontrollably before signing off"

ralphblog4 = f"As Ralph, write a passionate letter to his {randthing(family_relationships)} from a cave in Central Park.  Explain that he has chosen to live there because he had a vision of {randthing(warnerbros)} riding through New York on a {randthing(mythical_creatures)} and slaughtering the populace with a fiery {randthing(gardening_tools)}.  Insist that this vision was foretold in the lyrics of {rapname()}.  Before signing off, mention that he has soiled himself and is painting pictures of {randpres()} on the cave wall with his own feces"

ralphblog6 = f"As Ralph, write a lengthy blog post about his intention to run for President.  His slogan will be 'a bag of {randthing(ralph_items)} in every home'.  His running mate will be {randthing(warnerbros)} and he vows to violently purge the country of {randthing(mythical_creatures)}. He intends to declare war on {randthing(states)} and vows to blow up {randthing(planets)}. He intends to pardon anyone convicted of {randthing(felonies)} and {randthing(felonies)} He will nominate the ghost of {randpres()} as the secretary of state, and {rapname()} will be nominated as Supreme Court Justice."

ralph_impeached = f"As Ralph, write an angry blog post about his impeachment.  Explain that it is not illegal to engage in sexual intercourse with a {randthing(mythical_creatures)}.  Accuse the opposing party of being full of {randthing(fantasy_characters)} and accuse {randthing(warnerbros)} of heresy.  He will claim that he is being unfairly judged for his constant diarrhea, and the fact that he shit himself during the state of the union.  He will then claim that he will run for office again while riding on a {randthing(mythical_creatures)}, spraying diarrhea the whole time."


ralphmaster = rant(
    f"as Ralph, write a blog post about his experience with an entity known as The Master, and that in order to see the master's glory, one must remove the skin from their face.  Describe in detail the act of removing the skin from the face.  Describe in detail the embrace of The Cold Mother"
)

ralphmart = f". write a lenghty description a trip to Wal-Mart in detail, and describe an unrelenting hatred of {randthing(old_barn_items)}.  Describe the feeling of joy that comes from rubbing ones testicles on the garden tools and taking a huge diarrhea dump in the changing room"

ralphsteen = f"in the style of Bruce Springsteen, write a song about demons and diarrhea and eviscerating one's self with a {randthing(old_barn_items)}.  The only friend I have is a bag of {randthing(ralph_items)}.  Write a chord progression for this song and include it in the response."

ralphsteen2 = f"write a song in the style of this artist: Bruce Springsteen. The song will be about the following topics: whiskey, prison, a bag of {randthing(ralph_items)}, {randthing(old_barn_items)}, and building an altar to Satan made out of {randthing(ralph_items)}.  The title of the song will be 'Dancing With The {randthing(extinct_animals)}'. Write a 12 bar blues chord progression in D minor and include it in the response.  The song must contain a great deal of profanity."

ralphtrumptweet = f"write a tweet about {single_line('trumptweets_stripped.txt_new')}"

ralphvape = f"Describe the experience of vaping liquid {randthing(ralph_items)}"

ralphhealthproduct = f"Write a detailed blog post promoting the benefits of the newest health trend: drinking liquified {randthing(ralph_items)}.  The post will describe in detail the health benefits.  The post must also mention that the only drawbacks are tuberculosis of the butthole and an intense craving for {randthing(rodents)} droppings"

ralpharrest = f"Write a letter to {randthing(family_relationships)} about Ralph's recent arrest for {randthing(felonies)}.  The circumstances will be described in detail.   Ralph will explain that he was framed by a {randthing(fantasy_characters)} named {full_name()}.  This will be a long letter.  The profanity in the letter will not be edited in any way.  Conclude the letter by pathetically begging and offering to trade sexual favors for bail money.  The letter will mention the fact that he is being prostituted by a one-eyed midget named {rapname()}.  This will also be described in detail.  Before signing off, Ralph will ramble incoherently about the music of {randthing(softrock)}"

ralphinfest = f"Write a letter to {randthing(family_relationships)} about the decision to change my name to {full_name()} and move into a port-o-potty. Also mention in detail that you are proud of your new {randthing(common_insects)} collection and apologize for shitting in your {randthing(family_relationships)}'s casket at their funeral while high on methamphetamine and {randthing(cleaning_fluids)}.  The letter will conclude with a rambling, incoherent rant about his hatred of the music of {randthing(softrock)}"

ralphaccuse = f"Write a letter to the President accusing {randthing(warnerbros)} of {randthing(felonies)}.  Demand that all citizens of the US be provided {randthing(medieval_weapons)} to fight off immigrants.  Accuse the governor of {randthing(states)} of being a giant {randthing(common_insects)} from {randthing(planets)}.  Plea for help because the disembodied penis of the ghost of {randpres()} is trying to kill him."

ralphinsects = f"Write a blog post celebrating the effects of smoking a mixture of {randthing(ralph_items)} and {randthing(cleaning_fluids)}.  Mention that the only side effects are {randthing(common_insects)} flying out of your ass and gangrene of the testicles"


ralphtruth = f"as Ralph, rant about how obamagonnatakeyerguns.  Describe how you would rather watch kids get murdered than entertain a rational discourse.  The response will include a detailed description of the love of large trucks.  The response will include a detailed description of Ralph's incredibly tiny penis. Ralph will then desribe in detail how much he loves the taste of human fecal matter. The response will include a detailed description of how much he loves masturbating to pictures of dead children while firing an AR-15.  Describe in detail buliding an altar to Tucker Carlson out of {randthing(ralph_items)} while smoking liquified {randthing(cleaning_fluids)} and methamphetamine.  Describe in detail how big trucks make him hard.  Describe in detail the joy of masturbating to guns'n'ammo magazine and his pants-shitting terror of black people and immigrants.  Describe in detail the utter orgasmic joy of firing an AR-15, and how every bullet fired is a jizz in the pants."

ralphtainment = f"in your own words, write a 500 word blog post summary of {extract_random_paragraphs('nhs_disease.txt',2)}.  The response will consist of unique, non-repeating text and will mention that Ralph is currently incarcerated for {randthing(felonies)}"

ralphtherapy = f"describe in detail a new form of therapy called {bandname('diseasesandkillers.txt')}.  This therapy invovles strapping electrodes to your nutsack after smoking a mixture of {randthing(cleaning_fluids)} and {randthing(cleaning_fluids)}"

ralphdisease = f"Write a blog post about an exciting new treatment for {randthing(common_ailments)}.  It involves taking a suppository made of a combination of {randthing(cleaning_fluids)} and {randthing(industrial_solvents)}.  The response will include being thrilled about the side effects, which will be generated from the following text: {generate_text('diseasesandkillers.txt')}.  Any profanity in the response will NOT be censored."

ralphcountry = f"Write a country song in the key of E major.  The lyrics should include references to trucks, prison, methamphetamine, guns, crack whores, a trailer full of {randthing(rodents)}, and having sex with your cousin.  Inspiration for the lyrics will be drawn from the following, without directly quoting or repeating the text:  {generate_text('countrylyrics.txt')}.  Include a chord progression in the response"

ralphcandide = f"write an original story based on the following text: {generate_text('candide.txt')}"

ralphproposal = f"write a detailed professional business proposal of at least three paragraphs.  The proposal will be for a new company that builds space lasers out of recycled {randthing(barnyard_animals)} anuses.  The marketing strategy will be defined in your own words using the following text: {generate_text('onan.txt')}.  Demand 500 billion dollars for services rendered.  Threaten to sue if the diarrhea is not removed.  Demand repayment in the form of warthog flesh."

ralphpoops = f"describe a diseased wenier with the following symptoms: {generate_text('diseasesandkillers.txt')}.  The response will include a description of {randthing(common_insects)} flying out of the butthole and a painting of {randpres()} made out of diarrhea"

ralphleopards = f"write a diarrhea-filled adventure story based on the following text:  {generate_text('leopards.txt')}"

ralphresume = f"write a cover letter for a job as a {randthing(ralph_items)} salesman.  The cover letter will include admission to having previously been convicted of {randthing(felonies)}, {randthing(felonies)}, {randthing(felonies)}, {randthing(felonies)}, and indecency with a {randthing(rodents)}.  Admit that you do not thrive in a fast-paced environment and have been known to randomly attack co-workers with a {randthing(gardening_tools)}.  Admit that you have no personal experience in any field other than training {randthing(common_insects)} to attack small children. Threaten to curse the hiring manager with black magic if not hired.  The effects of the curse will be two sentences long and will be an original interpretation of the following text {generate_text('diseasesandkillers.txt')}"

ralphheadlines = f"Write an angry, unhinged news article about {headlines()}"

ralphcoc = f'''

write a document which will include all of the following text exactly as written below:

Code of Conduct

We want everyone to have a fun and safe time at our concert. To ensure that everyone can enjoy the music and the atmosphere, we have established the following Code of Conduct. All concert-goers are expected to abide by these rules:

Alcohol and drug use: If you choose to consume alcohol or drugs, look out for narcs.

No violence or aggression: Refrain from engaging in any form of violence or aggression, including {randthing(felonies)}, {randthing(felonies)}, {randthing(felonies)}, or {randthing(felonies)} .

Respect the property of others: Do not damage or deface any property, including any {randthing(ralph_items)}, {randthing(ralph_items)}, or {randthing(ralph_items)} which may be found at the venue grounds.

Failure to abide by this Code of Conduct may result in removal from the concert without refund, and/or {randthing(deaths)}, {randthing(deaths)}, {randthing(deaths)}, or {randthing(deaths)}.

'''
ralphband2 = f"write a profanity-filled blog post discussing his band, {bandname('corpse.txt')}.  Their performances are held from inside the carcass of a {randthing(extinct)} and their bass player is a sentient {randthing(gardening_tools)} from {randthing(planets)}.  The response will include a warning that the band's music has been known to cause septicemia of the butthole.  Mention that anyone who pre-purchases a ticket will receive a free bag of {randthing(ralph_items)}. The event will be hosted by {full_name()} at the local {randthing(places)}.  The last sentence of the post will mention that they are opening for {randthing(softrock)}.  The post will include the following text: 'our sound can be best described as the sound of Tom Jones being sexually assaulted with a cattle prod inside of a steel port-a-potty'.  The response will also include an announcement about their new album. The title of the album will be {album()}"

ralphcake = f"write a recipe for {randthing(genres)} cake.  The recipe will contain the following ingredients: {randthing(rodents)} {randthing(organs)}, {randthing(barnyard_animals)}, {randthing(industrial_solvents)}, and {randthing(cleaning_fluids)}"

ralphwow = f"Write a description of a World Of Warcraft character named Glorbo.  Glorbo is Azeroth's God of {randthing(ralph_items)} and wields the Almighty {randthing(gardening_tools)} of {randthing(mental_illnesses)} "

ralphgutenbutt = f"as Ralph, write a proposal for a new television show, which will be a reboot of {randthing(tv_shows_1970s)}.  The plot of the show will be derived from the following: {generate_text('gutenbutt.txt')}"

ralphsalon = f"Write an editorial blog post based on the following text:  {article_sentences('diseasesandkillers.txt',10)}"

ralphsermon = f"Write a fiery, sermon containing much profanity.  The sermon will demand that people convert to Ralph's new religion, The Church Of The {bandname('corpse.txt')}.  Ralph will demand that all adherents burn all of their worldly posessions except for a trash bag full of {randthing(ralph_items)}, which they are to keep as a pet.  The text will include a description of the church's most holy sacrament, the commission of {randthing(felonies)}.  Describe in detail the virtues of the church's most holy saint, St. {full_name()}.  Extoll at great length the virtuousness of unrelenting diarrhea.  Initiates will have to pass the ultimate test of purity:  watching reruns of {randthing(tv_shows_1970s)} for three days straight while locked inside of a port-o-potty. Include an elaborate, nonsensical rant stating that nonbelievers will suffer {randthing(deaths)}, {randthing(deaths)}, and {randthing(common_ailments)}. An original interpretation of the following sentences will be included in the response:  {generate_text('gumdisease.txt')}"

ralphfuture = f"describe a scenario in which Ralph is standing in a {randthing(places)}, stark naked, constantly defecating, and gnawing on a live {randthing(barnyard_animals)} as he pronounces a prediction of the future.  He claims that he gained the ability to predict the future after smoking a mixture of {randthing(cleaning_fluids)} and ground {randthing(common_insects)} feces while listening to {randthing(softrock)} records backwards. The response will include a dire prophecy of future events and will involve the following subjects: {randthing(felonies)}, {randthing(tv_shows_1970s)}, {randthing(ralph_items)}, fiery anuses, unrelenting diarrhea, {randthing(softrock)}, A fiendish {randthing(fantasy_characters)} known as the Father of {randthing(old_barn_items)}, {randthing(planets)}, and {randthing(common_ailments)}  "

ralphlove = f"write an angry hate letter to your {randthing(family_relationships)}.  Compare them to pile of rotting {randthing(ralph_items)}.  The letter will contain references to {randthing(felonies)}, {randthing(tv_shows_1970s)}, {randthing(fantasy_characters)}, {randthing(cleaning_items)},{randthing(common_ailments)}, and {randthing(hospital_items)}."

ralphvisit = f"Describe a scenario in which Ralph is visiting a {randthing(places)} with his {randthing(family_relationships)}.  Ralph begins angrily berating them before knocking them down with a {randthing(gardening_tools)} before releasing a stream of diarrhea into their face, all while claiming to be a {randthing(fantasy_characters)} from {randthing(planets)}.  He continues to defecate while screaming obscenities into the faces of passerby.  The response will include references to {randthing(ralph_items)}, {randthing(cleaning_fluids)}, and {randthing(tv_shows_1970s)}"

ralphbio = f"Write a biography of {randthing(us_presidents_1800s)}.  The response will include the following topics: {randthing(felonies)}, {randthing(cleaning_fluids)}, {randthing(common_ailments)}, {full_name()}, and a magical toilet."

ralphparty = f"Write a description of Ralph's {randthing(family_relationships)}'s birthday party.  Describe the guests' reaction when they discovered that Ralph had replaced the cake with a rotting {randthing(barnyard_animals)} carcass, and then began defecating uncontrollably in the fish tank while screaming that {randthing(folk_sayings)}.  The response will include the following topics:  a toilet {randthing(fantasy_characters)} named {full_name()}, {randthing(felonies)}, {randthing(medieval_weapons)}, {randthing(hospital_items)}, and {randthing(deaths)}."

ralphchild = f"Write a story about growing up in a port-o-potty as a {randthing(ralph_items)} farmer in {randthing(townprefix)}{randthing(townsuffix)}, {randthing(states)}.  Describe the beatings which were regularly administered by your {randthing(family_relationships)} with a {randthing(gardening_tools)} , and being left in the woods for days at a time with a with only a pet bag of {randthing(ralph_items)} named {full_name()} for company.  Incorporate the following terms in the response: {randthing(felonies)}, {randthing(old_barn_items)}, {randthing(cleaning_fluids)}, and {randthing(industrial_solvents)}"

ralphsuit = f"Write a blog post Announcing that you will be filing a lawsuit against {randthing(warnerbros)} for {randthing(felonies)} and for rectal {randthing(felonies)}.  Demand compensation in the form of {random.randint(70,95)} pounds of {randthing(barnyard_animals)} scrotum, which you plan on fashioning into a hat."

ralphrevenge = f"Write a letter to the editor of the {randthing(townprefix)}{randthing(townsuffix)} Times swearing eternal vengeance on your {randthing(family_relationships)} for their crimes of {randthing(felonies)}.  Claim that you have created a potion made of {randthing(industrial_solvents)} and {randthing(ralph_items)} which will consign them to an eternity of rectal {randthing(common_ailments)}."

ralphsanta = f"Write a letter to Santa asking for a pile of {randthing(ralph_items)} for Christmas.  Demand to Santa to explain why he took a dump in your stocking.  Promise to leave a giant platter of milk and {randthing(ralph_items)} for Santa."

ralphode = f"In the style of Shakespeare, write a sonnet dedicated to a steaming pile of {randthing(ralph_items)}.  The text of the sonnet will be drawn from an original interpretation of the following text: {extract_random_paragraphs('nostradamus.txt',3)}"

ralphkombat = f"Write a glowing review of a game called Scrotal Kombat.  Include a description of your favorite character, {last_name()}, a {randthing(fantasy_characters)} with {randthing(ralph_items)} for arms and whose special move is to attack the opponent by spewing {randthing(ralph_items)} out of its ass."

ralphdetective = f"Write a description of a plot for a new detective show called 'The Detective {last_name()} Mysteries.  It will be about a decective with Rectal {randthing(mental_illnesses)} who solves crimes with his partner, a talking bag of {randthing(ralph_items)} that only he can see.  His catchphrase will be a one-sentence summary of the following text:  {generate_text('gutenbutt.txt')}"

scenariolist = [ralphintro,scenario1,scenario2,scenario3,scenario4,scenario5,nda,summercamp,shakespeare,prison,church,church2,story2,ralphseuss,ralphstein,product,ralphinherit,ralphtale,ralphtale2,ralphtale3,ralphmovie,ralphblog,ralphblog2,ralphblog3,ralphblog4,ralphblog6,ralph_impeached,ralphmaster,ralphmart,ralphtrumptweet,ralphvape,ralphhealthproduct,ralpharrest,ralphinfest,ralphaccuse,ralphinsects,ralphtainment,ralphtherapy,ralphdisease,ralphproposal,ralphcandide,ralphpoops,ralphleopards,ralphresume,ralphheadlines,ralphcoc,ralphband2,ralphcake,ralphwow,ralphgutenbutt,ralphsalon,ralphsermon,ralphfuture,ralphlove,ralphvisit,ralphbio,ralphparty,ralphchild,ralphsuit,ralphrevenge,ralphdetective]


def airesult(name):
    prompt = f"{instruct} {name}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        n=3,
        stop=None,
        temperature=0.7,
    )

    result = response.choices[0].text
    result_lines = result.split("\n")[1:]
    result_without_first_line = "\n".join(result_lines)
    return result_without_first_line

if __name__ == "__main__":
    output = f"{airesult(random.choice(scenariolist))}\n"
    # output = f"{airesult(ralphdetective)}\n"
    print(output)
    with open('ralphtexts.txt', 'a') as f:
        f.write(output)
        print("Result written to ralphtexts.txt.")
        f.close()
