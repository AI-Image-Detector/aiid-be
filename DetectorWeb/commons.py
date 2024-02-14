import io

import torch 
import torch.nn as nn
from torchvision import models,transforms
from PIL import Image 


def get_model():
	# checkpoint_path='classifier.pt'
	# model=models.densenet121(pretrained=True)
	# model.classifier=nn.Linear(1024,102)
	# model.load_state_dict(torch.load(checkpoint_path,map_location='cpu'),strict=False)
	# model.eval()

	checkpoint_path='pt.pt'
	model = models.resnet50(pretrained=False)
	for param in model.parameters():
		param.requires_grad=True
	n_inputs = model.fc.in_features
	last_layer = nn.Linear(n_inputs, 2)
	model.fc = last_layer
	model.load_state_dict(torch.load(checkpoint_path,map_location='cpu'))
	return model

def get_tensor(image_bytes):
	my_transforms=transforms.Compose([transforms.Resize(300),
                                    transforms.CenterCrop(299),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.485, 0.456, 0.406],
                                                        [0.229, 0.224, 0.225])])
	image=Image.open(io.BytesIO(image_bytes))
	# image=Image.open(image_bytes)
	return my_transforms(image).unsqueeze(0)
	# return my_transforms(image)