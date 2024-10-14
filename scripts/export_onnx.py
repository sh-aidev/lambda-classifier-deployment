import torch
import torch.onnx
import timm
import onnxruntime as ort
import numpy as np
import requests
from PIL import Image
from io import BytesIO

model = timm.create_model('resnetv2_50', pretrained=True)
model = model.eval()
model_script = torch.jit.script(model)

print("exporting onnx...")
torch.onnx.export(model_script, torch.randn(1, 3, 224, 224), "checkpoints/resnetv2_50.onnx", verbose=True, input_names=[
                  'input'], output_names=['output'], dynamic_axes={'input': {0: 'batch'}})