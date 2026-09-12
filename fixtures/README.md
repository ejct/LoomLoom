# Bootstrap fixtures

These cases are behavioral eval prompts for the bootstrap skill.

They are not deterministic unit tests of an LLM. They define expected routing/authority behavior to use during R1 dogfooding.

Run them against at least:

1. a new ChatGPT chat with connected Drive, when available;
2. a repository-aware coding agent;
3. an Agent Skills-compatible client;
4. portable/no-connected-source mode.

Record whether the resulting Context Receipt matches each expected disposition.
