"""Module for SNMP connections. The two variants return
either a single variable list (snmp_binds), or the entire
table for that OID (snmp_table).
"""

import pysnmp.error
from pysnmp.entity.rfc3413.oneliner import cmdgen


def snmp_binds(switch, config, oid_var):
    """Returns a single variable list for requested OID."""
    try:
        auth = cmdgen.CommunityData(config["comm_string"])
        cmd = cmdgen.CommandGenerator()
        error_indication, error_status, error_index, varbinds = cmd.getCmd(
            auth,
            cmdgen.UdpTransportTarget((switch, 161)),
            cmdgen.MibVariable(oid_var),
            lookupMib=False,
        )

        if error_indication:
            print(f"something went wrong while connecting to {switch}")
            return "", False

        return varbinds, True

    except pysnmp.error.PySnmpError:
        print(f"Something went wrong with {switch}'s SNMP poll")
        return "", False






def snmp_table(switch, config, oid_var):
    """Returns entire table for requested OID."""

    try:
        auth = cmdgen.CommunityData(config["comm_string"])
        cmd = cmdgen.CommandGenerator()
        error_indication, error_status, error_index, vartable = cmd.nextCmd(
            auth,
            cmdgen.UdpTransportTarget((switch, 161)),
            cmdgen.MibVariable(oid_var),
            lookupMib=False,
        )

        if error_indication:
            print(f"something went wrong while connecting to {switch}")
            return "", False

        return vartable, True

    except pysnmp.error.PySnmpError:
        print(f"Something went wrong with {switch}'s SNMP poll")
        return "", False
