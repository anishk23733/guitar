import copy
from components.fretboard import Fretboard
from components.key import KeyBuilder
from components.permutation import select_permutation

if __name__ == "__main__":
    fboard = Fretboard()
    k = KeyBuilder()
    output_str = ""

    fretboard_sliced = fboard.copy_slice(0, 5)
    output_str += fretboard_sliced.visualize_tabs() + '\n'
    perm = select_permutation(seq_range=5)
    output_str += f"Practice Sequence: {'-'.join(perm)}\n"
    tab_sequence = fretboard_sliced.parse_pattern_seq(pattern=perm)
    output_str += fretboard_sliced.visualize_tab_sequence(tab_sequence) + "\n"

    for note in KeyBuilder.notes:
        for scale in ["major", "minor", "harmonic-minor"]:
            key = k.get_key(note, "harmonic-minor")
            output_str += (f"Key {note} {scale}\n")
            key_fretboard = fboard.copy_in_key(key)
            key_fretboard_sliced = key_fretboard.copy_slice(0, 5)
            output_str += key_fretboard_sliced.visualize_tabs() + '\n'

            perm = select_permutation(seq_range=5)
            output_str += f"Practice Sequence: {'-'.join(perm)}\n"
            tab_sequence = key_fretboard_sliced.parse_pattern_seq(pattern=perm)
            output_str += key_fretboard_sliced.visualize_tab_sequence(tab_sequence) + "\n"
    
    with open("doc.txt", "w") as f:
        f.write(output_str)
