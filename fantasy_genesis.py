#!/usr/bin/env python2
'''
This script outputs a random selection from the tables of the game Fantasy
Genesis. You can find the book here:

http://www.amazon.com/Fantasy-Genesis-Creativity-Game-Artists/dp/1600613373

'''

from random import choice

ANIMA = {
    'Sea life': [
        'Mollusk',
        'Crab, Lobster',
        'Squid, Mudskipper',
        'Fish - Deep Sea',
        'Jellyfish, Octopus',
        'Fish - Fresh Water',
        'Whale, Dolphin',
        'Shell',
        'Eel, Leech',
        'Coral, Anemone',
        'Shark, Ray',
        ],
    'Insect': [
        'Worm',
        'Ant',
        'Mosquito',
        'Moth, Butterfly',
        'Fly, Dragonfly',
        'Lotus, Mantis',
        'Bee, Wasp',
        'Caterpiller',
        'Beetle, Scarab',
        'Flea, Mite',
        'Spider',
        ],
    'Mammal': [
        'Sheep, Cow',
        'Mouse, Rabbit',
        'Pig, Bear',
        'Deer, Pronghorn',
        'Ram, Bull, Buck',
        'Elephant, Giraffe',
        'Bat',
        'Bear',
        'Lupine - Wild Dog',
        'Horse, Zebra',
        'Feline - Wild Cat',
        'Primate',
        ],
    'Reptile': [
        'Crocodile, Gila',
        'Frog, Newt',
        'Lizard, Snake',
        'Turtle',
        ],
    'Bird': [
        'Wild Fowl, Duck',
        'Farm Fowl, Rooster',
        'Seabird, Penguin',
        'City - Raven, Sparrow',
        'Tropical - Parrot, Heron',
        'Bird of Prey - Hawk, Owl',
        ],
}

VEGGIE = {
    'Plant': [
        'Seaweed',
        'Fern',
        'Desert Cacti',
        'Thick Leaf - Jade',
        'Flower - Domestic',
        'Vine',
        'Poppy',
        'Grass, Dandelion',
        'Bamboo',
        'Flower - Wild',
        'Carnivorous',
        ],
    'Fruit & Vegetable': [
        'Asparagus',
        'Pinecone',
        'Berry, Grapes',
        'Ginger',
        'Tree Fruit (Apple, Orange)',
        'Bean',
        'Pumpkin, Gourd',
        'Broccoli, Artichoke',
        'Corn',
        'Grain, Wheat',
        'Pineapple',
        ],
    'Fungi': [
        'Moss',
        'Ooze, Jelly',
        'Lichen',
        'Mushroom',
        ],
    'Tree': [
        'Willow',
        'Birch',
        'Maple, Oak',
        'Banyan',
        'Pine',
        'Palm',
        ]
}

ELEMENTAL_AND_MINERAL = {
    'Fire & Electric': [
        'Fire, Vapor',
        'Electric Bolt',
        'Ember, Hot Coal',
        'Molten Lava',
        ],
    'Liquid': [
        'Icicles',
        'Fog, Vapor',
        'Wave',
        'Dew Drops',
        'Ripple',
        'Frost, Snow',
        'Suds, Bubbles',
        'Tar, Gum',
        ],
    'Earth & Metal': [
        'Malachite',
        'Mountain, Cliff Face',
        'Brick, Cobblestone',
        'Rust, Oxide',
        'Cracked Clay',
        'Stalactite, Stalagmite',
        'Glass, Crystals',
        'Powder, Sand',
        'Slate, Shale',
        'Cement, Sediment',
        'Mercury, Chrome',
        ],
    'Astral & Atmospheric': [
        'Moon Cycles',
        'Starfield',
        'Crater, Asteroid',
        'Solar Flare',
        'Galaxy Form',
        'Volcano',
        'Planets, Saturn\'s Rings',
        'Cloud, Cyclone'
        ],
}

