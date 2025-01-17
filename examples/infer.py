from graphsense import GraphSense

g = GraphSense()

g.load_model("output/graph_embeddings.model")
next = g.infer("def factorial(n):")

print("next item predicted: ", next)