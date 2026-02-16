---
title: "Python and SublimeText"
date: 2017-10-10T11:39:00.003Z
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

Function hints and autofill of function parameters - notes to help me out in the future.

Install the SublimeText Anaconda Package (not the Python distribution Anaconda).

The Python Improved package and the Neon Color Scheme provide nice Python typing support

When using Docker, Anaconda doesn't necessarily know where the python package your are editing is so you need to help it by adding the following into the SublimeText Project settings (Project -> Edit Project). Note you can't open up the .sublime-project file using SublimeText as it will just keep opening up the Project and not the file. Add in the settings with the top folder of the python package:

```
"settings": {
        "extra_paths":
        [
            ""
        ]
    }
```

Also, make sure you add the python modules using pip that you are using in the Docker python system to the python interpreter (you can also use a virtual env for the project and that should be added to the SublimeText project.
You should now have function and method hints from your project and any additional python modules you are using.
My Anaconda user settings:

```
{
    "python_interpreter": "/opt/local/bin/python",
    /*
        If complete_parameters is true, anaconda will add function and class
        parameters to its completions.

        If complete_all_parameters is true, it will add all the possible
        parameters, if it's false, it will add only required parameters
    */
    "complete_parameters": true,
    "complete_all_parameters": false,

    // If true, anaconda draws gutter marks on line with errors
    "anaconda_gutter_marks": true,

    // Inline error messages by inserting extra lines as needed
    "anaconda_linter_phantoms": false,

    /*

        If anaconda_gutter_marks is true, this determines what theme is used.
        Theme 'basic' only adds dots and circles to gutter.

        Other available themes are 'alpha', 'bright', 'dark', 'hard' and
        'simple'. To see icons that will be used for each theme check
        gutter_icon_themes folder in Anaconda package.
    */
    "anaconda_gutter_theme": "bright",

    /*
        If 'outline' (default) anaconda will outline error lines
        If 'fill' anconda will fill the lines
        If 'none' anaconda will not draw anything on error lines
    */
    "anaconda_linter_mark_style": "outline",

    /*
        A list of pep8 error numbers to ignore. By default "line too long" errors are ignored.
        The list of error codes is in this file: https://github.com/jcrocholl/pep8/blob/master/pep8.py.
        Search for "Ennn:", where nnn is a 3-digit number.
    */
    "pep8_ignore": [
        "E127", "E128", "E501", "E402"
    ],

    "anaconda_linter_mark_style": "outline",

    /*
        Set the following option to true if you want anaconda to check
        the validity of your imports when the linting process is fired.

        WARNING: take into account that anaconda compiles and import the
        modules in the JsonServer memory segment in order to check this
    */
    "validate_imports": false,

    /*
        MyPy

        Set the following option to true to enable MyPy checker.
    */
    "mypy": false,

    /*
        Command to execute tests with. nosetests by default
    */
    "test_command": "py.test",

    // Maximum line length for pep8
    "pep8_max_line_length": 79

}
```
