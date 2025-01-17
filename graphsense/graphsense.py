import os
import csv
from typing import List
from collections import Counter
import pandas as pd
import networkx as nx
from node2vec import Node2Vec
from gensim.models import Word2Vec

class GraphSense:
    def __init__(self):
        self.data_location = None
        self.model = None
        self.output_file = None

    def get_python_files_in_directory(self, directory_path):
        """Get all Python files in a directory, including subdirectories."""
        self.data_location = directory_path
        python_files = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
        return python_files


    def is_comment_or_empty(self, line: str, in_block_comment: bool) -> (bool, bool):
        """Check if a line is a comment or part of a multi-line comment."""
        stripped = line.strip()

        # Handle block comments (triple quotes)
        if stripped.startswith('"""') or stripped.startswith("'''"):
            if stripped.endswith('"""') or stripped.endswith("'''"):
                # If the line contains both start and end of block comment, treat it as a single-line comment
                return True, False
            elif in_block_comment:
                # If we are already inside a block comment, this ends it
                return True, False
            else:
                # If we are not inside a block comment, this starts it
                return True, True

        if stripped.endswith('"""') or stripped.endswith("'''"):
            if in_block_comment:
                # If we are inside a block comment, this ends it
                return True, False
            else:
                # If we're not inside a block comment, we shouldn't reach here
                return False, in_block_comment

        # If we are inside a block comment, skip all lines until the end of the block
        if in_block_comment:
            return True, True

        # Handle single-line comments (e.g., # or //)
        if stripped.startswith("#") or stripped.startswith("//") or stripped.startswith("/*") or stripped.endswith("*/"):
            return True, False

        # Handle empty lines
        if stripped == "":
            return True, False

        return False, in_block_comment


    def datagen(self, input_files: List[str], output_csv: str):
        """
        Generate a CSV dataset with columns `current_word`, `next_word`, and `occurrence_ct`.
        
        Args:
            input_files (List[str]): List of paths to the input Python files.
            output_csv (str): Path to the output CSV file.
        """
        pairs = []
        in_block_comment = False

        for input_file in input_files:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Input file {input_file} does not exist.")

            with open(input_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Process each line
            for line in lines:
                # Check if the line is a comment or empty and if we are inside a block comment
                is_comment, in_block_comment = self.is_comment_or_empty(line, in_block_comment)
                if not is_comment and not in_block_comment:
                    current_line = line.split()  # Remove leading/trailing whitespace
                    for i in range(len(current_line)-1):
                        pairs.append((current_line[i], current_line[i+1]))

        # Count occurrences of each pair
        pair_counts = Counter(pairs)
        rows = [(current_word, next_word, count) for (current_word, next_word), count in pair_counts.items()]

        # Write to CSV
        with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["current_word", "next_word", "occurrence_ct"])
            writer.writerows(rows)

        print(f"Dataset created at {output_csv} with {len(rows)} rows.")
        self.output_file = output_csv


    def datagen_line(self, input_files: List[str], output_csv: str):
        """
        Generate a CSV dataset with columns `current_line`, `next_line`, and `occurrence_ct`.
        
        Args:
            input_files (List[str]): List of paths to the input Python files.
            output_csv (str): Path to the output CSV file.
        """
        pairs = []
        in_block_comment = False

        for input_file in input_files:
            if not os.path.exists(input_file):
                raise FileNotFoundError(f"Input file {input_file} does not exist.")

            with open(input_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            current_line = None
            next_line = None
            # Process each line
            for i in range(len(lines) - 1):
                # Check if the line is a comment or empty and if we are inside a block comment
                is_comment, in_block_comment = self.is_comment_or_empty(lines[i], in_block_comment)
                if not is_comment and not in_block_comment:
                    current_line = lines[i].strip()  # Remove leading/trailing whitespace
                    if current_line != "" and current_line != None:  # Only consider non-empty lines
                        is_comment, in_block_comment = self.is_comment_or_empty(lines[i+1], in_block_comment)
                        if not is_comment and not in_block_comment:
                            next_line = lines[i+1].strip()  # Remove leading/trailing whitespace
                            if(current_line != "" and current_line != None and next_line != "" and next_line != None):
                                pairs.append((current_line, next_line))
                                current_line = None
                                next_line = None

        # Count occurrences of each pair
        pair_counts = Counter(pairs)
        rows = [(current_line, next_line, count) for (current_line, next_line), count in pair_counts.items()]

        # Write to CSV
        with open(output_csv, "w", encoding="utf-8", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["current_line", "next_line", "occurrence_ct"])
            writer.writerows(rows)

        print(f"Dataset created at {output_csv} with {len(rows)} rows.")
        self.output_file = output_csv

    
    def line_completion(self, input_path: str, output_path: str):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Folder created: {output_path}")
        else:
            print(f"Folder already exists: {output_path}")
    
        input_files = self.get_python_files_in_directory(input_path)
        output_csv = f"{output_path}/edges.csv"
        self.datagen_line(input_files, output_csv)

        graph = pd.read_csv(output_csv)

        edge_list = [[x[0], x[1], x[2]] for x in graph[['current_line', 'next_line', 'occurrence_ct']].to_numpy()]

        G = nx.Graph()
        G.add_weighted_edges_from(edge_list)
        print("Edges added")

        # Initialize Node2Vec with the graph
        node2vec = Node2Vec(G, dimensions=64, walk_length=20, num_walks=200, p=2, q=1, workers=1)

        # Train the Node2Vec model with progress enabled
        model = node2vec.fit(window=10, min_count=1, batch_words=10000)

        self.model = model

        print("Saving the model...")
        # Save the model
        model.save(f'{output_path}/graph_embeddings.model')


    def word_completion(self, input_path: str, output_path: str):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Folder created: {output_path}")
        else:
            print(f"Folder already exists: {output_path}")

        input_files = self.get_python_files_in_directory(input_path)
        output_csv = f"{output_path}/edges.csv"
        self.datagen(input_files, output_csv)

        graph = pd.read_csv(output_csv)

        edge_list = [[x[0], x[1], x[2]] for x in graph[['current_word', 'next_word', 'occurrence_ct']].to_numpy()]

        G = nx.Graph()
        G.add_weighted_edges_from(edge_list)
        print("Edges added")

        # Initialize Node2Vec with the graph
        node2vec = Node2Vec(G, dimensions=64, walk_length=20, num_walks=200, p=2, q=1, workers=1)

        # Train the Node2Vec model with progress enabled
        model = node2vec.fit(window=10, min_count=1, batch_words=10000)

        self.model = model

        print("Saving the model...")
        # Save the model
        model.save(f'{output_path}/graph_embeddings.model')


    def load_model(self, path):
        # Load the saved Node2Vec model
        try:
            self.model = Word2Vec.load(path)
        except Exception as e:
            print("Error loading model: ", e)
    

    def infer(self, input):
        if self.model:
            next = ""
            # Find and print the most similar tokens
            for similar in self.model.wv.most_similar(input)[:1]:
                next = similar[0]
            
            return next
        else:
            raise Exception("Load or Train Model First")


class PreProcessor:
    '''
    Upcoming dataset processor

    '''

