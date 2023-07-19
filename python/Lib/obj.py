class Obj(object):
    def __init__(self, filename):
        with open(filename, "r") as file:
            self.lines = file.read().splitlines()

        self.vertices = []
        self.texcoords = []
        self.normals = []
        self.faces = []
        for line in self.lines:
            try:
                prefix, values = line.split(" ", 1)
                values = values.lstrip(" ").rstrip(" ")
            except:
                continue

            if prefix == "v":  # Vertices
                self.vertices.append(list(map(float, values.split(" "))))
            elif prefix == "vt":  # Texture Coordinates
                self.texcoords.append(list(map(float, values.split(" "))))
            elif prefix == "vn":  # Normals
                self.normals.append(list(map(float, values.split(" "))))
            elif prefix == "f":  # Faces
                self.faces.append([list(map(int, vert.split("/"))) for vert in values.split(" ")])
