# To run, use the following command. The input files should be in the same directory as the python file:
# python Wells_Chris_Prob1.py <vertex record filename> <face record filename> <half edge record filename>
# ex. python Wells_Chris_Prob1.py VertexRecord.csv FaceRecord.csv HalfEdgeRecord.csv
# The output will go to std out
import csv
import sys


class VertexRecordEntry:
    def __init__(self, entry_list):
        self.id = entry_list[0]
        self.coordinates = tuple(int(num) for num in entry_list[1].replace('(', '').replace(')', '').split(','))
        self.incident_edge = entry_list[2]

    def setup_pointers(self, hedge_records):
        for hedge_record in hedge_records:
            if hedge_record.id == self.incident_edge:
                self.incident_edge = hedge_record
                break


class FaceRecordEntry:
    def __init__(self, entry_list):
        self.id = entry_list[0]
        if entry_list[1] == "null":
            self.inner_components = None
        else:
            self.inner_components = list(hedge_id for hedge_id in entry_list[1].split(","))
        if entry_list[2] == "null":
            self.outer_component = None
        else:
            self.outer_component = entry_list[2]

    def setup_pointers(self, hedge_records):
        for hedge_record in hedge_records:
            if hedge_record.id == self.outer_component:
                self.outer_component = hedge_record
            if self.inner_components is not None:
                for i in range(0, len(self.inner_components)):
                    if hedge_record.id == self.inner_components[i]:
                        self.inner_components[i] = hedge_record

    def __str__(self):
        return "Face " + self.id


class HalfEdgeRecordEntry:
    def __init__(self, entry_list):
        self.id = entry_list[0]
        self.origin = entry_list[1]
        self.twin = entry_list[2]
        self.incident_face = entry_list[3]
        self.next = entry_list[4]
        self.previous = entry_list[5]

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

    with open(input_file, 'r'):

        # read all the lines and get rid of the column names
        with open(input_file, newline='') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(csvreader, None)

            # now for each row
            for row in csvreader:
                if entry_class == VertexRecordEntry.__name__:
                    output_entries.append(VertexRecordEntry(row))
                if entry_class == FaceRecordEntry.__name__:
                    output_entries.append(FaceRecordEntry(row))
                if entry_class == HalfEdgeRecordEntry.__name__:
                    output_entries.append(HalfEdgeRecordEntry(row))

    # Pass back the list of input segments
    return output_entries


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # The input parameters are the vertex, face, and half edge records in that order
    vertex_filename = sys.argv[1]
    face_filename = sys.argv[2]
    hedge_filename = sys.argv[3]

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

    # Now to solve the problem - initialize the boundary faces list to return
    boundary_faces = set()

    # First, find the unbounded outer face - its OuterComponents should be None
    outer_face = None
    for face in face_record:
        if face.outer_component is None:
            outer_face = face
            break
    if outer_face is not None:
        print("Outer face is " + str(outer_face))

    # Next, go thru the half-edge cycles on each of the boundary face's inner components
    for half_edge in outer_face.inner_components:
        origin = half_edge
        current = origin.next

        # add the twin's incident face to the set of boundary faces
        while current != origin:
            boundary_faces.add(current.twin.incident_face)
            current = current.next

    # Now print the contents of the set
    print("Boundary Faces Output:")
    for boundary_face in list(boundary_faces):
        print(str(boundary_face))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
