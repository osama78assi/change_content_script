# Long Story Short
What I hate and everyone hate is refactoring it's annoying and costs a lot of time. While there are many tools and ways in text editors to help you change something like quick fixs or even match by Regex. There is small things that theses **Can't** do. And maybe you have a lot of files with the same things to change

# Simple Script
This may not be the perfect script. and it **shouldn't** be. but it was **very helpful** with me so maybe someone can use it.

This simple script can read all files in passed directory (recursivly if you want) and replace what ever you want by whatever you want also

in my simple case. I have a code in nodeJs with *CommonJs modules* and it has something like this

```js
const { Request, Response } = require("express");

/**
 *
 * @param {Request} req
 * @param {Response} res
 */
async function controller(req, res, next) {
    try {
        
    } catch(err) {
        next(err);
    }
}

module.export = controller;
```

to replace that there is a quick fix but unfortunately it can't help you. But why ?

it will make it

```js
import { Request, Response } from "express";

/**
 *
 * @param {Request} req
 * @param {Response} res
 */
async function controller(req, res, next) {
    try {
        
    } catch(err) {
        next(err);
    }
}

export default controller;
```

But that throws an **error** with me

```
import { Request, Response } from "express";
         ^^^^^^^
SyntaxError: Named export 'Request' not found. The requested module 'express' is a CommonJS module, which may n
CommonJS modules can always be imported via the default export, for example using:

import pkg from 'express';
const { Request, Response } = pkg;

```

and simpply I don't want to load entire **express** module just for types!

so I will go with simple solution **CHANGE IT.** But that will take time. A lot of time and I have a lot of files. that's annoying simply.

So I said what if I have something that read these files and change what I want ?

let's get over with. I added the script file in **my root directory**
and wrote this in it. Run it and call it a day

```py

def repl(match: Match[str]):
    # Change the Request type
    if match.group(0).startswith("@param {Req"):
        return '@param {import(\'express\').Request} req'
    # Change the Response type
    if match.group(0).startswith("@param {Res"):
        return '@param {import(\'express\').Response} res'
    # Remove the require
    if match.group(0).startswith("const { Request"):
        return ""
    # Export default
    if match.group(0).startswith("module"):
        return 'export default' + ' ' + match.group(0).split('=')[1]
    # For safety if we matched something by mistake
    return match.group(0)


change_text_from_files(
    rec_read_all_files_paths(ignore=['node_modules'], wanted_exts='js'),
    r'(@param\s*\{\w+\d*\}\s*\w+\d*|const\s*\{\s*Request,\s*Response\s*\}\s*=\s*require\("express"\);\n|module\.export\s*=\s*\w+\d*)',
    repl
)


```
so the result become

```js


/**
 *
 * @param {import('express').Request} req
 * @param {import('express').Response} res
 */
async function controller(req, res, next) {
    try {
        
    } catch(err) {
        next(err);
    }
}

export default controller;
```

### Simple Use Cases

1. When you want some directory not is the root you can pass it with extension. while the default is current working directory

```py
rec_read_all_files_paths(dir_path="testingMyScript", wanted_exts='js')
```

or extensions

```py
rec_read_all_files_paths(wanted_exts=['js', 'ts'])
```

2. In case you want to exclude some files/folders like node_modules

```py
rec_read_all_files_paths(ignore=['node_modules', 'keepItSafe.js', 'dontTouchIt.ts'], wanted_exts=['js', 'ts'])
```

3. If (for some reason) you want to touch hidden files. this script by default doesn't touch them like ignoring **.git** folder (because it has a lot of files that I don't need to do anything with them). but you can enable it

```py
rec_read_all_files_paths(wanted_exts='py', skip_hidden=False)
```

4. When you want just to get files paths from a directory

```py
paths = read_files_paths_from_dir(wanted_exts=['js', 'txt'])
```

5. In case you want to see all the paths in all nested directories

```py
# For reading files in all directories
for path in rec_read_all_file_paths(ignore=['node_modules'], wanted_exts=['js', 'txt']):
    print(path)
```

6. When you want just to do it for a file

```py
# Change in one file. one thing
change_text_from_file(
    r'F:\my_files\myDir\test.js',
    r'(@param \{Request\} req)',
    '@param {import(\'express\').Request} req'
)
```

7. When **find references** get crashed in my VS code I get depressed and especially when my project is large a bit. So this function just find the references for a variable, method or class you want in the provided file paths
```py
# Get all files in my current working directory
files = rec_read_all_files_paths(ignore=['node_modules'], wanted_exts='js')

# Check for authRouter variable
res = check_references(files, "authRouter")

for r in res:
    print(r) # authRouter in file F:\test\app.js in line 9
```

btw If you want to make updates or improvements to the code in this repo, feel free to make your changes and open a pull request.

Also, if you have any ideas or suggestions, you're welcome to implement them and submit a PR!
