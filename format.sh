black nr_vocabularies tests --target-version py310
autoflake --in-place --remove-all-unused-imports --recursive nr_vocabularies tests
isort nr_vocabularies tests  --profile black
