from flask import Flask
from flask import request
from flask import render_template
from mapper import set_default_map, make_map

app = Flask(__name__)
map_file = 'map.html'

@app.route('/')
def form():
    set_default_map(map_file)
    return render_template('form.html')

@app.route('/', methods=['POST'])
def form_post():
    site_id = request.form['site_id']
    travel_dist = request.form['travel_dist']
    try:
        make_map(int(site_id), int(travel_dist), map_file)
    except KeyError:
        return 'Site ID: {} not found.'.format(site_id)
    return render_template('form.html')

@app.route('/' + map_file)
def show_map():
    return render_template(map_file)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
