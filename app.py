from flask import Flask, render_template, request
import requests
import json

API_URL = "https://world.openfoodfacts.org/cgi/search.pl?search_terms={0}&search_simple=1&action=process&json=1"

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/search")
def search():
  query = request.args.get('q')
  return get_products(query)

def get_products(query):
  products = []
  url = API_URL.format(query)
  r = requests.get(url)
  if r.status_code == 200:
    data = r.json()
    for product in data['products']:
      products.append(Product(product).to_json())
    products = json.dumps(products)
  return products

class Product:
  NUTRI_SCORE = {'a': 4, 'b': 3, 'c': 2, 'd': 1, 'e': 0}
  NOVA_SCORE = {'1': 3, '2': 2, '3': 1, '4': 0}

  KEY_BIO = ['bio', 'biologique']

  def __init__(self, data):
    self.name = data['product_name']
    self.image = self.get_image(data)
    self.errors = []
    if self.is_water(data):
      self.score = 100
      return
    self.nova_score = self.get_nova_score(data)
    self.nutri_score = self.get_nutri_score(data)
    self.bio_score = self.get_bio_score(data)
    self.score = self.get_score() if len(self.errors) == 0 else 0

  def get_image(self, data):
    if data.get('image_url'):
      return data['image_url']
    elif data.get('image_thumb_url'):
      return data['image_thumb_url']
    elif data.get('image_front_thumb_url'):
      return data['image_front_thumb_url']
    elif data.get('image_front_small_url'):
      return data['image_front_small_url']
    else:
      return 'https://media.forgecdn.net/avatars/141/115/636539774401917932.jpeg'

  def get_nova_score(self, data):
    if data.get('nova_group_tags') and 'not-applicable' in data['nova_group_tags']:
      self.errors.append('Nova score undefined')
      return 0
    return self.NOVA_SCORE[str(data['nova_groups'])]
    
      
  def get_nutri_score(self, data):
    if data.get('nutrition_grades_tags') and 'not-applicable' in data['nutrition_grades_tags']:
      self.errors.append('Nutri score undefined')
      return 0
    grade = None
    if data.get('nutrition_grades'):
      grade = data['nutrition_grades']
    elif data.get('nutrition_grade_fr') :
      grade = data['nutrition_grade_fr']
    if grade is None:
      self.errors.append('Nutri score undefined')
      return 0
    return self.NUTRI_SCORE[grade]

  def is_water(self, data):
    if data.get('categories_tags'):
      return 'en:waters' in data['categories_tags']
    return False

  def get_bio_score(self, data):
    if data.get('_keywords'):
      return 1.0 if any(x in self.KEY_BIO for x in  data['_keywords']) else 0.0
    
    self.errors.append('bio')
    return 0

  def get_score(self):
    #a revoir car la formule données est mauvaise dans le pdf
    calcul_de_base = (0.6 * float(self.nutri_score) + 0.3 * float(self.nova_score) + 0.1 * self.bio_score) * 100
    calcul_modifier = round(calcul_de_base / 3.45, 0) + 1
    return calcul_modifier
  
  def to_json(self):
    return {
      'name': self.name,
      'image': self.image,
      'score': self.score,
      'errors': self.errors  
    }
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                