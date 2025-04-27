import random
import time

blues_progression = [
    ("C2", "E2", "G2", "A2"),  # I chord
    ("F2", "A2", "C3", "D3"),  # IV chord
    ("G2", "B2", "D3", "E3")   # V chord
]

note_map = {
    "C2": 36, "E2": 40, "G2": 43, "A2": 45,
    "F2": 41, "A2": 45, "C3": 48, "D3": 50,
    "G2": 43, "B2": 47, "D3": 50, "E3": 52
}