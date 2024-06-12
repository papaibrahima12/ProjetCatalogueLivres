from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Charger les fichiers Excel
catalogues = {
    'catalogue1': pd.read_excel('./Catalogue_TDM.ods'),
    # 'catalogue2': pd.read_excel('chemin/vers/votre/catalogue2.xlsx')
    # Ajoutez d'autres catalogues si nécessaire
}

@app.route('/', methods=['GET'])
def home():
    return "Hello world"

@app.route('/search', methods=['GET'])
def search():
    titre = request.args.get('titre')
    auteur = request.args.get('auteur')
    annee_pub = request.args.get('annee_pub')

    resultats = []

    for nom, catalogue in catalogues.items():
        # Appliquer les filtres selon les paramètres de requête
        df_result = catalogue
        if titre:
            df_result = df_result[df_result['TITRE'].str.contains(titre, case=False, na=False)]
        if auteur:
            df_result = df_result[df_result['AUTEUR'].str.contains(auteur, case=False, na=False)]
        if annee_pub:
            df_result = df_result[df_result['ANNEE DE PUBLICATION'] == annee_pub]
        
        resultats.extend(df_result.to_dict(orient='records'))

    return jsonify(resultats)

if __name__ == '__main__':
    app.run(debug=True)
