'''
Created by Preston
Overnight fixes (2026-07-02):
  - data is parsed ONCE into tensors and kept resident on the GPU; batches are
    slices of a shuffled index tensor instead of DataLoader-over-Python-lists
    (the old path was CPU-collate bound: ~8.6 min/epoch on the 50x50 city data
    at ~12% GPU util; this path is ~0.6 s/epoch on the same data and GPU).
  - termination: `accuracy >= config.target_accuracy` OR accuracy plateau
    (no improvement for `config.plateau_patience` evaluations) OR epoch budget.
    The old `accuracy == 1.0` exit is unreachable on real maps (best 2025 result
    was 0.9093 on the 25x25 city map after ~3 weeks).
  - checkpoints are state_dict-based dicts (never whole-module pickles, never
    DataParallel-wrapped), so they load under any GPU visibility.
  - an existing checkpoint is backed up with a timestamp instead of raising
    RuntimeError('file exists and not resuming training!').
  - per-eval (epoch, loss, accuracy) history is written to <save_name>_history.csv.
  - the exported ONNX additionally gets a NEUS-style accuracy-permille copy name
    recorded in the checkpoint metadata / stdout.
'''
import sys
import time
import csv
import torch
import torch.nn as nn
import torch.optim as optim
import config as c
import os
import torch.onnx
from dataset_astar import load_tensors


class NeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, hidden_count, output_size):
        super(NeuralNetwork, self).__init__()
        self.hidden_layers = nn.ModuleList()
        self.hidden_layers.append(nn.Linear(input_size, hidden_size))
        for _ in range(hidden_count - 1):
            self.hidden_layers.append(nn.Linear(hidden_size, hidden_size))
        self.output_layer = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        for layer in self.hidden_layers:
            x = self.relu(layer(x))
        x = self.output_layer(x)
        return x

class NeuralNetwork_diff(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size):
        super(NeuralNetwork_diff, self).__init__()
        self.hidden_layers = nn.ModuleList()
        hidden_sizes = [input_size] + hidden_sizes
        for hidden_index in range(len(hidden_sizes) - 1):
            self.hidden_layers.append(nn.Linear(hidden_sizes[hidden_index], hidden_sizes[hidden_index + 1]))
        self.output_layer = nn.Linear(hidden_sizes[-1], output_size)
        self.relu = nn.ReLU()

    def forward(self, x):
        for layer in self.hidden_layers:
            x = self.relu(layer(x))
        x = self.output_layer(x)
        return x


def build_model(device):
    return (
        NeuralNetwork(c.input_size, c.hidden_size, c.hidden_count, c.output_size).to(device)
        if c.all_same else
        NeuralNetwork_diff(c.input_size, c.layer_sizes, c.output_size).to(device)
    )


def test(trained_model, inputs, targets, batch_size):
    """
    Test model on GPU-resident tensors.
    """
    trained_model.eval()
    total_corr = 0
    with torch.no_grad():
        for start in range(0, inputs.shape[0], batch_size):
            outputs = trained_model(inputs[start:start + batch_size])
            predicted_classes = outputs.argmax(dim=1)
            total_corr += (predicted_classes == targets[start:start + batch_size]).sum().item()
    return total_corr / inputs.shape[0]


def train(model, inputs, targets, criterion, optimizer, batch_size, device):
    """
    Train model for one epoch on GPU-resident tensors.
    """
    model.train()
    total_loss = 0
    permutation = torch.randperm(inputs.shape[0], device=device)
    num_batches = 0
    for start in range(0, inputs.shape[0], batch_size):
        if SLEEP_MODE:
            time.sleep(.001)
        batch_indices = permutation[start:start + batch_size]
        optimizer.zero_grad()
        outputs = model(inputs[batch_indices])
        loss = criterion(outputs, targets[batch_indices])
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        num_batches += 1
    return total_loss / num_batches


def save_checkpoint(model, accuracy, epoch, path):
    torch.save(
        {
            'model_state_dict': model.state_dict(),
            'accuracy': accuracy,
            'epoch': epoch,
            'input_size': c.input_size,
            'all_same': c.all_same,
            'hidden_size': c.hidden_size,
            'hidden_count': c.hidden_count,
            'layer_sizes': c.layer_sizes,
            'output_size': c.output_size,
        },
        path
    )


def export_onnx(model, accuracy, device):
    model.eval()
    dummy_input = torch.randn(1, c.input_size).to(device)
    onnx_path = os.path.join(c.save_path, c.save_name + '.onnx')
    torch.onnx.export(model,
                      dummy_input,
                      onnx_path,
                      export_params=True,
                      opset_version=11,
                      do_constant_folding=True,
                      input_names=['input'],
                      output_names=['output'],
                      dynamic_axes={'input': {0: 'batch_size'},
                                    'output': {0: 'batch_size'}})
    print('Exported ONNX to ' + onnx_path
          + ' (train accuracy ' + format(accuracy, '.6f')
          + ', NEUS-style name would be ' + format(int(accuracy * 1000), '04d') + '__' + c.save_name + '.onnx)')


