# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class VertexRecordEntry:
    def __init__(self, entry_string):
        entry_string_split = entry_string.split(',')
        self.id = entry_string_split[0]

        coordinates = (entry_string_split[1].replace("\"(", ""), entry_string_split[2].replace(")\"", ""))
        self.coordinates = (int(coordinates[0]), int(coordinates[1]))

        self.incident_edge = entry_string_split[3]

    def setup_pointers(self, hedge_records):
        for hedge_record in hedge_records:
            if hedge_record.id == self.incident_edge:
                self.incident_edge = hedge_record
                break


class FaceRecordEntry:
    def __init__(self, entry_string):
        entry_string_split = entry_string.split(',')
        self.id = entry_string_split[0]
        self.outer_component = entry_string_split[1]

    def setup_pointers(self, hedge_records):
        for hedge_record in hedge_records:
            if hedge_record.id == self.outer_component:
                self.outer_component = hedge_record
                break


class HalfEdgeRecordEntry:
    def __init__(self, entry_string):
        entry_string_split = entry_string.split(',')
        self.id = entry_string_split[0]
        self.origin = entry_string_split[1]
        self.twin = entry_string_split[2]
        self.incident_face = entry_string_split[3]
        self.next = entry_string_split[4]
        self.previous = entry_string_split[5]

    def setup_pointers(self, vertex_records, face_records, half_edge_records):
        for v_record in vertex_records:
            if v_record.id == self.origin:
                self.origin = v_record
                break
        for f_record in face_records:
            if f_record.id == self.incident_face:
                self.incident_face = f_record
                break
        for he_record in half_edge_records:
            if he_record.id == self.twin:
                self.twin = he_record
            if he_record.id == self.next:
                self.next = he_record
            if he_record.id == self.previous:
                self.previous = he_record


# Read the input record
# Returns a list of record entries of the specified type
def read_input_csv(input_file, entry_class):

    output_entries = []

    with open(input_file, 'r') as f:

        # read all the lines and get rid of the column names
        input_lines = f.readlines()
        input_lines = input_lines[1:]

        # add to vertex entry list
        for input_line in input_lines:
            if entry_class == VertexRecordEntry.__name__:
                output_entries.append(VertexRecordEntry(input_line.strip()))
            if entry_class == FaceRecordEntry.__name__:
                output_entries.append(FaceRecordEntry(input_line.strip()))
            if entry_class == HalfEdgeRecordEntry.__name__:
                output_entries.append(HalfEdgeRecordEntry(input_line.strip()))

    # Pass back the list of input segments
    return output_entries


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Input filenames
    vertex_filename = "VertexRecord.csv"
    face_filename = "FaceRecord.csv"
    hedge_filename = "HalfEdgeRecord.csv"

    # Initialize the three DCEL records
    print("Reading " + vertex_filename + "...")
    print("Reading " + face_filename + "...")
    print("Reading " + hedge_filename + "...")
    vertex_record = read_input_csv(vertex_filename, VertexRecordEntry.__name__)
    face_record = read_input_csv(face_filename, FaceRecordEntry.__name__)
    half_edge_record = read_input_csv(hedge_filename, HalfEdgeRecordEntry.__name__)
    print("Done reading input")

    # Now set up the necessary pointers in the DCEL structures
    for vertex in vertex_record:
        vertex.setup_pointers(half_edge_record)
    for face in face_record:
        face.setup_pointers(half_edge_record)
    for hedge in half_edge_record:
        hedge.setup_pointers(vertex_record, face_record, half_edge_record)
    print("Done setting up pointers")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
