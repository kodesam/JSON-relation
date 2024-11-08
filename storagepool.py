from graphviz import Digraph

# Initialize a directed graph
dot = Digraph(comment='Storage Pool JSON Structure')

# Define the main entities
dot.node('StoragePoolListV5', 'StoragePoolListV5\n(category: storage-pools)\n(uri: /rest/storage-pools)')
dot.node('StoragePoolV5_1', 'StoragePoolV5\n(name: CPG001_R6_SSD)\n(storageSystemUri: CZ29410720)\n(totalCapacity: 58.5TB)')
dot.node('StoragePoolV5_2', 'StoragePoolV5\n(name: CPG001_R6_SSD)\n(storageSystemUri: CZ2941071Z)\n(totalCapacity: 38.5TB)')
dot.node('DeviceAttributes1', 'DeviceSpecificAttributes\n(uuid: da809657-1c12-45b9-8051-6a9b454f6e19)\n(domain: VD1-VMWARE-HRL1-3P2)\n(type: SSD)\n(RAID: RAID6)')
dot.node('DeviceAttributes2', 'DeviceSpecificAttributes\n(uuid: a52583f5-33de-4066-bb1c-703b0a8ed716)\n(domain: VD1-VMWARE-HRL1-3P2)\n(type: SSD)\n(RAID: RAID6)')

# Define relationships
dot.edge('StoragePoolListV5', 'StoragePoolV5_1', label='contains')
dot.edge('StoragePoolListV5', 'StoragePoolV5_2', label='contains')
dot.edge('StoragePoolV5_1', 'DeviceAttributes1', label='has')
dot.edge('StoragePoolV5_2', 'DeviceAttributes2', label='has')

# Render the diagram
dot.render('/mnt/data/storage_pool_structure', format='png', cleanup=False)

print("Diagram generated and saved as storage_pool_structure.png")
