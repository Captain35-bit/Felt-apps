import flet as ft
from datetime import datetime
import json
import os

class MyNotebook:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "My Notebook & Dictionary"
        self.page.window_width = 1200
        self.page.window_height = 800
        
        self.notes = []
        self.dictionary = {}
        self.current_note_index = None
        self.notes_file = "notes.json"
        self.dictionary_file = "dictionary.json"
        
        self.setup_ui()
        self.load_notes()
        self.load_dictionary()
        
    def setup_ui(self):
        """Setup the user interface with tabs"""
        
        # Notebook Tab
        notebook_tab = self.create_notebook_tab()
        
        # Dictionary Tab
        dictionary_tab = self.create_dictionary_tab()
        
        # Tab view
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="📓 Notebook",
                    content=notebook_tab,
                ),
                ft.Tab(
                    text="📚 Dictionary",
                    content=dictionary_tab,
                ),
            ],
            expand=True,
        )
        
        self.page.add(tabs)
        
    def create_notebook_tab(self):
        """Create the notebook tab"""
        
        # Title
        title = ft.Text(
            "📓 My Notebook",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_600
        )
        
        # Note list
        self.notes_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
        )
        
        # Text editor
        self.note_title_input = ft.TextField(
            label="Note Title",
            width=400,
            border_radius=8,
        )
        
        self.note_content_input = ft.TextField(
            label="Note Content",
            multiline=True,
            min_lines=8,
            width=400,
            border_radius=8,
        )
        
        # Buttons
        save_btn = ft.ElevatedButton(
            "Save Note",
            on_click=self.save_note,
            bgcolor=ft.colors.GREEN_600,
            color=ft.colors.WHITE,
            width=150,
        )
        
        new_btn = ft.ElevatedButton(
            "New Note",
            on_click=self.new_note,
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE,
            width=150,
        )
        
        delete_btn = ft.ElevatedButton(
            "Delete Note",
            on_click=self.delete_note,
            bgcolor=ft.colors.RED_600,
            color=ft.colors.WHITE,
            width=150,
        )
        
        # Button row
        button_row = ft.Row(
            controls=[new_btn, save_btn, delete_btn],
            spacing=10,
        )
        
        # Layout: Left panel (notes list) and right panel (editor)
        left_panel = ft.Container(
            content=self.notes_list,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
            width=300,
            height=600,
        )
        
        editor_column = ft.Column(
            controls=[
                self.note_title_input,
                self.note_content_input,
                button_row,
            ],
            spacing=10,
            width=400,
        )
        
        main_row = ft.Row(
            controls=[left_panel, editor_column],
            spacing=20,
            expand=True,
        )
        
        # Main container
        return ft.Container(
            content=ft.Column(
                controls=[
                    title,
                    main_row,
                ],
                spacing=20,
                expand=True,
            ),
            padding=20,
        )
    
    def create_dictionary_tab(self):
        """Create the dictionary tab"""
        
        # Title
        title = ft.Text(
            "📚 My Dictionary",
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.PURPLE_600
        )
        
        # Dictionary list
        self.dictionary_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
        )
        
        # Word input
        self.word_input = ft.TextField(
            label="Word",
            width=400,
            border_radius=8,
        )
        
        # Definition input
        self.definition_input = ft.TextField(
            label="Definition",
            multiline=True,
            min_lines=6,
            width=400,
            border_radius=8,
        )
        
        # Buttons
        add_word_btn = ft.ElevatedButton(
            "Add Word",
            on_click=self.add_word,
            bgcolor=ft.colors.GREEN_600,
            color=ft.colors.WHITE,
            width=150,
        )
        
        clear_btn = ft.ElevatedButton(
            "Clear",
            on_click=self.clear_dictionary_form,
            bgcolor=ft.colors.ORANGE_600,
            color=ft.colors.WHITE,
            width=150,
        )
        
        delete_word_btn = ft.ElevatedButton(
            "Delete Word",
            on_click=self.delete_word,
            bgcolor=ft.colors.RED_600,
            color=ft.colors.WHITE,
            width=150,
        )
        
        # Button row
        button_row = ft.Row(
            controls=[add_word_btn, clear_btn, delete_word_btn],
            spacing=10,
        )
        
        # Layout: Left panel (word list) and right panel (editor)
        left_panel = ft.Container(
            content=self.dictionary_list,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
            width=300,
            height=600,
        )
        
        editor_column = ft.Column(
            controls=[
                self.word_input,
                self.definition_input,
                button_row,
            ],
            spacing=10,
            width=400,
        )
        
        main_row = ft.Row(
            controls=[left_panel, editor_column],
            spacing=20,
            expand=True,
        )
        
        self.selected_word = None
        
        # Main container
        return ft.Container(
            content=ft.Column(
                controls=[
                    title,
                    main_row,
                ],
                spacing=20,
                expand=True,
            ),
            padding=20,
        )
    
    # ============ NOTEBOOK METHODS ============
    
    def load_notes(self):
        """Load notes from file"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, "r") as f:
                    self.notes = json.load(f)
                self.refresh_notes_list()
        except Exception as e:
            print(f"Error loading notes: {e}")
    
    def save_notes(self):
        """Save notes to file"""
        try:
            with open(self.notes_file, "w") as f:
                json.dump(self.notes, f, indent=2)
        except Exception as e:
            print(f"Error saving notes: {e}")
    
    def refresh_notes_list(self):
        """Refresh the notes list display"""
        self.notes_list.controls.clear()
        for i, note in enumerate(self.notes):
            note_item = ft.ListTile(
                title=ft.Text(note.get("title", "Untitled")),
                subtitle=ft.Text(note.get("timestamp", "")),
                on_click=lambda e, idx=i: self.select_note(idx),
            )
            self.notes_list.controls.append(note_item)
        self.page.update()
    
    def select_note(self, index):
        """Select a note to edit"""
        self.current_note_index = index
        note = self.notes[index]
        self.note_title_input.value = note.get("title", "")
        self.note_content_input.value = note.get("content", "")
        self.page.update()
    
    def new_note(self, e):
        """Create a new note"""
        self.current_note_index = None
        self.note_title_input.value = ""
        self.note_content_input.value = ""
        self.page.update()
    
    def save_note(self, e):
        """Save the current note"""
        title = self.note_title_input.value.strip()
        content = self.note_content_input.value.strip()
        
        if not title or not content:
            self.show_message("Please enter both title and content")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if self.current_note_index is not None:
            # Update existing note
            self.notes[self.current_note_index] = {
                "title": title,
                "content": content,
                "timestamp": timestamp,
            }
        else:
            # Create new note
            self.notes.append({
                "title": title,
                "content": content,
                "timestamp": timestamp,
            })
        
        self.save_notes()
        self.refresh_notes_list()
        self.show_message("Note saved successfully!")
        self.new_note(None)
    
    def delete_note(self, e):
        """Delete the current note"""
        if self.current_note_index is not None:
            del self.notes[self.current_note_index]
            self.save_notes()
            self.refresh_notes_list()
            self.show_message("Note deleted!")
            self.new_note(None)
        else:
            self.show_message("Please select a note to delete")
    
    # ============ DICTIONARY METHODS ============
    
    def load_dictionary(self):
        """Load dictionary from file"""
        try:
            if os.path.exists(self.dictionary_file):
                with open(self.dictionary_file, "r") as f:
                    self.dictionary = json.load(f)
                self.refresh_dictionary_list()
        except Exception as e:
            print(f"Error loading dictionary: {e}")
    
    def save_dictionary(self):
        """Save dictionary to file"""
        try:
            with open(self.dictionary_file, "w") as f:
                json.dump(self.dictionary, f, indent=2)
        except Exception as e:
            print(f"Error saving dictionary: {e}")
    
    def refresh_dictionary_list(self):
        """Refresh the dictionary list display"""
        self.dictionary_list.controls.clear()
        for word in sorted(self.dictionary.keys()):
            word_item = ft.ListTile(
                title=ft.Text(word, weight=ft.FontWeight.BOLD),
                subtitle=ft.Text(self.dictionary[word][:100] + "..." if len(self.dictionary[word]) > 100 else self.dictionary[word]),
                on_click=lambda e, w=word: self.select_word(w),
            )
            self.dictionary_list.controls.append(word_item)
        self.page.update()
    
    def select_word(self, word):
        """Select a word to edit"""
        self.selected_word = word
        self.word_input.value = word
        self.definition_input.value = self.dictionary[word]
        self.page.update()
    
    def add_word(self, e):
        """Add or update a word in the dictionary"""
        word = self.word_input.value.strip().lower()
        definition = self.definition_input.value.strip()
        
        if not word or not definition:
            self.show_message("Please enter both word and definition")
            return
        
        if self.selected_word and self.selected_word != word:
            # If changing the word, delete the old one
            del self.dictionary[self.selected_word]
        
        self.dictionary[word] = definition
        self.save_dictionary()
        self.refresh_dictionary_list()
        self.show_message(f"Word '{word}' saved successfully!")
        self.clear_dictionary_form(None)
    
    def delete_word(self, e):
        """Delete a word from the dictionary"""
        if self.selected_word and self.selected_word in self.dictionary:
            del self.dictionary[self.selected_word]
            self.save_dictionary()
            self.refresh_dictionary_list()
            self.show_message(f"Word '{self.selected_word}' deleted!")
            self.clear_dictionary_form(None)
        else:
            self.show_message("Please select a word to delete")
    
    def clear_dictionary_form(self, e):
        """Clear the dictionary form"""
        self.selected_word = None
        self.word_input.value = ""
        self.definition_input.value = ""
        self.page.update()
    
    # ============ UTILITY METHODS ============
    
    def show_message(self, message):
        """Show a temporary message"""
        snack = ft.SnackBar(ft.Text(message))
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()


def main(page: ft.Page):
    app = MyNotebook(page)


if __name__ == "__main__":
    ft.app(target=main)
