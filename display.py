from blessed import Terminal
from colors import *
import os

from art import *

import re

import parser

from PIL import Image

import random

color_map ="""                                                                                
                                                                                
                                                                                
                               00   00000   00                                  
                            00000000000000000000000000                          
                            000000000000000000000000000                         
                          0000000000000000000000000000000                       
                    00000000000000000000000000000000000                          
                  000000000000000000000000000000000000000                       
                  000000000000000000000000000000000000000                       
                    0000000000000000000000000000000000000                       
                       0000000000000000000001100000000000                       
                       0000000000000000000001100000000000                       
                    00000000000000001100772211111   00                          
                       00000000000111111772211111                               
                         00000000011111111111111111                             
                          00000000111111111111111111                            
                          44444441111111111111111                               
                       44444444333331111111111133344                            
                       44444444443333333333333333344                            
                       44444444433333333333333333344                            
                       44444444433333333333333333344                            
                       44444444433333333333333333344                            
                       44444444433333333333333333344                            
                       4444444443333333333333311111111                          
                       1111111113333333333331111111111                          
                       1111111111133333333331111111111                          
                       1111111111133333333333311111111                          
                          11111155555555555555555555                            
                          55555555555555555555555555                            
                               555555555555555555                               
                            555555555555555555555                               
                            555555555555555555555                               
                            555555555555555555555                               
                            555555555555666655555666                            
                            555555555555666655555666                            
                             55555555555666655555666                            
                                                                                
                                                                                """

