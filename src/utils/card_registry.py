import random
from collections import Counter
from game_objects.card_definitions.amplifier import Amplifier
from game_objects.card_definitions.archive import Archive
from game_objects.card_definitions.battleaxe import BattleAxe
from game_objects.card_definitions.bricklayer import Bricklayer
from game_objects.card_definitions.bulwark import Bulwark
from game_objects.card_definitions.decoy_server import DecoyServer
from game_objects.card_definitions.defensive_nanobots import DefensiveNanobots
from game_objects.card_definitions.defensive_spikes import DefensiveSpikes
from game_objects.card_definitions.fireball import Fireball
from game_objects.card_definitions.halberd import Halberd
from game_objects.card_definitions.lance import Lance
from game_objects.card_definitions.mod_extender import ModExtender
from game_objects.card_definitions.modular_polearm import ModularPolearm
from game_objects.card_definitions.multitasking import Multitasking
from game_objects.card_definitions.neural_interface import NeuralInterface
from game_objects.card_definitions.overclock import Overclock
from game_objects.card_definitions.patch import Patch
from game_objects.card_definitions.payload_extender import PayloadExtender
from game_objects.card_definitions.popup_ad import PopupAd
from game_objects.card_definitions.power_mod import PowerMod
from game_objects.card_definitions.query import Query
from game_objects.card_definitions.remote_miner import RemoteMiner
from game_objects.card_definitions.sandbox import Sandbox
from game_objects.card_definitions.security_group import SecurityGroup
from game_objects.card_definitions.shiv import Shiv
from game_objects.card_definitions.spike import Spike
from game_objects.card_definitions.super_amplifier import SuperAmplifier
from game_objects.card_definitions.vector_extender import VectorExtender


card_list = [
    Amplifier,
    Archive,
    BattleAxe,
    Bricklayer,
    Bulwark,
    DecoyServer,
    DefensiveSpikes,
    DefensiveNanobots,
    Fireball,
    Halberd,
    Lance,
    ModExtender,
    ModularPolearm,
    Multitasking,
    NeuralInterface,
    Overclock,
    Patch,
    PayloadExtender,
    PopupAd,
    PowerMod,
    Query,
    RemoteMiner,
    Sandbox,
    SecurityGroup,
    Shiv,
    Spike,
    SuperAmplifier,
    VectorExtender,
]

card_registry = {}
for card_def in card_list:
    card_registry[card_def.id] = card_def


def get_new_card(name):
    if name not in card_registry:
        raise KeyError(f'Card "{name}" not found in card registry.')

    return card_registry[name]()

def get_card_stats():
    rarity = Counter()
    types = Counter()
    both = Counter()
    for card in card_registry.values():
        rarity[card.rarity] += 1
        types[card.type] += 1
        both[f'{card.type} - {card.rarity}'] += 1
    return rarity


def random_card_choices(count):
    available_cards = [c for c in list(card_registry.values()) if c.rarity in ['simple', 'intermediate', 'elite']]
    card_sample = random.sample(available_cards, count)
    return [c() for c in card_sample]
