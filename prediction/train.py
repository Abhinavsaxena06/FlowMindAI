from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split

from prediction.dataset import (
    TrafficSequenceDataset,
    load_states,
    generate_demo_states
)

from prediction.model import (
    TrafficTransformer
)


DEVICE = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


def train_model(
    epochs=15,
    sequence_length=20,
    batch_size=32
):

    states = load_states()

    if len(states) < 100:

        print(
            "Not enough real traffic states."
        )

        print(
            "Generating demo training data..."
        )

        states = generate_demo_states(
            2000
        )

    dataset = TrafficSequenceDataset(
        states,
        sequence_length=sequence_length
    )

    if len(dataset) < 20:

        raise RuntimeError(
            "Not enough training sequences."
        )

    train_size = int(
        len(dataset) * 0.8
    )

    validation_size = (
        len(dataset)
        -
        train_size
    )

    train_dataset, validation_dataset = (
        random_split(
            dataset,
            [
                train_size,
                validation_size
            ]
        )
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size=batch_size
    )

    model = TrafficTransformer().to(
        DEVICE
    )

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=0.001,
        weight_decay=0.0001
    )

    criterion = nn.MSELoss()

    best_loss = float("inf")

    checkpoint_dir = Path(
        "prediction/checkpoints"
    )

    checkpoint_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    checkpoint_path = (
        checkpoint_dir
        /
        "traffic_transformer.pt"
    )

    for epoch in range(
        epochs
    ):

        model.train()

        train_loss = 0.0

        for x, y in train_loader:

            x = x.to(
                DEVICE
            )

            y = y.to(
                DEVICE
            )

            optimizer.zero_grad()

            prediction = model(
                x
            )

            loss = criterion(
                prediction,
                y
            )

            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                1.0
            )

            optimizer.step()

            train_loss += (
                loss.item()
            )

        model.eval()

        validation_loss = 0.0

        with torch.no_grad():

            for x, y in validation_loader:

                x = x.to(
                    DEVICE
                )

                y = y.to(
                    DEVICE
                )

                prediction = model(
                    x
                )

                loss = criterion(
                    prediction,
                    y
                )

                validation_loss += (
                    loss.item()
                )

        train_loss /= max(
            1,
            len(train_loader)
        )

        validation_loss /= max(
            1,
            len(validation_loader)
        )

        print(
            f"Epoch "
            f"{epoch + 1}/{epochs} "
            f"| train={train_loss:.5f} "
            f"| validation={validation_loss:.5f}"
        )

        if validation_loss < best_loss:

            best_loss = validation_loss

            torch.save(
                {
                    "model_state_dict":
                        model.state_dict(),

                    "validation_loss":
                        validation_loss
                },
                checkpoint_path
            )

            print(
                "  ✓ Best model saved"
            )

    print()
    print(
        "Training complete."
    )

    print(
        f"Model: {checkpoint_path}"
    )


if __name__ == "__main__":

    train_model()