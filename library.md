### Requirements

* Python 3.8 or greater


### installation:
```
pip install graphsense
```


### Training example:

```
from graphsense import GraphSense

g = GraphSense()

g.line_completion(input_path="code_files", output_path="output")

```

### Inference example:

```
from graphsense import GraphSense

g = GraphSense()

g.load_model("output/graph_embeddings.model")
next = g.infer("def factorial(n):")

print("next item predicted: ", next)
```

### Performance Comparison with gpt2_medium finetuned model
Dataset used to train models: https://github.com/TheAlgorithms/Python 
#### gpt2_medium finetuned model
```
input: def factorial(n)  
output: return 1 if n == 1 else n * factorial(n - 1)   
model size: 1.44GB   
avg inference time: 10.3302 seconds  
CPU Usage: 8.3%  
Memory Usage: 68.54 MB  
```

#### graph embedding model 
```
input: def factorial(n)  
output: return 1 if n == 1 else n * factorial(n - 1)   
model size: 13.2MB
avg inference time: 2.1870 seconds  
CPU Usage: 0.2%
Memory Usage: 4.54 MB  
``` 
