from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Mock database simulating PostgreSQL performance records
database = {
    'dancers': {
        '1': {'name': 'Emma Davis', 'troupe': 'Advanced Contemporary'},
        '2': {'name': 'Liam Smith', 'troupe': 'Hip Hop Crew'}
    },
    'routines': {
        'R01': {'title': 'Autumn Leaves', 'genre': 'Contemporary'},
        'R02': {'title': 'Urban Beat', 'genre': 'Hip Hop'}
    },
    'performance_evaluations': []
}

@app.route('/evaluations', methods=['POST'])
def add_evaluation():
    """Log a new dance performance evaluation for a routine."""
    data = request.json
    dancer_id = str(data.get('dancer_id'))
    routine_id = str(data.get('routine_id'))
    
    # 1 to 10 Rubric Scores
    technique = float(data.get('technique', 0))
    timing = float(data.get('timing', 0))
    expression = float(data.get('expression', 0))
    feedback = data.get('feedback', '')

    if dancer_id in database['dancers'] and routine_id in database['routines']:
        # Calculate overall score average across rubric criteria
        overall_score = round((technique + timing + expression) / 3.0, 2)
        
        evaluation = {
            'eval_id': len(database['performance_evaluations']) + 1,
            'dancer_id': dancer_id,
            'dancer_name': database['dancers'][dancer_id]['name'],
            'routine_id': routine_id,
            'routine_title': database['routines'][routine_id]['title'],
            'scores': {
                'technique': technique,
                'timing': timing,
                'expression': expression,
                'overall': overall_score
            },
            'feedback': feedback,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        database['performance_evaluations'].append(evaluation)
        return jsonify({
            'message': f"Performance evaluation logged successfully for {database['dancers'][dancer_id]['name']}.",
            'evaluation': evaluation
        }), 201

    return jsonify({'error': 'Invalid Dancer ID or Routine ID.'}), 404


@app.route('/performance/<dancer_id>', methods=['GET'])
def get_dancer_performance(dancer_id):
    """Retrieve performance evaluation history and overall progress for a dancer."""
    dancer_id = str(dancer_id)
    if dancer_id not in database['dancers']:
        return jsonify({'error': 'Dancer not found.'}), 404

    dancer_evals = [e for e in database['performance_evaluations'] if e['dancer_id'] == dancer_id]
    
    if not dancer_evals:
        return jsonify({
            'dancer_name': database['dancers'][dancer_id]['name'],
            'message': 'No performance evaluations logged yet.',
            'evaluations': []
        }), 200

    avg_overall = round(sum(e['scores']['overall'] for e in dancer_evals) / len(dancer_evals), 2)

    return jsonify({
        'dancer_id': dancer_id,
        'dancer_name': database['dancers'][dancer_id]['name'],
        'troupe': database['dancers'][dancer_id]['troupe'],
        'total_evaluations': len(dancer_evals),
        'average_overall_score': avg_overall,
        'evaluations': dancer_evals
    }), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)