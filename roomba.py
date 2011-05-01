#!/usr/bin/env python

from RoombaSCI import RoombaAPI
import os
import sys

# the full picture
ROOMBA = "\
                OOOOOOO                \n\
            OOOOOOOOOOOOOOO            \n\
         OOOOO           OOOOO         \n\
       OOOOO               OOOOO       \n\
     OOOO     OOOOOOOOOOO      OOOO    \n\
   OOOO    OOOOO       OOOOO    OOOO   \n\
  OOOO   OOO               OOO   OOOO  \n\
 OOOO   OO       OOOOO       OO   OOOO \n\
 OOO   OO     OOOOOOOOOOO     OO   OOO \n\
OOO    OO    OOOOOOOOOOOOO    OO    OOO\n\
OOO         OOOOOOO_OOOOOOO         OOO\n\
OOO  I=I   OOOOOOO/ \OOOOOOO   I=I  OOO\n\
OOO  I=I   OOOOOO|   |OOOOOO   I=I  OOO\n\
OOO  I=I   OOOOOOO\_/OOOOOOO   I=I  OOO\n\
OOO  I=I   OOOOOOOOOOOOOOOOO   I=I  OOO\n\
OOO  I=I    OOOOOOOOOOOOOOO    I=I  OOO\n\
 OOO          OOOOOOOOOOO          OOO \n\
  OOO            OOOOO            OOO  \n\
   OOO                           OOO   \n\
    OOO                         OOO    \n\
     OOOO                     OOOO     \n\
      OOOOO       OOO       OOOOO      \n\
         OOOOOOOOOOOOOOOOOOOOO         \n\
              OOOOOOOOOOO              \n\
".split("\n")

TOP_LINES = range(0, 4)
MIDDLETOP_LINES = range(4, 5)
SUBTOP_LINES = range(5, 9)
MIDDLE_LINES = range(9, 11)
WHEEL_LINES = range(11, 16)
WHEEL_ASCII = "I=I"
BOTTOM_LINES = range(16, 24)

class AsciiRoombaStaticLines:
    def __init__(self, lines_nb):
        self.piece = []
        for line_nb in lines_nb:
            self.piece.append("%20s%s" % ("", ROOMBA[line_nb]))

    def construct(self, sensors = None, ansi = False):
        pass

class AsciiRoombaWall:
    def __init__(self):
        self.piece = []

    def construct(self, sensors, ansi = False):
        if sensors.wall:
            self.piece.append("%20s=============     WALL     =============" % (""))
        if sensors.virtual_wall:
            self.piece.append("%20s------------- VIRTUAL WALL -------------" % (""))
        if len(self.piece) > 0:
            self.piece.append("")

class AsciiRoombaBasicPiece:
    def __init__(self):
        pass

    def construct_clean(self, lines_nb, left_side):
        self.piece = []
        for line_nb in lines_nb:
            line = ROOMBA[line_nb]
            sline = line.strip()
            middle = (len(sline) / 2) + (len(line) - len(sline))
            if left_side:
                line = line[:middle]
            else:
                line = line[middle:]
            self.piece.append(line)

    def add_text(self, left_side, text_lines):
        for i in range(0, len(self.piece)):
            if i < len(text_lines):
                text = text_lines[i]
            else:
                text = ""
            if left_side:
                if i == 0 and text != "":
                    text = "%s --> " % (text)
                else:
                    text = "%s     " % (text)
                self.piece[i] = "%20s%s" % (text, self.piece[i])
            else:
                if i == 0 and text != "":
                    text = " <-- %s" % (text)
                else:
                    text = "     %s" % (text)
                self.piece[i] = "%s%s" % (self.piece[i], text)


class AsciiRoombaTop(AsciiRoombaBasicPiece):
    def __init__(self, left_side):
        self.left_side = left_side

    def construct(self, sensors, ainsi = False):
        AsciiRoombaBasicPiece.construct_clean(self, TOP_LINES, self.left_side)
        if ainsi:
            # TODO
            pass

        status = []
        if self.left_side:
            cliff_status = sensors.cliff.front_left
        else:
            cliff_status = sensors.cliff.front_right
        if cliff_status:
            status.append("Cliff detected !")
        if self.left_side:
            bump_status = sensors.bumps.left
        else:
            bump_status = sensors.bumps.right
        if bump_status:
            status.append("Bump !")

        AsciiRoombaBasicPiece.add_text(self, self.left_side, status)

class AsciiRoombaSubTop(AsciiRoombaBasicPiece):
    def __init__(self, left_side):
        self.left_side = left_side

    def construct(self, sensors, ainsi = False):
        AsciiRoombaBasicPiece.construct_clean(self, SUBTOP_LINES, self.left_side)

        if ainsi:
            # TODO
            pass

        status = []
        if self.left_side:
            cliff_status = sensors.cliff.left
        else:
            cliff_status = sensors.cliff.right
        if cliff_status:
            status.append("Cliff detected !")
        AsciiRoombaBasicPiece.add_text(self, self.left_side, status)


