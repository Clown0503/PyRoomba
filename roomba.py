#!/usr/bin/env python

from RoombaSCI import RoombaAPI
import sys

def usage():
    print "Syntax: %s <order 1> [<order 2> [<order3> [...]]]" % sys.argv[0]
    print "Possible orders are:"
    print "\tclean : Start cleaning the room you lazy robot !"
    print "\tdock : Ok, forget it, you're making more crap than you're cleaning"
    print "\toff : OMG, stop breaking things ! right now !"

if __name__ == "__main__":
    if len(sys.argv) <= 1 or "-h" in sys.argv or "--help" in sys.argv:
        usage()
        sys.exit(2)

    sys.stdout.write("Connecting to the Rootooth ... ")
    sys.stdout.flush()
    roomba = RoombaAPI("/dev/rfcomm0", 115200);
    sys.stdout.write("OK\n")

    try:
        sys.stdout.write("Rootooth version: ")
        sys.stdout.flush()
        sys.stdout.write(roomba.rootoothVersion + "\n")

        sys.stdout.write("Connecting to the Roomba ... ")
        sys.stdout.flush()
        roomba.connect()
        sys.stdout.write("OK\n")
        sys.stdout.flush()

        print "Sending orders:";
        orders = sys.argv[1:] 
        for order in orders:
            print "- %s" % order
            if order == "clean":
                roomba.clean()
            elif order == "dock":
                roomba.dock()
            elif order == "off":
                roomba.off()
            else:
                usage()
                sys.exit(2)
        print "Done"
    finally:
        roomba.close()

    sys.exit(0)

