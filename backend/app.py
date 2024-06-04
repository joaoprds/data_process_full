from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)


@app.route('/process', methods=['POST'])
def process_files():
    try:
        # Get Files to FrontEnd
        bills_file = request.files['bills']
        legislators_file = request.files['legislators']
        votes_file = request.files['votes']
        vote_results_file = request.files['vote_results']

        # Read files with Pandas
        bills = pd.read_csv(bills_file)
        legislators = pd.read_csv(legislators_file)
        votes = pd.read_csv(votes_file)
        vote_results = pd.read_csv(vote_results_file)



        # Count of support and opposition by legislator
        support_opposition = vote_results.merge(votes, left_on='vote_id', right_on='id', how='left')
        support_opposition['num_supported_bills'] = support_opposition['vote_type'].apply(lambda x: 1 if x == 1 else 0)
        support_opposition['num_opposed_bills'] = support_opposition['vote_type'].apply(lambda x: 1 if x == 2 else 0)
        support_opposition = support_opposition.groupby('legislator_id').agg({
            'num_supported_bills': 'sum',
            'num_opposed_bills': 'sum'
        }).reset_index()
        support_opposition = support_opposition.merge(legislators, left_on='legislator_id', right_on='id', how='left')[
            ['id', 'name', 'num_supported_bills', 'num_opposed_bills']]
        support_opposition.to_csv('data/legislators-support-oppose-count.csv', index=False)

        # conference log file
        print("file legislators-support-oppose-count.csv created.")

        # Counting support and opposition per bill
        bill_support = vote_results.merge(legislators, left_on='legislator_id', right_on='id', how='left')
        bill_support['supporter_count'] = bill_support['vote_type'].apply(lambda x: 1 if x == 1 else 0)
        bill_support['opposer_count'] = bill_support['vote_type'].apply(lambda x: 1 if x == 2 else 0)
        bill_support = bill_support.groupby('vote_id').agg({
            'supporter_count': 'sum',
            'opposer_count': 'sum'
        }).reset_index()



        bill_support = bill_support.merge(votes, left_on='vote_id', right_on='id', how='left')[
            ['bill_id', 'supporter_count', 'opposer_count']]



        bill_support = bill_support.merge(bills, left_on='bill_id', right_on='id', how='left')[
            ['id', 'title', 'supporter_count', 'opposer_count', 'sponsor_id']]



        bill_support = bill_support.merge(legislators, left_on='sponsor_id', right_on='id', how='left')[
            ['id_x', 'title', 'supporter_count', 'opposer_count', 'name']]
        bill_support.rename(columns={'id_x': 'id', 'name': 'sponsor_id'}, inplace=True)
        bill_support['sponsor_id'] = bill_support['sponsor_id'].fillna('Unknown')


        bill_support.to_csv('data/bills.csv', index=False)


        print(" bills.csv created with Success.")

        return jsonify({
            'message': 'Files processed successfully',
            'files': ['legislators-support-oppose-count.csv', 'bills.csv']
        })
    except Exception as e:
        print("Error While process. Error:", str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join('data', filename)
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    app.run(debug=True)
