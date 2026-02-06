from flask import Flask, request, jsonify
import numpy as np
import torch
import traceback

from workflow import train

app = Flask(__name__)


def validate_and_convert(payload: dict):
    if payload is None:
        raise ValueError("Missing JSON payload")

    if 'X' not in payload or 'Y' not in payload:
        raise ValueError("JSON payload must include 'X' and 'Y' arrays")

    X = np.array(payload['X'], dtype=float)
    Y = np.array(payload['Y'], dtype=float)

    if X.ndim != 3:
        raise ValueError(f"X must be a 3D array [seq_len, batch_size, input_dim], got shape {X.shape}")
    if Y.ndim != 3:
        raise ValueError(f"Y must be a 3D array [seq_len, batch_size, 1], got shape {Y.shape}")

    # Convert to torch tensors
    X_t = torch.tensor(X, dtype=torch.float32)
    X_t.requires_grad_()
    Y_t = torch.tensor(Y, dtype=torch.float32)

    return X_t, Y_t


def extract_train_params(payload: dict):
    allowed = {
        'epochs': int,
        'output_dim': int,
        'num_pde_constraints': int,
        'd_model': int,
        'num_heads': int,
        'dim_feedforward': int,
        'num_layers': int,
        'dropout': float,
        'learning_rate': float,
        'lambda_data': float,
        'lambda_pde': float,
        'live_mode': bool
    }
    params = {}
    for k, t in allowed.items():
        if k in payload:
            params[k] = payload[k]
    return params


@app.route('/train', methods=['POST'])
def train_route():
    try:
        payload = request.get_json()
        X_t, Y_t = validate_and_convert(payload)
        params = extract_train_params(payload)

        # Call the workflow train function (synchronous)
        results = train(X_t, Y_t, **params)

        # Ensure results are JSON serializable (convert tensors/floats)
        if isinstance(results, dict):
            safe = {}
            for k, v in results.items():
                if isinstance(v, torch.Tensor):
                    safe[k] = v.detach().cpu().tolist()
                else:
                    try:
                        # convert numpy arrays, lists, numbers
                        import numbers
                        if isinstance(v, numbers.Number) or isinstance(v, str) or isinstance(v, list) or isinstance(v, dict):
                            safe[k] = v
                        else:
                            safe[k] = v
                    except Exception:
                        safe[k] = v
            return jsonify(safe)

        return jsonify({"status": "success", "result": results})

    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"status": "error", "message": str(e), "traceback": tb}), 400


@app.route('/', methods=['GET'])
def test():
    return jsonify({
        "status": "OK",
        "message": "You've reached the DCA_PINN training server."
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
