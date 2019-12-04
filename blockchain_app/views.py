from uuid import uuid4
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from utils.blockchain import Blockchain

blockchain = Blockchain()
# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace("-", "")


def mine(request):
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    proof = blockchain.proof_of_work(last_block)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0", recipient=node_identifier, amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    blockchain.new_block(proof, previous_hash)
    return JsonResponse({"message": "New Block Forged"}, status=200)


"""
class Transaction(View):
    def get(self, request):
        return render(request, "transaction.html")

    def post(self, request):
        values = request.POST
        required = ["sender", "recipient", "amount"]
        if not all(k in values for k in required):
            return "Missing values", 400

        index = blockchain.new_transaction(values["sender"], values["recipient"], values["amount"])

        response = {"message": f"Transaction will be added to Block {index}"}
        return render(request, "transaction.html", {"response": response})
"""


def new_transaction(request):
    values = request.POST
    # Check that the required fields are in the POST'ed data
    if not values["sender"] or not values["recipient"] or not values["amount"]:
        return JsonResponse({"message": "Missing value."}, status=200)
    # Create a new Transaction
    index = blockchain.new_transaction(values["sender"], values["recipient"], values["amount"])
    return JsonResponse({"message": f"Transaction will be added to Block {index}."}, status=201)


def full_chain(request):
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    # return JsonResponse(response, status=200)
    return render(request, "chain.html", {"response": response})


def full_chain_json(request):
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return JsonResponse(response, status=200)


class Node(View):
    def get(self, request):
        response = {
            "total_nodes": list(blockchain.nodes),
        }
        return render(request, "node.html", {"response": response})

    def post(self, request):
        node = request.POST["node"]
        blockchain.register_node(node)

        response = {
            "message": "New nodes have been added",
            "total_nodes": list(blockchain.nodes),
        }
        return render(request, "node.html", {"response": response})


"""
def register_nodes(request):
    node = request.POST["node"]
    blockchain.register_node(node)

    response = {
        "message": "New nodes have been added",
        "total_nodes": list(blockchain.nodes),
    }
    return JsonResponse(response, status=201)
"""


def consensus(request):
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {"message": "Our chain was replaced", "new_chain": blockchain.chain}
    else:
        response = {"message": "Our chain is authoritative", "chain": blockchain.chain}
    return JsonResponse(response, status=200)