class Display:
    def __init__(self):
        self.character = character.splitlines()
        self.color_map = color_map.splitlines()
        self.term = Terminal()
        self.sprite_atlas = Image.open("./images/items.png")

    def visible_length(self,s):
        ansi_escape = re.compile(r'\033\[[0-9;]*m')
        return len(ansi_escape.sub('', s))
    
    def display_name(self,text):
        result = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)
        return result

    def find_player_files(self):
        """Searches for .plr files in the user's Terraria player directory."""
        documents_folder = os.path.join(os.path.expanduser("~"), "Documents")
        terraria_player_folder = os.path.join(documents_folder, "My Games", "Terraria", "Players")
        tmodloader_player_folder = os.path.join(documents_folder, "My Games", "Terraria", "tModLoader", "Players")
        if not os.path.exists(terraria_player_folder):
            print("Terraria player folder not found!")
            return []

        return [os.path.join(terraria_player_folder, f) for f in os.listdir(terraria_player_folder) if f.endswith(".plr") or f.endswith(".bak")] + [
                os.path.join(tmodloader_player_folder, f) for f in os.listdir(tmodloader_player_folder) if f.endswith(".plr") or f.endswith(".bak")
            ]

    def render_select_player(self):
        """Renders the .plr file selection menu and returns the selected file path."""
        player_files = self.find_player_files()
        if not player_files:
            print("No .plr files found!")
            return None

        index = 0
        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            while True:
                print(self.term.clear())
                print(logo)
                for i, file in enumerate(player_files):
                    file_name = os.path.basename(file)
                    if i == index:
                        print(self.term.move(5+i,45) + self.term.reverse(f"> {file_name}{CRED2}{' This file is a backup file do not edit it if not needed!' if file_name.endswith('.bak') else ''}{CEND}"))
                    else:
                        print(self.term.move(5+i,45) + f"  {file_name}")

                key = self.term.inkey()
                if key.name == "KEY_UP":
                    index = (index - 1) % len(player_files)
                elif key.name == "KEY_DOWN":
                    index = (index + 1) % len(player_files)
                elif key.name == "KEY_ENTER" or key == "\n":
                    return player_files[index]

    def print_instructions(self, content, x, y):
        box_width = 62
        padding = 2
        content_width = box_width - 2 * padding - 2
        
        content += ' ' * (content_width - self.visible_length(content))

        print(self.term.move(y - 3, x-5) + f"╭{'─' * (box_width - 2)}╮")

        padded_content = f"{' ' * padding}{content}{' ' * padding}"
        print(self.term.move(y - 2, x-5) + f"│{padded_content}│")

        print(self.term.move(y - 1, x-5) + f"╰{'─' * (box_width - 2)}╯")
        
    def render(self, parsed_data):
        print(self.term.clear())
        current_item_index = 0
        items_per_page = len(self.character) - 15

        items = ["inventory","armor","bank","dye","miscEquips","miscDyes"]
        item_colors = [CBLUE,CGREY,CVIOLET2,CRED2,CYELLOW2,CBEIGE2]
        selected_item = 0
        with self.term.fullscreen(), self.term.hidden_cursor(),self.term.cbreak():
            clothing = ["hairColor", "skinColor", "eyeColor", "shirtColor", "underShirtColor", "pantsColor", "shoeColor"]
            for i, line in enumerate(self.character):
                for ii, c in enumerate(line):
                    color_index = self.color_map[i][ii]
                    if color_index.isnumeric() and int(color_index) < len(clothing):
                        color = parsed_data[clothing[int(color_index)]]
                    else:
                        color = {"r": 255, "g": 255, "b": 255}
                    r, g, b = color['r'], color['g'], color['b']
                    print(self.term.move(i+3, ii) + self.term.color_rgb(r,g,b) + c + self.term.normal)
            info_box_x = len(self.character[0]) + 2
            current_y = 2
            print(self.term.move(current_y, info_box_x) + f"╭─ Stats {'─' * 42}╮")
            print(self.term.move(current_y + 1, info_box_x) + f"│ {parsed_data['name']:48} │")
            print(self.term.move(current_y + 2, info_box_x) + f"│ {parsed_data['playTime']:48} │")
            
            health_text = (CRED2+'❤'+CEND) * (parsed_data['maxHealth'] // 20)
            padding = 48 - self.visible_length(health_text)
            health_text = f"{health_text}{' ' * padding}"

            print(self.term.move(current_y + 3, info_box_x) + f"│ {health_text} │")

            mana_text = (CBLUE2+'★'+CEND) * (parsed_data['maxMana'] // 20)
            padding = 48 - self.visible_length(mana_text)
            mana_text = f"{mana_text}{' ' * padding}"
            print(self.term.move(current_y + 4, info_box_x) + f"│ {mana_text} │")
            print(self.term.move(current_y + 5, info_box_x) + f"╰{'─' * 50}╯")
            
            buffs_box_width = 50 
            current_y += 7
            print(self.term.move(current_y, info_box_x) + f"╭─ Buffs {'─' * (buffs_box_width - 8)}╮")
            current_y += 1

            for buff in parsed_data["buffs"]:
                if buff.type == 0:
                    continue
                buff_text = f"{self.display_name(buff.name)} - {buff.readable_time}"
                padding = buffs_box_width - 2 - self.visible_length(buff_text)
                buff_text = f"{buff_text}{' ' * padding}"
                print(self.term.move(current_y, info_box_x) + f"│ {buff_text} │")
                current_y += 1

            print(self.term.move(current_y, info_box_x) + f"╰{'─' * (buffs_box_width)}╯")

            instructions = f"{CBLUE2}↑/↓{CEND} Scroll | {CBLUE2}←/→{CEND} Select | {CBLUE2}abc{CEND} Search | {CBLUE2}Q{CEND} Quit | {CBLUE2}S{CEND} Save"
            self.print_instructions(instructions, info_box_x, current_y + 2+items_per_page+6)
            while True:
                selected_items = items[selected_item]
                color = item_colors[selected_item]

                items_box_x = info_box_x
                items_box_y = current_y+2

                for i in range(items_per_page + 2):
                    print(self.term.move(items_box_y + i, items_box_x) + " " * 52)

                print(self.term.move(items_box_y, items_box_x) + f"{color}╭─ {selected_items.capitalize()} {'─' * (50-len(selected_items)-3)}╮{color}")
                for i in range(items_per_page):
                    item_index = current_item_index + i
                    if item_index < len(parsed_data[selected_items]):
                        item = parsed_data[selected_items][item_index]
                        if i == 0:
                            item_text = f"{color}{self.display_name(item.prefix_name)+' ' if item.prefix_name != ''else ''}{self.display_name(item.name)} x{item.stack}{CEND} [{CBLUE2}enter{CEND}] Edit"
                        else:
                            item_text = f"{self.term.color_rgb(item.color.r,item.color.g,item.color.b)}{self.display_name(item.prefix_name)+' ' if item.prefix_name != ''else ''}{self.display_name(item.name)} {CYELLOW2}x{item.stack}{CEND}"

                        padding = 48 - self.visible_length(item_text)
                        item_text = f"{item_text}{' ' * padding}"
                    else:
                        item_text = ""
                        padding = 48 - self.visible_length(item_text)
                        item_text = f"{item_text}{' ' * padding}"
                    print(self.term.move(items_box_y + i + 1, items_box_x) + f"{color}│{CEND} {item_text} {color}│{CEND}")
                print(self.term.move(items_box_y + items_per_page + 1, items_box_x) + f"{color}╰{'─' * 50}╯{CEND}")

                curent_item = parsed_data[selected_items][current_item_index]

                print(self.term.move(items_box_y, items_box_x+59) + f"{color}╭─ {self.display_name(curent_item.name)} {'─' * (40-len(self.display_name(curent_item.name))-3)}╮{color}")
                self.display_sprite(curent_item.netID,items_box_x+60,items_box_y+1,color)
                print(self.term.move(items_box_y+20, items_box_x+59) + f"{color}╰{'─' * 40}╯{CEND}")

                key = self.term.inkey(timeout=None)
                if key.code == self.term.KEY_UP and current_item_index > 0:
                    current_item_index -= 1
                elif key.code == self.term.KEY_DOWN and current_item_index + items_per_page < len(parsed_data[selected_items])-1:
                    current_item_index += 1
                if key.code == self.term.KEY_LEFT and selected_item > 0:
                    current_item_index = 0
                    selected_item -= 1
                elif key.code == self.term.KEY_RIGHT and selected_item < len(items)-1:
                    current_item_index = 0
                    selected_item += 1
                if key == '\r':
                    item = parsed_data[selected_items][current_item_index]
                    
                    prefix_input = self.get_prefix_from_suggestions("prefix", list(parser.prefixToid.keys()), 
                                                                   item.prefix_name, items_box_y, items_box_x, parsed_data,selected_items,current_item_index,
                                                                   color)
                    item.Prefix(parser.prefixToid.get(prefix_input,0))

                    name_input = self.get_name_from_suggestions("name", list(parser.itemToid.keys()), item.name, items_box_y, items_box_x, parsed_data,selected_items,current_item_index,
                                                                   color)
                    item.netDefaults(parser.itemToid.get(name_input,0))

                    stack_input = self.get_stack(items_box_y, items_box_x, parsed_data,selected_items,current_item_index,
                                                                   color)
                    item.stack = stack_input
                elif key == 's':
                    return True
                elif key == 'q':
                    return False

    def get_prefix_from_suggestions(self, field, suggestions, current_value, items_box_y, items_box_x,parsed_data,selected_items,current_item_index,
                                                                   color):
        item = parsed_data[selected_items][current_item_index]
        suggestion_index = 0
        typed_input = item.prefix_name

        while True:
            filtered_suggestions = [sug for sug in suggestions if typed_input.lower() in sug.lower()]

            if not filtered_suggestions:
                filtered_suggestions = [""]

            item_text = f"{CBLINK2}{self.display_name(filtered_suggestions[suggestion_index])+' ' if filtered_suggestions[suggestion_index] != '' else ''}{CEND}{color}{self.display_name(item.name)} x{item.stack}{CEND}"
            padding = 48 - self.visible_length(item_text)
            item_text = f"{item_text}{' ' * padding}"

            
            print(self.term.move(items_box_y - 1, items_box_x) + " "*50)
            print(self.term.move(items_box_y - 1, items_box_x) + f'{color}{"🔎"}{CEND} {typed_input}')
            print(self.term.move(items_box_y + 1, items_box_x) + f"{color}│{CEND} {item_text} {color}│{CEND}")


            key = self.term.inkey()

            if key.code == self.term.KEY_RIGHT:
                suggestion_index = (suggestion_index + 1) % len(filtered_suggestions)
            elif key.code == self.term.KEY_LEFT:
                suggestion_index = (suggestion_index - 1) % len(filtered_suggestions)
            elif key == '\r':
                return filtered_suggestions[suggestion_index]
            elif key == '\x7f':
                typed_input = typed_input[:-1]
            else:
                typed_input += str(key)
            print(self.term.move(items_box_y + 1, items_box_x) + ' ' * 50)
            
    def get_name_from_suggestions(self, field, suggestions, current_value, items_box_y, items_box_x,parsed_data,selected_items,current_item_index,
                                                                   color):
        item = parsed_data[selected_items][current_item_index]
        suggestion_index = 0
        typed_input = item.name

        while True:
            filtered_suggestions = [sug for sug in suggestions if typed_input.lower() in sug.lower()]
            if not filtered_suggestions:
                filtered_suggestions = [""]
            item_text = f"{color}{self.display_name(item.prefix_name)+' ' if item.prefix_name != '' else ''}{CBLINK2}{self.display_name(self.display_name(filtered_suggestions[suggestion_index]))}{CEND}{color} x{item.stack}{CEND}"
            padding = 48 - self.visible_length(item_text)
            item_text = f"{item_text}{' ' * padding}"

            print(self.term.move(items_box_y - 1, items_box_x) + " "*50)
            print(self.term.move(items_box_y - 1, items_box_x) + f'{color}{"🔎"}{CEND} {typed_input}')
            print(self.term.move(items_box_y + 1, items_box_x) + f"{color}│{CEND} {item_text} {color}│{CEND}")
            
            key = self.term.inkey()

            if key.code == self.term.KEY_RIGHT:
                suggestion_index = (suggestion_index + 1) % len(filtered_suggestions)
            elif key.code == self.term.KEY_LEFT:
                suggestion_index = (suggestion_index - 1) % len(filtered_suggestions)
            elif key == '\r':
                return filtered_suggestions[suggestion_index]
            elif key == '\x7f':
                typed_input = typed_input[:-1]
            else:
                typed_input += str(key)

            print(self.term.move(items_box_y + 1, items_box_x) + ' ' * 50)

    def get_stack(self, items_box_y, items_box_x,parsed_data,selected_items,current_item_index,
                                                                   color):
        item = parsed_data[selected_items][current_item_index]
        stack = item.stack
        while True:
            item_text = f"{color}{self.display_name(item.prefix_name)+' ' if item.prefix_name != ''else ''}{self.display_name(item.name)} x{CBLINK2}{stack}{CEND}"
            padding = 48 - self.visible_length(item_text)
            item_text = f"{item_text}{' ' * padding}"
            print(self.term.move(items_box_y - 1, items_box_x) + " "*50)
            print(self.term.move(items_box_y + 1, items_box_x) + f"{color}│{CEND} {item_text} {color}│{CEND}")
            key = self.term.inkey()

            if key.code == self.term.KEY_RIGHT:
                stack += 1
            elif key.code == self.term.KEY_LEFT:
                stack = max(0, stack-1)
            elif key == '\r':
                return stack

    def display_sprite(self, sprite_id, x, y, color,scale=1):
        sprite_width = 40
        sprite_height = 40

        atlas_width, atlas_height = self.sprite_atlas.size
        sprites_per_row = atlas_width // sprite_width
        col = sprite_id % sprites_per_row
        row = sprite_id // sprites_per_row
        sprite = self.sprite_atlas.crop((col * sprite_width, row * sprite_height, (col + 1) * sprite_width, (row + 1) * sprite_height))

        sprite = sprite.resize((int(sprite_width * scale), int(sprite_height * scale*0.5)), Image.ANTIALIAS)

        grayscale_sprite = sprite.convert("L")
        ascii_art = []
        for py in range(grayscale_sprite.height):
            line = []
            for px in range(grayscale_sprite.width):
                pixel_value = grayscale_sprite.getpixel((px, py))
                pixel_color = sprite.getpixel((px, py))
                char = "█" + self.term.color_rgb(pixel_color[0],pixel_color[1],pixel_color[2]) if pixel_value * 10 // 256 != 0 else " "

                line.append((char))
            ascii_art.append(line)
        for row_idx, row in enumerate(ascii_art):
            for col_idx, char in enumerate(row):
                if col_idx == 0:
                    print(self.term.move(y + row_idx, x + col_idx-1) + color+"│"+CEND)
                if col_idx == 39:
                    print(self.term.move(y + row_idx, x + col_idx+1) + color+"│"+CEND)
                print(self.term.move(y + row_idx, x + col_idx) + char)
               