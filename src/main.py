import tkinter as tk
from heapq import heappop, heappush, heapify
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    freq = defaultdict(int)
    for char in text:
        freq[char] += 1

    heap = [HuffmanNode(char, freq) for char, freq in freq.items()]
    heapify(heap)

    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        merged_node = HuffmanNode(None, left.freq + right.freq)
        merged_node.left = left
        merged_node.right = right
        heappush(heap, merged_node)

    return heap[0]

def build_huffman_codes(root, code, huffman_codes):
    if root is None:
        return

    if root.char is not None:
        huffman_codes[root.char] = code
    build_huffman_codes(root.left, code + '0', huffman_codes)
    build_huffman_codes(root.right, code + '1', huffman_codes)

def compress_text(text):
    root = build_huffman_tree(text)
    huffman_codes = {}
    build_huffman_codes(root, '', huffman_codes)
    compressed_text = ''.join(huffman_codes[char] for char in text)
    return compressed_text, root

def decompress_text(compressed_text, root):
    decompressed_text = ""
    current_node = root

    for bit in compressed_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.left is None and current_node.right is None:
            decompressed_text += current_node.char
            current_node = root

    return decompressed_text

def compress_button_click():
    input_text = input_text_entry.get("1.0", "end-1c")
    compressed_text, huffman_tree = compress_text(input_text)
    compressed_text_label.config(text=f"Compressed Text: {compressed_text}")
    huffman_tree_label.config(text=f"Huffman Tree: {huffman_tree}")

def decompress_button_click():
    compressed_text = compressed_text_entry.get("1.0", "end-1c")
    huffman_tree = huffman_tree_label.cget("text")
    root = HuffmanNode(None, 0)
    decompressed_text = decompress_text(compressed_text, root)
    decompressed_text_label.config(text=f"Decompressed Text: {decompressed_text}")

# Configuração da janela principal
window = tk.Tk()
window.title("Huffman Text Compressor")

# Elementos da GUI
input_text_label = tk.Label(window, text="Input Text:")
input_text_label.pack()
input_text_entry = tk.Text(window, height=5, width=40)
input_text_entry.pack()

compress_button = tk.Button(window, text="Compress", command=compress_button_click)
compress_button.pack()

compressed_text_label = tk.Label(window, text="Compressed Text:")
compressed_text_label.pack()

huffman_tree_label = tk.Label(window, text="Huffman Tree:")
huffman_tree_label.pack()

compressed_text_label = tk.Label(window, text="Compressed Text:")
compressed_text_label.pack()

compressed_text_entry = tk.Text(window, height=5, width=40)
compressed_text_entry.pack()

decompress_button = tk.Button(window, text="Decompress", command=decompress_button_click)
decompress_button.pack()

decompressed_text_label = tk.Label(window, text="Decompressed Text:")
decompressed_text_label.pack()

# Iniciar a janela principal
window.mainloop()