TECHNE = {
    'Transportation': [
        'Car, Truck, Bus',
        'Aircraft',
        'Rail, Train, Trolley',
        'Cycle',
        'Sled, Ski',
        'Boat, Ship',
        'Spacecraft',
        'Tank Tread',
        ],
    'Architecture': [
        'Ornament, Gargoyle',
        'Bridge, Framework',
        'Castle, Domed',
        'Ornament, Pillar',
        'Modern Skyscraper',
        'Place of Worship, Totem',
        'Doorway, Archway',
        'Old Village, Cottage',
        ],
    'Tool': [
        'Drill',
        'Cups, Plates',
        'Umbrella',
        'Bundle, Bale'
        'Hammer, Axe',
        'Brush - Hair, Tooth',
        'Razor, Knife',
        'Spigot, Faucet',
        'Rope',
        'Silverware',
        'Lock, Key',
        'Adhesive, Bandage',
        'Shovel, Pick',
        'Capsule, Tablet',
        'Nuts, Bolts',
        'Chain',
        'Thread, Stitch',
        'Shears, Scissors',
        'Pen, Paintbrush',
        'Spring, Coil',
        'Syringe',
        'Tube, Plumbing',
        ],
    'Machine': [
        'Switch, Dial, Button',
        'Turbine',
        'Bulb, Lamp',
        'Clock, Gears',
        'Fan, Propeller',
        'Saw',
        'Reactor Core',
        'Telephone',
        'Solar Panel',
        'Engine',
        'Laser Beam',
        'Microchip',
        'Dish Antenna',
        'Rocket',
        ],
}

EMOTION = [
    'Embarassed',
    'Anger',
    'Timid, Bashful',
    'Giggle, Smiling',
    'Squint, Wink',
    'Bored',
    'Stressed, Fatigued',
    'Fear',
    'Thought',
    'Meditation',
    'Deadpan',
    'Insane, Berserker',
    'Insane, Happy',
    'Pining, Furrowed',
    'Laughing, Hysterical',
    'Attentive, Shock',
    'Stern, Grumpy',
    'Clenched Teeth',
    'Gape, Gawk',
    'Relief',
    'Sneering',
    'Paranoid, Shifty',
    'Bliss, Joy',
    'Confusion',
]

ACTION = [
    'Recoil, Akimbo',
    'Drenched, Thirst',
    'Blown by Cyclone',
    'Push, Pull',
    'Snoop, Listen',
    'Crouched for Attack',
    'Hang, Climb',
    'Recoil, Head/Torso',
    'Float, Levitate',
    'Swinging Weapon',
    'Twisting, Stretching',
    'Kicking, Punching',
    'Squeeze, Tackle',
    'Absorb, Eat',
    'Limp, Injured',
    'Curse, Swear',
    'Run, Jump',
    'Melt, Glow, Fire',
    'Stuck, Trapped',
    'Pull, Push',
    'Shoot Weapon',
    'Dying, Gaunt',
    'Fly, Swim',
    'Shed, Molting',
    'Chant, Recite',
    'Punch, Kick',
    'Crawl, Emerge',
]

def selector(set_):
    '''Make a random selection from a set'''
    list_key = choice(set_.keys())
    list_ = set_[list_key]
    return list_key, choice(list_)


def main():
    '''Select from sets, output nicely'''
    print 'Major:'
    print '  Anima: %s/%s' % selector(ANIMA)
    print '  Veggie: %s/%s' % selector(VEGGIE)
    print '  Elemental & Mineral: %s/%s' % selector(ELEMENTAL_AND_MINERAL)
    print '  Techne: %s/%s' % selector(TECHNE)

    print 'Minor:'
    print '  Anima: %s/%s' % selector(ANIMA)
    print '  Veggie: %s/%s' % selector(VEGGIE)
    print '  Elemental & Mineral: %s/%s' % selector(ELEMENTAL_AND_MINERAL)
    print '  Techne: %s/%s' % selector(TECHNE)
    print
    print 'If necessary:'
    print '  Emotion: %s' % choice(EMOTION)

    print '  Action: %s' % choice(ACTION)

if __name__ == '__main__':
    main()
