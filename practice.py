import copy
from components.fretboard import Fretboard
from components.key import KeyBuilder
from components.permutation import select_permutation

if __name__ == "__main__":
    fboard = Fretboard()
    k = KeyBuilder()

    # Get fretboard in a key/scale
    start_fret = input("Starting fret (Enter for 0): ")
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

    perm = input("Permutation (Enter for random): ")
    if not perm:
        perm = select_permutation(seq_range=4)
    
    print(f"Practice Sequence: {'-'.join(perm)}")
    tab_sequence = fretboard_sliced.parse_pattern_seq(pattern=perm)
    
    fretboard_sliced.start_interactive_tab_sequence(tab_sequence)