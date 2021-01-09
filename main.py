import os

from flask import Flask
from google.cloud import storage
app = Flask(__name__)
sc = storage.Client()
bucket_name = 'simplelist_datastore'
bucket = sc.bucket(bucket_name)
MAX_DIG = 15
RES_PER_PG = 30

@app.route("/new_post/<content>")
def new_post(content):
	# get max key.
	max_key_ob = bucket.get_blob('#max.txt')
	max_key = int(max_key_ob.download_as_bytes())
	# write new max key.
	new_max = str(max_key + 1).zfill(MAX_DIG)
	max_key_ob = bucket.get_blob('#max.txt')
	max_key_ob.upload_from_string(f'{new_max}')
	# put new post
	new_b = bucket.blob(f'{new_max}.txt')
	new_b.upload_from_string(content)
	return f'{max_key}->{int(new_max)},{content}'

@app.route("/")
@app.route("/<pg_back>")
def get_posts(pg_back=''):
	# get max key
	max_key_ob = bucket.get_blob('#max.txt')
	max_id = int(max_key_ob.download_as_bytes())
	# handle pagination
	if pg_back == '':
		start_id = max_id - RES_PER_PG + 1
		start_key = str(max(1,start_id)).zfill(15) + '.txt'
		end_key = None
	else:
		start_id = max_id - RES_PER_PG * (int(pg_back) + 1) + 1
		start_key = str(max(1,start_id)).zfill(15) + '.txt'
		req_end_id = start_id + RES_PER_PG
		end_id = req_end_id if req_end_id < max_id else None
		end_key = str(end_id).zfill(15) + '.txt'
	# listing
	blobs = sc.list_blobs(
		bucket_name,
		start_offset = start_key,
		end_offset = end_key,
	)
	# get names and contents
	contents = [
		[
			b.name,
			b.download_as_bytes(),
			str(b.updated)
		]
		for b in blobs
	]
	contents.sort(reverse=True)
	nice_contents = '\n'.join([str(x) for x in contents])
	return f'<pre>{nice_contents}</pre>'

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))