from flask import Flask, render_template, request, jsonify
import redis

app = Flask(__name__)

# Configurações do Redis
r = redis.Redis(
    host='redis-11070.c270.us-east-1-3.ec2.cloud.redislabs.com',
    port=11070,
    password='nzOPiXGtMmhZOhjMbU6xjIpsW0y59OLj')

@app.route('/')
def index():
    keys = r.keys('*')
    records = [{'key': key.decode('utf-8'), 'value': r.get(key).decode('utf-8')} for key in keys]
    return render_template('index.html', records=records)
@app.route('/crud', methods=['POST'])
def create_update_value():
    key = request.form.get('key')
    value = request.form.get('value')
    r.set(key, value)
    message = f'Registro criado/atualizado: Chave: {key}, Valor: {value}'
    return jsonify({'message': message, 'redirect': '/'})  # Return the redirect URL

@app.route('/crud', methods=['PUT'])
def edit_value():
    key = request.form.get('key')
    value = request.form.get('value')
    if r.exists(key):
        r.set(key, value)
        message = f'Registro editado: Chave: {key}, Valor: {value}'
        return jsonify({'message': message, 'redirect': '/'})  # Return the redirect URL
    else:
        message = 'Chave não encontrada'
        return jsonify({'message': message})

@app.route('/crud', methods=['DELETE'])
def delete_value():
    key = request.form.get('key')
    r.delete(key)
    message = 'Registro excluído com sucesso'
    return jsonify({'message': message, 'redirect': '/'})  # Return the redirect URL


if __name__ == '__main__':
    app.run(debug=True)
