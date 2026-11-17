//! Regression coverage for the extractor over a frozen console specification.
//!
//! The fixture is a write-once copy of `SPECIFICATION/history/v061`. Keeping
//! the extractor's ground truth here deliberately decouples it from live spec
//! revisions: a normative-clause change may update `SPECIFICATION/` without
//! requiring any `console-spec-check` test edit.

use std::path::Path;

use console_spec_check::extract_rules;

const FIXTURE_ROOT: &str = concat!(env!("CARGO_MANIFEST_DIR"), "/tests/data/frozen-spec/v061");

#[test]
fn extract_rules_matches_frozen_spec_v061_ground_truth() -> Result<(), Box<dyn std::error::Error>> {
    let root = Path::new(FIXTURE_ROOT);
    assert!(
        root.is_dir(),
        "frozen v061 ground-truth spec directory must exist: {}",
        root.display()
    );

    let cases = [
        ("spec.md", 22_usize),
        ("contracts.md", 163),
        ("constraints.md", 24),
        ("non-functional-requirements.md", 110),
    ];
    let mut total = 0;
    for (file, want) in cases {
        let text = std::fs::read_to_string(root.join(file))?;
        let count = extract_rules(file, &text).len();
        assert_eq!(count, want, "frozen clause count for {file}");
        total += count;
    }
    assert_eq!(total, 319, "frozen total normative clause count");
    Ok(())
}
