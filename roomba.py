#!/usr/bin/env python

from RoombaSCI import RoombaAPI
import sys

def usage():
    print "Syntax: %s [<options>] <order 1> [<order 2> [<order3> [...]]]" % sys.argv[0]
    print "Possible options are:"
    print "\t-v : verbose"
    print "Possible orders are:"
    print "\tclean : Start cleaning the room you lazy robot !"
    print "\tdock : Ok, forget it, you're making more crap than you're cleaning"
    print "\toff : OMG, stop breaking things ! right now !"
    print "\tbattery : Tell me if you can keep working or if I have to flog you"

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
        if "battery" in orders or \
           "sensors" in orders:
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
            elif order == "battery":
                assert(sensors != None)
                print "Charge: %dmA / %dmA" % (sensors.charge, sensors.capacity)
            elif order == "sensors":
                assert(sensors != None)
                print "Cliffs:                %-7r | %-7r | %-7r | %-7r" % (
                    roomba.sensors.cliff.left,
                    roomba.sensors.cliff.front_left,
                    roomba.sensors.cliff.front_right,
                    roomba.sensors.cliff.right
                )
                print "Wheels drops:                    %-7r | %-7r" % (
                    roomba.sensors.wheel_drops.left,
                    roomba.sensors.wheel_drops.right
                )
                print "Bumps:                           %-7r | %-7r" % (
                    roomba.sensors.bumps.left,
                    roomba.sensors.bumps.right
                )
                print "Wall:                                %-7r" % (roomba.sensors.wall)
                print "Virtual wall:                        %-7r" % (roomba.sensors.virtual_wall)
                print "Battery temperature:              %d Celsius" % (roomba.sensors.temperature)


            else:
                usage()
                sys.exit(2)
        if verbose:
            print "Done"
    finally:
        roomba.close()

    sys.exit(0)

