class AbstractResource:
    def __init__(self, name, materials):
        self.name = name

        material_names = []
        for material in materials:
            material_names.append(str(material()))
        self.materials = material_names
