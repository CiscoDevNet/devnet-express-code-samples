#!/usr/bin/env python
"""
Check dCloud instances.

Validate that hosts and services are up and running in the dCloud pod.
darien@sdnessentials.com
"""

from hello_lab import APIC_EM_URL
from hello_lab import check_apic_em
from hello_lab import check_restconf
from hello_lab import RESTCONF_URL
import sys


def main():
    """Main method to validate dCloud connectivity."""
    # Check for reachability to the APIC-EM and CSR1000V RESTCONF URL
    try:
        if check_apic_em(APIC_EM_URL) is not True:
            print("Oh no! The APIC-EM API service is down.")
            print("Try requesting a new dCloud pod.")
        elif check_restconf(RESTCONF_URL) is not True:
            print("Oh no! The CSR1000V RESTCONF service is down.")
            print("Try requesting a new dCloud pod.")
        else:
            print("Awesome! The dCloud pod is ready for your labs!")
    except Exception as e:
        print("Oh no! The hosts in dCloud aren't reachable.")
        print("Try requesting a new dCloud pod.")
        # print(e)


if __name__ == '__main__':
    sys.exit(main())
