from blessed import Terminal
from colors import *
import os

from art import *

import re

import parser

from PIL import Image


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
                          00000000111111111111111                            
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
        self.render_image = True

    def visible_length(self,s):
        ansi_escape = re.compile(r'\033\[[0-9;]*m')
        return len(ansi_escape.sub('', s))
    
    def display_name(self,text):
        result = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', text)
        return result


    def render_player_select(self, player_files, parsers):
        deserialized_data = []
        for parser in parsers:
            deserialized_data.append(parser.deserialized)
        index = 0
        visible_count = 3

        def draw_rounded_box(x, y, width, height, border_color, inner_color=None):
            for i in range(height):
                for j in range(width):
                    if i == 0 and j == 0:
                        char = "╭"
                    elif i == 0 and j == width - 1:
                        char = "╮"
                    elif i == height - 1 and j == 0:
                        char = "╰"
                    elif i == height - 1 and j == width - 1:
                        char = "╯"
                    elif i == 0 or i == height - 1:
                        char = "─"
                    elif j == 0 or j == width - 1:
                        char = "│"
                    else:
                        char = " "
                    color = border_color if char != " " else inner_color
                    if color:
                        print(self.term.move(y + i, x + j) + color + char + self.term.normal)


        with self.term.fullscreen(), self.term.cbreak(), self.term.hidden_cursor():
            while True:
                print(self.term.clear())
                start = index
                end = min(index + visible_count, len(deserialized_data))

                for i, data in enumerate(deserialized_data[start:end]):
                    x = i * 80 
                    y = 3

                    self.render_player(data, x, y)
                    name = data.get("name", "Unknown")
                    name_box_width = len(name) + 4
                    name_box_x = x + 40 - name_box_width // 2
                    name_box_y = y + 38
                    draw_rounded_box(name_box_x, name_box_y, name_box_width, 3, self.term.color_rgb(200, 200, 200))
                    print(self.term.move(name_box_y + 1, name_box_x + 2) + name)

                draw_rounded_box(15, 1, 45, 45, self.term.color_rgb(255, 255, 255))
                instructions = f"{CBLUE2}←/→{CEND} Cycle | {CBLUE2}enter{CEND} Select"
                self.print_instructions(instructions, 15+5, 50)
                key = self.term.inkey(timeout=None)
                if key.name == "KEY_LEFT":
                    index = max(index - 1, 0)
                elif key.name == "KEY_RIGHT":
                    index = min(index + 1, len(deserialized_data))
                elif key.name == "KEY_ENTER" or key == "\n":
                    return (parsers[index],player_files[index])
                elif key.name == "KEY_ESCAPE":
                    return None

    def print_instructions(self, content, x, y):
        box_width = self.visible_length(content)+6
        padding = 2
        content_width = box_width - 2 * padding - 2
        
        content += ' ' * (content_width - self.visible_length(content))

        print(self.term.move(y - 3, x-5) + f"╭{'─' * (box_width - 2)}╮")

        padded_content = f"{' ' * padding}{content}{' ' * padding}"
        print(self.term.move(y - 2, x-5) + f"│{padded_content}│")

        print(self.term.move(y - 1, x-5) + f"╰{'─' * (box_width - 2)}╯")
    
    def render_player(self, parsed_data, x, y):
        clothing = ["hairColor", "skinColor", "eyeColor", "shirtColor", "underShirtColor", "pantsColor", "shoeColor"]

        for i, line in enumerate(self.character):
            buffer = ""
            for ii, c in enumerate(line):
                color_index = self.color_map[i][ii]
                if color_index.isnumeric() and int(color_index) < len(clothing):
                    color = parsed_data[clothing[int(color_index)]]
                else:
                    color = {"r": 255, "g": 255, "b": 255}
                
                shading_factor = (1 - (ii / len(line))) + 0.2
                r = int(color['r'] * shading_factor)
                g = int(color['g'] * shading_factor)
                b = int(color['b'] * shading_factor)

                buffer += self.term.color_rgb(r, g, b) + c + self.term.normal

            print(self.term.move(i + y, x) + buffer)


    def render(self, parsed_data):
        print(self.term.clear())
        current_item_index = 0
        items_per_page = len(self.character) - 15

        items = ["inventory","armor","bank","dye","miscEquips","miscDyes"]
        item_colors = [CBLUE,CGREY,CVIOLET2,CRED2,CYELLOW2,CBEIGE2]
        selected_item = 0
        with self.term.fullscreen(), self.term.hidden_cursor(),self.term.cbreak():

            self.render_player(parsed_data,0,3)

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

            instructions = f"{CBLUE2}↑/↓{CEND} Scroll | {CBLUE2}←/→{CEND} Select | {CBLUE2}I{CEND} Item preview | {CBLUE2}abc{CEND} Search | {CBLUE2}Q{CEND} Quit | {CBLUE2}S{CEND} Save"
            self.print_instructions(instructions, info_box_x+5, current_y + 2+items_per_page+6)
            while True:
                selected_items = items[selected_item]
                color = item_colors[selected_item]

                items_box_x = info_box_x
                items_box_y = current_y+2

                for i in range(items_per_page + 2):
                    print(self.term.move(items_box_y + i, items_box_x) + " " * 102)

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

                if self.render_image:
                    print(self.term.move(items_box_y, items_box_x+59-5) + f"{color}╭─ {self.display_name(curent_item.name)} {'─' * (40-len(self.display_name(curent_item.name))-3)}╮{color}")
                    self.display_sprite(curent_item.netID,items_box_x+60-5,items_box_y+1,color)
                    print(self.term.move(items_box_y+20, items_box_x+59-5) + f"{color}╰{'─' * 40}╯{CEND}")

                key = self.term.inkey(timeout=None)
                if key.code == self.term.KEY_UP and current_item_index > 0:
                    current_item_index -= 1
                elif key.code == self.term.KEY_DOWN and current_item_index < len(parsed_data[selected_items])-1:
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
                elif key == 'i':
                    self.render_image = not self.render_image
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

    def prepare_sprite(self,sprite_id):
        sprite_width = 40
        sprite_height = 40

        atlas_width, atlas_height = self.sprite_atlas.size
        sprites_per_row = atlas_width // sprite_width
        col = sprite_id % sprites_per_row
        row = sprite_id // sprites_per_row
        sprite = self.sprite_atlas.crop((col * sprite_width, row * sprite_height, (col + 1) * sprite_width, (row + 1) * sprite_height))
        return sprite.resize((int(sprite_width), int(sprite_height *0.5)), Image.ANTIALIAS)
    
    def display_sprite(self, sprite_id, x, y, color):
        sprite = self.prepare_sprite(sprite_id)
        grayscale_sprite = sprite.convert("L")
        ascii_art = []

        for py in range(grayscale_sprite.height):
            line = f"{self.term.move(y + py, x - 1)}{color}│{CEND}"
            for px in range(grayscale_sprite.width):
                pixel_value = grayscale_sprite.getpixel((px, py))
                pixel_color = sprite.getpixel((px, py))
                char = "█" + self.term.color_rgb(pixel_color[0], pixel_color[1], pixel_color[2]) if pixel_value * 10 // 256 != 0 else " "
                line += char
            line += f"{color}│{CEND}"
            ascii_art.append(line)

        for row in ascii_art:
            print(row)

               