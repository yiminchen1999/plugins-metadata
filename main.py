import json
import quart
import quart_cors
import matplotlib.pyplot as plt
import numpy as np
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

# Database of literature data. Does not persist if Python session is restarted.
_DATABASE = {}

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
    # fail silently, it's a simple plugin
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
