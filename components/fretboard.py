import copy
from components.key import KeyBuilder

from components.audio import AudioAnalyzer, frequency_to_note_name
from components.queue import ProtectedList
import time
import sys

class Fretboard():
    strings = ["E", "A", "D", "G", "B", "E"]
    num_frets = 22 + 1

    def fix_string_for_grid(c):
        if len(c) == 1:
            return f'-{c}'
        return c

    def __init__(self, fretboard:list=None, startfret:int=0, lenboard:int=23):
        if fretboard:
            self.fretboard = fretboard
            self.startfret = startfret
            self.len_fret_board = lenboard
        else:
            self.fretboard = []

            for string in self.strings:
                curr = string
                string_frets = []
                for i in range(self.num_frets):
                    string_frets.append(curr)
                    curr = KeyBuilder.next_note(curr)
                self.fretboard.append(string_frets)
            
            self.startfret = 0
            self.len_fret_board = self.num_frets

    def __str__(self):
        len_fret_board = len(self.fretboard[0]) # length of first string == length of all
        return_str = ""
        return_str += ("--".join(map(Fretboard.fix_string_for_grid, 
                            map(str, range(self.startfret, self.startfret + self.len_fret_board)))))
        return_str += "\n"
        for string_frets in self.fretboard[::-1]:
            return_str += ("--".join(map(Fretboard.fix_string_for_grid, string_frets)))
            return_str += "\n"
        return return_str
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self):
        return self.len_fret_board
    
    def copy_in_key(self, key):
        new_fretboard = copy.deepcopy(self.fretboard)
        for string_ in new_fretboard:
            for i in range(len(string_)):
                if string_[i] not in key:
                    string_[i] = "--"
        return Fretboard(new_fretboard, self.startfret, self.len_fret_board)

    def copy_slice(self, start=0, length=num_frets):
        new_fretboard = []
        for string in self.fretboard:
            actual_len = len(string[start:start+length])
            if actual_len < length:
                length = actual_len
            new_fretboard.append(string[start:start+length])
        return Fretboard(new_fretboard, self.startfret + start, length)

    def parse_tabs(self):
        tabs_in_key = []
        for i, string in enumerate(self.fretboard):
            string_tabs = []
            for j, note in enumerate(string):
                if note != "--":
                    string_tabs.append((i, self.startfret + j))
            tabs_in_key.append(string_tabs)
        
        self.tabs = tabs_in_key
        self.flattened_tabs = tabs_in_key[0]
        
        for next_tab in tabs_in_key[1:]:
            self.flattened_tabs.extend(next_tab)
        self.total_tabs = len(self.flattened_tabs)

    def parse_pattern_seq(self, pattern="012", ascending=True, descending=True):
        self.parse_tabs()

        # seq_len = max(len(pattern), max([int(c) + 1 for c in pattern]))
        seq_len = max([int(c) + 1 for c in pattern])

        scale = []
        if ascending:
            scale += self.flattened_tabs
        if descending:
            scale += self.flattened_tabs[::-1]

        tab_sequence = []
        for i in range(len(scale)-(seq_len-1)):
            window = scale[i:i+seq_len]
            if seq_len == 1:
                tab_sequence.append(scale[i])
            else:
                for c in pattern:
                    tab_sequence.append(window[int(c)])
        
        return tab_sequence

    def visualize_tab_sequence(self, tab_sequence, length=24):
        output_str = ""
        for i in range(0, len(tab_sequence), length):
            strings_str = [f"{s}|-" for s in Fretboard.strings]
            actual_notes_covered = len(tab_sequence[i:i+length])
            for tab in tab_sequence[i:i+length]:
                string_index, fret = tab
                for j in range(len(strings_str)):
                    if j == string_index:
                        strings_str[j] += Fretboard.fix_string_for_grid(str(fret)) + '-'
                    else:
                        strings_str[j] += "---"

            if length > actual_notes_covered:
                for i in range(length - actual_notes_covered):
                    for i in range(len(strings_str)):
                        strings_str[i] += "---"

            for string in strings_str[::-1]:
                output_str += (f"{string}|\n")
            output_str += "\n"
        
        return output_str

    def start_interactive_tab_sequence(self, tab_sequence, length=24):
        q = ProtectedList()
        a = AudioAnalyzer(q)
        a.start()

        for i in range(0, len(tab_sequence), length):
            strings_str = [f"{s}|-" for s in Fretboard.strings]
            num_actual_notes_covered = len(tab_sequence[i:i+length])
            actual_notes_covered = tab_sequence[i:i+length]
            for tab in tab_sequence[i:i+length]:
                string_index, fret = tab
                for j in range(len(strings_str)):
                    if j == string_index:
                        strings_str[j] += Fretboard.fix_string_for_grid(str(fret)) + '-'
                    else:
                        strings_str[j] += "---"
            if length > num_actual_notes_covered:
                for i in range(length - num_actual_notes_covered):
                    for i in range(len(strings_str)):
                        strings_str[i] += "---"

            for string in strings_str[::-1]:
                print(f"{string}|")
            notes_required = [self.fretboard[note[0]][note[1] - self.startfret] for note in actual_notes_covered]
            sys.stdout.write("X|-")
            sys.stdout.flush()
            while notes_required:
                note_required = notes_required[0]
                q_data = q.get()
                if q_data is not None and q_data > 80:
                    note = frequency_to_note_name(q_data, 440)
                    if note != note_required:
                        continue
                    else:
                        sys.stdout.write("-X-")
                        sys.stdout.flush()
                        notes_required.pop(0)
                time.sleep(0.02)
            if length > num_actual_notes_covered:
                for i in range(length - num_actual_notes_covered):
                    sys.stdout.write("---")
            sys.stdout.write("|\n")
            sys.stdout.flush()
            print()
        
        a.stop()

    def visualize_tabs(self):
        output_str = ""
        strings_str = [f"{s}|-" for s in Fretboard.strings]
        for i in range(0, self.len_fret_board):
            for j in range(len(Fretboard.strings)):
                if self.fretboard[j][i] != "--":
                    strings_str[j] += Fretboard.fix_string_for_grid(str(i + self.startfret)) + '-'
                else:
                    strings_str[j] += '---'

        for string in strings_str[::-1]:
            output_str += (f"{string}|\n")
        return output_str

