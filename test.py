import copy
from components.fretboard import Fretboard
from components.key import KeyBuilder

if __name__ == "__main__":
    fboard = Fretboard()
    k = KeyBuilder()

    key = k.get_key("G#", "harmonic-minor")
    print("Key:", "-".join(key))

    key_fretboard = fboard.copy_in_key(key)
    print("Full Fretboard")
    print(key_fretboard)
    
    print("Full Fret Numbers")
    print(key_fretboard.visualize_tabs())

    key_fretboard_sliced = key_fretboard.copy_slice(0, 5)

    print("Sliced Fretboard")
    print(key_fretboard_sliced)
    
    print("Sliced Fret Numbers")
    print(key_fretboard_sliced.visualize_tabs())

    tab_sequence = key_fretboard_sliced.parse_pattern_seq(pattern="0321")
    
    print("Practice Sequence")
    print(key_fretboard_sliced.visualize_tab_sequence(tab_sequence))
