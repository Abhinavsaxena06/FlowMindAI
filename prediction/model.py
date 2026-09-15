import torch
import torch.nn as nn


class PositionalEncoding(
    nn.Module
):

    def __init__(
        self,
        d_model,
        max_length=500
    ):

        super().__init__()

        position = torch.arange(
            max_length
        ).unsqueeze(1)

        div_term = torch.exp(
            torch.arange(
                0,
                d_model,
                2
            )
            *
            (
                -torch.log(
                    torch.tensor(
                        10000.0
                    )
                )
                /
                d_model
            )
        )

        pe = torch.zeros(
            max_length,
            d_model
        )

        pe[:, 0::2] = torch.sin(
            position * div_term
        )

        pe[:, 1::2] = torch.cos(
            position * div_term
        )

        pe = pe.unsqueeze(0)

        self.register_buffer(
            "pe",
            pe
        )

    def forward(
        self,
        x
    ):

        length = x.size(1)

        return (
            x
            +
            self.pe[
                :,
                :length
            ]
        )


class TrafficTransformer(
    nn.Module
):

    def __init__(
        self,
        input_size=10,
        d_model=64,
        nhead=4,
        num_layers=3,
        dropout=0.1
    ):

        super().__init__()

        self.input_projection = (
            nn.Linear(
                input_size,
                d_model
            )
        )

        self.position = (
            PositionalEncoding(
                d_model
            )
        )

        encoder_layer = (
            nn.TransformerEncoderLayer(
                d_model=d_model,
                nhead=nhead,
                dropout=dropout,
                batch_first=True,
                activation="gelu"
            )
        )

        self.encoder = (
            nn.TransformerEncoder(
                encoder_layer,
                num_layers=num_layers
            )
        )

        self.norm = nn.LayerNorm(
            d_model
        )

        self.output = nn.Sequential(

            nn.Linear(
                d_model,
                64
            ),

            nn.GELU(),

            nn.Dropout(
                dropout
            ),

            nn.Linear(
                64,
                input_size
            )
        )

    def forward(
        self,
        x
    ):

        x = self.input_projection(
            x
        )

        x = self.position(
            x
        )

        x = self.encoder(
            x
        )

        x = x[:, -1, :]

        x = self.norm(
            x
        )

        return self.output(
            x
        )