import json

class Guild:
    @classmethod
    def read(cls, id):
        try:
            with open(f"data/{id}.json", mode="r") as f:
                data = json.loads(f.read())
        except e:
            raise e
        return cls(data["name"], data["author_id"], data["id"], data["members"])

    def __init__(self, name, author_id, id, members):
        self.name = name
        self.author_id = author_id
        self.id = id
        self.members = members

    def add_member(self, member_id):
        if member_id not in self.members:
            self.members.append(member_id)
        return self

    def store(self):
        data = json.dumps({"members": self.members, "author_id": self.author_id, "id": self.id, "name": self.name})
        with open(f"data/{self.id}.json", mode="w") as f:
            f.write(data)

class GuildTemplate:

    def __init__(self, name, author_id, id):
        self.name = name
        self.author_id = author_id
        self.id = id
        self.members = []

    def add_member(self, member_id):
        if member_id not in self.members:
            self.members.append(member_id)
        return self

    def create(self):
        return Guild(self.name, self.author_id, self.id, self.members)
