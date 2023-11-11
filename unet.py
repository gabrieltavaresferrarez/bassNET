import torch
import torch.nn as nn

class convolution_block(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()

        self.conv1 = nn.Conv2d(in_c, out_c, kernel_size = 3, padding=1, )
        self.bn1 = nn.BatchNorm2d(out_c, )
        self.relu1 = nn.ReLU()

        self.conv2 = nn.Conv2d(in_c, out_c, kernel_size = 3, padding=2, )
        self.bn2 = nn.BatchNorm2d(out_c, )
        self.relu2 = nn.ReLU()

        self.conv3 = nn.Conv2d(in_c, out_c, kernel_size = 3, padding=1, )
        self.bn3 = nn.BatchNorm2d(out_c, )
        self.relu3 = nn.ReLU()

    def forward(self, inputs):
        x = self.conv1(inputs)
        x = self.bn1(x)
        x = self.relu1(x)

        x = self.conv2(inputs)
        x = self.bn2(x)
        x = self.relu2(x)

        x = self.conv3(inputs)
        x = self.bn3(x)
        x = self.relu3(x)

        return x

class encoder_block(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()
        self.conv = convolution_block(in_c, out_c)
        self.pool = nn.MaxPool2d((2,2), )

    def forward(self, x):
        x = self.conv(x)
        p = self.pool(x)
        return x, p

class decoder_block(nn.Module):
    def __init__(self, in_c, out_c):
        super().__init__()
        self.up = nn.ConvTranspose2d(in_c, out_c, kernel_size=2, stride=2, padding = 0, )
        self.conv = convolution_block(out_c*2, out_c)

    def forward(self, x, skip):
        x = self.up(x)
        x = torch.cat((x, skip), axis=1)
        x = self.conv(x)
        return x



class unet(nn.Module):
    def __init__(self, verbose=False):
        super().__init__()
        self.verbose=verbose

        """encoder"""
        self.e1= encoder_block(2, 64)
        self.e2= encoder_block(64, 128)
        self.e3= encoder_block(128, 256)
        self.e4= encoder_block(256, 512)

        """bottleneck"""
        self.b = convolution_block(512, 1024)

        """decoder"""
        self.d1 = decoder_block(1024, 512)
        self.d2 = decoder_block(512, 256)
        self.d3 = decoder_block(256, 128)
        self.d4 = decoder_block(128, 64)

        """classifier"""
        self.outputs = nn.Conv2d(64, 2, kernel_size = 1, padding=0, )


    def forward(self, inputs):
        """encoder"""
        if self.verbose:
            print(f'size of input : {inputs.size()}')
        s1, p1 = self.e1(inputs)
        if self.verbose:
            print(f'size of s1 : {s1.size()}')
            print(f'size of p1 : {p1.size()}')
        s2, p2 = self.e2(p1)
        if self.verbose:
            print(f'size of s2 : {s2.size()}')
            print(f'size of p2 : {p2.size()}')
        s3, p3 = self.e3(p2)
        if self.verbose:
            print(f'size of s3 : {s3.size()}')
            print(f'size of p3 : {p3.size()}')
        s4, p4 = self.e4(p3)
        if self.verbose:
            print(f'size of s4 : {s4.size()}')
            print(f'size of p4 : {p4.size()}')
        """bottleneck"""
        b = self.b(p4)
        if self.verbose:
            print(f'size of b : {b.size()}')
        """decoder"""
        d1 = self.d1(b, s4)
        if self.verbose:
            print(f'size of d1 : {d1.size()}')
        d2 = self.d2(d1, s3)
        if self.verbose:
            print(f'size of d2 : {d2.size()}')
        d3 = self.d3(d2, s2)
        if self.verbose:
            print(f'size of d3 : {d3.size()}')
        d4 = self.d4(d3, s1)
        if self.verbose:
            print(f'size of d4 : {d4.size()}')
        """outputs"""
        y = self.outputs(d4)
        if self.verbose:
            print(f'size of y : {y.size()}')


        return y