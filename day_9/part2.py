from dataclasses import dataclass
from typing import Generator, Optional


@dataclass
class Node:
    value: int
    parent: Optional["Node"] = None
    left_child: Optional["Node"] = None
    right_child: Optional["Node"] = None

    def __str__(self) -> str:
        return f"Node(value={self.value})"
    def __repr__(self) -> str:
        return f"Node(value={self.value})"

def next_layer(nodes: list[Node]) -> list[Node]:
    next_nodes: list[Node] = []
    for node, adjacent in zip(nodes, nodes[1:]):
        diff = adjacent.value - node.value
        new_node = Node(diff)
        node.parent = new_node
        adjacent.parent = new_node
        new_node.left_child = node
        new_node.right_child = adjacent
        next_nodes.append(new_node)
    return next_nodes

def all_zeroes(nodes: list[Node]) -> bool:
    return all(node.value == 0 for node in nodes)


def parse(line: str) -> list[Node]:
    return [Node(int(num)) for num in line.split()]

def main(filename: str) -> None:
    with open(filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    acc = 0
    for line in lines:
        nodes = parse(line)
        layers: list[list[Node]] = [nodes]
        while not all_zeroes(nodes):
            nodes = next_layer(nodes)
            layers.append(nodes)
        assert len(layers) >= 2

        layers[-1].insert(0, Node(value=0, right_child=layers[-2][0]))
        for index in range(len(layers) - 2, -1, -1):
            prev_layer_first_node = layers[index + 1][0]
            assert prev_layer_first_node.right_child is not None
            new_node = Node(prev_layer_first_node.right_child.value - prev_layer_first_node.value)
            new_node.parent = prev_layer_first_node
            if index > 0:
                new_node.right_child = layers[index - 1][0]
            prev_layer_first_node.left_child = new_node
            layers[index].insert(0, new_node)

        longest = len(str(layers[0]))
        for layer in layers:
            print(f"{str(layer):^{longest}s}")
        acc += layers[0][0].value
    print(acc)

if __name__ == "__main__":
    main("input.txt")
    main("test.txt")
