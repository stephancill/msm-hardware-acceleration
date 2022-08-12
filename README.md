# Hardware Accelerator for zk-SNARKs

## Testing

```
cd tb/ModMul
SIM=icarus pipenv run pytest -o log_cli=True test_modmul.py
```

## Directory structure references

- https://github.com/nmk456/fpga-sdr
- https://github.com/cocotb/cocotb-bus
- https://github.com/alexforencich/cocotbext-pcie
