Common Operations
=================

Generating XML attributes
~~~~~~~~~~~~~~~~~~~~~~~~~

There are two ways for creating an attribute. The first is using URL
notation within a node name:

::

    grammar input:
        match 'User' nl '----' nl 'Name:' ws value field_end:
            out.enter('user?name="$6"')
            user()

The second, equivalent way calls add\_attribute() explicitely:

::

    grammar input:
        match 'User' nl '----' nl 'Name:' ws value field_end:
            out.enter('user')
            out.add_attribute('.', 'name', '$6')
            user()

Skipping Values
~~~~~~~~~~~~~~~

::

    match /# .*[\r\n]/:
        do.skip()

Matching Multiple Values
~~~~~~~~~~~~~~~~~~~~~~~~

::

    match /# .*[\r\n]/
        | '/*' /[^\r\n]/ '*/' nl:
        do.skip()

Grammar Inheritance
~~~~~~~~~~~~~~~~~~~

A grammar that uses inheritance executes the inherited match statements
before trying it's own::

    grammar default:
        match nl:
            do.return()
        match ws:
            do.next()

    grammar user(default):
        match fieldname ':' ws value field_end:
            out.add('$0', '$3')

In this case, the *user* grammar inherits the whitespace rules from the
*default* grammar.
