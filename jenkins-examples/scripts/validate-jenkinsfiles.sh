#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

docs_paths="AGENTS.md GUIDE.md README.md scripts/validate-jenkinsfiles.sh"
if [ -f .gitignore ]; then
    docs_paths=".gitignore $docs_paths"
fi

all_jenkinsfiles="$(find . -mindepth 2 -maxdepth 2 -name Jenkinsfile | sort)"
jenkinsfiles="$(find . -mindepth 2 -maxdepth 2 -path './[0-9][0-9]-*/Jenkinsfile' | sort)"

if [ -z "$all_jenkinsfiles" ]; then
    echo "No Jenkinsfile examples found."
    exit 1
fi

if [ "$all_jenkinsfiles" != "$jenkinsfiles" ]; then
    echo "Every Jenkinsfile must live at NN-topic-name/Jenkinsfile."
    find . -mindepth 2 -maxdepth 2 -name Jenkinsfile ! -path './[0-9][0-9]-*/Jenkinsfile' -print
    exit 1
fi

example_count="$(printf '%s\n' "$jenkinsfiles" | sed '/^$/d' | wc -l | tr -d ' ')"
echo "Found ${example_count} Jenkinsfile examples."

echo "Checking example numbering..."
expected=1
printf '%s\n' "$jenkinsfiles" | while IFS= read -r file; do
    [ -n "$file" ] || continue

    dir="${file#./}"
    dir="${dir%%/*}"
    number="${dir%%-*}"
    current=$((10#$number))

    if [ "$current" -ne "$expected" ]; then
        printf 'Expected example %02d but found %s (%s).\n' "$expected" "$number" "$file"
        exit 1
    fi

    expected=$((expected + 1))
done

echo "Checking Jenkinsfile structure..."
printf '%s\n' "$jenkinsfiles" | while IFS= read -r file; do
    [ -n "$file" ] || continue

    if ! grep -Eq '^[[:space:]]*pipeline[[:space:]]*\{' "$file"; then
        echo "${file}: missing top-level pipeline block."
        exit 1
    fi

    if ! grep -Eq '^[[:space:]]*agent[[:space:]]+' "$file"; then
        echo "${file}: missing agent directive."
        exit 1
    fi

    if ! grep -Eq '^[[:space:]]*stages[[:space:]]*\{' "$file"; then
        echo "${file}: missing stages block."
        exit 1
    fi
done

echo "Checking whitespace and merge markers..."
for file in $docs_paths $jenkinsfiles; do
    [ -f "$file" ] || continue

    if grep -n '[[:blank:]]$' "$file"; then
        echo "${file}: trailing whitespace found."
        exit 1
    fi

    if grep -n $'\r' "$file"; then
        echo "${file}: CRLF line ending found."
        exit 1
    fi

    if grep -nE '^(<<<<<<<|=======|>>>>>>>)' "$file"; then
        echo "${file}: merge conflict marker found."
        exit 1
    fi
done

if [ -n "${JENKINS_URL:-}" ] && [ -n "${JENKINS_CLI_JAR:-}" ]; then
    if [ ! -f "$JENKINS_CLI_JAR" ]; then
        echo "JENKINS_CLI_JAR does not exist: ${JENKINS_CLI_JAR}"
        exit 1
    fi

    echo "Running Jenkins Declarative Linter..."
    printf '%s\n' "$jenkinsfiles" | while IFS= read -r file; do
        [ -n "$file" ] || continue
        echo "Linting ${file}"
        java -jar "$JENKINS_CLI_JAR" -s "$JENKINS_URL" declarative-linter < "$file"
    done
else
    echo "Skipping Jenkins Declarative Linter."
    echo "Set JENKINS_URL and JENKINS_CLI_JAR to enable full Jenkinsfile validation."
fi
