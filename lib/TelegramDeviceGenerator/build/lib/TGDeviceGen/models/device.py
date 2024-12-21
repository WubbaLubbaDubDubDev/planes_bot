class Device:
    def __init__(self, model: str, android_versions: list,  performance_class: str):
        self.model = model
        self.android_versions = android_versions
        self.performance_class = performance_class
