import copy
from components.fretboard import Fretboard
from components.key import KeyBuilder

fboard = Fretboard()
key_fretboard = fboard.copy_in_key(["C", 'E', "G"]).copy_slice(0, 5)
print(key_fretboard)
