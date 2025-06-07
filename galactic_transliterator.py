#!/usr/bin/env python3

language_map = {
    'ENGLISH_TO_SURZHYK': {
        'a': "а", 'b': "б", 'd': "д", 'e': "е", 'f': "ф", 'g': "г", "g'": "ґ",
        'h': "х", 'i': "и", 'yi': 'ї', 'j': "й", 'k': "к", 'l': "л", 'm': "м",
        'n': "н", 'o': "о", 'p': "п", 'r': "р", 's': "с", 't': "т", 'u': "у",
        'v': "в", 'y': "ы", 'z': "з", '#': 'ъ', 'yo': 'ё', 'je': 'є',
        'zh': 'ж', 'ch': 'ч', 'sh': 'ш', 'shch': 'щ', 'ye': 'э', 'yu': 'ю',
        'ya': 'я', "'": 'ь', "ts": "ц", "tsya": 'тся',

        'w': 'у', 'c': 'к', 'x': 'кс', 'q': 'ку', "ph": 'ф', 'kn': 'н', 'oo': 'у'
    },
    'SURZHYK_TO_ENGLISH': {
        'а': 'a', 'б': 'b', 'д': 'd', 'е': 'e', 'ф': 'f', 'г': 'g', 'ґ': "g'",
        'х': 'h', 'и': 'i', 'ї': 'yi', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'в': 'v', 'ы': 'y', 'з': 'z', 'ъ': '#', 'ё': 'yo', 'є': 'je', 'ж': 'zh',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'э': 'ye', 'ю': 'yu', 'я': 'ya',
        'ь': "'", 'ц': 'ts', 'тся': 'tsya'
    },
    'ENGLISH_TO_GALACTIC': {
        'a': "ᔑ", 'b': "ʖ", 'c': "ᓵ", 'd': "↸", 'e': "ᒷ", 'f': "⎓", 'g': "⊣",
        'h': "⍑", 'i': "╎", 'j': "⋮", 'k': "ꖌ", 'l': "ꖎ", 'm': "ᒲ", 'n': "リ",
        'o': "𝙹", 'p': "!¡", 'q': "ᑑ", 'r': "∷", 's': "ᓭ", 't': "ℸ", 'u': "⚍",
        'v': "⍊", 'w': "∴", 'x': "̇/", 'y': "||", 'z': "⨅"
    }
}

def transliterate(translated_text, mode):
    translated_text = translated_text.lower()

    global language_map
    if not mode in language_map:
        source_language, target_language = mode.split('_TO_')
        reversed_mode = f"{target_language}_TO_{source_language}"
        language_map[mode] = {value:key for key, value in language_map[reversed_mode].items()}

    _map = language_map[mode]

    for key in sorted(_map.keys(), key=len, reverse=True):
        translated_text = translated_text.replace(key, _map[key])
    
    return translated_text

# UI beyond this point

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()
    root.title("Galactic Transliterator 🪐")
    root.geometry("600x450")
    root.minsize(350, 250)
    root.resizable(True, True)

    root.grid_columnconfigure(1, weight=1)
    for i in range(3):
        root.grid_rowconfigure(i, weight=1)

    def make_text_area(parent):
        frame = tk.Frame(parent)
        frame.grid(sticky='nsew')

        text = tk.Text(frame, wrap='word', undo=True)
        text.grid(row=0, column=0, sticky='nsew')

        scrollbar = tk.Scrollbar(frame, command=text.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')

        text.config(yscrollcommand=scrollbar.set)

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        return frame, text

    english_label = tk.Label(root, text="English")
    english_label.grid(row=0, column=0, padx=10, pady=10, sticky='n')
    english_frame, english_input = make_text_area(root)
    english_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

    surzhyk_label = tk.Label(root, text="Surzhyk")
    surzhyk_label.grid(row=1, column=0, padx=10, pady=10, sticky='n')
    surzhyk_frame, surzhyk_input = make_text_area(root)
    surzhyk_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

    galactic_label = tk.Label(root, text="Galactic")
    galactic_label.grid(row=2, column=0, padx=10, pady=10, sticky='n')
    galactic_frame, galactic_input = make_text_area(root)
    galactic_frame.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')

    # UI Functionality

    def read_field(input):
        return input.get("1.0", tk.END).strip()

    def update_field(input, text):
        input.delete("1.0", tk.END)
        input.insert(tk.END, text)

    def auto_transliterate(event):
        if event.widget == surzhyk_input:
            surzhyk_text = read_field(surzhyk_input)
            update_field(
                english_input,
                transliterate(surzhyk_text, mode='SURZHYK_TO_ENGLISH')
            )
            english_text = read_field(english_input)
            update_field(
                galactic_input,
                transliterate(english_text, mode='ENGLISH_TO_GALACTIC')
            )
        elif event.widget == english_input:
            english_text = read_field(english_input)
            update_field(
                galactic_input,
                transliterate(english_text, mode='ENGLISH_TO_GALACTIC')
            )
            update_field(
                surzhyk_input,
                transliterate(english_text, mode='ENGLISH_TO_SURZHYK')
            )
        elif event.widget == galactic_input:
            galactic_text = read_field(galactic_input)
            update_field(
                english_input,
                transliterate(galactic_text, mode='GALACTIC_TO_ENGLISH')
            )
            english_text = read_field(english_input)
            update_field(
                surzhyk_input,
                transliterate(english_text, mode='ENGLISH_TO_SURZHYK')
            )

    def select_all(event):
        event.widget.tag_add("sel", "1.0", "end-1c")
        return "break"
    
    def custom_paste(event):
        _input = event.widget
        try:
            sel_start = _input.index("sel.first")
            sel_end = _input.index("sel.last")
            full_text = _input.get("1.0", "end-1c")
            selected_text = _input.get(sel_start, sel_end)

            if selected_text == full_text:
                _input.delete("1.0", "end")
                clipboard_text = root.clipboard_get()
                _input.insert("1.0", clipboard_text)
        except:
            clipboard_text = root.clipboard_get()
            _input.insert(tk.INSERT, clipboard_text)
        return "break"

    surzhyk_input.bind("<KeyRelease>", auto_transliterate)
    english_input.bind("<KeyRelease>", auto_transliterate)
    galactic_input.bind("<KeyRelease>", auto_transliterate)

    surzhyk_input.bind("<FocusIn>", auto_transliterate)
    english_input.bind("<FocusIn>", auto_transliterate)
    galactic_input.bind("<FocusIn>", auto_transliterate)
    
    surzhyk_input.bind("<Control-a>", select_all)
    english_input.bind("<Control-a>", select_all)
    galactic_input.bind("<Control-a>", select_all)

    surzhyk_input.bind("<Control-v>", custom_paste)
    english_input.bind("<Control-v>", custom_paste)
    galactic_input.bind("<Control-v>", custom_paste)

    surzhyk_input.bind("<Control-z>", lambda e: surzhyk_input.edit_undo())
    english_input.bind("<Control-z>", lambda e: english_input.edit_undo())
    galactic_input.bind("<Control-z>", lambda e: galactic_input.edit_undo())
    
    surzhyk_input.focus_set()

    root.mainloop()
