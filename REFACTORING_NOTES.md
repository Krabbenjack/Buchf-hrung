# Refactoring Notes

## Code Review Findings

The code review identified 2 potential issues in `src/ui.py`:

1. **Line 282**: `lfd_nr=self.index + 2` calculation
2. **Lines 285-289**: Booking update/add logic condition

### Important Note
These issues **existed in the original `buchung.py` file** and were preserved during the refactoring as per the requirement:

> "This is a refactor, not a rewrite. Preserve all existing features."

The refactoring successfully separated concerns without changing behavior. The identified issues are pre-existing and were not introduced by this refactoring.

## Recommendation
If these issues need to be addressed, they should be fixed in a separate PR after the refactoring is merged, to maintain a clear separation between:
1. Structural refactoring (this PR)
2. Bug fixes (future PR)

This approach ensures:
- Clear git history
- Easy to verify refactoring didn't break anything
- Easier to review bug fixes separately

## What Was Changed vs. Preserved

### Changed (Structural Only)
- Split monolithic `buchung.py` into separate modules
- Converted `konten.py` to `konten.json`
- Updated imports across all modules
- No logic changes, only code organization

### Preserved (Exact Behavior)
- All UI behavior
- All business logic
- All data formats
- All existing issues/quirks
- All functionality
