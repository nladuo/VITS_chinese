import os
import json
import argparse
import itertools
import math
import torch
from torch import nn, optim
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
import torch.multiprocessing as mp
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.cuda.amp import autocast, GradScaler

import commons
import utils
from data_utils import (
    TextAudioLoader,
    TextAudioCollate,
    DistributedBucketSampler
)
from models import (
    SynthesizerTrn,
    MultiPeriodDiscriminator,
)
from losses import (
    generator_loss,
    discriminator_loss,
    feature_loss,
    kl_loss
)
from mel_processing import mel_spectrogram_torch, spec_to_mel_torch
from text.symbols import symbols
hps = utils.get_hparams()
train_dataset = TextAudioLoader(hps.data.training_files, hps.data)

for i in range(len(train_dataset)):
    train_dataset.__getitem__(i)

# collate_fn = TextAudioCollate()
# train_loader = DataLoader(train_dataset, num_workers=1, shuffle=False, pin_memory=True,
#                               collate_fn=collate_fn)
#
# for batch_idx, (x
#                 , x_lengths, spec, spec_lengths, y, y_lengths) in enumerate(train_loader):
#     print(x.shape)