``validict``
============

Description
-----------

``validict`` is a Python module for comparing an unknown value to a
desired template. It is intended for the top-level type to be a
``dict``, but should be flexible enough to deal with ``list``\ s or
scalars (though if you're dealing at scalars, might I suggest running
away from this and just using Python's ``isinstance``). *Important: this
library specifically does not treat ``tuple``\ s as template
expectations but instead as a set of expectations for a given position
in a template.*

Usage
-----

Install with `pip <http://www.pip-installer.org/>`__.

::

    shell~$ pip install validict

Using ``validict`` is simple. First, declare your template:

.. code:: python

    from validict import validate

    template = {
        'name': str,
        'age': int,
        'pets': [
            {
                'name': str,
                'kind': str
            }
        ],
        'parents': ([{'name': str}], int, None)
    }

    kid = {
        'name': "Bart Simpson",
        'age': 10,
        'pets': [
            {'name': "Santa's Little Helper", 'kind': "Dog"},
            {'name': "Snowball II", 'kind': "Cat"}
        ],
        'parents': [
            {'name': "Homer Simpson"},
            {'name': "Marge Simpson"}
        ]
    }

    validate(template, kid)  # returns True

    bad_kid = {
        'name': "Nelson Muntz",
        'age': 12
    }

    validate(template, bad_kid)  # raises FailedValidationError
    validate(template, bad_kid, quiet=True)  # returns False

    optional_kid = {
        'name': "Milhouse Van Houten",
        'age': 10,
        'pets': [
            {'name': "Lhasa Apso", 'kind': "Dog"}
        ],
        'parents': None  # Okay, not really, but for demonstration purposes...
    }

    validate(template, optional_kid)  # returns True

You might be asking yourself -- or me -- "what the hell is this
garbage?" Allow me to briefly explain, and you'll see that the template
language is pretty simple.

1. We use plain, naked Python ``type``\ s to indicate that the expected
   value for the given key should be an object of that type. So, if the
   passed-in dict has a value for ``'name'`` that isn't a ``str``,
   validation fails.

2. When we are expecting a ``list`` of elements, we only need to declare
   in our template one instance of that item, if the ``list``'s children
   are expected to be homogenous. Therefore, ``'pets'`` is expected to
   be a ``list`` of ``dict``\ s, all containing ``str`` value for keys
   ``'name'`` and ``'kind'``.

3. We can use a ``tuple`` to declare that there may be multiple types of
   values, even including (but not demonstrated) further depth of
   structure. In the above, the value of ``'parents'`` can be a ``dict``
   with parents' names, an ``int`` (perhaps representing the number of
   parents), or ``None`` (if you're Batman).

4. Calling ``validate`` with the template and unvalidated value,
   positionally, will result either in a return value of ``True`` or a
   raise of ``FailedValidationError``.

5. Calling ``validate`` as above with the keyword parameter
   ``quiet=True`` will return ``False`` instead of raising
   ``FailedValidationError`` on validation failure.

6. Allowing a ``None`` type as a ``dict`` value or as a member of a
   ``tuple`` signifies that the value is optional. Using it in a
   ``tuple`` allows you to declare that the value can either be matching
   some type or otherwise can be nothing at all.

7. (*Undemonstrated*) Your template can declare scalar values as well.
   So if all inputs must have some specific K/V pair, you can declare
   that.

Why do I want to use this?
--------------------------

If you're using a web framework like, say,
`Falcon <http://falconframework.org>`__ and you wanted to set up a
`before hook <http://falcon.readthedocs.org/en/latest/api/hooks.html>`__
to validate the body of the incoming HTTP request, the function in this
method is for you. At least that's why it's for me.

Bonus!
------

There is an experimental (read: *not heavily tested*) function in this
module called ``deep_merge``, which takes as its arguments two
dictionaries. The second will be merged into the first, in a fashion
such that keys are merged on every level instead of top-level key-values
clobbering over all nested data.
