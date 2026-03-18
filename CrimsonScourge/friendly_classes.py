class Human:
    def __init__(self, name, stats, resistences, equipment):
        self.name = name
        self.__stats = stats
        self.__resistences = resistences
        self.equipment = equipment

    def inventory(self, item_dict: dict, carry_cap=6):
        inventory_dict = {}
        open = True
        while open:
            for description, item in item_dict.items():
                inventory_dict[description] = item
            open = False
        return inventory_dict

    def add_to_inv(self, item: dict):
        self.inventory(item)

    def select_from_inv(self, item: str):
        current_inv = self.inventory()

    def equipment(self, weapon: str, head_slot: str, chest_slot: str, boot_slot: str):
        open = True
        while open:
            print("You have equipped:")
            print(f"""
            Weapon: {weapon}
            Head: {head_slot}
            Chest: {chest_slot}
            Boots: {boot_slot}
            """)
            await_input = input("""
            Change equiped: Type 'Weapon'/'Head'/'Chest'/'Boots'
            Type 'close' to close equipment view...
            """)
            match await_input:
                case "Weapon":
                    self.inventory(await_input)
                case "Head":
                    self.inventory(await_input)
                case "Chest":
                    self.inventory(await_input)
                case "Boots":
                    self.inventory(await_input)
