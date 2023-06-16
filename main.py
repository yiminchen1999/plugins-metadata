import json
import quart
import quart_cors
import matplotlib.pyplot as plt
import numpy as np
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Database
_DATABASE = {
    "username1": [
        {
            "title": "Sample Paper 1",
            "author": "John Doe",
            "year": 2021,
            "value": 10.5
        },
        {
            "title": "Sample Paper 2",
            "author": "Jane Smith",
            "year": 2022,
            "value": 8.2
        },
        {
            "title": "Sample Paper 3",
            "author": "David Johnson",
            "year": 2020,
            "value": 6.9
        }
    ],
    "username2": [
        {
            "title": "Research Study 1",
            "author": "Alice Brown",
            "year": 2019,
            "value": 7.8
        },
        {
            "title": "Research Study 2",
            "author": "Bob Wilson",
            "year": 2023,
            "value": 9.1
        }
    ]
}


@app.post("/literature/<string:username>")
async def add_literature(username):
    data = await quart.request.get_json(force=True)
    if username not in _DATABASE:
        _DATABASE[username] = []
    _DATABASE[username].append(data)
    return quart.Response(response='OK', status=200)

@app.get("/literature/<string:username>")
async def get_literature(username):
    return quart.Response(response=json.dumps(_DATABASE.get(username, [])), status=200)

@app.delete("/literature/<string:username>")
async def delete_literature(username):
    data = await quart.request.get_json(force=True)
    literature_idx = data["literature_idx"]

    if 0 <= literature_idx < len(_DATABASE[username]):
        _DATABASE[username].pop(literature_idx)
    return quart.Response(response='OK', status=200)

@app.get("/plot/<string:username>")
async def generate_plot(username):
    literature_data = _DATABASE.get(username, [])
    if not literature_data:
        return quart.Response(response='No literature data found', status=404)

    # Generate plot from literature data
    x_values = np.arange(len(literature_data))
    y_values = [item["value"] for item in literature_data]

    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values)
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title('Literature Data')
    plt.grid(True)

    # Save plot to a temporary file
    plot_filename = 'plot.png'
    plt.savefig(plot_filename)

    # Return the plot file to the client
    return await quart.send_file(plot_filename, mimetype='image/png')

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
