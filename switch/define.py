"""http://kms2.h3c.com/View.aspx?id=40150 """
from switch import base  


ACCESS = (
       (0, 'Access Switch'),
       (1, 'Access Computer'),
       (2, 'Access Other'),
    )

portStatus = (
        (0, 'Other'),
        (1, 'Up'),
        (2, 'Down'),
    )

ipStatus = (
        (0, 'offLine'),
        (1, 'onLine'),
    )
snmpVersion = (
        (1, 'Version 1C'),
        (2, 'Version 2C'),
        (3, 'Version 3C'),
    )

flag = (
        (0, 'NO'),
        (1, 'YES'),
    )

switchStatus = (
        (0, 'offLine'),
        (1, 'onLine'),
)


### swtype from config.cf section
swType = base.get_SwType()



GET_DATA = {
        'enable':1,
        'initPort':2,
        'getMac':4,
        'getIpMac':8,
        'getsysDecr':16,
        'makeDesc':32

        }




processNumber = 20

## days =2
REMOVE_FILE =2


########## get_mac_control#########################
GET_MAC_CONTROL = {
        'standard_getMac' : 1,
        'port_access_check' : 2
}

#########################
MaxMacPortNumber = 3

AllowUpdateDhcplease = 0
AllowUpdateComputer  = 0
