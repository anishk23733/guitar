class KeyBuilder():
    notes = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    key_maps = {
        "major": 'WWHWWWH',
        "ionian": 'WWHWWWH',

        "minor":'WHWWHWW',
        "natural-minor": 'WHWWHWW',
        "aeolian": 'WHWWHWW',

        "harmonic-minor": 'WHWWHWH',

        "dorian": 'WHWWWHW',
        "phrygian": 'HWWWHWW',
        "lydian": "WWWHWWH",
        "mixolydian": "WWHWWHW",
        "locrian": "HWWHWWW"
    }
    # static function
    def next_note(note):
        i = KeyBuilder.notes.index(note) + 1
        if i >= len(KeyBuilder.notes):
            i = 0
        return KeyBuilder.notes[i]

    def build_key(self, note, key_formula):
        key = [note]
        curr = note
        for f in key_formula:
            if f == "W":
                curr = KeyBuilder.next_note(KeyBuilder.next_note(curr))
                key.append(curr)
            elif f == "H":
                curr = KeyBuilder.next_note(curr)
                key.append(curr)
        return key

    def get_key(self, note, key_name):
        key_name = key_name.lower()
        return self.build_key(note, self.key_maps.get(key_name))