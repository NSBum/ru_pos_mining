#!/usr/bin/env python3

"""ru_pos_mining

Usage:
    main.py show RUWORD [--code=INFLECTION] [--format=FORMAT]
    main.py runserver
    main.py --version

Options:
    -h --help                           Show this screen.
    --version                           Show version.
    -c INFLECTION --code=INFLECTION     Return only form for code.
    -f FORMAT --format=FORMAT           Output format 'json' or 'xml'. [default: json]

"""
from docopt import docopt
from ruwiktionary import *
from grammar import *
import json
from flask import Flask
from flask import request, jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSON_AS_ASCII'] = False


@app.route('/forms/<w>')
def serve_word(w):
    ru_word = urllib.parse.unquote(w)
    # print(ru_word)
    w_page = RuWikitionary(ru_word, False)
    w_tree = w_page.root_tree
    w_word = w_page.parse()
    if w_page.pos is None:
        w_output = {'in': ru_word, 'error': 'Not found. Is this an uninflected form? Spelling?'}
    else:
        w_output = {'in': ru_word, 'pos': w_page.pos.to_upos()}
        w_outforms = []
        try:
            for w in w_word.inflection_code_list:
                (term, inflection_code) = w
                description = code2term(inflection_code)
                w_outforms.append({'code': inflection_code, 'form': term, 'desc': description})
            w_output['forms'] = w_outforms
        except AttributeError:
            pass
    # print(w_word.inflection_code_list)
    return jsonify(w_output)


def object_to_xml(data: Union[dict, bool], root='object'):
    xml = f'<{root}>'
    if isinstance(data, dict):
        for key, value in data.items():
            xml += object_to_xml(value, key)
    elif isinstance(data, (list, tuple, set)):
        for item in data:
            xml += object_to_xml(item, 'inflection')
    else:
        xml += str(data)
    xml += f'</{root}>'
    return xml


if __name__ == "__main__":
    # show "собака" --format=xml
    arguments = docopt(__doc__, version='ru_pos_mining 0.75')
    print(arguments)
    if arguments['RUWORD']:
        page = RuWikitionary(arguments['RUWORD'], False)
        tree = page.root_tree
        # print(page.pos)
        word = page.parse()
        print(word.inflection_code_list)
        if arguments['--code']:
            code = int(arguments['--code'])
            words = [w[0] for w in word.inflection_code_list if w[1] == code]
            print(words)
        if arguments['--format']:
            if arguments['--format'] == 'json':
                output = {'in': arguments['RUWORD'], 'pos': page.pos.to_upos()}
                outforms = [{f'{x[1]}': x[0]} for x in word.inflection_code_list]
                output['forms'] = outforms
                print(json.dumps(output))
            elif arguments['--format'] == 'xml':
                output = {'in': arguments['RUWORD'], 'pos': page.pos.to_upos()}

                def forms2dict(x):
                    return {'code': f'{x[1]}', 'form': f'{x[0]}'}
                outforms = list(map(forms2dict, word.inflection_code_list))
                output['forms'] = outforms
                print(object_to_xml(output, 'inflections'))
    elif arguments['runserver']:
        app.run(debug=True, host='0.0.0.0', port='43561')




