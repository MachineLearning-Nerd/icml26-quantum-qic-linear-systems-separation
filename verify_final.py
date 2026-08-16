#!/usr/bin/env python3
"""Fail-closed structural checks for the quantum/QIC separation audit."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EXPECTED_REPOSITORY = (
    "MachineLearning-Nerd/"
    "icml26-quantum-qic-linear-systems-separation"
)
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = (
    "37579156+MachineLearning-Nerd@users.noreply.github.com"
)
EXPECTED_PDF_SHA = (
    "581d57e998439c2ad73b68f02dcf62fb3a54c655f6d8903c4767de2ce3968a70"
)
EXPECTED_SOURCE_ARCHIVE_SHA = (
    "1729ecf6489a345ff10b6433ce8256a9bc88028dcf68b469e0dd2de50e223eb6"
)
EXPECTED_CONTRACT_SHA = (
    "a5fe8f32a92be2d7bda9647535221a7d551b0f7cf76cb40c082340f1d4fe499f"
)
EXPECTED_BRANCHES = {"main"}
EXPECTED_CLAIMS = {
    "C1": "TOY",
    "C2": "UNVERIFIED",
    "C3": "UNVERIFIED",
    "C4": "UNVERIFIED",
    "C5": "UNVERIFIED",
}
REQUIRED_FILES = {
    "README.md",
    "STATUS.md",
    "REPORT.md",
    "CLAIM_EVIDENCE.md",
    "SOURCE_AUDIT.md",
    "BRANCH_AUDIT.md",
    "ENVIRONMENT.md",
    "AUTHOR_THANK_YOU.md",
    "CITATION.cff",
    "claims.json",
    "EVIDENCE_MANIFEST.json",
    "verify_final.py",
    "AUTONOMOUS_STATE.json",
}
EXPECTED_AUDIT_FILES = REQUIRED_FILES - {"AUTONOMOUS_STATE.json"}
EXPECTED_EVIDENCE_FILES = {
    "contract/challenge_readme.md",
    "contract/metadata.json",
    "contract/live_claims.json",
    "contract/contract_manifest.json",
    "evidence/source/SHA256SUMS",
    "evidence/source/arxiv.pdf",
    "evidence/source/arxiv_source.tar.gz",
    "evidence/source/source_inventory.txt",
    "outputs/claim1_source_audit/SHA256SUMS",
    "outputs/claim1_source_audit/result.json",
    "outputs/claim1_random_walk_oracle_fixture/SHA256SUMS",
    "outputs/claim1_random_walk_oracle_fixture/config.json",
    "outputs/claim1_random_walk_oracle_fixture/results.csv",
    "outputs/claim1_random_walk_oracle_fixture/summary.json",
    "outputs/claim1_random_walk_oracle_fixture/run.log",
    "src/claim1_source_audit.py",
    "src/claim1_random_walk_oracle_fixture.py",
    "tests/test_claim1_random_walk_oracle.py",
    "tests/test_contract.py",
    "logbook/claim-1.md",
    "requirements.txt",
}
EXPECTED_EVIDENCE_DIRS = {
    "contract",
    "evidence/source",
    "outputs/claim1_source_audit",
    "outputs/claim1_random_walk_oracle_fixture",
    "src",
    "tests",
    "logbook",
}
CONTENT_ADDRESSED_PATHS = {
    *EXPECTED_AUDIT_FILES - {"EVIDENCE_MANIFEST.json"},
    "branch-audit.md",
    *EXPECTED_EVIDENCE_FILES,
}


def fail(message: str) -> None:
    raise AssertionError(message)


def run(*args: str) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def read_json(relative_path: str) -> object:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(relative_path: str) -> str:
    digest = hashlib.sha256()
    with (ROOT / relative_path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def local_branches() -> set[str]:
    refs = run(
        "git",
        "for-each-ref",
        "refs/heads",
        "--format=%(refname:strip=2)",
    )
    return {ref.strip() for ref in refs.splitlines() if ref.strip()}


def remote_branches() -> set[str]:
    prefix = "refs/remotes/origin/"
    refs = run(
        "git",
        "for-each-ref",
        "refs/remotes/origin",
        "--format=%(refname)",
    )
    return {
        ref.strip()[len(prefix):]
        for ref in refs.splitlines()
        if ref.strip().startswith(prefix)
        and ref.strip() != prefix + "HEAD"
    }


def verify_remote() -> None:
    remote = run("git", "config", "--get", "remote.origin.url").strip()
    normalized = remote.removesuffix(".git").rstrip("/")
    if not normalized.endswith(EXPECTED_REPOSITORY):
        fail(f"origin is {remote!r}, expected {EXPECTED_REPOSITORY!r}")


def verify_branch_tips() -> None:
    if remote_branches() != EXPECTED_BRANCHES:
        fail(f"remote branch set is {sorted(remote_branches())!r}")
    local = local_branches()
    if "main" not in local:
        fail("local main branch is missing")
    remote_tip = run(
        "git",
        "rev-parse",
        "refs/remotes/origin/main",
    ).strip()
    local_tip = run("git", "rev-parse", "refs/heads/main").strip()
    if local_tip != remote_tip:
        fail("local main and origin/main tips differ")
    head = run("git", "symbolic-ref", "refs/remotes/origin/HEAD").strip()
    if head != "refs/remotes/origin/main":
        fail(f"origin HEAD is {head!r}, expected origin/main")


def verify_history() -> None:
    records = run(
        "git",
        "log",
        "--all",
        "--format=%an%x00%ae%x00%cn%x00%ce",
    ).splitlines()
    if not records:
        fail("no reachable commits")
    expected = (
        f"{CANONICAL_NAME}\x00{CANONICAL_EMAIL}\x00"
        f"{CANONICAL_NAME}\x00{CANONICAL_EMAIL}"
    )
    unexpected = sorted({record for record in records if record != expected})
    if unexpected:
        fail(f"non-canonical reachable identities: {unexpected}")
    if "co-authored-by:" in run("git", "log", "--all", "--format=%B").lower():
        fail("co-author trailer found")
    if int(run("git", "rev-list", "--count", "--all").strip()) < 11:
        fail("historical evidence commits are missing")
    if run(
        "git",
        "for-each-ref",
        "refs/original",
        "--format=%(refname)",
    ).strip():
        fail("temporary refs/original remain")
    refs = run("git", "for-each-ref", "--format=%(refname)").splitlines()
    if any("orx/" in ref or ref.endswith("/orx") for ref in refs):
        fail("legacy orx ref remains")


def verify_manifest() -> None:
    manifest = read_json("EVIDENCE_MANIFEST.json")
    if not isinstance(manifest, dict):
        fail("manifest must be a JSON object")
    if manifest.get("repository") != EXPECTED_REPOSITORY:
        fail("manifest repository marker is wrong")
    if manifest.get("claim_statuses") != EXPECTED_CLAIMS:
        fail("manifest claim statuses are wrong")
    if set(manifest.get("required_audit_files", [])) != EXPECTED_AUDIT_FILES:
        fail("manifest audit-file list is wrong")
    if set(manifest.get("required_evidence_files", [])) != EXPECTED_EVIDENCE_FILES:
        fail("manifest evidence-file list is wrong")
    if set(manifest.get("required_evidence_directories", [])) != EXPECTED_EVIDENCE_DIRS:
        fail("manifest evidence-directory list is wrong")
    branches = manifest.get("branches", {})
    if set(branches.get("expected_final", [])) != EXPECTED_BRANCHES:
        fail("manifest branch set is wrong")
    if branches.get("historical_remote_branch_count") != 1:
        fail("manifest historical branch count is wrong")
    if branches.get("legacy_prefixes_removed") != ["orx/"]:
        fail("manifest legacy-prefix record is wrong")
    if manifest.get("attribution", {}).get("email") != CANONICAL_EMAIL:
        fail("manifest attribution is wrong")
    artifacts = manifest.get("content_addressed_artifacts", [])
    if {item.get("path") for item in artifacts} != CONTENT_ADDRESSED_PATHS:
        fail("manifest content-addressed path list is wrong")
    for item in artifacts:
        relative_path = item.get("path")
        expected_hash = item.get("sha256")
        if not isinstance(relative_path, str) or not isinstance(expected_hash, str):
            fail("malformed content-addressed artifact")
        if not (ROOT / relative_path).is_file():
            fail(f"missing content-addressed artifact: {relative_path}")
        if sha256(relative_path) != expected_hash:
            fail(f"artifact hash mismatch: {relative_path}")


def verify_checksum_file(relative_path: str, base: str) -> None:
    for line in (ROOT / relative_path).read_text(encoding="utf-8").splitlines():
        expected_hash, filename = line.split()
        candidate = str(Path(base) / filename)
        if sha256(candidate) != expected_hash:
            fail(f"checksum mismatch in {relative_path}: {filename}")


def verify_evidence() -> None:
    manifest = read_json("EVIDENCE_MANIFEST.json")
    for relative_path in manifest.get("required_evidence_files", []):
        if not (ROOT / relative_path).is_file():
            fail(f"missing required evidence file: {relative_path}")
    for relative_path in manifest.get("required_evidence_directories", []):
        if not (ROOT / relative_path).is_dir():
            fail(f"missing required evidence directory: {relative_path}")

    verify_checksum_file("evidence/source/SHA256SUMS", "evidence/source")
    verify_checksum_file(
        "outputs/claim1_source_audit/SHA256SUMS",
        "outputs/claim1_source_audit",
    )
    verify_checksum_file(
        "outputs/claim1_random_walk_oracle_fixture/SHA256SUMS",
        "outputs/claim1_random_walk_oracle_fixture",
    )

    contract = read_json("contract/contract_manifest.json")
    if contract.get("claim_count") != 5 or contract.get("maximum_points") != 10:
        fail("contract count or maximum points are wrong")
    if contract.get("openreview_id") != "eTUljZ6e8c":
        fail("contract OpenReview ID is wrong")
    source_hashes = contract.get("sha256", {})
    if source_hashes.get("metadata.json") != "4f02b4203d25ce9ca7947f431225d97f646f0cbd33af1060249140a60c8ed823":
        fail("contract metadata hash is wrong")
    if source_hashes.get("live_claims.json") != "e1dabeadc76e4f7be48b96eb8819e2c1c339f324adc85ce857d2e0ec3aff4121":
        fail("contract live-claims hash is wrong")
    if source_hashes.get("challenge_readme.md") != "027f66e6da758c4a0d75fff6c9298e5322dde64d21a97d33e4367e42c3a421c5":
        fail("contract challenge-readme hash is wrong")

    source_audit = read_json("outputs/claim1_source_audit/result.json")
    if (
        source_audit.get("n") != 64
        or source_audit.get("sparsity_max") != 2
        or source_audit.get("kappa_fixture") != 4.0
        or source_audit.get("epsilon") != 0.01
        or source_audit.get("quantum_formula_variables")
        != ["s", "kappa", "log(1/epsilon)", "log(n)"]
    ):
        fail("source-parameter audit is wrong")
    if "lower.tex" not in (ROOT / "evidence/source/source_inventory.txt").read_text():
        fail("source inventory is missing lower.tex")

    summary = read_json(
        "outputs/claim1_random_walk_oracle_fixture/summary.json"
    )
    if (
        summary.get("verdict") != "toy"
        or summary.get("connected_cycle_mean_hit_probability") != 0.78006
        or summary.get("broken_cross_tree_mean_hit_probability") != 0.0
        or summary.get("control_expected_zero") is not True
        or summary.get("rows") != 10
    ):
        fail("Claim 1 fixture summary is wrong")
    if "not a QIC query lower-bound proof" not in summary.get("scope", ""):
        fail("Claim 1 scope boundary is missing")
    config = read_json(
        "outputs/claim1_random_walk_oracle_fixture/config.json"
    )
    if (
        config.get("height") != 4
        or config.get("walks") != 10000
        or config.get("steps") != 256
        or config.get("seeds")
        != [20260801, 20260802, 20260803, 20260804, 20260805]
    ):
        fail("Claim 1 fixture configuration is wrong")
    rows = (
        ROOT / "outputs/claim1_random_walk_oracle_fixture/results.csv"
    ).read_text(encoding="utf-8").splitlines()
    if len(rows) != 11:
        fail("Claim 1 raw row count is wrong")
    connected = [
        float(row.split(",")[9])
        for row in rows[1:]
        if row.split(",")[5] == "False"
    ]
    broken = [
        float(row.split(",")[9])
        for row in rows[1:]
        if row.split(",")[5] == "True"
    ]
    if len(connected) != 5 or len(broken) != 5:
        fail("Claim 1 connected/control row partition is wrong")
    if not math.isclose(sum(connected) / len(connected), 0.78006, abs_tol=1e-12):
        fail("Claim 1 connected mean is wrong")
    if any(value != 0.0 for value in broken):
        fail("Claim 1 broken control is not zero")

    live_claims = read_json("contract/live_claims.json")
    if len(live_claims) != 5 or any(
        item.get("status") != "unverified" for item in live_claims
    ):
        fail("live claim contract is not the expected five-claim boundary")
    if "Theorem 1" not in live_claims[0].get("text", ""):
        fail("Claim 1 anchor is missing")


def verify_ledgers_and_state() -> None:
    claims = read_json("claims.json")
    state = read_json("AUTONOMOUS_STATE.json")
    if not isinstance(claims, dict) or not isinstance(state, dict):
        fail("claim ledger and state must be JSON objects")
    if {
        row.get("id"): row.get("status") for row in claims.get("claims", [])
    } != EXPECTED_CLAIMS:
        fail("claims.json statuses are wrong")
    if claims.get("repository") != EXPECTED_REPOSITORY:
        fail("claims.json repository marker is wrong")
    paper = claims.get("paper", {})
    if paper.get("pdf_sha256") != EXPECTED_PDF_SHA:
        fail("claims.json PDF source hash is wrong")
    if paper.get("source_archive_sha256") != EXPECTED_SOURCE_ARCHIVE_SHA:
        fail("claims.json source archive hash is wrong")
    if state.get("github_repository") != "https://github.com/" + EXPECTED_REPOSITORY:
        fail("state repository marker is wrong")
    if state.get("canonical_branch") != "main":
        fail("state canonical branch is wrong")
    if set(state.get("expected_branches", [])) != EXPECTED_BRANCHES:
        fail("state branch set is wrong")
    if state.get("historical_branch_count") != 0:
        fail("state historical branch count is wrong")
    if state.get("paper_pdf_sha256") != EXPECTED_PDF_SHA:
        fail("state PDF source hash is wrong")
    if state.get("paper_source_archive_sha256") != EXPECTED_SOURCE_ARCHIVE_SHA:
        fail("state source archive hash is wrong")
    if state.get("contract_manifest_sha256") != EXPECTED_CONTRACT_SHA:
        fail("state contract hash is wrong")
    identity = state.get("canonical_identity", {})
    if identity.get("name") != CANONICAL_NAME or identity.get("email") != CANONICAL_EMAIL:
        fail("state canonical identity is wrong")
    if state.get("phase") not in {
        "dossier_ready_for_publication",
        "dossier_published_claim_1_random_walk_toy_only",
    }:
        fail("state phase is not a dossier phase")


def verify_documentation() -> None:
    for relative_path in REQUIRED_FILES:
        if not (ROOT / relative_path).is_file():
            fail(f"required file is missing: {relative_path}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for marker in (
        "CLAIM_EVIDENCE.md",
        "SOURCE_AUDIT.md",
        "BRANCH_AUDIT.md",
        "ENVIRONMENT.md",
        "REPORT.md",
        "CITATION.cff",
        "AUTHOR_THANK_YOU.md",
        "EVIDENCE_MANIFEST.json",
        "TOY",
        "UNVERIFIED",
        "verify_final.py",
    ):
        if marker not in readme:
            fail(f"README is missing marker {marker!r}")
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
    for marker in (
        "dossier_published_claim_1_random_walk_toy_only",
        "Evidence boundary",
        "Verification status",
    ):
        if marker not in status:
            fail(f"STATUS is missing marker {marker!r}")
    branch_audit = (ROOT / "BRANCH_AUDIT.md").read_text(encoding="utf-8")
    if "main" not in branch_audit or "MachineLearning-Nerd" not in branch_audit:
        fail("branch audit is incomplete")
    if "ORX" not in branch_audit:
        fail("branch audit legacy-prefix boundary is missing")
    source_audit = (ROOT / "SOURCE_AUDIT.md").read_text(encoding="utf-8")
    for source_hash in (
        EXPECTED_PDF_SHA,
        EXPECTED_SOURCE_ARCHIVE_SHA,
        EXPECTED_CONTRACT_SHA,
    ):
        if source_hash not in source_audit:
            fail("source audit hash is missing")
    thanks = (ROOT / "AUTHOR_THANK_YOU.md").read_text(encoding="utf-8")
    for author in ("Allan Grønlund", "Kasper Green Larsen"):
        if author not in thanks:
            fail(f"author thanks is missing {author}")


def main() -> int:
    verify_documentation()
    verify_remote()
    verify_branch_tips()
    verify_history()
    verify_manifest()
    verify_evidence()
    verify_ledgers_and_state()
    print("PASS: published quantum/QIC separation audit state is structurally verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
