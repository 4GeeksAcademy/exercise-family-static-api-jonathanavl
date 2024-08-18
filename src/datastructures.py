from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

        self.add_member({
            "id": self._generate_id(),
            "first_name": "John",
            "last_name": self.last_name,
            "age": 33,
            "lucky_numbers": [7, 13, 22]
        })
        self.add_member({
            "id": self._generate_id(),
            "first_name": "Jane",
            "last_name": self.last_name,
            "age": 35,
            "lucky_numbers": [10, 14, 3]
        })
        self.add_member({
            "id": self._generate_id(),
            "first_name": "Jimmy",
            "last_name": self.last_name,
            "age": 5,
            "lucky_numbers": [1]
        })

    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        if not all(key in member for key in ("first_name", "age", "lucky_numbers")):
            raise ValueError("Missing fields in member data")
        
        member["id"] = self._generate_id()
        member["last_name"] = self.last_name
        self._members.append(member)

    def delete_member(self, id):
        initial_count = len(self._members)
        self._members = [member for member in self._members if member["id"] != id]
        return len(self._members) < initial_count  

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def get_all_members(self):
        return self._members
