Contributing to this repository
======================

I have written this package mainly as a gift to the SETI community, in the hope they find it a useful tool for simulating scenarios appropriate to their work.  I suspect that as time goes on, I will no longer be the sole owner of the repository, and that its maintenance may pass to other people.

If you want to use it and contribute to its development, here are the following steps that I'd like you to take:

1.  Create an issue on the github repository 
2.  Fork the repository on github,
3.  Create a branch and produce the code changes to your satisfaction
4.  Submit a pull request (tagging the issue number)

At the moment, I (@dh4gan) will be the arbiter of what pull requests are accepted, but that may change (and the CONTRIBUTING.md file should be changed appropriately).

Code Style
-------------

Where possible, I have tried to adopt a consistent naming scheme where possible:

1. File names are written in lower case,
2. Class names are written in CamelCase
3. Methods are written using '_' for spaces, and all keyword arguments are given default values.  Not doing so can cause nasty TypeError messages when attempting to add None to something.
4. Indentation is with tabs (I know, I know).
5. Docstrings are written with PEP8 in mind.  Please follow the conventions within the code as possible.
