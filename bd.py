import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# chave é o id único da tarefa e o valor é a descricao da tarefa.
# O id é usado como chave primária, garantindo que cada tarefa tenha um identificador único. 
# A descricao da tarefa é armazenada como o valor correspondente. Isso torna mais eficiente a leitura e manipulação das tarefas, 
# uma vez que é mais fácil e rápido buscar uma tarefa específica por seu id.

def criar_tabela():
    conn = sqlite3.connect('lista_tarefas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY,
            descricao TEXT
        )
    ''')
    conn.close()

def criar_tarefa(descricao):
    conn = sqlite3.connect('lista_tarefas.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tarefas (descricao) VALUES (?)', (descricao,))
    conn.commit()
    conn.close()

def ler_tarefas():
    conn = sqlite3.connect('lista_tarefas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, descricao FROM tarefas')
    tarefas = cursor.fetchall()
    conn.close()
    return tarefas

def ler_tarefa_por_id(id):
    conn = sqlite3.connect('lista_tarefas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, descricao FROM tarefas WHERE id = ?', (id,))
    tarefa = cursor.fetchone()
    conn.close()
    return tarefa

def atualizar_tarefa(id, nova_descricao):
    conn = sqlite3.connect('lista_tarefas.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tarefas SET descricao = ? WHERE id = ?', (nova_descricao, id))
    conn.commit()
    conn.close()

def deletar_tarefa(id):
    conn = sqlite3.connect('lista_tarefas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tarefas WHERE id = ?', (id,))
    conn.commit()
    conn.close()

@app.route('/')
def exibir_tarefas():
    criar_tabela()
    tarefas = ler_tarefas()
    return render_template('tarefas.html', tarefas=tarefas)

@app.route('/adicionar', methods=['POST'])
def adicionar_tarefa():
    descricao = request.form.get('descricao')
    criar_tarefa(descricao)
    return redirect('/')

@app.route('/editar/<int:id>')
def editar_tarefa(id):
    tarefa = ler_tarefa_por_id(id)
    return render_template('editar_tarefa.html', tarefa=tarefa)

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar_tarefa_rota(id):
    nova_descricao = request.form.get('nova_descricao')
    atualizar_tarefa(id, nova_descricao)
    return redirect('/')

@app.route('/deletar/<int:id>')
def deletar_tarefa_rota(id):
    deletar_tarefa(id)
    return redirect('/')

if __name__ == '__main__':
    app.run()
