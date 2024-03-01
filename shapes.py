import copy
from components.fretboard import Fretboard
from components.key import KeyBuilder
from components.permutation import select_permutation

if __name__ == "__main__":
    start_fret = input("Starting fret (Enter for 0): ")
    while start_fret != 'stop':
        fboard = Fretboard()
        k = KeyBuilder()

        # Get fretboard in a key/scale
        if start_fret:
            fretboard_sliced = fboard.copy_slice(int(start_fret), 4)
        else:
            fretboard_sliced = fboard.copy_slice(0, 5)
        
        # Get fretboard in a key/scale
        key_note = input("Key Note (Enter for None): ")
        if key_note:
            scale = input("Scale (Enter to list): ")
            while not scale:
                print(" | ".join(KeyBuilder.key_maps.keys()))
                scale = input("Scale (Enter to list): ")
            key = k.get_key(key_note, scale)
            fretboard_sliced = fretboard_sliced.copy_in_key(key)
            print(fretboard_sliced)
            print(fretboard_sliced.visualize_tabs())

        start_fret = input("Starting fret (Enter for 0): ")