from graphsense import GraphInfer

g = GraphInfer()

g.load_artifacts()  # load the artifacts to memory
suggestions = g.infer("def factorial(n):")
g.unload_artifacts()  # clean memory

print("top 10 suggestions: ", suggestions)