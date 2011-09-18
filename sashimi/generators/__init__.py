
"""
The :py:module:`sashimi.generators` module provides classes that
can generate test content for standard content types.

These objects implement a ``can_fuzz`` function so we can determine
if they can generate test content for a particular field.

Their ``fuzz`` method returns a random piece of data that is valid for
the field. For example, the regex generator will generate test data
that passes the regex validation.
"""

from sashimi.generators import \
    bool, numbers, vocabulary, ipsum, regex, dtfuzz, file, reference
