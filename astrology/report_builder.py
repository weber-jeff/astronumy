class AstrologyReportBuilder:
    def __init__(self, data):
        self.data = data

    def build(self):
        return f"Sun: {self.data['Sun']}\nMoon: {self.data['Moon']}"
