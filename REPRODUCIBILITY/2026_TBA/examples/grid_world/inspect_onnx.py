"""Inspect the grid world ONNX model to determine output class ordering."""
import numpy as np
import onnx
import onnxruntime as ort

ONNX_PATH = "./networks/1000__6_18_0__0200_1.onnx"

# --- Structural inspection ---
model = onnx.load(ONNX_PATH)
print("=== ONNX model metadata ===")
print(f"IR version: {model.ir_version}")
for prop in model.metadata_props:
    print(f"  {prop.key}: {prop.value}")

print("\n=== Inputs ===")
for inp in model.graph.input:
    print(f"  {inp.name}: {inp.type}")

print("\n=== Outputs ===")
for out in model.graph.output:
    print(f"  {out.name}: {out.type}")

# --- Runtime probe: run known inputs and read raw logits ---
sess = ort.InferenceSession(ONNX_PATH)
input_name = sess.get_inputs()[0].name
output_name = sess.get_outputs()[0].name
print(f"\nInput  name: {input_name}")
print(f"Output name: {output_name}")

# Grid is 0-6. Probe with intuitive cases to infer class order.
# Case 1: Drone at (0,3), goal at (6,3) → should strongly prefer East
# Case 2: Drone at (6,3), goal at (0,3) → should strongly prefer West
# Case 3: Drone at (3,0), goal at (3,6) → should strongly prefer North
# Case 4: Drone at (3,6), goal at (3,0) → should strongly prefer South
probes = [
    ([0, 3, 6, 3], "East expected  (drone W, goal E)"),
    ([6, 3, 0, 3], "West expected  (drone E, goal W)"),
    ([3, 0, 3, 6], "North expected (drone S, goal N)"),
    ([3, 6, 3, 0], "South expected (drone N, goal S)"),
    ([3, 3, 3, 3], "XX expected    (drone == goal)"),
]

print("\n=== Logit probes ===")
print(f"{'Input':<25} {'Description':<35} {'Logits (raw)':<50} {'Argmax idx'}")
print("-" * 120)
for inputs, desc in probes:
    x = np.array([inputs], dtype=np.float32)
    logits = sess.run([output_name], {input_name: x})[0][0]
    argmax = int(np.argmax(logits))
    logit_str = "  ".join(f"{v:6.2f}" for v in logits)
    print(f"{str(inputs):<25} {desc:<35} [{logit_str}]  idx={argmax}")

print("\nIf argmax matches expected direction, the index of that direction is the argmax index.")
