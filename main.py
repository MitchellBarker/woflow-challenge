import requests

class Node:
	def __init__(self, id, child_node_ids):
		# set universal unique identifier and children
		self.id = id
		self.child_node_ids = child_node_ids
		# number of times this node is a child node for others
		self.references = 0

class NodeHashTable:
	def __init__(self):
		self.lookup = {}
		self.api = NodeAPIController()

	def traverse(self, id):
		if id not in self.lookup:
			node_data = self.api.get_node_data([id])
			if isinstance(node_data,list):
				self.lookup[id] = Node(id, node_data[0]['child_node_ids'])
				for t_id in self.lookup[id].child_node_ids:
					self.traverse(t_id)
				self.load_children(self.lookup[id])
		else:
			self.lookup[id].references += 1

	def load_children(self, node):
		if len(node.child_node_ids) > 0:
			node_data = self.api.get_node_data(node.child_node_ids)

			if isinstance(node_data,list):
				for n in node_data:
					if n['id'] not in self.lookup:
						self.lookup[n['id']] = Node(n['id'], n['child_node_ids'])
					else:
						self.lookup[n['id']].references += 1

class NodeAPIController:
	def __init__(self, endpoint="https://nodes-on-nodes-challenge.herokuapp.com/nodes/"):
		self.endpoint = endpoint

	def get_node_data(self, node_ids):
		if not isinstance(node_ids,list):
			raise Exception('node_ids must be a List')
		
		# grab the json for these nodes
		r = requests.get(self.endpoint + ','.join(node_ids));

		if r.status_code == 200:
			return r.json()
		else:
			raise Exception(r.status_code + ': did not return valid content for this node data')

if __name__ == '__main__':
	node_hash = NodeHashTable()
	node_hash.traverse('089ef556-dfff-4ff2-9733-654645be56fe')

	# lame way to anser our questions
	print(len(node_hash.lookup))
	print(node_hash.lookup)
	for key,val in node_hash.lookup.items():
		print(key + ':' + str(val.references))
