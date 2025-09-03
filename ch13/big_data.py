import sys
[sys.stdout.buffer.write(b'Hello! >') for _ in range(100000000)]
sys.stdout.flush()