class AsciiRoombaWheel(AsciiRoombaBasicPiece):
    def __init__(self, left_side):
        self.left_side = left_side

    def construct(self, sensors, ansi = False):
        AsciiRoombaBasicPiece.construct_clean(self, WHEEL_LINES, self.left_side)
        if ansi:
            # TODO
            pass

        status = []
        if self.left_side:
            cliff_status = sensors.wheel_drops.left
        else:
            cliff_status = sensors.wheel_drops.right
        if cliff_status:
            status.append("Wheel drop !")
        AsciiRoombaBasicPiece.add_text(self, self.left_side, status)

class AsciiRoombaBattery:
    def __init__(self):
        self.piece = []

    def construct(self, sensors, ansi = False):
        self.piece.append("")
        self.piece.append("Battery: %dmA / %dmA" % (sensors.charge, sensors.capacity))

class AsciiRoomba:
    def __init__(self):
        self.pieces = [
            [ AsciiRoombaWall() ],
            [ AsciiRoombaTop(True), AsciiRoombaTop(False) ],
            [ AsciiRoombaStaticLines(MIDDLETOP_LINES) ],
            [ AsciiRoombaSubTop(True), AsciiRoombaSubTop(False) ],
            [ AsciiRoombaStaticLines(MIDDLE_LINES) ],
            [ AsciiRoombaWheel(True), AsciiRoombaWheel(False) ],
            [ AsciiRoombaStaticLines(BOTTOM_LINES) ],
            [ AsciiRoombaBattery() ],
        ]

    def display(self, sensors):
        ansi = sys.stdout.isatty()

        for pieces_line in self.pieces:

            for piece in pieces_line:
                piece.construct(sensors, ansi)
                nb_lines = len(piece.piece)

            for nb_line in range(nb_lines):
                for piece in pieces_line:
                    sys.stdout.write(piece.piece[nb_line])
                sys.stdout.write("\n")

        sys.stdout.write("\n")
        sys.stdout.flush()

def usage():
    print "Syntax: %s [<options>] <order 1> [<order 2> [<order3> [...]]]" % sys.argv[0]
    print "Possible options are:"
    print "\t-v : verbose"
    print "Possible orders are:"
    print "\tclean : Start cleaning the room you lazy robot !"
    print "\tdock : Ok, forget it, you're making more crap than you're cleaning"
    print "\toff : OMG, stop breaking things ! right now !"
    print "\tstatus : Show me"

if __name__ == "__main__":
    verbose = False

    if len(sys.argv) <= 1 or "-h" in sys.argv or "--help" in sys.argv:
        usage()
        sys.exit(2)
    
    orders = sys.argv[1:]
    if "-v" in orders:
        orders.remove("-v")
        verbose = True

    if verbose:
        sys.stdout.write("Connecting to the Rootooth ... ")
        sys.stdout.flush()
    roomba = RoombaAPI("/dev/rfcomm0", 115200);
    if verbose:
        sys.stdout.write("OK\n")

    try:
        if verbose:
            sys.stdout.write("Rootooth version: ")
            sys.stdout.flush()
            sys.stdout.write(roomba.rootoothVersion + "\n")

        if verbose:
            sys.stdout.write("Connecting to the Roomba ... ")
            sys.stdout.flush()
        roomba.connect()
        if verbose:
            sys.stdout.write("OK\n")
            sys.stdout.flush()

        sensors = None
        if "sensors" in orders or \
           "status" in orders:
            if verbose:
                sys.stdout.write("Loading sensors informations ... ");
                sys.stdout.flush()
            sensors = roomba.sensors
            if verbose:
                sys.stdout.write("OK\n")

        if verbose:
            print "Sending orders:";
        for order in orders:
            if verbose:
                print "- %s" % order
            if order == "clean":
                roomba.clean()
            elif order == "dock":
                roomba.dock()
            elif order == "off":
                roomba.off()
            elif order == "sensors":
                assert(sensors != None)
                print "Battery Charge: %dmA / %dmA" % (sensors.charge, sensors.capacity)
                print "Cliffs:                %-7r | %-7r | %-7r | %-7r" % (
                    sensors.cliff.left,
                    sensors.cliff.front_left,
                    sensors.cliff.front_right,
                    sensors.cliff.right
                )
                print "Wheels drops:                    %-7r | %-7r" % (
                    sensors.wheel_drops.left,
                    sensors.wheel_drops.right
                )
                print "Bumps:                           %-7r | %-7r" % (
                    sensors.bumps.left,
                    sensors.bumps.right
                )
                print "Wall:                                %-7r" % (sensors.wall)
                print "Virtual wall:                        %-7r" % (sensors.virtual_wall)
                print "Battery temperature:              %d Celsius" % (sensors.temperature)
                print "Dirt detector:                   %-7d | %-7d" % (
                    sensors.dirt_detector.left,
                    sensors.dirt_detector.right)
            elif order == "status":
                assert(sensors != None)
                ascii_roomba = AsciiRoomba()
                ascii_roomba.display(sensors)
            else:
                usage()
                sys.exit(2)
            print ""
        if verbose:
            print "Done"
    finally:
        roomba.close()

    sys.exit(0)

