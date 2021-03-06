from cs285.infrastructure import pytorch_util as ptu
from .base_exploration_model import BaseExplorationModel
import torch.optim as optim
from torch import nn
import numpy as np
from collections import defaultdict
import torch

def init_method_1(model):
    model.weight.data.uniform_()
    model.bias.data.uniform_()

def init_method_2(model):
    model.weight.data.normal_()
    model.bias.data.normal_()


class RNDModel(nn.Module, BaseExplorationModel):
    def __init__(self, hparams, optimizer_spec, **kwargs):
        super().__init__(**kwargs)
        self.ob_dim = hparams['ob_dim']
        self.output_size = hparams['rnd_output_size']
        self.n_layers = hparams['rnd_n_layers']
        self.size = hparams['rnd_size']
        self.optimizer_spec = optimizer_spec
        self.hash = hparams["hash"]

        # TODO: Create two neural networks:
        # 1) f, the random function we are trying to learn
        # 2) f_hat, the function we are using to learn f
        # WARNING: Make sure you use different types of weight
        #          initializations for these two functions

        # HINT 1) Check out the method ptu.build_mlp
        # HINT 2) There are two weight init methods defined above
        if self.hash:
            self.encoder = ptu.build_mlp(self.ob_dim, self.output_size, self.n_layers, self.size)
            self.decoder = ptu.build_mlp(self.output_size, self.ob_dim, self.n_layers, self.size)
            self.ae_loss = nn.MSELoss()

            self.f = ptu.build_mlp(self.ob_dim, self.output_size, self.n_layers, self.size, init_method=init_method_1)
            self.f_hat = ptu.build_mlp(self.ob_dim, self.output_size, self.n_layers, self.size, init_method=init_method_2)

            self.optimizer = self.optimizer_spec.constructor(
                list(self.encoder.parameters()) + list(self.decoder.parameters()),
                **self.optimizer_spec.optim_kwargs
            )
            self.learning_rate_scheduler = optim.lr_scheduler.LambdaLR(
                self.optimizer,
                self.optimizer_spec.learning_rate_schedule,
            )

            self.counts = defaultdict(int)

            self.pretrain_autoencoder()

        else:
            self.f = ptu.build_mlp(self.ob_dim, self.output_size, self.n_layers, self.size, init_method=init_method_1)
            self.f_hat = ptu.build_mlp(self.ob_dim, self.output_size, self.n_layers, self.size, init_method=init_method_2)

            self.optimizer = self.optimizer_spec.constructor(
                self.f_hat.parameters(),
                **self.optimizer_spec.optim_kwargs
            )
            self.learning_rate_scheduler = optim.lr_scheduler.LambdaLR(
                self.optimizer,
                self.optimizer_spec.learning_rate_schedule,
            )

            self.f.to(ptu.device)
            self.f_hat.to(ptu.device)

    def pretrain_autoencoder(self):
        samples = np.random.uniform(0, 1, size=(10000, 2))
        ob_no = ptu.from_numpy(samples)
        reconstruction = self.decoder(self.encoder(ob_no))
        loss = self.ae_loss(ob_no, reconstruction)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def forward(self, ob_no):
        if self.hash:
            # print(ob_no)
            codes = ptu.to_numpy(self.encoder(ob_no).round())
            counts = np.zeros(len(codes))
            for i, code in enumerate(codes):
                counts[i] = self.counts[str(code)]
                self.counts[str(code)] += 1
            return 1 / np.sqrt(counts+1)
        # TODO: Get the prediction error for ob_no
        # HINT: Remember to detach the output of self.f!
        else:
            error = ((self.f.forward(ob_no).detach() - self.f_hat(ob_no)) ** 2).mean(axis=1)
        return error

    def forward_np(self, ob_no):
        ob_no = ptu.from_numpy(ob_no)
        if self.hash:
            return self(ob_no)
        error = self(ob_no)
        return ptu.to_numpy(error)

    def update(self, ob_no):
        if self.hash:
            ob_no = ptu.from_numpy(ob_no)
            reconstruction = self.decoder(self.encoder(ob_no))
            loss = self.ae_loss(ob_no, reconstruction)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            return loss.item()
        # TODO: Update f_hat using ob_no
        # Hint: Take the mean prediction error across the batch
        ob_no = ptu.from_numpy(ob_no)
        loss = self.forward(ob_no).mean()
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()
