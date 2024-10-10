'''
This script will build out the required CSV file for creating all patching between the rear ports of two patch panels. 

The script will require some information to run, these can be passed are arguments at run-time or if any are missing you'll be prompted by the script to enter them.

apanel [ --apanel ] - String with the Netbox name for the A end patch panel.
bpanel [ --bpanel ] - String with the Netbox name for the B end patch panel.
portcount [ --portcount ] - Int with the number of ports the patch panel has. It assumes both patch panels have the same number of ports and a 1:1 mapping.
porttype [ --porttype ] - String with the type of port the cable will be.

Once completed, the script will export the data to a .csv file using the apanel argument. 

Example usage: python3 usefulScripts/createPPCableing.py --apanel test-pp01 --bpanel test-pp02 --portcount 24 --porttype cat6a 

'''

import csv
import argparse

def setVariables(args):

    if args.apanel != None:
        patchPanelAName = args.apanel
    else:
        patchPanelAName = input('Please entery the A end patch panel name: ')
        
    if args.bpanel != None:
        patchPanelBName = args.bpanel
    else:
        patchPanelBName = input('Please entery the B end patch panel name: ')
    
    if args.portcount != None:
        portcount = int(args.portcount)
    else:
        portcount = int(input('Please enter the number of ports patch panels have: '))
        
    if args.porttype != None:
        porttype = args.porttype
    else:
        porttype = input('Please enter the type of cable the patch panel uses: ')
    
    return patchPanelAName, patchPanelBName, portcount, porttype


def createdict(patchPanelAName, patchPanelBName, portCount, portType):
    
    newDictList = []
    count = 0
    
    while count < portCount:
        count = count + 1
        newDictList.append({
            'side_a_device':patchPanelAName,
            'side_a_type':'dcim.rearport',
            'side_a_name':f'Port {count}',
            'side_b_device':patchPanelBName,
            'side_b_type':'dcim.rearport',
            'side_b_name':f'Port {count}',
            'type':portType
        })
    
    return newDictList

def exportCSV(exportData, patchPanelAName):
    
    file = f'{patchPanelAName}.csv'
    headers = ['side_a_device','side_a_type','side_a_name','side_b_device','side_b_type','side_b_name','type']
    
    with open(file, 'w', newline='') as csvoutput:
        writer = csv.DictWriter(csvoutput, delimiter=',', fieldnames=headers)
        writer.writeheader()
        for row in exportData:
            writer.writerow(row)    
    


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("--apanel",
                        help='A end patch panel name')
    parser.add_argument("--bpanel",
                        help='B end patch panel name'
                        )
    parser.add_argument("--portcount",
                        help='Number of ports patch panel has'
                        )
    parser.add_argument("--porttype",
                        help='Type of ports patch panel has'
                        )
    
    args = parser.parse_args()

    patchPanelAName, patchPanelBName, portCount, portType = setVariables(args)
        
    patchingDictList = createdict(patchPanelAName, patchPanelBName, portCount, portType)
    
    exportCSV(exportData=patchingDictList, patchPanelAName=patchPanelAName)