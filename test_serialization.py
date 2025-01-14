import shellphone
import display
import parser

display = display.Display()
selected_file = display.render_select_player()
decrypted_data = shellphone.decrypt_file(selected_file)

p = parser.PlayerParser(decrypted_data)

deserialized = p.deserialize()

for buff in deserialized["buffs"]:
    print(f'{buff.type} - {buff.name} - {buff.time}')

print("-----")
serilalized = p.serialize(deserialized)

p = parser.PlayerParser(serilalized)

deserialized = p.deserialize()

for buff in deserialized["buffs"]:
    print(f'{buff.type} - {buff.name} - {buff.time}')