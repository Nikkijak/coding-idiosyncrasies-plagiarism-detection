import pygments.token
from pygments.lexers import JavaLexer, guess_lexer_for_filename


def tokenize(filename, include_classes=True, include_methods=True, handle_scope=True):
    """ Perform lexical tokenization and normalization on a source code file.
    The output of this function is a normalized token stream that is used in later stages."""

    # Reading the source file
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    # Choosing a lexer based on file type
    if filename.endswith(".java"):
        lexer = JavaLexer()
    else:
        lexer = guess_lexer_for_filename(filename, text)

    tokens = list(lexer.get_tokens(text))
    result = []

    total_tokens = len(tokens)
    original_pos = 0
    processed_pos = 0
    scope_stack = []

    for i in range(total_tokens):
        token_type = tokens[i][0]
        token_value = tokens[i][1]

        # Normalize control structures
        if token_type == pygments.token.Keyword:
            if token_value in ["if", "else", "for", "while", "switch"]:
                result.append(("CTRL_STRUCT", original_pos, processed_pos))

        # Normalize identifiers that are not function calls
        elif token_type == pygments.token.Name and i != total_tokens - 1 and tokens[i + 1][1] != "(":
            if handle_scope and scope_stack:
                result.append((f"N_{scope_stack[-1]}", original_pos, processed_pos))
            else:
                result.append(("N", original_pos, processed_pos))
            processed_pos += 1

        # Normalize string literals
        elif token_type in pygments.token.Literal.String:
            result.append(("S", original_pos, processed_pos))
            processed_pos += 1

        # Normalize function or method names
        elif include_methods and token_type in pygments.token.Name.Function:
            result.append(("F", original_pos, processed_pos))
            processed_pos += 1

        # Normalize class names
        elif include_classes and token_type in pygments.token.Name.Class:
            result.append(("C", original_pos, processed_pos))
            processed_pos += 1

        # Normalize numeric literals
        elif token_type in pygments.token.Literal.Number:
            result.append(("NUM", original_pos, processed_pos))
            processed_pos += len(token_value)

        # Normalize operators
        elif token_type in pygments.token.Operator:
            result.append(("OP", original_pos, processed_pos))
            processed_pos += len(token_value)

        # Normalize punctuation
        elif token_type in pygments.token.Punctuation:
            result.append(("PUNC", original_pos, processed_pos))
            processed_pos += len(token_value)

        # Ignoring whitespace and comments
        elif token_type == pygments.token.Text or token_type in pygments.token.Comment:
            pass

        # Keeping remaining tokens as-is
        else:
            result.append((token_value, original_pos, processed_pos))
            processed_pos += len(token_value)

        original_pos += len(token_value)

        # Tracking scope for brace-based languages
        if handle_scope:
            if token_value == "{":
                scope_stack.append(processed_pos)
            elif token_value == "}":
                if scope_stack:
                    scope_stack.pop()

    return result


def toText(arr):
    """Convert normalized tokens into a single string."""
    return "".join(str(x[0]) for x in arr)


if __name__ == "__main__":
    pass