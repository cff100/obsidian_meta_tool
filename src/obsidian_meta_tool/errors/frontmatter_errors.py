
class FrontamatterError(Exception):
    """Base class for all frontmatter related errors."""
    pass



class NoLinesError(FrontamatterError):
    """Raised when the file has no lines to process."""
    pass

class NoFrontmatterError(FrontamatterError):
    """Raised when there is no frontmatter in the file."""
    pass

class UnclosedFrontmatterError(FrontamatterError):
    """Raised when the frontmatter of the file is not properly closed."""
    pass

class EmptyFrontmatterError(FrontamatterError):
    """Raised when the frontmatter of the file is empty (no values between the '---' markers)."""
    pass