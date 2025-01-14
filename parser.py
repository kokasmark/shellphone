import struct
import json
import random

from dataclasses import dataclass

idToitem = {}
itemToid = {}

idTobuff = {}
buffToId = {}

idToprefix = {}
prefixToId = {}

rarities = {}

with open("idToitem.json","r") as f:
    idToitem = json.loads(f.read())

with open("idTobuff.json","r") as f:
    idTobuff = json.loads(f.read())

with open("idToprefix.json","r") as f:
    idToprefix = json.loads(f.read())

with open("rarities.json","r") as f:
    rarities = json.loads(f.read())



@dataclass
class Color:
    r: int
    g: int
    b: int

class ItemRarity:
    # Define colors corresponding to rarity values
    RarityAmber = Color(255, 175, 0)
    RarityTrash = Color(130, 130, 130)
    RarityNormal = Color(255, 255, 255)  # White
    RarityBlue = Color(150, 150, 255)
    RarityGreen = Color(150, 255, 150)
    RarityOrange = Color(255, 200, 150)
    RarityRed = Color(255, 150, 150)
    RarityPink = Color(255, 150, 255)
    RarityPurple = Color(210, 160, 255)
    RarityLime = Color(150, 255, 10)
    RarityYellow = Color(255, 255, 10)
    RarityCyan = Color(5, 200, 255)
    RarityStrongRed = Color(255, 50, 50)
    RarityPurpleStrong = Color(180, 100, 255)

    @staticmethod
    def get_color_by_rarity(rare):
        # Map the 'rare' value to the corresponding color
        rarity_colors = {
            -11: ItemRarity.RarityAmber,
            -1: ItemRarity.RarityTrash,
            0: ItemRarity.RarityNormal,
            1: ItemRarity.RarityBlue,
            2: ItemRarity.RarityGreen,
            3: ItemRarity.RarityOrange,
            4: ItemRarity.RarityRed,
            5: ItemRarity.RarityPink,
            6: ItemRarity.RarityPurple,
            7: ItemRarity.RarityLime,
            8: ItemRarity.RarityYellow,
            9: ItemRarity.RarityCyan,
            10: ItemRarity.RarityStrongRed,
            11: ItemRarity.RarityPurpleStrong
        }

        # Return the color based on the 'rare' value
        return rarity_colors.get(rare, ItemRarity.RarityNormal)

class Item:
    stack = 1
    favorited = False
    name = idToitem[str(0)]
    prefix_name = ""
    color = Color(255,255,255)
    rare = 0
    value = 0
    def __init__(self):
        pass
    
    def netDefaults(self,type):
        try:
            self.name = idToitem[str(type)]
            self.rare = rarities.get(str(type),0)
        except KeyError:
            self.name = "Unknown"

    def prefix(self,type):
        self.calculate_rare(type)
        try:
            self.prefix_name = idToprefix[str(type)]
        except KeyError:
            self.prefix_name = ""
        pass

    def RollAPrefix(self, unifiedRandom, num):
        # Simulate prefix rolling logic, return True or False
        return random.choice([True, False])
    
    
    def calculate_rare(self, prefixWeWant):
        num = prefixWeWant
        num2 = 1.0
        num3 = 1.0
        num4 = 1.0
        num5 = 1.0
        num6 = 1.0
        num7 = 1.0
        num8 = 0
        flag = True

        while flag:
            flag = False
            if num == -1 and random.randint(0, 3) == 0:
                num = 0
            if prefixWeWant < -1:
                num = -1
            if num in [-1, -2, -3] and not self.RollAPrefix(random, num):
                return False
            if prefixWeWant == -3:
                return True
            if prefixWeWant == -1 and random.randint(0, 2) != 0:
                num = 0
            if prefixWeWant == -2 and num == 0:
                num = -1
                flag = True

        num9 = 1.0 * num2 * (2.0 - num4) * (2.0 - num7) * num5 * num3 * num6 * (1.0 + num8 * 0.02)
        
        if num in [62, 69, 73, 77]:
            num9 *= 1.05
        if num in [63, 70, 74, 78, 67]:
            num9 *= 1.1
        if num in [64, 71, 75, 79, 66]:
            num9 *= 1.15
        if num in [65, 72, 76, 80, 68]:
            num9 *= 1.2

        if num9 >= 1.2:
            self.rare += 2
        elif num9 >= 1.05:
            self.rare += 1
        elif num9 <= 0.8:
            self.rare -= 2
        elif num9 <= 0.95:
            self.rare -= 1

        if self.rare > -11:
            if self.rare < -1:
                self.rare = -1
            if self.rare > 11:
                self.rare = 11

        num9 *= num9
        self.value = round(self.value * num9)
        self.prefix = num

        self.color = ItemRarity.get_color_by_rarity(self.rare)
        return self.rare

