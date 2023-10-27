import tkinter as tk
from tkinter import filedialog, Menu, messagebox
from heapq import heappop, heappush, heapify
from collections import defaultdict
import pickle

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        self.arvore = None

    def __lt__(self, other):
        return self.freq < other.freq

class InterfaceGrafica:
    small_pad = 10

    def __init__(self, root):
        self.root = root
        self.root.title("Código de Huffman")
        self.criar_widgets()

    def cria_arvore(self, text):
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
        
        self.arvore = heap
        return heap[0]

    def constroi_codigo(self, raiz, code, huffman_codes):
        if raiz is None:
            return

        if raiz.char is not None:
            huffman_codes[raiz.char] = code
        self.constroi_codigo(raiz.left, code + '0', huffman_codes)
        self.constroi_codigo(raiz.right, code + '1', huffman_codes)

    def criar_janelas(self):
        esquerda = tk.Frame(self.root)
        esquerda.pack(
            side="top", padx=self.small_pad, pady=self.small_pad, expand=True
        )

        # direita = ttk.Frame(self.root, height=400, width=650, style="Custom.TFrame")
        # direita.pack(
        #     side="right", padx=self.small_pad, pady=self.small_pad, expand=True
        # )

        return esquerda#, direita

    def is_binary_string(self, s):
        for char in s:
            if char != '0' and char != '1':
                return False
        return True

    def comprimir(self, text):
        raiz = self.cria_arvore(text)
        huffman_codes = {}
        self.constroi_codigo(raiz, '', huffman_codes)
        texto_comprimido = ''.join(huffman_codes[char] for char in text)

        self.saida.insert(tk.END, texto_comprimido)

    def descomprimir(self, entrada):
        texto_descomprimido = ""
        try:
            no_atual = self.arvore[0]
        except AttributeError:
            messagebox.showwarning("Aviso", "Comprima um texto para gerar uma árvore, ou abra um arquivo gerado pelo programa.")
            return

        for bit in entrada:
            if bit == '0':
                no_atual = no_atual.left
            else:
                no_atual = no_atual.right

            if no_atual.left is None and no_atual.right is None:
                texto_descomprimido += no_atual.char
                no_atual = self.arvore[0]

        self.saida.delete(1.0, tk.END)
        self.saida.insert(tk.END, texto_descomprimido)

    def escolhe_operacao(self):
        text = self.entrada.get("1.0", "end-1c")
        if self.is_binary_string(text):
            self.descomprimir(text)
        else:
            self.comprimir(text)

    def abrir(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
                arvore = data['arvore']
                texto_comprimido = data['texto_comprimido']
                self.arvore = arvore
                self.saida.delete(1.0, tk.END)
                self.entrada.delete(1.0, tk.END)
                self.entrada.insert(tk.END, texto_comprimido)

    def salvar(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".huf", filetypes=[("All Files", "*.*")])
        with open(file_path, 'wb') as file:
            data = {
                'arvore': self.arvore,
                'texto_comprimido': self.saida.get("1.0", "end-1c")
            }
            pickle.dump(data, file)
    
    def criar_widgets(self):
        janela_esq = self.criar_janelas()

        menu_bar = Menu(root)
        root.config(menu=menu_bar)

        menu_bar.add_command(label="Abrir", command=self.abrir)
        menu_bar.add_command(label="Salvar", command=self.salvar)

        entrada_label = tk.Label(janela_esq, text="Entrada:")
        entrada_label.pack()

        self.entrada = tk.Text(janela_esq, wrap=tk.WORD, height=10, width=60)
        self.entrada.pack()

        comprimir_botao = tk.Button(janela_esq, text="Comprimir / Descomprimir", command=self.escolhe_operacao)
        comprimir_botao.pack()

        saida_label = tk.Label(janela_esq, text="Saida:")
        saida_label.pack()

        self.saida = tk.Text(janela_esq, wrap=tk.WORD, height=10, width=60)
        self.saida.pack()

root = tk.Tk()
app = InterfaceGrafica(root)
root.mainloop()