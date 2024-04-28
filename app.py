from tkinter import ttk
from tkinter import *
import sqlite3

class Produto:
    db = r'C:\Users\Renan Freitas\PycharmProjects\GestorProdutos\database\produtos.db'

    def __init__(self, root):
        self.janela = root
        self.janela.title("App Gestor de Produtos")
        self.janela.geometry("300x200")
        self.janela.resizable(1, 1)
        self.janela.wm_iconbitmap('recursos/icon.ico')

        # Criação da tabela de Produtos
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        self.tabela = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.tabela.grid(row=4, column=0, columnspan=2)
        self.tabela.heading('#0', text='Nome', anchor=CENTER)
        self.tabela.heading('#1', text='Preço', anchor=CENTER)

        # Botões de Eliminar e Editar
        botao_eliminar = ttk.Button(text='ELIMINAR', command=self.del_produto)
        botao_eliminar.grid(row=6, column=0, sticky=W + E)
        botao_editar = ttk.Button(text='EDITAR', command=self.edit_produto)
        botao_editar.grid(row=6, column=1, sticky=W + E)
        self.mensagem = Label(self.janela, text='', font=('Calibri', 12))
        self.mensagem.grid(row=7, column=0, columnspan=2)

        self.nome = Entry(self.janela)
        self.nome.grid(row=0, column=0, padx=5, pady=5)
        self.preco = Entry(self.janela)
        self.preco.grid(row=1, column=0, padx=5, pady=5)

        # Rótulos para os campos de entrada
        Label(self.janela, text="Nome do Produto:").grid(row=0, column=1, padx=5, pady=5, sticky=W)
        Label(self.janela, text="Preço do Produto:").grid(row=1, column=1, padx=5, pady=5, sticky=W)

        # Botão para adicionar produto
        botao_adicionar = ttk.Button(text='ADICIONAR', command=self.add_produto)
        botao_adicionar.grid(row=2, column=0, columnspan=2, pady=5)

        self.get_produtos()



    def db_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            cursor.execute(consulta, parametros)
            resultado = cursor.fetchall()
            con.commit()
            return resultado

    def get_produtos(self):
        registros_tabela = self.tabela.get_children()
        for linha in registros_tabela:
            self.tabela.delete(linha)

        query = 'SELECT * FROM produto ORDER BY nome DESC'
        registros_db = self.db_consulta(query)

        for linha in registros_db:
            self.tabela.insert('', 0, text=linha[1], values=linha[2])

    def validacao_nome(self):
        nome_introduzido_por_utilizador = self.nome.get()
        return len(nome_introduzido_por_utilizador) != 0

    def validacao_preco(self):
        preco_introduzido_por_utilizador = self.preco.get()
        return len(preco_introduzido_por_utilizador) != 0

    def add_produto(self):
        if self.validacao_nome() and self.validacao_preco():
            query = 'INSERT INTO produto VALUES(NULL, ?, ?)'
            parametros = (self.nome.get(), self.preco.get())
            self.db_consulta(query, parametros)
            self.mensagem['text'] = 'Produto {} adicionado com êxito'.format(self.nome.get())
            self.nome.delete(0, END)
            self.preco.delete(0, END)
        elif self.validacao_nome() and self.validacao_preco() == False:
            self.mensagem['text'] = 'O preço é obrigatório'
        elif self.validacao_nome() == False and self.validacao_preco():
            self.mensagem['text'] = 'O nome é obrigatório'
        else:
            self.mensagem['text'] = 'O nome e o preço são obrigatórios'
        self.get_produtos()

    def del_produto(self):
        self.mensagem['text'] = ''
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return
        self.mensagem['text'] = ''
        nome = self.tabela.item(self.tabela.selection())['text']
        query = 'DELETE FROM produto WHERE nome = ?'
        self.db_consulta(query, (nome,))
        self.mensagem['text'] = 'Produto {} eliminado com êxito'.format(nome)
        self.get_produtos()

    def edit_produto(self):
        self.mensagem['text'] = ''
        try:
            self.tabela.item(self.tabela.selection())['text'][0]
        except IndexError as e:
            self.mensagem['text'] = 'Por favor, selecione um produto'
            return
        nome = self.tabela.item(self.tabela.selection())['text']
        old_preco = self.tabela.item(self.tabela.selection())['values'][0]
        self.janela_editar = Toplevel()
        self.janela_editar.title("Editar Produto")
        self.janela_editar.resizable(1, 1)
        self.janela_editar.wm_iconbitmap('recursos/icon.ico')

        titulo = Label(self.janela_editar, text='Edição de Produtos', font=('Calibri', 14, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2)

        frame_ep = LabelFrame(self.janela_editar, text="Editar o seguinte Produto")
        frame_ep.grid(row=1, column=0, columnspan=2, pady=20)

        self.etiqueta_nome_antigo = Label(frame_ep, text="Nome antigo: ")
        self.etiqueta_nome_antigo.grid(row=2, column=0)
        self.input_nome_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=nome),
                                       state='readonly')
        self.input_nome_antigo.grid(row=2, column=1)

        self.etiqueta_preco_antigo = Label(frame_ep, text="Preço antigo: ")
        self.etiqueta_preco_antigo.grid(row=3, column=0)
        self.input_preco_antigo = Entry(frame_ep, textvariable=StringVar(self.janela_editar, value=old_preco),
                                        state='readonly')
        self.input_preco_antigo.grid(row=3, column=1)

        self.etiqueta_nome_novo = Label(frame_ep, text="Nome novo: ")
        self.etiqueta_nome_novo.grid(row=4, column=0)
        self.input_nome_novo = Entry(frame_ep)
        self.input_nome_novo.grid(row=4, column=1)
        self.input_nome_novo.focus()

        self.etiqueta_preco_novo = Label(frame_ep, text="Preço novo: ")
        self.etiqueta_preco_novo.grid(row=5, column=0)
        self.input_preco_novo = Entry(frame_ep)
        self.input_preco_novo.grid(row=5, column=1)

        self.botao_atualizar = ttk.Button(frame_ep, text="Atualizar Produto",
                                          command=lambda: self.atualizar_produto(self.input_nome_novo.get(),
                                                                                 nome,
                                                                                 self.input_preco_novo.get(),
                                                                                 old_preco))

        style = ttk.Style()
        style.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.botao_atualizar = ttk.Button(frame_ep, text="Atualizar Produto",
                                          style='my.TButton',
                                          command=lambda: self.atualizar_produto(self.input_nome_novo.get(),
                                                                                 nome,
                                                                                 self.input_preco_novo.get(),
                                                                                 old_preco))
        self.botao_atualizar.grid(row=6, columnspan=2, sticky=W + E)

    def atualizar_produto(self, novo_nome, antigo_nome, novo_preco, antigo_preco):
        produto_modificado = False
        query = 'UPDATE produto SET nome = ?, preco = ? WHERE nome = ? AND preco = ?'
        if novo_nome != '' and novo_preco != '':
            parametros = (novo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome != '' and novo_preco == '':
            parametros = (novo_nome, antigo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        elif novo_nome == '' and novo_preco != '':
            parametros = (antigo_nome, novo_preco, antigo_nome, antigo_preco)
            produto_modificado = True
        if produto_modificado:
            self.db_consulta(query, parametros)
            self.janela_editar.destroy()
            self.mensagem['text'] = 'O produto {} foi atualizado com êxito'.format(antigo_nome)
            self.get_produtos()
        else:
            self.janela_editar.destroy()
            self.mensagem['text'] = 'O produto {} NÃO foi atualizado'.format(antigo_nome)

if __name__ == '__main__':
        root = Tk()
        my_app = Produto(root)
        root.mainloop()
