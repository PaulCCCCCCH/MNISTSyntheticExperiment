import torch.nn as nn
import os
import torch


class LeNet(nn.Module):
    def __init__(self, args):
        super(LeNet, self).__init__()
        in_channels = 3 if args.is_rgb_data else 1
        self.conv1 = nn.Sequential(
            # (1, 28, 28) => (6, 28, 28)
            nn.Conv2d(in_channels=in_channels,
                      out_channels=6,
                      kernel_size=5,
                      padding=2),
            nn.ReLU(),
            # (6, 28, 28) => (6, 14, 14)
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.conv2 = nn.Sequential(
            # (6, 14, 14) => (16, 10, 10)
            nn.Conv2d(in_channels=6,
                      out_channels=16,
                      kernel_size=5),
            nn.ReLU(),
            # (16, 10, 10) => (16, 5, 5)
            nn.MaxPool2d(2, 2)
        )

        # A flatten layer here: (16, 5, 5) => (16*5*5)

        self.fc1 = nn.Sequential(
            # (16*5*5) => (120)
            nn.Linear(16 * 5 * 5, 120),
            nn.ReLU()
        )
        self.fc2 = nn.Sequential(
            # (120, 84)
            nn.Linear(120, 84),
            nn.ReLU()
        )

        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size()[0], -1)
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x


class LeNetWithReg(nn.Module):
    def __init__(self, args):
        super(LeNetWithReg, self).__init__()
        self.args = args

        in_channels = 3 if args.is_rgb_data else 1
        self.conv1 = nn.Sequential(
            # (1, 28, 28) => (6, 28, 28)
            nn.Conv2d(in_channels=in_channels,
                      out_channels=6,
                      kernel_size=5,
                      padding=2),
            nn.ReLU(),
            # (6, 28, 28) => (6, 14, 14)
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.conv2 = nn.Sequential(
            # (6, 14, 14) => (16, 10, 10)
            nn.Conv2d(in_channels=6,
                      out_channels=16,
                      kernel_size=5),
            nn.ReLU(),
            # (16, 10, 10) => (16, 5, 5)
            nn.MaxPool2d(2, 2)
        )

        # A flatten layer here: (16, 5, 5) => (16*5*5)
        self.fc1 = nn.Sequential(
            # (16*5*5) => (120)
            nn.Linear(16 * 5 * 5, 120),
            nn.ReLU()
        )

        if args.use_dropout:
            self.fc2 = nn.Sequential(
                # (120, 84)
                nn.Linear(120, 84),
                nn.ReLU(),
                nn.Dropout()
            )
        else:
            self.fc2 = nn.Sequential(
                # (120, 84)
                nn.Linear(120, 84),
                nn.ReLU(),
            )

        self.fc3 = nn.Linear(84, 10)

        self.cnn_parameters = set(self.parameters())

        # CNN ends here. Following are regularization layers
        if args.reg_layers == 1:
            if args.method == 1 or args.method == 5:
                if args.reg_object == 0:
                    self.fc_reg = nn.Sequential(
                        nn.Linear(10, 1, bias=not args.method == 5)
                    )
                elif args.reg_object == 1:
                    self.fc_reg = nn.Sequential(
                        nn.Linear(84, 1, bias=not args.method == 5)
                    )

        elif args.reg_layers == 2:
            if args.method == 1 or args.method == 5:
                if args.reg_object == 0:
                    self.fc_reg = nn.Sequential(
                        nn.Linear(10, 10, bias=not args.method == 5),
                        nn.Linear(10, 1, bias=not args.method == 5)
                    )
                elif args.reg_object == 1:
                    self.fc_reg = nn.Sequential(
                        nn.Linear(84, 50, bias=not args.method == 5),
                        nn.Linear(50, 1, bias=not args.method == 5)
                    )
        self.reg_parameters = set(self.parameters()) - self.cnn_parameters


    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size()[0], -1)

        x = self.fc1(x)
        h = self.fc2(x)

        logit = self.fc3(h)

        if self.args.reg_object == 0:
            reg_obj = logit
        elif self.args.reg_object == 1:
            reg_obj = h

        if self.args.method == 1 or self.args.method == 5:
            reg = self.fc_reg(reg_obj)
        else:
            reg = None

        return logit, reg, reg_obj


def save_model(state_dict: dict, args, new=False):
    if new:
        torch.save(state_dict, args.new_save_path)
    else:
        torch.save(state_dict, args.save_path)


def load_model(args):
    save_path = args.save_path
    if not os.path.exists(save_path):
        return None
    return torch.load(save_path)
