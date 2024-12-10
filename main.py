from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Função para validar CEP usando a API do ViaCEP
def validar_cep(cep):
    url = f"https://viacep.com.br/ws/{cep}/json/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Verifica se o CEP é válido
        return not data.get("erro", False)
    return False

@app.route('/validate', methods=['GET'])
def validate_custom_attribute():
    # Obtém os parâmetros da URL
    attribute_type = request.args.get('type')
    key = request.args.get('key')
    value = request.args.get('value')

    # Verifica se todos os parâmetros estão presentes
    if not attribute_type or not key or not value:
        return jsonify({"error": "Missing required parameters"}), 400

    # Valida o formato do CEP
    if len(value) != 8 or not value.isdigit():
        return jsonify({"error": "Invalid CEP format"}), 400

    # Valida o CEP com a API externa
    is_valid = validar_cep(value)
    if is_valid:
        return jsonify({"message": "Valid CEP"}), 200
    else:
        return jsonify({"error": "Invalid CEP"}), 400

if __name__ == '__main__':
    app.run(debug=True)
