class Memory:
    def __init__(self):
        self.history = []

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

        if len(self.history) > 10:
            self.history.pop(0)

    def get_history(self):
        return self.history
