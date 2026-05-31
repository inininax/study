# Repository Guidelines

## Project Structure & Module Organization

This repository is a beginner-focused Jenkins Pipeline examples collection. Each numbered directory contains one standalone `Jenkinsfile`:

- `01-hello-world/` through `08-docker-pipeline/`: progressive Declarative Pipeline examples.
- `README.md`: learning order, glossary, and basic usage.
- `GUIDE.md`: Jenkins Pipeline syntax and beginner reference.

There is no application source tree, package manifest, or shared test suite. Keep new examples in the existing pattern: `NN-topic-name/Jenkinsfile`, where `NN` preserves the learning sequence.

## Build, Test, and Development Commands

There is no repository-level build command. Validate examples with Jenkins or Jenkins tooling:

- `rg --files`: list all tracked example and documentation files.
- `rg "stage\\(" */Jenkinsfile`: review stage names across examples.
- `scripts/validate-jenkinsfiles.sh`: check whitespace issues and optionally run the Jenkins Declarative Linter.
- `java -jar jenkins-cli.jar -s http://localhost:8080/ declarative-linter < 01-hello-world/Jenkinsfile`: lint a Jenkinsfile against a running Jenkins controller with the Pipeline plugins installed.
- In Jenkins UI: create a Pipeline job, paste an example `Jenkinsfile`, then run **Build Now**.

For Docker-related examples, confirm Docker is available with `docker --version` before demonstrating real Docker commands.

## Coding Style & Naming Conventions

Use Declarative Pipeline syntax unless an example explicitly teaches another pattern. Indent Groovy blocks with 4 spaces, keep braces on the same line as declarations, and prefer readable stage names such as `Build`, `Test`, and `Docker Push`. Use `UPPER_SNAKE_CASE` for environment variables, for example `DOCKER_IMAGE` or `BUILD_OUTPUT_DIR`.

Comments may be instructional, but keep them focused on what the example teaches. Use single-line `sh 'command'` steps for simple commands, triple single-quoted shell blocks for literal multi-line scripts, and triple double quotes only when Groovy interpolation is required.

## Testing Guidelines

Before changing or adding a `Jenkinsfile`, run it through the Jenkins Declarative Linter or execute it in a disposable Pipeline job. Check both syntax and console output. For examples that simulate work, keep commands harmless and portable, such as `echo`, `mkdir -p`, and version checks.

## Commit & Pull Request Guidelines

The current history only contains `init`, so use concise imperative commit subjects going forward, for example `Add post actions example` or `Clarify Docker pipeline comments`.

Pull requests should describe the learning goal, list changed example directories, and note how the Jenkinsfile was validated. Include screenshots or console excerpts when behavior changes in Jenkins UI output.
