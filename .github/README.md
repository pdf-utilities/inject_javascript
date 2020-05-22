# Inject JavaScript
[heading__top]:
  #inject_javascript
  "&#x2B06; Inject JavaScript within PDF document body"


Inject JavaScript within PDF document body


## [![Byte size of Inject_javascript][badge__master__inject_javascript__source_code]][inject_javascript__master__source_code] [![Open Issues][badge__issues__inject_javascript]][issues__inject_javascript] [![Open Pull Requests][badge__pull_requests__inject_javascript]][pull_requests__inject_javascript] [![Latest commits][badge__commits__inject_javascript__master]][commits__inject_javascript__master]


------


- [:arrow_up: Top of Document][heading__top]

- [:building_construction: Requirements][heading__requirements]

- [:zap: Quick Start][heading__quick_start]

- [&#x1F5D2; Notes][heading__notes]

- [:card_index: Attribution][heading__attribution]

- [:balance_scale: Licensing][heading__license]


___


## Requirements
[heading__requirements]:
  #requirements
  "&#x1F3D7; Prerequisites and/or dependencies that this project needs to function properly"


> Note, the following steps are **not** required if installing this project via Pip.


Python version 3 based dependencies may be installed via one of the following methods...


- Scoped within current user...


```Bash
pip3 install --user -r requirements.txt
```


- Scoped with a _Virtual Environment_ local to the directory of this project...


```Bash
pip3 install --user pipenv

pipenv install -r requirements.txt
```


> Note, review [Python Guide -- `virtualenvs`](https://docs.python-guide.org/dev/virtualenvs/) for more information on Python Virtual Environments.


- Or scopped for the entire system...


```Bash
sudo pip3 install -r requirements.txt
```


> Note, generally installing dependencies system-wide is **not** recommended.


___


## Quick Start
[heading__quick_start]:
  #quick-start
  "&#9889; Perhaps as easy as one, 2.0,..."


Install this project via Pip


```Bash
pip3 install --user --upgrade inject-javascript
```


------


**Examples of running as command-line utility**


- Print available options and exit


```Bash
inject-pdf-javascript --help
```


- Inject `.js` into `.pdf` and save to `.pdf`


```Bash
inject-pdf-javascript --js index.js\
 --pdf document.pdf\
 --save-path enhanced.pdf\
 --escape
```


- Inject `.js` into `.pdf` and overwrite `.pdf`


```Bash
inject-pdf-javascript --js index.js\
 --pdf document.pdf\
 --escape\
 --clobber
```


------


Example of inheriting and modifying the `Inject_JavaScript` class...


```Python
#!/usr/bin/env python3


from argparse import ArgumentParser


from inject_javascript import Inject_JavaScript
from inject_javascript.lib import error


class Customized_Inject_JavaScript(Inject_JavaScript):
    """
    Customizes Inject_JavaScript class
    """

    def return_js_data(self, js_path = None):
        """
        Customizes how JavaScript data is processed prior to returning
        """
        js_data = super(Customized_Inject_JavaScript, self).return_js_data(js_path = js_path)

        return js_data


if __main__ == '__name__':
    """
    Code that is run if this file is executed as a script instead of imported
    """
    ## Command line argument parsing only if being called as a script

      arg_parser = ArgumentParser(
          prog = basename(argv[0]),
          usage = '%(prog)s --pdf "/tmp/boring.pdf" --js "/dir/script.js"',
          epilog = 'For more projects see: https://github.com/S0AndS0')

      arg_parser.add_argument('--pdf-path', '--pdf',
                              help = 'Out path to save PDF',
                              required = True)

      arg_parser.add_argument('--js-path', '--js',
                              help = 'JavaScript to inject into downloaded PDF',
                              required = True)

      arg_parser.add_argument('--save-path',
                              help = 'Path to save enhanced PDF to, ignored if clobber is True')

      arg_parser.add_argument('--escape',
                              help = 'Prevent replacing/escaping of specific character combos',
                              action = 'store_true',
                              default = False)

      arg_parser.add_argument('--clobber',
                              help = 'Overwrite preexisting/input PDF',
                              action = 'store_true',
                              default = False)

      arg_parser.add_argument('--verbose', '-v',
                              help = 'Loudness of this script',
                              action = 'count')

      verbose = arg_parser.parse_known_args()[0].verbose
      args = vars(arg_parser.parse_args())

      ## Use provided command line options
      injector = Customized_inject_javascript(clobber = args.get('clobber'),
                                              escape = args.get('escape'),
                                              verbose = verbose)

      injected_path = injector.inject_pdf_with_javascript(pdf_path = args.get('pdf_path'),
                                                          js_path = args.get('js_path'),
                                                          save_path = args.get('save_path'))

      if verbose > 0:
          print('Enhanced file maybe found at: {0}'.format(injected_path))
```


___


## Notes
[heading__notes]:
  #notes
  "&#x1F5D2; Additional things to keep in mind when developing"


The `inject_javascript.py` script currently is limited to injecting JavaScript into the document body of PDF file(s), which means certain APIs are **not** available such as `request`. Please submit a Pull Request for injecting folder level script features if additional API functionality is desired.


------


The `--escape` command-line option will _double-down_ on backslashes (`\`), for example...


```JavaScript
if (typeof app !== 'undefined') {
  var script_context = 'pdf';
} else {
  var script_context = 'browser';
};

if (script_context === 'pdf') {
  window.alert('Script context is -> PDF\nExpect features to be limited.');
} else {
  window.alert('Script context is -> Browser\nExpect features to _mostly_ be available.')
}
```


... the above code if injected with the `--escape` option would result in the following changes...


```JavaScript
var script_context = typeof app !== 'undefined' ? 'pdf' : 'browser';

if (script_context === 'pdf') {
  window.alert('Script context is -> PDF\\nExpect features to be limited.');
} else {
  window.alert('Script context is -> Browser\\nExpect features to _mostly_ be available.')
}
```


... while the default behavior of `inject_javascript.py` is to **not** add additional backslashes, generally such modifications are required for JavaScript to run properly within PDF(s).


------


Adobe Acrobat PDF readers as of last documentation checks run JavaScript based on version 1.5 of ISO-16262 (ECMA-262 Edition 3 from December 1999), meaning that some newer ECMA Script features may not be available, thus it may be a good idea to utilize a JavaScript transpiler such as TypeScript.


**`tsconfig.json`**


```JSON
{
  "compilerOptions": {
    "target": "es3",
    "module": "none",
    "lib": ["dom","es5"],
    "locale": "en-US",
    "noImplicitAny": false,
    "sourceMap": true,
    "outDir": "js"
  },
  "exclude": [
    "node_modules"
  ],
  "files": [
    "ts/index.ts"
  ]
}
```


> Note, above example configurations may transpile JavaScript of a version that is higher than supported by PDF readers of your target audience.


**`ts/index.ts`**


```TypeScript
let hello = (arg: string) => {
  window.alert(`Hello ${arg}!`);
};

hello('world');
```

**`js/index.js`**


```JavaScript
var hello = function (arg) {
    window.alert("Hello " + arg + "!");
};
hello('world');
//# sourceMappingURL=index.js.map
```


___


## Attribution
[heading__attribution]:
  #attribution
  "&#x1F4C7; Resources that where helpful in building this project so far."


  - [Adobe -- `JavaScript for Acrobat`](https://www.adobe.com/devnet/acrobat/javascript.html)

- [GitHub -- `github-utilities/make-readme`](https://github.com/github-utilities/make-readme)

- [Mozilla Developer -- `New in JavaScript 1.5`](https://developer.mozilla.org/en-US/docs/Archive/Web/JavaScript/New_in_JavaScript/1.5)

- [TypeScript -- `Compiler Options`](https://www.typescriptlang.org/docs/handbook/compiler-options.html)

- [YouTube -- Omar Rizwan (@rsnous)](https://www.youtube.com/watch?v=QEZ0N0rrbL0&t=3h59m)



___


## License
[heading__license]:
  #license
  "&#x2696; Legal side of Open Source"


```
Documentation for injecting JavaScript within PDF document body
Copyright (C) 2020 S0AndS0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```


For further details review full length version of [AGPL-3.0][branch__current__license] License.



[branch__current__license]:
  /LICENSE
  "&#x2696; Full length version of AGPL-3.0 License"


[badge__commits__inject_javascript__master]:
  https://img.shields.io/github/last-commit/pdf-utilities/inject_javascript/master.svg

[commits__inject_javascript__master]:
  https://github.com/pdf-utilities/inject_javascript/commits/master
  "&#x1F4DD; History of changes on this branch"


[inject_javascript__community]:
  https://github.com/pdf-utilities/inject_javascript/community
  "&#x1F331; Dedicated to functioning code"

[inject_javascript__gh_pages]:
  https://github.com/pdf-utilities/inject_javascript/tree/
  "Source code examples hosted thanks to GitHub Pages!"

[badge__gh_pages__inject_javascript]:
  https://img.shields.io/website/https/pdf-utilities.github.io/inject_javascript/index.html.svg?down_color=darkorange&down_message=Offline&label=Demo&logo=Demo%20Site&up_color=success&up_message=Online

[gh_pages__inject_javascript]:
  https/pdf-utilities.github.io/inject_javascript/index.html
  "&#x1F52C; Check the example collection tests"

[issues__inject_javascript]:
  https://github.com/pdf-utilities/inject_javascript/issues
  "&#x2622; Search for and _bump_ existing issues or open new issues for project maintainer to address."

[pull_requests__inject_javascript]:
  https://github.com/pdf-utilities/inject_javascript/pulls
  "&#x1F3D7; Pull Request friendly, though please check the Community guidelines"

[inject_javascript__master__source_code]:
  https://github.com/pdf-utilities/inject_javascript/
  "&#x2328; Project source!"

[badge__issues__inject_javascript]:
  https://img.shields.io/github/issues/pdf-utilities/inject_javascript.svg

[badge__pull_requests__inject_javascript]:
  https://img.shields.io/github/issues-pr/pdf-utilities/inject_javascript.svg

[badge__master__inject_javascript__source_code]:
  https://img.shields.io/github/repo-size/pdf-utilities/inject_javascript
