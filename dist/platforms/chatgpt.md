# ChatGPT

Two ways to install, depending on whether you want one assistant or six.

## One GPT for the whole chain (recommended)

1. **Explore GPTs → Create**.
2. Paste `../instructions/spec-writer.md` into **Instructions**.
3. Under **Knowledge**, upload `../universal/spec-writer-complete.md`.
4. Enable **Web Browsing** (the MRD stage needs it) and **Code Interpreter** (so it can hand back a real `.md` file instead of a chat block).

## A separate GPT per document

Same steps, but paste `../instructions/<name>.md` and upload the matching `../universal/<name>.md`.

## Projects

Paste `../universal/spec-writer-complete.md` into the project instructions, or attach it as a project file. Every chat in the project inherits it.

## Plain chat

Paste `../universal/<name>.md`, then your idea as the next message.

Without Code Interpreter, ChatGPT can't write a file — the output contract's tier 3 handles this: it emits the whole document in one fenced Markdown block, named, ready to save as `.md`.
