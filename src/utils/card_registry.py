import random
from collections import Counter

from src.game_objects.card_definitions.amplifier import Amplifier
from src.game_objects.card_definitions.archive import Archive
from src.game_objects.card_definitions.battleaxe import BattleAxe
from src.game_objects.card_definitions.bricklayer import Bricklayer
from src.game_objects.card_definitions.bulwark import Bulwark
from src.game_objects.card_definitions.decoy_server import DecoyServer
from src.game_objects.card_definitions.defensive_nanobots import DefensiveNanobots
from src.game_objects.card_definitions.defensive_spikes import DefensiveSpikes
from src.game_objects.card_definitions.desync import Desync
from src.game_objects.card_definitions.encryption import Encryption
from src.game_objects.card_definitions.fireball import Fireball
from src.game_objects.card_definitions.firewall import Firewall
from src.game_objects.card_definitions.hackjob import Hackjob
from src.game_objects.card_definitions.halberd import Halberd
from src.game_objects.card_definitions.lance import Lance
from src.game_objects.card_definitions.mod_extender import ModExtender
from src.game_objects.card_definitions.modular_polearm import ModularPolearm
from src.game_objects.card_definitions.monitoring import Monitoring
from src.game_objects.card_definitions.multitasking import Multitasking
from src.game_objects.card_definitions.neural_interface import NeuralInterface
from src.game_objects.card_definitions.overcharge import Overcharge
from src.game_objects.card_definitions.overclock import Overclock
from src.game_objects.card_definitions.override import Override
from src.game_objects.card_definitions.patch import Patch
from src.game_objects.card_definitions.payload_extender import PayloadExtender
from src.game_objects.card_definitions.popup_ad import PopupAd
from src.game_objects.card_definitions.power_mod import PowerMod
from src.game_objects.card_definitions.query import Query
from src.game_objects.card_definitions.remote_miner import RemoteMiner
from src.game_objects.card_definitions.sandbox import Sandbox
from src.game_objects.card_definitions.security_group import SecurityGroup
from src.game_objects.card_definitions.shiv import Shiv
from src.game_objects.card_definitions.shovelware import Shovelware
from src.game_objects.card_definitions.signal_enhancement import SignalEnhancement
from src.game_objects.card_definitions.spam import Spam
from src.game_objects.card_definitions.spike import Spike
from src.game_objects.card_definitions.super_amplifier import SuperAmplifier
from src.game_objects.card_definitions.vector_extender import VectorExtender


card_list = [
    Amplifier,
    Archive,
    BattleAxe,
    Bricklayer,
    Bulwark,
    DecoyServer,
    DefensiveSpikes,
    DefensiveNanobots,
    Desync,
    Encryption,
    Fireball,
    Firewall,
    Hackjob,
    Halberd,
    Lance,
    ModExtender,
    ModularPolearm,
    # Monitoring,   # Temporarily removed due to bugs in implementation
    Multitasking,
    NeuralInterface,
    Overcharge,
    Overclock,
    Override,
    Patch,
    PayloadExtender,
    PopupAd,
    PowerMod,
    Query,
    RemoteMiner,
    Sandbox,
    SecurityGroup,
    Shiv,
    Shovelware,
    SignalEnhancement,
    Spam,
    Spike,
    SuperAmplifier,
    VectorExtender
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
    weight_map = {
        'simple': 4,
        'intermediate': 2,
        'elite': 1,
        'built-in': 0,
        'special': 0
    }

    card_options = random.choices(
        list(card_registry.values()),
        weights=[weight_map[c.rarity] for c in card_registry.values()],
        k=count)

    return [c() for c in card_options]
