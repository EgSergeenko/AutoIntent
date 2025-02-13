import random


adjectives = [
    "adorable",
    "adventurous",
    "aggressive",
    "agile",
    "alert",
    "alive",
    "amused",
    "angry",
    "annoyed",
    "anxious",
    "arrogant",
    "ashamed",
    "attractive",
    "average",
    "awful",
    "bad",
    "beautiful",
    "better",
    "bewildered",
    "black",
    "bloody",
    "blue",
    "blue-eyed",
    "blushing",
    "bored",
    "brainy",
    "brave",
    "breakable",
    "bright",
    "busy",
    "calm",
    "careful",
    "cautious",
    "charming",
    "cheerful",
    "clean",
    "clear",
    "clever",
    "cloudy",
    "clumsy",
    "colorful",
    "combative",
    "comfortable",
    "concerned",
    "condemned",
    "confused",
    "cooperative",
    "courageous",
    "crazy",
    "creepy",
    "crowded",
    "cruel",
    "curious",
    "cute",
    "dangerous",
    "dark",
    "dead",
    "defeated",
    "defiant",
    "delightful",
    "depressed",
    "determined",
    "different",
    "difficult",
    "disgusted",
    "distinct",
    "disturbed",
    "dizzy",
    "doubtful",
    "drab",
    "dull",
    "eager",
    "easy",
    "elated",
    "elegant",
    "embarrassed",
    "enchanting",
    "encouraging",
    "energetic",
    "enthusiastic",
    "envious",
    "evil",
    "excited",
    "expensive",
    "exuberant",
    "fair",
    "faithful",
    "famous",
    "fancy",
    "fantastic",
    "fierce",
    "filthy",
    "fine",
    "foolish",
    "fragile",
    "frail",
    "frantic",
    "friendly",
    "frightened",
    "funny",
    "gentle",
    "gifted",
    "glamorous",
    "gleaming",
    "glorious",
    "good",
    "gorgeous",
    "graceful",
    "grieving",
    "grotesque",
    "grumpy",
    "handsome",
    "happy",
    "healthy",
    "helpful",
    "helpless",
    "hilarious",
    "homeless",
    "homely",
    "honest",
    "hopeful",
    "horrible",
    "hungry",
    "hurt",
    "hypnotic",
    "icky",
    "ill",
    "important",
    "impossible",
    "inexpensive",
    "innocent",
    "inquisitive",
    "itchy",
    "jealous",
    "jittery",
    "jolly",
    "joyous",
    "kind",
    "lazy",
    "light",
    "lively",
    "lonely",
    "long",
    "lovely",
    "lucky",
    "magnificent",
    "misty",
    "modern",
    "motionless",
    "muddy",
    "mysterious",
    "nasty",
    "naughty",
    "nervous",
    "nice",
    "nutty",
    "obedient",
    "obnoxious",
    "odd",
    "old",
    "open",
    "outrageous",
    "outstanding",
    "panicky",
    "perfect",
    "plain",
    "pleasant",
    "poised",
    "poor",
    "powerful",
    "precious",
    "prickly",
    "proud",
    "putrid",
    "puzzled",
    "quaint",
    "real",
    "relieved",
    "repulsive",
    "rich",
    "scary",
    "selfish",
    "shiny",
    "shy",
    "silly",
    "sleepy",
    "smiling",
    "smoggy",
    "sore",
    "sparkling",
    "splendid",
    "spotless",
    "stormy",
    "strange",
    "stupid",
    "successful",
    "super",
    "talented",
    "tame",
    "tasty",
    "tender",
    "tense",
    "terrible",
    "thankful",
    "thoughtful",
    "thoughtless",
    "tired",
    "tough",
    "troubled",
    "ugly",
    "uninterested",
    "unsightly",
    "unusual",
    "upset",
    "uptight",
    "vast",
    "victorious",
    "vivacious",
    "wandering",
    "weary",
    "wicked",
    "wide-eyed",
    "wild",
    "witty",
    "wonderful",
    "worried",
    "wrong",
    "zany",
    "zealous",
]

nouns = [
    "alligator",
    "ankylosaurus",
    "ant",
    "apple",
    "archaeopteryx",
    "auk",
    "banana",
    "bat",
    "bear",
    "bee",
    "beetle",
    "bird",
    "brontosaurus",
    "butterfly",
    "caribou",
    "cat",
    "caterpillar",
    "chameleon",
    "chicken",
    "compsognathus",
    "cow",
    "cricket",
    "crocodile",
    "deer",
    "dimetrodon",
    "dinosaur",
    "direwolf",
    "dodo",
    "dog",
    "dolphin",
    "dragonfly",
    "duck",
    "eagle",
    "elephant",
    "falcon",
    "fish",
    "flamingo",
    "fly",
    "fox",
    "frog",
    "gecko",
    "giraffe",
    "goat",
    "goose",
    "grasshopper",
    "hawk",
    "hippo",
    "horse",
    "ichthyosaurus",
    "iguana",
    "kangaroo",
    "koala",
    "ladybug",
    "leopard",
    "lion",
    "lizard",
    "mammoth",
    "megalodon",
    "moa",
    "monkey",
    "mosasaurus",
    "mosquito",
    "mouse",
    "owl",
    "panda",
    "parrot",
    "passengerpigeon",
    "penguin",
    "pigeon",
    "plesiosaurus",
    "pteranodon",
    "pterodactyl",
    "quagga",
    "rabbit",
    "rhino",
    "sabertooth",
    "salamander",
    "seagull",
    "shark",
    "sheep",
    "smilodon",
    "snake",
    "sparrow",
    "spider",
    "spinosaurus",
    "squirrel",
    "stegosaurus",
    "stellersea",
    "swan",
    "thylacine",
    "tiger",
    "toad",
    "triceratops",
    "turkey",
    "turtle",
    "tyrannosaurus",
    "velociraptor",
    "vulture",
    "wasp",
    "whale",
    "wolf",
    "zebra",
]


def generate_name():
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return f"{adjective}_{noun}"
