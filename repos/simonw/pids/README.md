# pids

Create short public identifiers based on integer IDs.

## Installation

    pip install pids

## Usage

    from pids import pid
    public_id = pid.from_int(1234)
    # public_id is now "gxd"
    id = pid.to_int("gxd")
    # id is now 1234
