# How to Contribute

Following these guidelines helps keep the project maintainable, easy to contribute to, and more secure.
Thank you for taking the time to read this.

## Where To Start

There are many ways to contribute.
You can fix a bug, improve the documentation, submit feature requests and issues, or work on a feature you need for yourself.

Pull requests are necessary for all contributions of code, documentation, or examples.
If you are new to open source and not sure what a pull request is ... welcome, we're glad to have you!
All of us once had a contribution to make and didn't know where to start.

Even if you don't write code for your job, don't worry, the skills you learn during your first contribution to open source can be applied in so many ways, you'll wonder what you ever did before you had this knowledge.
Here are a few resources on how to contribute to open source for the first time.

- [First Contributions](https://github.com/firstcontributions/first-contributions/blob/master/README.md)
- [Public Learning Paths](https://lab.github.com/githubtraining/paths)

## Pull Requests

- Make a pull request from your own fork of this repository
- Please use clear commit messages, so everyone understands what each commit does
- Validate your code using `pylint` as per below, and test your changes
- We might offer feedback or request modifications before merging


```
pylint pc_lib/*.py pc_lib/*/*.py scripts/*.py
```