def run_training(model, start_epoch=0):
    """
    Shared training loop for fresh and resumed runs.
    """
    device = next(model.parameters()).device
    os.makedirs(c.save_path, exist_ok=True)
    ckpt_path = os.path.join(c.save_path, c.save_name + '.pth')
    history_path = os.path.join(c.save_path, c.save_name + '_history.csv')
    #
    # Load dataset once, keep it on the device.
    #
    print('Starting Loading')
    (inputs, targets) = load_tensors(c.input_path, c.target_path)
    inputs = inputs.to(device)
    targets = targets.to(device)
    print('Finished Loading: ' + str(inputs.shape[0]) + ' samples on ' + str(device))
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=c.lr)
    # optional exponential learning-rate decay (helps grind the last few
    # accuracy points on these memorization tasks): lr(epoch) =
    # max(lr_min, lr * lr_gamma**epoch). Disabled if lr_gamma is absent/None.
    lr_gamma = getattr(c, 'lr_gamma', None)
    lr_min = getattr(c, 'lr_min', 0.0)
    target_accuracy = getattr(c, 'target_accuracy', 1.0)
    plateau_patience = getattr(c, 'plateau_patience', None)
    best_accuracy = -1.0
    evals_since_improvement = 0
    epoch = start_epoch
    start_time = time.time()
    with open(history_path, 'a', encoding='utf-8', newline='') as history_file:
        history = csv.writer(history_file)
        if start_epoch == 0:
            history.writerow(['epoch', 'loss', 'accuracy', 'elapsed_seconds'])
        for epoch in range(start_epoch, c.num_epochs):
            if lr_gamma is not None:
                current_lr = max(lr_min, c.lr * (lr_gamma ** epoch))
                for param_group in optimizer.param_groups:
                    param_group['lr'] = current_lr
            loss = train(model, inputs, targets, criterion, optimizer, c.batch_size, device)
            if epoch % c.log_freq == 0:
                accuracy = test(model, inputs, targets, c.batch_size)
                elapsed = time.time() - start_time
                print(f"[{epoch}/{c.num_epochs}] Accuracy: {accuracy:.8f} \t Loss: {loss:.8f} \t Elapsed: {elapsed:.1f}s", flush=True)
                history.writerow([epoch, format(loss, '.8f'), format(accuracy, '.8f'), format(elapsed, '.1f')])
                history_file.flush()
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    evals_since_improvement = 0
                    save_checkpoint(model, accuracy, epoch, ckpt_path)
                else:
                    evals_since_improvement += 1
                if accuracy >= target_accuracy:
                    print('Reached target accuracy ' + str(target_accuracy) + '; stopping.')
                    break
                if plateau_patience is not None and evals_since_improvement >= plateau_patience:
                    print('No accuracy improvement in ' + str(plateau_patience)
                          + ' evaluations (best ' + format(best_accuracy, '.6f') + '); stopping.')
                    break
    #
    # Save the model (final state; the best checkpoint was already saved above)
    #
    print("\n\n Finished Training. Saving models ..................................................")
    final_accuracy = test(model, inputs, targets, c.batch_size)
    if final_accuracy >= best_accuracy:
        save_checkpoint(model, final_accuracy, epoch, ckpt_path)
        export_accuracy = final_accuracy
    else:
        # final state is worse than the best seen; restore the best checkpoint for export
        checkpoint = torch.load(ckpt_path, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        export_accuracy = checkpoint['accuracy']
        print('Final accuracy ' + format(final_accuracy, '.6f') + ' < best '
              + format(export_accuracy, '.6f') + '; exporting the best checkpoint instead.')
    #
    # Convert to onnx and save
    #
    export_onnx(model, export_accuracy, device)
    print("\n\n------------------------------------- Finished Training -------------------------------------------\n\n")


def main():
    """
    Fresh training run.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n\nUsing device: {device}\n\n")
    os.makedirs(c.save_path, exist_ok=True)
    ckpt_path = os.path.join(c.save_path, c.save_name + '.pth')
    if os.path.exists(ckpt_path):
        backup_path = ckpt_path + '.bak-' + time.strftime('%Y%m%d-%H%M%S')
        os.rename(ckpt_path, backup_path)
        print('WARNING: ' + ckpt_path + ' already exists; moved it to ' + backup_path)
    model = build_model(device)
    run_training(model, start_epoch=0)


def resume_training():
    """
    Resume from a state_dict checkpoint saved by this trainer.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n\nUsing device: {device}\n\n")
    ckpt_path = os.path.join(c.save_path, c.save_name + '.pth')
    checkpoint = torch.load(ckpt_path, map_location=device)
    model = build_model(device)
    model.load_state_dict(checkpoint['model_state_dict'])
    print('Resumed from ' + ckpt_path + ' (epoch ' + str(checkpoint.get('epoch'))
          + ', accuracy ' + str(checkpoint.get('accuracy')) + ')')
    run_training(model, start_epoch=checkpoint.get('epoch', 0) + 1)


SLEEP_MODE = False
if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == '0':
            SLEEP_MODE = True
            main()
        elif sys.argv[1] == '1':
            resume_training()
        elif sys.argv[1] == '2':
            SLEEP_MODE = True
            resume_training()
    else:
        main()