class Buff:
    type = 0
    name = "None"
    time = 0
    def __init__(self):
        pass
    
    def set_type(self,type):
        self.type = type
        try:
            self.name = idTobuff[str(type)]
        except KeyError:
            self.name = "Unknown"
        pass

    def set_time(self,time):
        time = time
        pass

class PlayerParser:
    def __init__(self, data):
        self.data = data
        self.offset = 0
        self.parsed_bytes = 0

    def read_int32(self):
        value = struct.unpack_from('<i', self.data, self.offset)[0]
        self.offset += 4
        return value

    def read_uint32(self):
        value = struct.unpack_from('<i', self.data, self.offset)[0]
        self.offset += 4
        return value

    def read_uint8(self):
        value = self.data[self.offset]
        self.offset += 1
        return value

    def read_boolean(self):
        value = self.read_uint8() != 0
        return value

    def read_bytes(self, length):
        value = self.data[self.offset:self.offset + length]
        self.offset += length
        return value

    def read_string(self, length=None):
        if length is None:
            length = self.read_uint8()
        value = self.data[self.offset:self.offset + length].decode('utf-8',errors='ignore')
        self.offset += length
        return value

    def read_rgb(self):
        r = self.read_uint8()
        g = self.read_uint8()
        b = self.read_uint8()
        return {'r': r, 'g': g, 'b': b}

    def parse_bits_byte(self, count):
        bits = []
        while count > 0:
            byte = self.read_uint8()  # Read the next byte
            bits.extend([(byte & (1 << i)) != 0 for i in range(8)])  # Append the bits for this byte
            count -= 8  # Decrease the count by 8 (since a byte has 8 bits)
        return bits[:count]  # Slice the result to match the exact requested count if needed
    
    def parse_playtime(self, playTime_bytes):
        playTime_ticks = struct.unpack('<q', playTime_bytes)[0]
        total_seconds = playTime_ticks / 10_000_000

        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        return f"{hours}:{minutes}:{seconds}"
    def skip_bytes(self, length):
        self.offset += length

    def resolve_encoded_data(self, b1, b2):
        return b1 + (256 * b2)
    def parse(self):
        data = {}
        data["version"] = self.read_int32()
        release = data["version"]
        data["magicNumber"] = self.read_string(7)
        data["fileType"] = self.read_uint8()
        data["revision"] = self.read_uint32()
        self.skip_bytes(7)
        data["favorite"] = self.read_boolean()

        if data["version"] < 194 or data["magicNumber"] != "relogic" or data["fileType"] != 3:
            raise ValueError("Player file version is not supported (only 1.3.5.3) or corrupted metadata.")

        data["name"] = self.read_string()
        
        data["difficulty"] = ["Classic", "Mediumcore", "Hardcore", "Journey"][self.read_uint8()]

        data["playTime"] = self.parse_playtime(self.read_bytes(8))
        
        data["hair"] = self.read_int32()
        data["hairDye"] = self.read_uint8()
        data["hideVisual"] = self.parse_bits_byte(10)
        data["hideMisc"] = self.parse_bits_byte(8)
        data["skinVariant"] = self.read_uint8()
        
        data["health"] = self.read_int32()
        data["maxHealth"] = self.read_int32()
        data["mana"] = self.read_int32()
        data["maxMana"] = self.read_int32()
        
        data["extraAccessory"] = self.read_boolean()
        data["unlockedBiomeTorches"] = self.read_boolean()
        data["unsingBiomeTorches"] = self.read_boolean()
        data["ateArtisanBread"] = self.read_boolean() if release >= 256 else None
        data["usedAegisCrystal"] = self.read_boolean() if release >= 260 else None
        data["usedAegisFruit"] = self.read_boolean() if release >= 260 else None
        data["usedArcaneCrystal"] = self.read_boolean() if release >= 260 else None
        data["usedGalaxyPearl"] = self.read_boolean() if release >= 260 else None
        data["usedGummyWorm"] = self.read_boolean() if release >= 260 else None
        data["usedAmbrosia"] = self.read_boolean() if release >= 260 else None

        data["downedDD2EventAnyDifficulty"] = self.read_boolean() if release >= 182 else None
        data["taxMoney"] = self.read_int32() if release >= 128 else None
        data["numberOfDeathsPVE"] = self.read_int32() if release >= 254 else None
        data["numberOfDeathsPVP"] = self.read_int32() if release >= 254 else None

        data["hairColor"] = self.read_rgb()
        data["skinColor"] = self.read_rgb()
        data["eyeColor"] = self.read_rgb()
        data["shirtColor"] = self.read_rgb()
        data["underShirtColor"] = self.read_rgb()
        data["pantsColor"] = self.read_rgb()
        data["shoeColor"] = self.read_rgb()
        
        data["armor"] = []
        for i in range(20):
            item = Item()
            item.netDefaults(self.read_int32())
            item.prefix(self.read_uint8())
            data["armor"].append(item)

        data["dye"] = []
        for i in range(10):
            item = Item()
            item.netDefaults(self.read_int32())
            item.prefix(self.read_uint8())
            data["dye"].append(item)

        data["inventory"] = []

        for i in range(58):
            id = self.read_int32()

            if id >= 5456:
                item = Item()
                item.netDefaults(0)
                item.prefix(0)
                data["inventory"].append(item)
                self.read_int32()
                self.read_uint8()

                if release > 114:
                    self.read_boolean()
            else:
                item = Item()
                item.netDefaults(id)
                item.stack = self.read_int32()
                item.prefix(self.read_uint8())

                if release >= 114:
                    item.favorited = self.read_boolean()

                data["inventory"].append(item)

        data["miscEquips"] = []
        data["miscDyes"] = []

        for num12 in range(5):
            num13 = self.read_int32()
            item_equips = Item()
            if num13 >= 5456:
                item_equips.netDefaults(0)
                self.read_uint8()
            else:
                item_equips.netDefaults(num13)
                item_equips.prefix(self.read_uint8())
            data["miscEquips"].append(item_equips)

            num13 = self.read_int32()
            item_dyes = Item()
            if num13 >= 5456:
                item_dyes.netDefaults(0)
                self.read_uint8()
            else:
                item_dyes.netDefaults(num13)
                item_dyes.prefix(self.read_uint8())
            data["miscDyes"].append(item_dyes)

        if release >= 58:
            data["bank"] = []
            for i in range(40):
                item = Item()
                item.netDefaults(self.read_int32())
                item.stack = self.read_int32()
                item.prefix(self.read_uint8())
                data["bank"].append(item)
            
            for i in range(40):
                item = Item()
                item.netDefaults(self.read_int32())
                item.stack = self.read_int32()
                item.prefix(self.read_uint8())
                data["bank"].append(item)
            
            if release >= 182:
                for i in range(40):
                    item = Item()
                    item.netDefaults(self.read_int32())
                    item.stack = self.read_int32()
                    item.prefix(self.read_uint8())
                    data["bank"].append(item)

            if release >= 198:
                for i in range(40):
                    item = Item()
                    item.netDefaults(self.read_int32())
                    item.stack = self.read_int32()
                    item.prefix(self.read_uint8())
                    if release >= 255:
                        item.favorited = self.read_boolean()
                    data["bank"].append(item)

            if release >= 199:
                data["voidVaultInfo"] = self.read_uint8()

        if release >= 11:
            num27 = 22
            if release < 74:
                num27 = 10
            if release >= 252:
                num27 = 44

            data["buffs"] = []
            for num28 in range(num27):
                buff = Buff()
                buff.set_type(self.read_int32())
                buff.set_time(self.read_int32())

                if buff.type == 0:
                    num28 -= 1
                    num27 -= 1
                else:
                    data["buffs"].append(buff)

        self.parsed_bytes = self.offset
        return data
