"""The stacks SPEC.md shows as worked resolved-chain examples.

`sync.py` takes this list in when the file exists. It names stacks, which
belong to a fork rather than to upstream, so it lives beside them.
"""

# (heading, stack id) pairs, rendered in this order.
SPEC_CHAIN_EXAMPLES = [
    ("static-site-astro", "stack-astro"),
    ("python-flask", "stack-flask"),
]
